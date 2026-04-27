# Skills 使用例

## 研究ノートを作る

```text
$human-science-note-writer
「予測処理と統合失調症の関係について、初学者から研究者まで読める Obsidian ノートにして。数式は必要最低限で、関連ノート候補と MOC も提案して。」
```

## vault 内リンクを整理する

```text
$vault-linker-moc-builder
「content/ 以下を走査して、計算論的精神医学に関連するノートの MOC を更新して。壊れたリンク候補も教えて。」
```

## 文献ベースでまとめる

```text
$scientific-source-curator
「うつ病の認知バイアスに関する主要レビューと古典論文を整理して、ノート作成に使える参考文献リストを作って。」
```

## 数理モデルノートを作る

```text
$computational-math-model-note
「Rescorla-Wagner モデルを、強化学習・予測誤差・精神医学との関係がわかるように LaTeX つきでまとめて。」
```

## Quartz 公開前チェック

```text
$quartz-publish-preflight
「content/03_精神医学/うつ病の認知モデル.md を Quartz 公開前にチェックして。」
```

## 推奨ワークフロー

1. まずノートを書かせる。
2. vault 内の関連記事を探す。
3. 内部リンクを追加する。
4. MOC を更新する。
5. Quartz 公開前チェックを行う。
6. 公開する場合だけ `draft: false`, `publish: true` にする。

## 補助スクリプト

```bash
python .agents/skills/VaultリンクMOC管理/scripts/vault_index.py --root content --json
python .agents/skills/VaultリンクMOC管理/scripts/suggest_links.py --root content --title "予測処理と統合失調症" --tags "領域/計算論的精神医学,領域/精神医学"
python .agents/skills/VaultリンクMOC管理/scripts/update_moc.py --moc content/00_MOC/MOC｜計算論的精神医学.md --link "予測処理と統合失調症"
python .agents/skills/VaultリンクMOC管理/scripts/quartz_check.py --root content
```
