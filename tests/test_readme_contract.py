import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README_TEXT = (ROOT / "README.md").read_text(encoding="utf-8")


class ReadmeIntroductionTests(unittest.TestCase):
    def test_approved_introduction_precedes_support_scope(self):
        introduction = README_TEXT.split("## 支持范围", 1)[0]

        self.assertIn("大道五十，天衍四九，人遁其一。", introduction)
        self.assertIn("天行健，君子以自强不息。", introduction)
        self.assertIn("卦象提供参考，选择仍归于人。", introduction)
        self.assertIn("确定性排盘、可审计的三硬币模拟", introduction)
        self.assertNotIn("文王六爻纳甲排盘与断卦辅助 skill。", README_TEXT)


if __name__ == "__main__":
    unittest.main()
