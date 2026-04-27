import unittest
from pathlib import Path
import sys
import shutil

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))
TMP_ROOT = Path.cwd() / "test-work-runtime" / "vault_index"
TMP_ROOT.mkdir(parents=True, exist_ok=True)

from vault_index import build_index


class VaultIndexTest(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TMP_ROOT, ignore_errors=True)

    def test_extract_frontmatter_and_wikilink(self):
        root = TMP_ROOT
        note = root / "A.md"
        note.write_text(
            "---\n"
            'title: "予測処理"\n'
            "aliases:\n"
            "  - predictive processing\n"
            "tags:\n"
            "  - 領域/認知科学\n"
            "---\n\n"
            "# 予測処理\n\n"
            "[[統合失調症]] と関係する。\n",
            encoding="utf-8",
        )
        index = build_index(root)
        self.assertEqual(index[0]["title"], "予測処理")
        self.assertIn("predictive processing", index[0]["aliases"])
        self.assertIn("領域/認知科学", index[0]["tags"])
        self.assertIn("統合失調症", index[0]["wikilinks"])


if __name__ == "__main__":
    unittest.main()
