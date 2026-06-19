import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_TEXT = (ROOT / "SKILL.md").read_text(encoding="utf-8")


class SkillContractTests(unittest.TestCase):
    def test_hexagram_meaning_precedes_najia_analysis(self):
        headings = [
            "## 二、卦意解读",
            "### 本卦",
            "### 动爻",
            "### 变卦",
            "## 三、纳甲分析",
            "## 四、结论",
        ]

        positions = [SKILL_TEXT.index(heading) for heading in headings]

        self.assertEqual(positions, sorted(positions))

    def test_hexagram_meaning_is_not_applied_to_the_user(self):
        self.assertIn("只解释卦爻本义", SKILL_TEXT)
        self.assertIn("不得映射到用户、对方或现实事件", SKILL_TEXT)

    def test_output_does_not_keep_the_legacy_second_section(self):
        self.assertNotIn("## 二、用神选择", SKILL_TEXT)


if __name__ == "__main__":
    unittest.main()
