# Tianyan Assistant Coin Casting Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an auditable six-line three-coin casting script and allow Tianyan to use it only when the user explicitly requests assistant casting.

**Architecture:** Keep randomness in a new `scripts/qi_gua.py` module and keep `scripts/pai_gua.py` deterministic. The skill runs casting once, shows its audit record, and passes the resulting time and bottom-to-top lines into the existing chart script.

**Tech Stack:** Python 3.10+, standard library `secrets`, `hashlib`, `zoneinfo`, `argparse`, JSON, `unittest`

## Global Constraints

- Use three coins per line and six throws in bottom-to-top order.
- Map `字面=2`, `背面=3`, producing `6/7/8/9` with probability `1:3:3:1`.
- Live casting uses OS-backed entropy and the script's actual execution minute.
- Run live casting exactly once and never reroll because of an inconvenient result.
- Replay is audit-only and is never interpreted as a new cast.
- Manual user-supplied lines remain unchanged and take precedence.
- The hexagram layer contains only original text followed by plain translation; question-specific application begins in Najia analysis.
- Do not change chart mathematics in `scripts/pai_gua.py`.

---

### Task 1: Three-Coin Casting Core

**Files:**
- Create: `scripts/qi_gua.py`
- Create: `tests/test_qi_gua.py`

**Interfaces:**
- Produces: `line_from_bits(bits: tuple[int, int, int]) -> dict[str, object]`
- Produces: `build_cast(question: str, timezone_name: str, *, entropy: bytes | None = None, moment: datetime | None = None, mode: str = "live") -> dict[str, object]`
- CLI consumes: `--question`, `--timezone`, optional paired `--replay-entropy`, `--replay-time`
- CLI produces: UTF-8 JSON with method, algorithm, mode, entropy, time, throws, and line values

- [ ] **Step 1: Write failing mapping and replay tests**

```python
from itertools import product

from scripts.qi_gua import build_cast, line_from_bits


def test_all_coin_combinations_have_traditional_distribution():
    values = [line_from_bits(bits)["line_value"] for bits in product((0, 1), repeat=3)]
    assert {value: values.count(value) for value in range(6, 10)} == {
        6: 1,
        7: 3,
        8: 3,
        9: 1,
    }


def test_fixed_entropy_is_reproducible_bottom_to_top():
    cast = build_cast(
        "测试",
        "Asia/Shanghai",
        entropy=bytes(range(32)),
        moment=datetime(2026, 6, 21, 15, 46, tzinfo=ZoneInfo("Asia/Shanghai")),
        mode="replay",
    )
    assert cast["line_values"] == [7, 6, 8, 7, 7, 9]
    assert [throw_["line"] for throw_ in cast["throws"]] == [1, 2, 3, 4, 5, 6]
```

- [ ] **Step 2: Run focused tests and verify RED**

Run: `python -m unittest tests.test_qi_gua -v`

Expected: import failure because `scripts.qi_gua` does not exist.

- [ ] **Step 3: Implement the minimal casting core**

```python
DOMAIN = b"tianyan-three-coin-v1\0"
ENTROPY_BYTES = 32
LINE_NAMES = {6: "老阴", 7: "少阳", 8: "少阴", 9: "老阳"}


def _coin_bits(entropy: bytes) -> list[int]:
    digest = hashlib.sha256(DOMAIN + entropy).digest()
    return [(digest[index // 8] >> (7 - index % 8)) & 1 for index in range(18)]


def line_from_bits(bits):
    values = [2 + bit for bit in bits]
    line_value = sum(values)
    return {
        "coins": [
            {"side": "背面" if bit else "字面", "value": value}
            for bit, value in zip(bits, values)
        ],
        "sum": line_value,
        "line_value": line_value,
        "line_name": LINE_NAMES[line_value],
        "moving": line_value in {6, 9},
    }
```

`build_cast` must validate a non-empty question, IANA timezone, 32-byte entropy,
and mode. It must capture one timezone-aware minute, create six numbered throws,
and expose `entropy_hex`, `cast_time`, and `line_values`.

- [ ] **Step 4: Run focused tests and verify GREEN**

Run: `python -m unittest tests.test_qi_gua -v`

Expected: mapping and fixed-entropy tests pass.

- [ ] **Step 5: Add failing CLI tests**

Add tests that invoke `scripts/qi_gua.py` and assert:

