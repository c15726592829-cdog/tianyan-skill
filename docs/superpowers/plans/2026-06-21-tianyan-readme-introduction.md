# Tianyan README Introduction Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the repository's one-line README summary with the approved philosophical and engineering introduction.

**Architecture:** Keep the documentation change isolated to the opening of `README.md`. Add one contract test that fixes the approved wording and placement while leaving the existing technical sections untouched.

**Tech Stack:** Markdown, Python 3 standard-library `unittest`, Git.

## Global Constraints

- Replace `文王六爻纳甲排盘与断卦辅助 skill。`; do not retain it as duplicate copy.
- Place the approved motto and three paragraphs before `## 支持范围`.
- Preserve `## 支持范围` and every following README section unchanged.
- Do not change runtime skill behavior, scripts, references, or metadata.

---

### Task 1: Add The Approved README Introduction

**Files:**
- Create: `tests/test_readme_contract.py`
- Modify: `README.md:1-5`

**Interfaces:**
- Consumes: the approved copy in `docs/superpowers/specs/2026-06-21-tianyan-readme-introduction-design.md`
- Produces: a README opening whose wording and placement are enforced by `unittest`

- [ ] **Step 1: Write the failing README contract test**

```python
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
```

- [ ] **Step 2: Run the focused test and verify the expected failure**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_readme_contract
```

Expected: `FAIL` because the motto and approved introduction are absent.

- [ ] **Step 3: Replace the README one-line summary with the approved copy**

The beginning of `README.md` must become:

```markdown
# Tianyan Skill

> 大道五十，天衍四九，人遁其一。  
> 天行健，君子以自强不息。

**Tianyan** 是一个面向文王六爻的纳甲排盘与分析 Skill。它以传统卦理观察事物的结构、变化与趋势，却不把卦象视为不可更改的命令。

“四十九”代表可以推演和认识的部分；遁去的“一”，则留给人的智慧、勇气、实力与行动。卦象提供参考，选择仍归于人。所谓自强不息，正是在看见局势之后，仍以自身行动开辟可能。

在工程实现上，Tianyan 使用确定性排盘、可审计的三硬币模拟和明确的分析边界，力求让每一项排盘结果可复核、每一层判断有依据，并始终将现实事实置于象数推演之上。

## 支持范围
```

- [ ] **Step 4: Run the focused and full test suites**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_readme_contract
python -m unittest discover -s tests
```

Expected: the focused test passes and the full suite reports no failures.

- [ ] **Step 5: Verify the Markdown diff**

Run:

```powershell
git diff --check
git diff -- README.md tests/test_readme_contract.py
```

Expected: no whitespace errors; only the approved README opening and its contract test are changed.

- [ ] **Step 6: Commit and push**

```powershell
git add README.md tests/test_readme_contract.py
git commit -m "docs: introduce tianyan philosophy"
git push origin main
```

Expected: `main` is synchronized with `origin/main`.
