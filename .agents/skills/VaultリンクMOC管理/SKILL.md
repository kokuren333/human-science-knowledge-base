---
name: vault-linker-moc-builder
description: Scan content/ as the Obsidian/Quartz vault root, suggest related existing notes, create or update MOC pages, assign numbered Japanese directories and tags, place attachments when present, and add safe internal links only to confirmed existing notes or explicitly requested new notes. Use when the user asks to organize a vault, connect notes, create MOCs, update directories, add backlinks, or prepare Obsidian articles for Quartz without creating a vault/ directory. Do not create SVG, Mermaid/mermaid.js, HTML/CSS/canvas, ASCII-art, or code-generated diagrams. If a figure is explicitly requested, use only imagegen/image_gen raster image generation and store images under content/asset/.
---

# vault-linker-moc-builder

## 目的

Obsidian / Quartz の `content/` 配下で、記事の配置、関連既存ノート、MOC、タグ、添付ファイルの置き場所を整理する。記事作成後の受け入れ工程として使う。

画像生成や画像追加は通常行わない。既存の添付画像がある場合だけ配置とリンクを確認する。ユーザーが明示的に画像生成・画像追加を依頼した場合だけ `imagegen` / `image_gen` によるラスター画像生成や画像配置を行う。

画像を扱う場合は `content/asset/` 配下で管理する。記事別に分ける必要がある場合は `content/asset/{{記事スラッグ}}/` を使い、記事からは Quartz で解決しやすい相対パスで参照する。

SVG、Mermaid / mermaid.js、HTML/CSS/canvas、ASCII art、その他のコード生成による図・図解・概念図・フローチャート・模式図の作成は禁止する。

## vault root

- このリポジトリでは `content/` を vault root として扱う。
- `vault/` や `content/vault/` は作らない。
- `.agents/`, `.git/`, `node_modules/`, `.obsidian/`, `public/`, `dist/`, `tmp/` は通常のノート走査対象から除外する。

## 高速ワークフロー

1. `rg --files content` で既存ノートを把握する。
2. 必要最小限の `rg` でタイトル、alias、タグ、関連語を検索する。
3. 保存先カテゴリを既存ディレクトリから選ぶ。迷う場合は `content/90_未分類・インボックス/` を提案する。
4. 内部リンクは確認済みの既存ノート、またはユーザーが明示した作成対象だけにする。
5. MOC更新候補は、既存MOCの構造を優先し、無理に新規MOCを増やさない。
6. 画像ファイルがある場合は `content/asset/`、必要なら `content/asset/{{記事スラッグ}}/` に置く。画像以外の添付ファイルだけ、別の管理場所が必要かを提案する。

## 内部リンクの禁止事項

- 勝手に未作成ノートへの `[[...]]` を作らない。
- MOCテンプレート内でも、存在確認できないノートを wikilink 化しない。
- 未作成ノート候補は通常テキストで「今後の作成候補」に置く。
- 指示されていない関連ノートや空ファイルを作らない。

## ディレクトリ方針

```text
content/
├── 00_MOC/
├── 01_脳・神経科学/
├── 02_認知科学/
├── 03_精神医学/
├── 04_心理学/
├── 05_機械学習・AI/
├── 06_数理モデル・計算論/
├── 07_計算論的精神医学/
├── 08_研究方法・統計・因果推論/
├── 09_臨床実践/
├── 10_哲学・倫理・社会/
├── 20_生命科学・医学一般/
├── 30_人文・社会科学/
├── 40_技術・工学/
├── 50_キャリア・学習法/
├── 90_未分類・インボックス/
└── asset/
```

## MOC方針

- MOC は `content/00_MOC/` に置く。
- MOCファイル名は `MOC：{{領域名}}.md` を基本にする。
- MOC の frontmatter は `title`, `description`, `aliases`, `tags`, `created`, `updated`, `draft`, `publish`, `status`, `enableToc` の順にそろえる。
- 公開前提のMOCでは `draft: false`, `publish: true`, `status: published` とする。
- 既存MOCの見出し構成を優先する。
- MOCに追加する wikilink は、存在確認済みの既存ノート、またはユーザーが明示した作成対象だけにする。
- MOCには短い説明を添え、読者が次に読む理由が分かるようにする。

## 便利スクリプト

存在する場合に使う。

```bash
python .agents/skills/VaultリンクMOC管理/scripts/vault_index.py --root content --json
python .agents/skills/VaultリンクMOC管理/scripts/suggest_links.py --root content --title "{{title}}" --tags "{{tags}}"
python .agents/skills/VaultリンクMOC管理/scripts/update_moc.py --moc content/00_MOC/MOC：{{domain}}.md --link "{{note_title}}"
python .agents/skills/VaultリンクMOC管理/scripts/quartz_check.py --root content
```

## テスト

```bash
python -m unittest discover .agents/skills/VaultリンクMOC管理/tests
```
