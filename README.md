# Human Science Knowledge Base

Obsidian / Quartz 向けの人間科学ナレッジベースです。脳・神経科学、認知科学、精神医学、心理学、機械学習、数理モデル、計算論的精神医学を中心に、日本語の文献ベースノートを `content/` 配下に管理します。

## 構成

- `content/`: Obsidian / Quartz の vault root
- `content/00_MOC/`: 領域別MOC
- `.agents/skills/`: ノート作成・文献評価・MOC管理・公開前チェック用のCodex Skills
- `scripts/`: vault品質チェックや記事生成補助スクリプト
- `gen_article.py`: CSVからCodexに記事生成ジョブを投げるバッチランナー

## Frontmatter 標準

すべてのMarkdownノートは、原則として次の順序でプロパティを持ちます。

```yaml
title: ""
description: ""
aliases: []
tags: []
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
draft: true
publish: false
status: draft
enableToc: true
```

MOCなど公開前提の索引ノートは `draft: false`, `publish: true`, `status: published` を使います。

## よく使うコマンド

```powershell
python -m py_compile gen_article.py scripts\check_vault_quality.py scripts\generate_psychiatry_e_articles.py
python scripts\check_vault_quality.py --root content
python .agents\skills\VaultリンクMOC管理\scripts\quartz_check.py --root content
```

`gen_article.py` は Windows では既定で `%USERPROFILE%\AppData\Roaming\npm\codex.cmd` を探します。別の場所にある場合は `--codex-bin` で指定してください。

## 注意

医療・精神医学に関する内容は教育・研究目的です。個別診断や治療指示としては扱わないでください。
