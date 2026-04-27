#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Codex batch runner for Obsidian article generation.

CSV format:
[[記事タイトル]],記事の軽い説明,保存先ディレクトリ

Example:
[[ニューロンとは何か]],神経細胞の基本構造と情報処理単位としての役割を初学者向けに整理する,content/01_脳・神経科学/基礎神経科学
[[グリア細胞は単なる支持細胞なのか]],グリア細胞の種類と機能を整理する,content/01_脳・神経科学/基礎神経科学
"""

import argparse
import csv
import datetime
import os
import re
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from threading import Lock


INVALID_FILENAME_CHARS = r'[\\/:*?"<>|]'
DEFAULT_CODEX_BIN = Path.home() / "AppData" / "Roaming" / "npm" / "codex.cmd"

# Obsidianで content/ をVaultとして開いている前提。
# 画像は必ずVault内に置く。
VAULT_ROOT_REL = "content"
IMAGE_ROOT_REL = "content/asset/generated_infographics"

print_lock = Lock()


def log_print(message: str):
    with print_lock:
        print(message, flush=True)


def strip_wikilink_title(raw: str) -> str:
    raw = raw.strip()
    m = re.fullmatch(r"\[\[(.+?)\]\]", raw)
    return m.group(1).strip() if m else raw


def safe_filename(name: str) -> str:
    name = re.sub(INVALID_FILENAME_CHARS, "_", name)
    name = re.sub(r"\s+", " ", name)
    return name.strip()


def normalize_relative_dir(raw_dir: str) -> str:
    raw_dir = raw_dir.strip().replace("\\", "/").strip("/")

    if not raw_dir:
        raise ValueError("保存先ディレクトリが空です")

    p = Path(raw_dir)

    if p.is_absolute():
        raise ValueError(f"絶対パスは使えません: {raw_dir}")

    if ".." in p.parts:
        raise ValueError(f"'..' を含むパスは使えません: {raw_dir}")

    return raw_dir


def resolve_codex_bin(codex_bin: str) -> str:
    if codex_bin:
        p = Path(codex_bin)
        if p.exists():
            return str(p)

        found = shutil.which(codex_bin)
        if found:
            return found

    if DEFAULT_CODEX_BIN.exists():
        return str(DEFAULT_CODEX_BIN)

    for candidate in ["codex.cmd", "codex.exe", "codex"]:
        found = shutil.which(candidate)
        if found:
            return found

    raise FileNotFoundError(
        "codex 実行ファイルが見つかりません。"
        f" 既定パス {DEFAULT_CODEX_BIN} を確認するか、"
        " --codex-bin で codex.cmd のフルパスを指定してください。"
    )


def ensure_default_codex_args(extra_args: list[str]) -> list[str]:
    args = list(extra_args)

    if "--skip-git-repo-check" not in args:
        args.append("--skip-git-repo-check")

    if "--full-auto" not in args:
        args.append("--full-auto")

    return args


def read_tasks(csv_path: Path):
    tasks = []

    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)

        for row_index, row in enumerate(reader, start=1):
            if not row:
                continue

            if len(row) < 3:
                log_print(f"[WARN] {row_index}行目は列数不足のためスキップ: {row}")
                continue

            title_raw = row[0].strip()
            description = row[1].strip()
            output_dir_raw = row[2].strip()

            if not title_raw:
                log_print(f"[WARN] {row_index}行目はタイトル空欄のためスキップ")
                continue

            if title_raw.lower() in {"title", "article_title", "記事タイトル"}:
                continue

            try:
                output_dir = normalize_relative_dir(output_dir_raw)
            except ValueError as e:
                log_print(f"[WARN] {row_index}行目の保存先ディレクトリが不正なためスキップ: {e}")
                continue

            title = strip_wikilink_title(title_raw)

            tasks.append(
                {
                    "row_index": row_index,
                    "title_raw": title_raw,
                    "title": title,
                    "description": description,
                    "output_dir": output_dir,
                }
            )

    return tasks


def build_article_prompt(
    *,
    title_raw: str,
    title: str,
    description: str,
    output_dir: str,
    output_file: str,
    image_save_dir: str,
    image_markdown_dir: str,
    image_prefix: str,
    max_sources: int,
    image_count: str,
    parallel_safe: bool,
) -> str:
    if parallel_safe:
        moc_instruction = """
