# Tianyan Interpretation Order Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Tianyan explain primary hexagram, moving lines, and changed hexagram before applying Najia analysis.

**Architecture:** Keep deterministic charting unchanged. Enforce the new behavior as a documented output contract in `SKILL.md`, cover it with a repository-level contract test, and summarize it in `README.md`.

**Tech Stack:** Markdown, Python 3.10+, `unittest`

## Global Constraints

- The hexagram-meaning layer contains no real-person mapping or advice.
- The Najia layer follows the hexagram-meaning layer and may apply the chart to the question.
- Existing input, counting, repeat-question, and safety rules remain unchanged.

---

### Task 1: Add the output contract test

**Files:**
- Create: `tests/test_skill_contract.py`

**Interfaces:**
- Consumes: repository `SKILL.md` as UTF-8 text
- Produces: a regression test for section order and interpretation boundaries

- [ ] **Step 1: Write the failing test**

```python
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
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python -m unittest tests.test_skill_contract -v`

Expected: FAIL because `## 二、卦意解读` is absent.

### Task 2: Implement the layered reading contract

**Files:**
- Modify: `SKILL.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: deterministic chart JSON and existing interpretation references
- Produces: required output order `排盘结果 -> 卦意解读 -> 纳甲分析 -> 结论`

- [ ] **Step 1: Update `Interpretation Order`**

Require this sequence:

```text
排盘 -> 本卦 -> 动爻 -> 变卦 -> 用神及纳甲 -> 结论
```

State that the first three interpretation slots contain only original
hexagram and line meaning, while question-specific application begins in
`纳甲分析`.

- [ ] **Step 2: Replace the output template**

Add these headings in order:

```markdown
## 二、卦意解读
### 本卦
### 动爻
### 变卦
## 三、纳甲分析
## 四、结论
```

For static hexagrams, state `无动爻` and omit a separate changed-hexagram
interpretation.

- [ ] **Step 3: Document the order in `README.md`**

Add a short `输出顺序` section with the same four layers.

- [ ] **Step 4: Run focused and full tests**

Run: `python -m unittest tests.test_skill_contract -v`

Expected: 2 tests pass.

Run: `python -m unittest discover -s tests -v`

Expected: all tests pass.

### Task 3: Validate, install, and publish

**Files:**
- Sync: repository files to `C:\Users\c1572\.codex\skills\tianyan`

**Interfaces:**
- Consumes: verified repository skill
- Produces: matching installed skill and pushed GitHub commit

- [ ] **Step 1: Run official validation on the repository**

Run: `python C:\Users\c1572\.codex\skills\.system\skill-creator\scripts\quick_validate.py C:\tmp\tianyan-skill-review-20260615`

Expected: validation succeeds.

- [ ] **Step 2: Sync and validate the installed copy**

Copy the changed skill files, then run the validator against
`C:\Users\c1572\.codex\skills\tianyan`.

Expected: validation succeeds and file hashes match.

- [ ] **Step 3: Commit and push**

```bash
git add SKILL.md README.md tests/test_skill_contract.py docs/superpowers/plans/2026-06-19-tianyan-interpretation-order.md
git commit -m "feat: separate hexagram meaning from Najia analysis"
git push origin main
```

Expected: remote `main` advances to the new commit.
