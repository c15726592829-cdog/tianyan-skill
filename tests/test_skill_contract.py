from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class SkillContractTests(unittest.TestCase):
    def test_skill_declares_accuracy_mode_and_references(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("## Accuracy Test Mode", text)
        self.assertIn("references/classical-interpretation-rules.md", text)
        self.assertIn("references/accuracy-testing.md", text)
        self.assertIn("Scoring dimensions and match rules:", text)

    def test_classical_guardrail_phrases(self):
        path = ROOT / "references" / "classical-interpretation-rules.md"
        self.assertTrue(path.is_file(), f"missing reference: {path.name}")
        text = path.read_text(encoding="utf-8")
        for phrase in (
            "specific friend or outside person",
            "static line does not mean absence",
            "not universal gender labels",
            "three-combination",
            "named modern city",
            "branch match alone",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_accuracy_protocol_sections(self):
        path = ROOT / "references" / "accuracy-testing.md"
        self.assertTrue(path.is_file(), f"missing reference: {path.name}")
        text = path.read_text(encoding="utf-8")
        for heading in (
            "## Activation",
            "## Pre-Reveal Record",
            "## Post-Reveal Scoring",
            "## Reproducibility Record",
        ):
            with self.subTest(heading=heading):
                self.assertIn(heading, text)
        self.assertIn("does not count as a hit", text)
        self.assertIn("locked scoring dimensions", text)
        for dimension in ("direction", "date", "time-window"):
            with self.subTest(dimension=dimension):
                self.assertIn(dimension, text)

    def test_exact_answer_confidence_caps(self):
        text = (ROOT / "references" / "classical-interpretation-rules.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("open-world named modern city: weak", text)
        self.assertIn("exact date or clock time: weak", text)
        self.assertIn("exact modern object: at most medium", text)

    def test_question_routing_contract(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("references/question-types/index.md", text)
        self.assertIn("Primary category:", text)
        self.assertIn("Primary anchor or useful spirit:", text)
        self.assertIn("Maximum defensible resolution:", text)

    def test_accuracy_retrospective_is_bounded_reference(self):
        skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        common_text = (
            ROOT / "references" / "question-types" / "common-rules.md"
        ).read_text(encoding="utf-8")
        path = ROOT / "references" / "accuracy-retrospectives.md"
        self.assertTrue(path.is_file(), f"missing reference: {path.name}")
        text = path.read_text(encoding="utf-8")

        self.assertIn("references/accuracy-retrospectives.md", skill_text)
        self.assertIn("Accuracy Retrospective Use", common_text)
        for phrase in (
            "Prospective-only",
            "Context Isolation",
            "Resolution Limits",
            "not a predictive accuracy proof",
            "Do not score revealed-answer reinterpretations",
            "YES/NO",
            "open-ended exact questions",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_accuracy_retrospective_does_not_embed_revealed_answer_keys(self):
        retrospective = (
            ROOT / "references" / "accuracy-retrospectives.md"
        ).read_text(encoding="utf-8")
        all_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in ROOT.rglob("*")
            if path.suffix in {".md", ".py", ".json", ".yaml", ".yml"}
            and "tests" not in path.parts
        )

        for term in ("earphones",):
            with self.subTest(term=term, scope="retrospective"):
                self.assertNotIn(term, retrospective)

        for term in ("白色手机", "河南许昌", "许昌", "洛阳", "济宁市", "莱西市", "耳机", "真相"):
            with self.subTest(term=term, scope="skill"):
                self.assertNotIn(term, all_text)

    def test_reading_contract_and_review_protocol(self):
        skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        path = ROOT / "references" / "reading-contract-and-review.md"

        self.assertTrue(path.is_file(), f"missing reference: {path.name}")
        self.assertIn("references/reading-contract-and-review.md", skill_text)

        text = path.read_text(encoding="utf-8")
        for heading in (
            "## Question Lock",
            "## External Context Boundary",
            "## Ordinary Outcome Review",
        ):
            with self.subTest(heading=heading):
                self.assertIn(heading, text)

        for phrase in (
            "exact user question",
            "maximum defensible resolution",
            "already been revealed",
            "舍卦从应",
            "does not justify a recast",
            "preserve the original conclusion",
            "future unrevealed case",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_output_exposes_question_lock(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        for field in (
            "Exact question:",
            "Locked before interpretation:",
            "Concrete matter or event:",
            "Requested time window:",
            "Known real-world facts:",
            "Outcome already revealed:",
        ):
            with self.subTest(field=field):
                self.assertIn(field, text)

    def test_skill_line_count_stays_compact(self):
        line_count = len((ROOT / "SKILL.md").read_text(encoding="utf-8").splitlines())
        self.assertLess(line_count, 500)


if __name__ == "__main__":
    unittest.main()