# 並列実行時の注意
このジョブは他の記事生成ジョブと並列実行される可能性があります。
そのため、MOC・索引・グローバルな内部リンク一覧など、複数ジョブが同時編集しそうなファイルの大規模更新は避けてください。
必要な場合は、記事末尾に関連ノート候補を記載するに留めてください。
MOC更新はバッチ完了後の統合ジョブで行います。
""".strip()
    else:
        moc_instruction = """
# MOC更新
MOCや索引ノートの更新がSkillsで定められている場合は、それに従って必要最小限の更新を行ってください。
""".strip()

    return f"""
このディレクトリにある Skills を使って、以下の記事作成タスクを実行してください。

# 対象記事
- 記事タイトル: {title_raw}
- 実タイトル: {title}
- 記事の軽い説明: {description}

# 保存先
- 保存先ディレクトリ: {output_dir}
- 記事ファイル: {output_file}

# 画像保存先とMarkdownリンク
- 画像の実保存先ディレクトリ: {image_save_dir}
- 記事から見たMarkdown画像リンク用ディレクトリ: {image_markdown_dir}
- 画像ファイル接頭辞: {image_prefix}
- 画像作成枚数: {image_count}枚

重要:
- 画像は必ず `画像の実保存先ディレクトリ` に保存すること。
- Markdown本文に挿入する画像リンクは、必ず `記事から見たMarkdown画像リンク用ディレクトリ` を使うこと。
- 実保存先とMarkdownリンク用パスを混同しないこと。
- Markdownに画像リンクを挿入する前に、該当画像ファイルが実在することを確認すること。
- 画像生成に失敗した場合、存在しない画像リンクを挿入してはならない。
- 画像生成に失敗した場合は、代わりに「図解案」として日本語インフォグラフィック用プロンプトを残すこと。

{moc_instruction}

# 必須実行要件
1. このプロジェクトディレクトリ内にある Skills を必ず確認し、それに従って作業すること。
2. Obsidian記事作成、内部リンク管理、画像生成に関する Skills がある場合は、それらを優先すること。
3. 記事は日本語 Markdown で作成すること。
4. 記事は指定された `記事ファイル` に作成・更新すること。
5. 既存記事がある場合は、重複作成せず、既存記事を改善・拡張すること。
6. 信頼できるソースを調査したうえで執筆すること。
7. 参考文献は最大 {max_sources} 件を目安に、信頼度の高いものを優先すること。
8. 本文中の該当箇所に引用番号 [1], [2], [3] ... を付けること。
9. 末尾に「参考文献」セクションを置き、本文中の引用番号と対応させること。
10. Obsidianの内部リンク [[...]] を適切に入れること。
11. `$imagegen` スキル、または画像生成に関する Skills を使って、日本語インフォグラフィックスを {image_count} 枚作成すること。
12. 画像ファイル名は `{image_prefix}_01.png`, `{image_prefix}_02.png`, `{image_prefix}_03.png` のように連番にすること。
13. 作成した画像は、記事中の適切な位置に Markdown 画像リンクとして配置すること。
14. 画像リンクは以下の形式にすること。
    - `![日本語のaltテキスト]({image_markdown_dir}/{image_prefix}_01.png)`
15. 画像の alt テキストは日本語で簡潔に書くこと。
16. 不要なファイル変更は避け、この記事作成・内部リンク挿入・関連画像生成に必要な範囲だけ変更すること。

# 記事構成の推奨
Skills側の指定がある場合はそちらを優先してください。

---
title: "{title}"
description: "{title}について、基礎概念、仕組み、研究・臨床との接続を整理する。"
aliases:
  - "{title}"
tags:
  - neuroscience
  - basic-neuroscience
  - obsidian
created: "{datetime.date.today().isoformat()}"
updated: "{datetime.date.today().isoformat()}"
draft: true
publish: false
status: draft
enableToc: true
---

# {title}

## 要点

## この記事で答える問い

## まず結論

## 背景

## 基本概念

## 仕組み

## 図解

## 臨床・研究との接続

## よくある誤解

## 関連ノート

## 理解チェック

## 参考文献

# 図解方針
この記事につき、以下のような画像を {image_count} 枚作成してください。