```python
payload["method"] == "three_coin"
payload["algorithm"] == "tianyan-three-coin-v1"
payload["mode"] == "replay"
payload["line_values"] == [7, 6, 8, 7, 7, 9]
len(payload["throws"]) == 6
```

Also assert that `--replay-entropy` without `--replay-time` exits with code `2`.

- [ ] **Step 6: Implement live and replay CLI modes**

Live mode must call `secrets.token_bytes(32)` and `datetime.now(ZoneInfo(...))`.
Replay mode must require 64 hexadecimal characters and strict
`YYYY-MM-DD HH:MM` time. Both modes emit UTF-8 JSON; invalid input emits one
error on stderr and exits `2`.

- [ ] **Step 7: Run the casting test suite**

Run: `python -m unittest tests.test_qi_gua -v`

Expected: all casting tests pass without random-distribution assertions.

### Task 2: Skill Workflow And Output Contract

**Files:**
- Modify: `SKILL.md`
- Modify: `README.md`
- Modify: `tests/test_skill_contract.py`

**Interfaces:**
- Consumes: explicit assistant-casting requests and `qi_gua.py` JSON
- Produces: two input paths, no-reroll behavior, and pure original-plus-translation hexagram sections

- [ ] **Step 1: Add failing contract tests**

```python
def test_assistant_casting_requires_explicit_request_and_one_live_run(self):
    self.assertIn("你帮我起卦", SKILL_TEXT)
    self.assertIn("run `qi_gua.py` exactly once", SKILL_TEXT)
    self.assertIn("Never rerun", SKILL_TEXT)


def test_hexagram_layer_is_original_text_plus_plain_translation_only(self):
    self.assertIn("- 白话文：", SKILL_TEXT)
    self.assertIn("question-specific interpretation begins in `纳甲分析`", SKILL_TEXT)
    self.assertNotIn("- 本卦至变卦的结构变化：", SKILL_TEXT)
```

- [ ] **Step 2: Run contract tests and verify RED**

Run: `python -m unittest tests.test_skill_contract -v`

Expected: new assistant-casting and translation assertions fail.

- [ ] **Step 3: Update `SKILL.md`**

Add separate `Manual Casting` and `Assistant Casting` paths. Document the
three-coin table, exact CLI sequence, actual-time rule, audit fields, replay
restriction, single-run rule, daily count, and script-failure behavior.

Replace each `卦意`/`爻意` slot in the hexagram layer with `白话文`, remove the
structural-application slot, and state that all application begins in
`纳甲分析`.

- [ ] **Step 4: Update `README.md`**

Document:

```text
python scripts/qi_gua.py --question "问题" --timezone Asia/Shanghai
```

Include the coin-value table, actual-time behavior, entropy disclosure, replay
purpose, and no-reroll rule.

- [ ] **Step 5: Run contract and full tests**

Run: `python -m unittest tests.test_skill_contract -v`

Expected: contract tests pass.

Run: `python -m unittest discover -s tests -v`

Expected: all old and new tests pass.

### Task 3: Validate, Install, And Publish

**Files:**
- Sync: repository skill files to `C:\Users\c1572\.codex\skills\tianyan`

**Interfaces:**
- Consumes: verified repository files
- Produces: matching installed skill and GitHub `main`

- [ ] **Step 1: Run official validation**

Run the official `quick_validate.py` against the repository and installed copy
with UTF-8 mode and the existing temporary PyYAML dependency.

Expected: both print `Skill is valid!`.

- [ ] **Step 2: Sync the installed skill**

Copy `SKILL.md`, `scripts/qi_gua.py`, and any changed runtime files into
`C:\Users\c1572\.codex\skills\tianyan`. Compare SHA-256 hashes with the
repository copies.

- [ ] **Step 3: Run an installed replay smoke test**

Run `qi_gua.py` from the installed skill with entropy
`000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f`
and time `2026-06-21 15:46`.

Expected: replay mode and line values `[7, 6, 8, 7, 7, 9]`.

- [ ] **Step 4: Commit and push**

```bash
git add SKILL.md README.md scripts/qi_gua.py tests/test_qi_gua.py tests/test_skill_contract.py docs/superpowers/plans/2026-06-21-tianyan-assistant-coin-casting.md
git commit -m "feat: add auditable assistant coin casting"
git push origin main
```

Expected: GitHub `main` contains the casting script and updated skill contract.
