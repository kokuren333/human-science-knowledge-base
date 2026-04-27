---
name: quartz-publish-preflight
description: Check Obsidian Markdown articles under content/ for Quartz publication readiness, including frontmatter, wikilinks, aliases, tags, descriptions, file paths, attachments when present, numbered in-text citations, references with URLs, one-article scope, and readability. Use before publishing a content/ vault or article with Quartz. Do not require or add images unless the article or user explicitly requires them; when images are used, require them under content/asset/.
---

# quartz-publish-preflight

## 目的

Obsidian / Quartz 向け記事を公開前に点検する。公開可能性、frontmatter、内部リンク、参考文献、本文品質、医療安全表現を確認し、修正すべき点を blocking issues / warnings / suggested fixes に分ける。

画像は必須条件にしない。こちらから画像追加を要求しない。記事内に画像がある場合だけ、alt text、キャプション、配置、Quartzで解決できるパスを確認する。

## チェック項目

- frontmatter があるか。
- frontmatter が `title`, `description`, `aliases`, `tags`, `created`, `updated`, `draft`, `publish`, `status`, `enableToc` の順にそろっているか。
- 通常記事は `draft: true`, `publish: false`, `status: draft`、公開済みMOCや公開前提の索引は `draft: false`, `publish: true`, `status: published` になっているか。
- 記事が下書きではなく、完成記事として読めるか。
- `[[ノート名]]` が既存ノート、またはユーザーが明示した作成対象だけを指しているか。
- 勝手に未作成ノートへの wikilink が追加されていないか。
- 指示されていない関連ノートや記事ファイルが作成されていないか。
- 参考文献が番号付きで存在するか。
- 本文中引用番号と参考文献番号が対応しているか。
- 参考文献に DOI URL または公式URLがあるか。
- 強い主張、統計値、診断分類、介入効果、理論名、歴史的経緯に引用が付いているか。
- 1つの記事内で複数テーマを無理に統合していないか。
- 長文記事では目次に耐える見出し構成か。
- 保存先が `content/` 配下で、`vault/` を作っていないか。
- 医療・精神医学ノートで個別診断や治療指示として読める断定がないか。
- 初学者から中上級者まで読める導入、用語説明、深掘りがあるか。

## 画像がある場合だけ確認

- Markdown画像に alt text があるか。
- 日本語キャプションまたは本文中の説明があるか。
- 画像ファイルが `content/asset/` 管理下にあり、Quartzで解決しやすい相対パスになっているか。
- 未検証の因果関係、診断・治療効果、過度に断定的な図になっていないか。

## 出力形式

```markdown
## Preflight report

### Blocking issues

- {{公開前に必ず直す問題}}

### Warnings

- {{公開可能だが改善したい点}}

### Suggested fixes

- {{具体的な修正案}}

### Publish readiness

- verdict: ready / needs-fixes / do-not-publish
- reason: {{短い理由}}
```