- 1枚目: 記事全体の概念地図、または要約インフォグラフィック
- 2枚目: 最も重要なメカニズムの図解
- 3枚目: 必要なら、比較表・フロー図・臨床/研究応用への接続図

# 最終報告
作業後、以下だけを簡潔に報告してください。

- 作成・更新した記事ファイル
- 作成した画像ファイル
- 更新した関連ファイル
- 参照した主要ソース数
""".strip()


def build_moc_prompt(output_dirs: list[str]) -> str:
    dirs_text = "\n".join(f"- {d}" for d in sorted(set(output_dirs)))

    return f"""
このディレクトリにある Skills を使って、今回のバッチ生成後の Obsidian Vault を整理してください。

# 対象ディレクトリ
{dirs_text}

# 実行要件
1. Obsidian記事作成、MOC、内部リンク管理に関する Skills を確認し、それに従うこと。
2. 対象ディレクトリ内の記事を確認し、関連する MOC にリンクを追加・整理すること。
3. 特に `content/00_MOC/MOC｜脳・神経科学.md` と、必要なら領域別MOCを更新すること。
4. 記事間の内部リンクが不足していれば、必要最小限の範囲で補うこと。
5. 既存の構造や表記を壊さないこと。
6. 大規模なリライトは避け、今回生成・更新された記事を見つけやすくする整理を優先すること。
7. 画像リンクは `content/asset/generated_infographics` 配下の実在ファイルを参照しているか確認すること。
8. 存在しない画像リンクがあれば、実在する画像のパスへ修正すること。

