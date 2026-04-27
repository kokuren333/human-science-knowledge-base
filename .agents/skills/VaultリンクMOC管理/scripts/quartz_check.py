import argparse
import re
from pathlib import Path

from safe_paths import sanitize_filename
from vault_index import build_index, parse_frontmatter


REQUIRED = [
    "title",
    "description",
    "aliases",
    "tags",
    "created",
    "updated",
    "draft",
    "publish",
    "status",
    "enableToc",
]
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
ATTACH_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")


def note_names(index: list[dict]) -> set[str]:
    names = set()
    for note in index:
        path = Path(note["path"])
        names.add(path.stem)
        names.add(str(note.get("title", "")))
        for alias in note.get("aliases", []):
            names.add(alias)
    return {name for name in names if name}


def check_file(path: Path, root: Path, known_names: set[str]) -> list[str]:
    issues = []
    text = path.read_text(encoding="utf-8-sig")
    fm = parse_frontmatter(text)
    rel = path.relative_to(root)
    if not fm:
        issues.append(f"{rel}: frontmatter がありません")
    for key in REQUIRED:
        if key not in fm:
            issues.append(f"{rel}: frontmatter `{key}` がありません")
    if "tags" in fm and not isinstance(fm["tags"], list):
        issues.append(f"{rel}: `tags` は配列形式を推奨します")
    for link in WIKILINK_RE.findall(text):
        if link not in known_names:
            issues.append(f"{rel}: 壊れた wikilink 候補 [[{link}]]")
    for attachment in ATTACH_RE.findall(text):
        if attachment.startswith(("http://", "https://")):
            continue
        target = (path.parent / attachment).resolve()
        try:
            target.relative_to(root.resolve())
        except ValueError:
            issues.append(f"{rel}: content root 外の添付参照 {attachment}")
    if len(path.name) > 140:
        issues.append(f"{rel}: ファイル名が長すぎる可能性があります")
    if sanitize_filename(path.stem) != path.stem:
        issues.append(f"{rel}: ファイル名に危険文字または非推奨文字があります")
    return issues


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="content")
    args = parser.parse_args()
    root = Path(args.root)
    if not root.exists():
        print(f"root not found: {root}")
        return
    index = build_index(root)
    known = note_names(index)
    issues = []
    for note in index:
        issues.extend(check_file(root / note["path"], root, known))
    if not issues:
        print("Quartz check passed.")
    else:
        for issue in issues:
            print(f"- {issue}")


if __name__ == "__main__":
    main()
