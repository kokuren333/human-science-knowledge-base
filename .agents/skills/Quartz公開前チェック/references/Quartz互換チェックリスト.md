# Quartz 互換チェックリスト

- frontmatter が `---` で囲まれている。
- `title`, `description`, `tags`, `draft`, `publish`, `created`, `updated` がある。
- 長文ノートでは `enableToc: true` がある。
- 内部リンク `[[...]]` が既存ノート、title、alias のいずれかに対応している。
- 画像や添付が `content/` 以下にある。
- Obsidian プラグイン専用構文に依存しすぎていない。
- 見出し階層が `#` から自然に下がっている。
- 公開ページの description が検索結果やカード表示に耐える。
