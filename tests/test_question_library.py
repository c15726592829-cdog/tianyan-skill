from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_question_library import validate_library


class QuestionLibraryTests(unittest.TestCase):
    def test_question_library_schema_and_contract_is_valid(self):
        # The JSON cases are coverage fixtures for the LLM routing contract.
        # This skill does not currently expose a deterministic NLP classifier.
        self.assertEqual(validate_library(ROOT), [])


if __name__ == "__main__":
    unittest.main()
