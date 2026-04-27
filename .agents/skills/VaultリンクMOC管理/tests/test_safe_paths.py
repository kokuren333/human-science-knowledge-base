import unittest
from pathlib import Path
import sys
import shutil

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))
TMP_ROOT = Path.cwd() / "test-work-runtime" / "safe_paths"
TMP_ROOT.mkdir(parents=True, exist_ok=True)

from safe_paths import sanitize_filename, safe_join, unique_path


class SafePathsTest(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TMP_ROOT, ignore_errors=True)

    def test_japanese_title_is_preserved(self):
        self.assertEqual(sanitize_filename("予測処理と統合失調症"), "予測処理と統合失調症")

    def test_dangerous_chars_are_removed(self):
        self.assertEqual(sanitize_filename('a<b>c:d/e\\f|g?h*'), "abcdefgh")

    def test_unique_path_adds_suffix(self):
        path = TMP_ROOT / "ノート.md"
        sibling = TMP_ROOT / "ノート-2.md"
        for candidate in (path, sibling):
            if candidate.exists():
                candidate.unlink()
        path.write_text("x", encoding="utf-8")
        self.assertEqual(unique_path(path).name, "ノート-2.md")

    def test_safe_join_blocks_traversal(self):
        root = TMP_ROOT / "join"
        root.mkdir(exist_ok=True)
        joined = safe_join(root, "..", "危険")
        self.assertTrue(str(joined).startswith(str(root.resolve())))


if __name__ == "__main__":
    unittest.main()
