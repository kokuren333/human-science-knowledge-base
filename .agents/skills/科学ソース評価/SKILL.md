---
name: scientific-source-curator
description: Evaluate, rank, and summarize scientific and clinical sources for one Obsidian article at a time. Use when the user asks for reliable sources, citations, literature review, evidence grading, psychiatric or neuroscience references, source-first article creation, efficient source discovery, numbered in-text citation planning, or references that must include URLs/DOIs. Do not create SVG, Mermaid/mermaid.js, HTML/CSS/canvas, ASCII-art, or code-generated diagrams. If a figure is explicitly requested, prepare only an imagegen/image_gen raster image brief.
---

# scientific-source-curator

## 目的

記事作成の前工程として、信頼できるソースを高速に選び、主要主張と根拠の対応を整理する。最終出力は、記事本文に渡せる `Source brief`、`Claim-evidence table`、`Article brief`、番号付き参考文献にする。

画像生成は通常行わない。ユーザーが明示的に画像生成を依頼した場合だけ、`imagegen` / `image_gen` 用のラスター画像 brief を作る。SVG、Mermaid / mermaid.js、HTML/CSS/canvas、ASCII art、その他のコード生成による図・図解・概念図・フローチャート・模式図の brief は作らない。

## 高速ソース探索

1. テーマを1本の記事で扱えるリサーチクエスチョンに変換する。
2. 必要なソース種別を先に決める。医学・精神医学はガイドライン、公的資料、分類体系、システマティックレビューを優先する。
3. 通常は3-6件の最重要ソースで骨格を作り、必要に応じて6-10件まで広げる。
4. claim-evidence table の主要行に引用番号が付いた時点で探索を止める。
5. 根拠が見つからない主張は本文に入れず、「未解決問題」または「避けるべき断定」に回す。

検索を広げる前に、今あるソースで記事の中心主張を支えられるか確認する。広く浅く集めるより、少数の強い根拠を読む。

## ソース優先順位

医療・精神医学:

1. 診療ガイドライン、WHO/NIH/NIMH/学会などの公的資料
2. DSM / ICD などの分類体系
3. システマティックレビュー / メタ解析
4. 大規模RCT / コホート研究
5. 主要レビュー論文
6. 歴史的に重要な原著論文
7. 教科書・専門書

神経科学・認知科学:

1. Nature Reviews、Annual Review、Trends 系などの主要レビュー
2. 原著論文
3. 方法論レビュー
4. 研究機関・学会の解説

機械学習・統計・数理モデル:

1. 原著論文
2. 方法論論文
3. 公式ドキュメント
4. CONSORT / STROBE / TRIPOD / SPIRIT などの報告ガイドライン
5. 標準的教科書・レビュー

## 評価基準

- 何を支える根拠かを1文で言えるか。
- 研究デザイン、対象、限界、一般化可能性が分かるか。
- DOI URL または公式URLを確認できるか。
- 記事の中心主張に直接関係するか。
- 医学的・臨床的主張を過剰に一般化していないか。

## 出力形式

```markdown
## Source brief

- 中心問い:
- 重要な背景:
- 確立している点:
- 議論中の点:
- 避けるべき断定:

## Claim-evidence table

| citation_no | article_section | 主張 | 根拠 | ソース種別 | 確信度 | 注意点 |
|---|---|---|---|---|---|---|
| [1] | {{section}} | {{claim}} | {{source}} | review/guideline/original/etc | 高/中/低 | {{limitation}} |

## Article brief

- タイトル候補:
- 中心問い:
- 想定読者:
- 主要主張と引用番号:
- 推奨見出し:
- 初学者向け導入:
- 深掘りすべき点:
- 未解決問題:

## 参考文献

[1] 著者. (年). タイトル. *雑誌名/出版社*, 巻(号), ページ. https://doi.org/... または公式URL
```

## 医療安全

臨床ノートでは、「研究で示されていること」「臨床現場での考え方」「未確立な仮説」を分ける。個別症例への診断や治療指示として読める書き方は避ける。
