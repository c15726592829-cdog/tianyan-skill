# Tianyan Original Text Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Require original Zhouyi text before every hexagram and moving-line interpretation.

**Architecture:** Extend the existing Markdown output contract without changing the charting script. Enforce the order with a UTF-8 contract test.

**Tech Stack:** Markdown, Python 3.10+, `unittest`

## Global Constraints

- Original text precedes interpretation.
- Only actual moving lines are quoted.
- Paraphrases and modern translations are never labeled as original text.

---

### Task 1: Lock the output order

**Files:**
- Modify: `tests/test_skill_contract.py`

**Interfaces:**
- Consumes: `SKILL.md`
- Produces: assertions for original-text field order and source integrity

- [ ] Add assertions for `卦辞与大象原文 -> 卦意` and `爻辞原文 -> 爻意`.
- [ ] Run the focused test and confirm it fails against the old template.

### Task 2: Update the skill contract

**Files:**
- Modify: `SKILL.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: the existing layered interpretation workflow
- Produces: original text before primary, moving-line, and changed interpretation

- [ ] Add source-integrity rules to `Interpretation Order`.
- [ ] Replace the three output slots with explicit original-text-first fields.
- [ ] Document the rule in `README.md`.
- [ ] Run focused and full tests.

### Task 3: Validate and publish

**Files:**
- Sync: `SKILL.md` to `C:\Users\c1572\.codex\skills\tianyan`

**Interfaces:**
- Consumes: verified repository skill
- Produces: matching installed and GitHub versions

- [ ] Run official validation for repository and installed copy.
- [ ] Compare repository and installed `SKILL.md` hashes.
- [ ] Commit and push `main`.
