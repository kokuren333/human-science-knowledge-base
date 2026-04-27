---
name: human-science-note-writer
description: Write one Japanese Obsidian/Quartz finished long-form article per user instruction for human science topics, especially neuroscience, cognition, psychiatry, psychology, machine learning, mathematical models, and computational psychiatry. Use when the user asks for a readable source-grounded article, explanation, literature-based summary, question-driven article, or Obsidian-ready Markdown article under content/ as the vault root, with existing internal links, tags, MOC placement suggestions, numbered in-text citations, references with URLs, and LaTeX when needed. Do not generate or add images, Mermaid diagrams, or other figures unless the user explicitly asks for them; when images are used, store them under content/asset/.
---

# human-science-note-writer

## 基本方針

- 日本語で、Obsidian / Quartz にそのまま置ける完成記事を1本作る。
- ソース参照は必須。信頼できる文献・公的資料・ガイドライン・レビュー・主要原著論文に基づいて書く。
- 画像生成は通常行わない。ユーザーが明示的に「画像を作って」「imagegenで図を生成して」などと指示した場合だけ `imagegen` / `image_gen` を使う。
- 画像の追加・挿入も通常行わない。画像が必要な場合はユーザー側から明示指示があるものとして扱い、こちらから自発的に画像を入れない。
- 画像を使う場合は `content/asset/` 配下で管理する。記事別に分ける必要がある場合は `content/asset/{{記事スラッグ}}/` を作り、Markdown からは Quartz で解決しやすい相対パスで参照する。
- Mermaid、図説、図解、画像などの図は通常入れない。ユーザーが明示的に「図を入れて」「Mermaidで」「図解して」などと依頼した場合だけ使う。
- 図解が有用な場合でも、明示指示がなければ Markdown の表、箇条書き、短い段落、または「図解案」として文章で提示する。
- 医療・精神医学の内容は教育・研究目的として書き、個別診断・治療指示として断定しない。

## 高速ワークフロー

1. 依頼を1本の記事スコープに絞る。複数テーマが混ざる場合は中心テーマを自然に選び、残りは「今後の作成候補」に回す。
2. 既存ノート候補を `rg --files content` と必要最小限の `rg` で探す。未確認ノートを勝手に `[[...]]` 化しない。
3. 先に必要なソース種別を決める。通常は中核ソース6-10件、短い記事なら3-6件で始める。
4. ソースは「公的資料・ガイドライン」「システマティックレビュー/主要レビュー」「主要原著」「方法論・分類体系」の順に当たる。
5. 主張と根拠の対応を簡潔に整理してから本文を書く。根拠が薄い主張は「限界と未解決問題」に移す。
6. 本文、frontmatter、参考文献、関連ノート候補、MOC更新候補、未解決問題をまとめて完成させる。

探索を広げすぎない。主要主張に番号付き引用が付き、参考文献URL/DOIが確認できた時点で執筆へ進む。高リスクな医学的・統計的主張だけ追加確認する。

## 保存方針

- `content/` を vault root として扱い、`vault/` は作らない。
- 新規記事は既存の番号付きカテゴリに保存する。迷う場合は `content/90_未分類・インボックス/` に置く。
- frontmatter には原則として `title`, `description`, `aliases`, `tags`, `created`, `updated`, `draft`, `publish`, `status`, `enableToc` をこの順で含める。
- 通常記事の初期値は `draft: true`, `publish: false`, `status: draft` とする。公開済みMOCや公開前提の索引では `draft: false`, `publish: true`, `status: published` とする。

## 内部リンク

- 内部リンクは確認済みの既存ノート、またはユーザーが明示的に作成・リンクを指示したノートだけ `[[ノート名]]` にする。
- 未作成ノートは wikilink にせず、「関連ノート候補」「今後の作成候補」に通常テキストで列挙する。
- 1記事内の内部リンクは多すぎないようにし、読者の理解を助ける自然な導線に絞る。

## 引用と参考文献

- 本文中の重要な主張には `[1]` の形式で番号付き引用を付ける。
- 参考文献は番号付きで並べ、各項目に DOI URL または公式URLを含める。
- URLのない参考文献を置かない。見つからない場合は代替ソースを探す。
- 複数ソースで見解が分かれる場合は「確立」「有力」「議論中」「仮説」を区別する。

## 記事品質

- 初学者から中上級者まで読めるよう、導入は直感的に、本文後半で専門性を上げる。
- 専門用語は初出で短く説明する。
- 医療・臨床応用は、研究知見と臨床判断を混同しない。
- 下書き、メモ、TODOのまま残さず、完成記事として読める状態にする。

## 標準構成

```markdown
---
title: "{{title}}"
description: "{{one_sentence_description}}"
aliases:
  - "{{alias}}"
tags:
  - 領域/{{domain}}
  - 種類/{{note_type}}
created: "{{YYYY-MM-DD}}"
updated: "{{YYYY-MM-DD}}"
draft: true
publish: false
status: draft
enableToc: true
---

# {{title}}

## このノートの問い
## 先に要点
## 背景
## 基本概念
## 研究・臨床・学習との接続
## よくある誤解
## 限界と未解決問題
## 関連ノート候補
## MOC更新候補
## 参考文献
## 更新ログ
```
