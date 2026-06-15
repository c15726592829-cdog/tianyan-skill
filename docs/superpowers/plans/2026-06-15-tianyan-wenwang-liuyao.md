# Tianyan Wenwang Liuyao Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build, verify, install, and publish a deterministic Wenwang Liuyao Najia skill named `tianyan`.

**Architecture:** A concise `SKILL.md` controls triggering and workflow, two reference files hold traditional charting and interpretation rules, and a standard-library Python CLI performs deterministic chart construction. Unit tests pin every table and transformation that must not be improvised by the model.

**Tech Stack:** Markdown, YAML, Python 3 standard library, `unittest`, Git.

---

### Task 1: Establish Failing Chart Tests

**Files:**
- Create: `tests/test_pai_gua.py`

- [ ] Write tests for strict `6/7/8/9` input validation and bottom-to-top order.
- [ ] Write tests for primary/changed line transformations.
- [ ] Write table-driven tests for trigram identity, sixty-four hexagram names,
  eight-palace affiliation, Shi/Ying positions, Najia, relatives, and spirits.
- [ ] Write calendrical tests for day stem-branch, month commander, and xunkong
  using independently checked fixtures.
- [ ] Run `python -m unittest discover -s tests -v` and verify failure because
  `scripts.pai_gua` does not exist.

### Task 2: Implement Deterministic Charting

**Files:**
- Create: `scripts/__init__.py`
- Create: `scripts/pai_gua.py`
- Test: `tests/test_pai_gua.py`

- [ ] Implement parsing and line transformation minimally.
- [ ] Run focused tests and verify they pass.
- [ ] Implement trigram, hexagram, eight-palace, Shi/Ying, and Najia tables.
- [ ] Run focused tests and verify they pass.
- [ ] Implement six relatives and six spirits.
- [ ] Run focused tests and verify they pass.
- [ ] Implement timezone-aware month commander, day stem-branch, and xunkong.
- [ ] Run the full test suite and verify zero failures.
- [ ] Add a JSON CLI accepting `--question`, `--time`, `--timezone`, and
  `--lines`.
- [ ] Run a CLI smoke test and verify valid JSON.

### Task 3: Build The Skill Package

**Files:**
- Create: `SKILL.md`
- Create: `agents/openai.yaml`
- Create: `references/wenwang-liuyao-rules.md`
- Create: `references/interpretation-guide.md`
- Delete: `TIANYAN-SKILL.md`
- Delete: `README.md`

- [ ] Write valid YAML frontmatter with `name: tianyan`.
- [ ] Document the three required user fields and strict line encoding.
- [ ] Route all chart construction through `scripts/pai_gua.py`.
- [ ] Document useful-spirit selection and the traditional interpretation
  precedence without mixing Meihua Ti-Yong.
- [ ] Preserve daily limits, repeated-question handling, real-world checks, and
  high-stakes disclaimers.
- [ ] Add UI metadata in `agents/openai.yaml`.

### Task 4: Validate And Review

**Files:**
- Verify all package files.

- [ ] Run `python -m unittest discover -s tests -v`.
- [ ] Run the skill validator against the repository root.
- [ ] Search for forbidden mixed-method terms and confirm no operative Meihua
  or number-divination instructions remain.
- [ ] Run representative CLI examples for static and moving hexagrams.
- [ ] Review the diff for correctness and unnecessary files.

### Task 5: Install And Publish

**Files:**
- Install to: `C:\Users\c1572\.codex\skills\tianyan`

- [ ] Copy the verified package to the local Codex skill directory.
- [ ] Re-run validation against the installed copy.
- [ ] Configure repository-local Git author identity if absent.
- [ ] Commit the replacement with a descriptive message.
- [ ] Push `main` to `origin`.
- [ ] Verify the remote `main` commit matches local `HEAD`.
