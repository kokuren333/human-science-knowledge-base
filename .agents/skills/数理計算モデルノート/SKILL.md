---
name: computational-math-model-note
description: Create one Japanese Obsidian/Quartz finished article per user instruction for mathematical models, machine learning, Bayesian inference, reinforcement learning, neural networks, predictive processing, active inference, dynamical systems, psychometrics, and computational psychiatry under content/ as the vault root. Use when LaTeX equations, model assumptions, algorithms, pseudocode, model-to-clinical interpretation, numbered in-text citations, and references with URLs are needed. Do not create SVG, Mermaid/mermaid.js, HTML/CSS/canvas, ASCII-art, or code-generated diagrams. If a figure is explicitly requested, use only imagegen/image_gen raster image generation and store images under content/asset/.
---

# computational-math-model-note

## 基本方針

- 数理モデル・機械学習・計算論的精神医学の記事を、日本語の完成ノートとして1本作る。
- ソース参照は必須。原著論文、方法論論文、主要レビュー、公式ドキュメントを優先する。
- 画像生成は通常行わない。ユーザーが明示的に依頼した場合だけ `imagegen` / `image_gen` によるラスター画像生成を使う。
- 画像の追加・挿入も通常行わない。画像が必要な場合はユーザー側から明示指示があるものとして扱い、こちらから自発的に画像を入れない。
- 画像を使う場合は `content/asset/` 配下で管理する。記事別に分ける必要がある場合は `content/asset/{{記事スラッグ}}/` を作り、Markdown からは Quartz で解決しやすい相対パスで参照する。
- SVG、Mermaid / mermaid.js、HTML/CSS/canvas、ASCII art、その他のコード生成による図・図解・概念図・フローチャート・模式図の作成は禁止する。
- 図が必要に見える場合でも、`imagegen` / `image_gen` の明示指示がなければ表、擬似コード、数式、箇条書き、短い段落、または文章による図解案で済ませる。
- 臨床解釈は教育・研究目的に限定し、個別診断や治療指示として書かない。

## 高速ワークフロー

1. 中心モデルを1つ決める。複数モデルがある場合は主モデルを選び、派生モデルは比較表や今後の候補に回す。
2. 既存ノートとMOC候補を `rg --files content` と必要最小限の `rg` で確認する。
3. 主要ソース5-8件を先に固める。式・アルゴリズム・仮定を確認するため、原著または方法論論文を必ず含める。
4. 変数、仮定、目的関数、推論・学習手順、応用、限界を整理してから本文を書く。
5. 式や解釈が不確かな箇所は断定せず、「表記揺れ」「未解決問題」「実装上の注意」に分ける。
6. frontmatter、本文中引用、参考文献、関連ノート候補、MOC更新候補まで整えて完了する。

探索は、モデルの定義・式・代表的応用を支える根拠がそろった時点で止める。高リスクな臨床解釈や比較主張だけ追加確認する。

## 保存方針

- `content/` を vault root として扱い、`vault/` は作らない。
- 主題に応じて `content/05_機械学習・AI/`, `content/06_数理モデル・計算論/`, `content/07_計算論的精神医学/` など既存カテゴリに保存する。
- 迷う場合は `content/90_未分類・インボックス/` に置き、MOC更新候補で移動先を提案する。
- frontmatter には `title`, `description`, `aliases`, `tags`, `created`, `updated`, `draft`, `publish`, `status`, `enableToc` をこの順で含める。
- 通常記事の初期値は `draft: true`, `publish: false`, `status: draft` とする。

## 引用と数式

- 本文中の重要なモデル定義、式、アルゴリズム、応用主張には `[1]` 形式で引用を付ける。
- DOIがある文献は `https://doi.org/...` を参考文献に入れる。ない場合は公式URLを使う。
- 数式は Quartz で読める LaTeX にする。
- 変数表を置き、記号の意味・単位・注意を短く説明する。

## 記事品質

- 直感、変数、式、アルゴリズム、応用、限界の順で説明する。
- 初学者を数式にいきなり落とさず、式の読み方を添える。
- モデルの説明力と予測力、記述モデルと生成モデル、相関と因果を混同しない。
- 計算論的精神医学・臨床応用では、モデルによる解釈を診断や治療方針として断定しない。

## 標準構成

````markdown
---
title: "{{title}}"
description: "{{one_sentence_description}}"
aliases:
  - "{{alias}}"
tags:
  - 領域/{{domain}}
  - 種類/数理モデル
created: "{{YYYY-MM-DD}}"
updated: "{{YYYY-MM-DD}}"
draft: true
publish: false
status: draft
enableToc: true
---

# {{title}}

## モデルが答えたい問い
## 直感
## 変数と記号

| 記号 | 意味 | 注意 |
|---|---|---|
| $x$ | {{meaning}} | {{note}} |

## 仮定
## 数式

$$
{{equation}}
$$

## 推論・学習の手順

```text
1. initialize ...
2. observe ...
3. update ...
```

## 心理・脳・臨床との接続
## 限界
## 関連ノート候補
## MOC更新候補
## 参考文献
````
