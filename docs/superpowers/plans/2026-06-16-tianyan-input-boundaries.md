# Tianyan Input Boundaries Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Tighten `tianyan` input validation and repository quality while keeping the skill strictly Wenwang Liuyao Najia.

**Architecture:** Keep deterministic mechanics in `scripts/pai_gua.py`, behavioral usage rules in `SKILL.md`, supporting domain detail in `references/`, and repository quality metadata in root config files and GitHub Actions.

**Tech Stack:** Python 3.10+ standard library, `unittest`, Codex skill validator, GitHub Actions.

---

### Task 1: Parser Regression Tests

**Files:**
- Modify: `tests/test_pai_gua.py`
- Modify: `scripts/pai_gua.py`

- [ ] Add tests that reject date-only, hour-only, and seconds-bearing cast time inputs.
- [ ] Run the focused input tests and verify the new tests fail before implementation.
- [ ] Add tests that accept Chinese line names and trailing timezone in `--time`.
- [ ] Implement strict `parse_cast_time()` validation and Chinese aliases in `parse_line_values()`.
- [ ] Run focused input and calendar tests and verify they pass.

### Task 2: Skill Documentation

**Files:**
- Modify: `SKILL.md`

- [ ] Add a clear user input template near the top.
- [ ] Clarify timezone defaulting at the skill layer.
- [ ] Clarify one-day-three-casts scope and repeated-question criteria.
- [ ] Explicitly reject digital or Meihua-style input.
- [ ] Replace the output template with the stricter four-section format.

### Task 3: Repository Metadata And CI

**Files:**
- Create: `README.md`
- Create: `pyproject.toml`
- Create: `.github/workflows/test.yml`

- [ ] Add a concise GitHub-facing README.
- [ ] Declare Python 3.10+ in `pyproject.toml`.
- [ ] Add a GitHub Actions workflow that runs `python -m unittest discover -s tests`.

### Task 4: Verification And Publication

**Files:**
- Verify all changed files.

- [ ] Run the full unit test suite.
- [ ] Run official skill validation for the repo.
- [ ] Install/update the local `tianyan` skill runtime copy.
- [ ] Run official skill validation for the installed copy.
- [ ] Commit changes.
- [ ] Push `main` to GitHub.
