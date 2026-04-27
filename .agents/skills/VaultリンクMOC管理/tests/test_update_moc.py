import unittest
from pathlib import Path
import sys
import shutil

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))
TMP_ROOT = Path.cwd() / "test-work-runtime" / "update_moc"
TMP_ROOT.mkdir(parents=True, exist_ok=True)

from update_moc import add_link_to_moc


class UpdateMocTest(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TMP_ROOT, ignore_errors=True)

    def test_add_link_is_idempotent(self):
        moc = TMP_ROOT / "MOC｜計算論的精神医学.md"
        if moc.exists():
            moc.unlink()
        self.assertTrue(add_link_to_moc(moc, "予測処理と統合失調症"))
        self.assertFalse(add_link_to_moc(moc, "予測処理と統合失調症"))
        text = moc.read_text(encoding="utf-8")
        self.assertEqual(text.count("[[予測処理と統合失調症]]"), 1)


if __name__ == "__main__":
    unittest.main()