# 最終報告
- 更新したMOC
- 更新した記事
- 追加・修正した主な内部リンク
- 修正した画像リンク
""".strip()


def run_codex(
    *,
    codex_bin: str,
    prompt: str,
    cwd: Path,
    log_path: Path,
    extra_args: list[str],
    timeout: int | None,
):
    """
    長い日本語プロンプトをWindowsのコマンドライン引数に直接載せると不安定なので、
    codex exec - にして stdin から渡す。
    """
    cmd = [codex_bin, "exec", *extra_args, "-"]

    started = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with log_path.open("w", encoding="utf-8") as logf:
        logf.write(f"[START] {started}\n")
        logf.write(f"[CWD] {cwd}\n")
        logf.write(f"[COMMAND] {' '.join(cmd)} <STDIN_PROMPT>\n")
        logf.write("=" * 80 + "\n")
        logf.write(prompt)
        logf.write("\n" + "=" * 80 + "\n\n")

        try:
            proc = subprocess.run(
                cmd,
                cwd=str(cwd),
                input=prompt,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout,
            )

            logf.write("[STDOUT]\n")
            logf.write(proc.stdout or "")
            logf.write("\n\n[STDERR]\n")
            logf.write(proc.stderr or "")
            logf.write("\n")

            return proc.returncode, proc.stdout, proc.stderr

        except subprocess.TimeoutExpired as e:
            logf.write("[TIMEOUT]\n")
            logf.write(str(e))
            logf.write("\n")
            return 124, "", str(e)

        except Exception as e:
            logf.write("[EXCEPTION]\n")
            logf.write(repr(e))
            logf.write("\n")
            return 1, "", repr(e)


def prepare_task(
    *,
    task: dict,
    index: int,
    total: int,
    project_root: Path,
    image_root: Path,
    logs_dir: Path,
    max_sources: int,
    image_count: str,
    parallel_safe: bool,
):
    title_raw = task["title_raw"]
    title = task["title"]
    description = task["description"]
    output_dir = task["output_dir"]

    safe_title = safe_filename(title)

    output_dir_abs = project_root / output_dir
    output_file_abs = output_dir_abs / f"{safe_title}.md"
    output_file_rel = output_file_abs.relative_to(project_root).as_posix()

    image_dir_abs = image_root / safe_title
    image_save_dir_rel = image_dir_abs.relative_to(project_root).as_posix()

    # Markdownリンクは、記事があるディレクトリから画像ディレクトリへの相対パスにする。
    image_markdown_dir_rel = os.path.relpath(
        image_dir_abs,
        start=output_dir_abs,
    ).replace("\\", "/")

    output_dir_abs.mkdir(parents=True, exist_ok=True)
    image_dir_abs.mkdir(parents=True, exist_ok=True)

    prompt = build_article_prompt(
        title_raw=title_raw,
        title=title,
        description=description,
        output_dir=output_dir,
        output_file=output_file_rel,
        image_save_dir=image_save_dir_rel,
        image_markdown_dir=image_markdown_dir_rel,
        image_prefix=safe_title,
        max_sources=max_sources,
        image_count=image_count,
        parallel_safe=parallel_safe,
    )

    log_path = logs_dir / f"{index:03d}_{safe_title}.log"

    return {
        "index": index,
        "total": total,
        "title": title,
        "safe_title": safe_title,
        "output_file_abs": output_file_abs,
        "output_file_rel": output_file_rel,
        "output_dir": output_dir,
        "output_dir_abs": output_dir_abs,
        "image_dir_abs": image_dir_abs,
        "image_save_dir_rel": image_save_dir_rel,
        "image_markdown_dir_rel": image_markdown_dir_rel,
        "prompt": prompt,
        "log_path": log_path,
    }


def print_stderr_tail(stderr: str, max_lines: int = 8):
    if not stderr:
        return

    lines = stderr.strip().splitlines()
    for line in lines[-max_lines:]:
        log_print(f"       STDERR: {line}")


def run_one_task(
    *,
    prepared: dict,
    codex_bin: str,
    project_root: Path,
    extra_args: list[str],
    retries: int,
    delay: float,
    timeout: int | None,
):
    index = prepared["index"]
    total = prepared["total"]
    title = prepared["title"]
    output_file_rel = prepared["output_file_rel"]
    prompt = prepared["prompt"]
    log_path = prepared["log_path"]

    log_print(f"[RUN ] {index}/{total} {title}")
    log_print(f"      -> {output_file_rel}")

    success = False
    last_rc = None
    last_stderr = ""

    for attempt in range(1, retries + 2):
        if attempt > 1:
            log_print(f"[RETRY] {title} attempt={attempt}")

        rc, stdout, stderr = run_codex(
            codex_bin=codex_bin,
            prompt=prompt,
            cwd=project_root,
            log_path=log_path,
            extra_args=extra_args,
            timeout=timeout,
        )

        last_rc = rc
        last_stderr = stderr or ""

        if rc == 0:
            log_print(f"[ OK ] {title}")
            success = True
            break

        log_print(f"[FAIL] {title} exit={rc}")
        print_stderr_tail(last_stderr)

        if delay > 0:
            time.sleep(delay)

    if not success:
        return {
            "ok": False,
            "title": title,
            "exit_code": last_rc,
            "log": log_path.as_posix(),
            "output_file": output_file_rel,
            "stderr_tail": "\n".join(last_stderr.strip().splitlines()[-8:]),
        }

    return {
        "ok": True,
        "title": title,
        "exit_code": 0,
        "log": log_path.as_posix(),
        "output_file": output_file_rel,
        "stderr_tail": "",
    }


def migrate_old_assets(project_root: Path):
    """
    旧保存先 assets/generated_infographics から
    新保存先 content/asset/generated_infographics へ移動する。
    """
    old_root = project_root / "assets" / "generated_infographics"
    new_root = project_root / IMAGE_ROOT_REL

    if not old_root.exists():
        return

    new_root.mkdir(parents=True, exist_ok=True)

    for item in old_root.iterdir():
        dest = new_root / item.name

        if dest.exists():
            continue

        shutil.move(str(item), str(dest))

    log_print(f"[INFO] migrated old assets: {old_root} -> {new_root}")


def fix_existing_image_links(project_root: Path):
    """
    既存記事内の旧画像リンクを可能な範囲で修正する。
    主に以下を直す:
    - ../../../assets/generated_infographics/
    - ../../assets/generated_infographics/
    - assets/generated_infographics/
    を content/ 配下Vault想定の ../../asset/generated_infographics/ に寄せる。
    """
    content_root = project_root / VAULT_ROOT_REL
    if not content_root.exists():
        return

    md_files = list(content_root.rglob("*.md"))

    for md in md_files:
        try:
            text = md.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        original = text

        # content/01_xxx/サブフォルダ/article.md から content/asset/... へは基本 ../../asset/...
        # 階層が違う場合もあるため、本来は個別計算が必要だが、旧リンクの代表パターンを補正する。
        text = text.replace("../../../assets/generated_infographics/", "../../asset/generated_infographics/")
        text = text.replace("../../assets/generated_infographics/", "../../asset/generated_infographics/")
        text = text.replace("../assets/generated_infographics/", "../asset/generated_infographics/")
        text = text.replace("assets/generated_infographics/", "asset/generated_infographics/")

        if text != original:
            md.write_text(text, encoding="utf-8")
            log_print(f"[FIX ] image links: {md.relative_to(project_root).as_posix()}")


def main():
    parser = argparse.ArgumentParser(
        description="Run Codex batch jobs from CSV with output directory column and parallel workers."
    )

    parser.add_argument(
        "--csv",
        required=True,
        help="入力CSV。形式: [[記事タイトル]],説明,保存先ディレクトリ",
    )
    parser.add_argument(
        "--workdir",
        default=".",
        help="Skillsが存在するプロジェクトディレクトリ。既定はカレントディレクトリ",
    )
    parser.add_argument(
        "--codex-bin",
        default=DEFAULT_CODEX_BIN,
        help=f"codex.cmd のパス。既定: {DEFAULT_CODEX_BIN}",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=4,
        help="並列実行数。デフォルト: 4",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.0,
        help="同一タスク内のリトライ間待機秒数",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=1,
        help="失敗時の再試行回数",
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="出力先記事ファイルが既に存在する場合はスキップ",
    )
    parser.add_argument(
        "--max-sources",
        type=int,
        default=8,
        help="参考文献の最大目安数",
    )
    parser.add_argument(
        "--image-count",
        default="2-3",
        help="1記事あたりの画像作成枚数。例: 2, 3, 2-3",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Codexを実行せず、生成されるタスクだけ確認する",
    )
    parser.add_argument(
        "--extra-codex-arg",
        action="append",
        default=[],
        help="codex exec に追加で渡す引数。複数指定可",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=None,
        help="1タスクあたりのタイムアウト秒数。未指定なら無制限",
    )
    parser.add_argument(
        "--no-final-moc-pass",
        action="store_true",
        help="最後のMOC整理ジョブを実行しない",
    )
    parser.add_argument(
        "--unsafe-parallel-moc",
        action="store_true",
        help="並列中でも各ジョブにMOC更新を許可する。競合リスクあり",
    )
    parser.add_argument(
        "--migrate-old-assets",
        action="store_true",
        help="旧 assets/generated_infographics から content/asset/generated_infographics へ画像を移動する",
    )
    parser.add_argument(
        "--fix-image-links-only",
        action="store_true",
        help="Codex実行はせず、既存Markdownの旧画像リンク補正だけ行う",
    )

    args = parser.parse_args()

    if args.workers < 1:
        print("[ERROR] --workers は1以上にしてください")
        sys.exit(1)

    args.extra_codex_arg = ensure_default_codex_args(args.extra_codex_arg)

    project_root = Path(args.workdir).resolve()
    csv_path = Path(args.csv).resolve()

    if not project_root.exists():
        print(f"[ERROR] workdir が見つかりません: {project_root}")
        sys.exit(1)

    if args.migrate_old_assets:
        migrate_old_assets(project_root)

    if args.fix_image_links_only:
        fix_existing_image_links(project_root)
        log_print("[DONE] image links fixed only")
        return

    if not csv_path.exists():
        print(f"[ERROR] CSV が見つかりません: {csv_path}")
        sys.exit(1)

    try:
        codex_bin = resolve_codex_bin(args.codex_bin)
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    tasks = read_tasks(csv_path)

    if not tasks:
        print("[ERROR] 有効なタスクがありません。")
        sys.exit(1)

    logs_dir = project_root / "logs" / "codex_batch"
    logs_dir.mkdir(parents=True, exist_ok=True)

    image_root = project_root / IMAGE_ROOT_REL
    image_root.mkdir(parents=True, exist_ok=True)

    log_print(f"[INFO] workdir: {project_root}")
    log_print(f"[INFO] csv: {csv_path}")
    log_print(f"[INFO] codex: {codex_bin}")
    log_print(f"[INFO] codex args: {' '.join(args.extra_codex_arg)}")
    log_print(f"[INFO] image root: {image_root}")
    log_print(f"[INFO] tasks: {len(tasks)}")
    log_print(f"[INFO] workers: {args.workers}")
    log_print(f"[INFO] logs: {logs_dir}")

    prepared_tasks = []
    skipped = []

    for i, task in enumerate(tasks, start=1):
        prepared = prepare_task(
            task=task,
            index=i,
            total=len(tasks),
            project_root=project_root,
            image_root=image_root,
            logs_dir=logs_dir,
            max_sources=args.max_sources,
            image_count=args.image_count,
            parallel_safe=(args.workers > 1 and not args.unsafe_parallel_moc),
        )

        if args.skip_existing and prepared["output_file_abs"].exists():
            log_print(f"[SKIP] {i}/{len(tasks)} 既存記事あり: {prepared['output_file_rel']}")
            skipped.append(prepared["output_file_rel"])
            continue

        prepared_tasks.append(prepared)

    if args.dry_run:
        log_print("\n=== Dry run tasks ===")
        for p in prepared_tasks:
            log_print(f"- {p['title']} -> {p['output_file_rel']}")
            log_print(f"  image save: {p['image_save_dir_rel']}")
            log_print(f"  image md:   {p['image_markdown_dir_rel']}")
        log_print(f"\nTotal: {len(tasks)} / To run: {len(prepared_tasks)} / Skipped: {len(skipped)}")
        return

    failed = []
    succeeded = []

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = [
            executor.submit(
                run_one_task,
                prepared=p,
                codex_bin=codex_bin,
                project_root=project_root,
                extra_args=args.extra_codex_arg,
                retries=args.retries,
                delay=args.delay,
                timeout=args.timeout,
            )
            for p in prepared_tasks
        ]

        for future in as_completed(futures):
            try:
                result = future.result()
            except Exception as e:
                result = {
                    "ok": False,
                    "title": "UNKNOWN",
                    "exit_code": -1,
                    "log": "",
                    "output_file": "",
                    "stderr_tail": repr(e),
                }
                log_print(f"[ERROR] worker exception: {repr(e)}")

            if result["ok"]:
                succeeded.append(result)
            else:
                failed.append(result)

    if failed:
        failed_txt = logs_dir / "failed_tasks.tsv"
        with failed_txt.open("w", encoding="utf-8") as f:
            f.write("title\texit_code\toutput_file\tlog\tstderr_tail\n")
            for item in failed:
                stderr_tail = (item.get("stderr_tail") or "").replace("\n", "\\n")
                f.write(
                    f"{item['title']}\t{item['exit_code']}\t{item['output_file']}\t{item['log']}\t{stderr_tail}\n"
                )

    final_moc_result = None

    if not args.no_final_moc_pass and succeeded:
        output_dirs = [p["output_dir"] for p in prepared_tasks]
        moc_prompt = build_moc_prompt(output_dirs)
        moc_log_path = logs_dir / "999_final_moc_pass.log"

        log_print("\n[RUN ] Final MOC/internal-link pass")

        rc, stdout, stderr = run_codex(
            codex_bin=codex_bin,
            prompt=moc_prompt,
            cwd=project_root,
            log_path=moc_log_path,
            extra_args=args.extra_codex_arg,
            timeout=args.timeout,
        )

        final_moc_result = {
            "exit_code": rc,
            "log": moc_log_path.as_posix(),
        }

        if rc == 0:
            log_print("[ OK ] Final MOC/internal-link pass")
        else:
            log_print(f"[FAIL] Final MOC/internal-link pass exit={rc}")
            print_stderr_tail(stderr or "")

    log_print("\n=== Batch finished ===")
    log_print(f"Total CSV tasks: {len(tasks)}")
    log_print(f"To run:          {len(prepared_tasks)}")
    log_print(f"Succeeded:       {len(succeeded)}")
    log_print(f"Skipped:         {len(skipped)}")
    log_print(f"Failed:          {len(failed)}")

    if final_moc_result:
        log_print(f"Final MOC pass:  exit={final_moc_result['exit_code']} / log={final_moc_result['log']}")

    if failed:
        log_print(f"\n[FAILED LIST] {logs_dir / 'failed_tasks.tsv'}")
        for item in failed:
            log_print(f"- {item['title']} / exit={item['exit_code']} / log={item['log']}")


if __name__ == "__main__":
    main()
