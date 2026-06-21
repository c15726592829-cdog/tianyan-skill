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

    def test_original_text_precedes_each_hexagram_interpretation(self):
        meaning_section = SKILL_TEXT.split("## 二、卦意解读", 1)[1].split(
            "## 三、纳甲分析", 1
        )[0]
        primary = meaning_section.split("### 本卦", 1)[1].split("### 动爻", 1)[0]
        moving = meaning_section.split("### 动爻", 1)[1].split("### 变卦", 1)[0]
        changed = meaning_section.split("### 变卦", 1)[1]

        self.assertLess(
            primary.index("- 卦辞与大象原文："), primary.index("- 白话文：")
        )
        self.assertLess(
            moving.index("- 爻辞原文："), moving.index("- 白话文：")
        )
        self.assertLess(
            changed.index("- 卦辞与大象原文："), changed.index("- 白话文：")
        )
        self.assertIn("不得把转述或白话释义标为原文", SKILL_TEXT)

    def test_assistant_casting_requires_explicit_request_and_one_live_run(self):
        self.assertIn("你帮我起卦", SKILL_TEXT)
        self.assertIn("python scripts/qi_gua.py", SKILL_TEXT)
        self.assertIn("run `qi_gua.py` exactly once", SKILL_TEXT)
        self.assertIn("Never rerun", SKILL_TEXT)
        self.assertIn("replay output is audit-only", SKILL_TEXT.lower())

    def test_manual_lines_take_precedence_over_assistant_casting(self):
        self.assertIn("Never replace user-supplied lines", SKILL_TEXT)
        self.assertIn("script's actual execution minute", SKILL_TEXT)

    def test_hexagram_layer_is_original_text_plus_plain_translation_only(self):
        meaning_section = SKILL_TEXT.split("## 二、卦意解读", 1)[1].split(
            "## 三、纳甲分析", 1
        )[0]

        self.assertEqual(meaning_section.count("- 白话文："), 3)
        self.assertNotIn("- 卦意：", meaning_section)
        self.assertNotIn("- 爻意：", meaning_section)
        self.assertNotIn("- 本卦至变卦的结构变化：", meaning_section)
        self.assertIn(
            "Question-specific interpretation begins in `纳甲分析`.",
            SKILL_TEXT,
        )


if __name__ == "__main__":
    unittest.main()
