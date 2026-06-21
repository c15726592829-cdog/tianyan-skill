# Tianyan Assistant Coin Casting Design

## Goal

Allow Tianyan to cast a Wenwang Liuyao hexagram on the user's behalf with a
transparent three-coin simulation, while preserving manual casting and the
existing Najia charting workflow.

## User Flows

### User-Supplied Lines

When the user supplies six line values, keep the current workflow unchanged.
Never replace or reroll user-supplied lines.

### Assistant Casting

Run assistant casting only when the user explicitly asks for it with wording
such as `你帮我起卦`, `代我抛硬币`, or `随机起卦`.

Require a finalized question and a known timezone. Capture the script's actual
execution minute as the cast time. Do not reuse a past time supplied before the
coins were cast.

## Three-Coin Method

Cast three coins for each line and repeat six times. Record lines from bottom
to top.

Use these fixed values:

| Coin side | Value |
|---|---:|
| 字面 | 2 |
| 背面 | 3 |

Map each three-coin sum as follows:

| Combination | Sum | Line |
|---|---:|---|
| 三字 | 6 | 老阴，动 |
| 两字一背 | 7 | 少阳，静 |
| 一字两背 | 8 | 少阴，静 |
| 三背 | 9 | 老阳，动 |

This gives the traditional `1:3:3:1` probability distribution for
`6:7:8:9`.

## Randomness And Auditability

Create `scripts/qi_gua.py` as a separate casting component. Keep
`scripts/pai_gua.py` responsible only for deterministic chart construction.

For a live cast:

1. Generate 32 bytes with Python's operating-system-backed `secrets` module.
2. Derive the coin bitstream with SHA-256 using a versioned domain prefix.
3. Read the first 18 bits in a documented order.
4. Map `0` to `字面/2` and `1` to `背面/3`.
5. Group the bits into six bottom-to-top three-coin throws.

Return UTF-8 JSON containing:

- method and algorithm version
- `live` mode
- actual cast time and timezone
- disclosed entropy in hexadecimal
- all 18 coin sides and values
- each line sum, line value, and line name
- the six line values in bottom-to-top order

The disclosed entropy makes the mapping reproducible. It does not prove a
metaphysical property or independently prove that the entropy was not selected.
Describe it only as an auditable software simulation of the traditional method.

Provide a replay mode that accepts previously disclosed entropy and cast time
only to verify an existing result. Replay output must be labeled `replay`, must
not count as a new cast, and must never be interpreted as a newly generated
hexagram.

## Skill Workflow

For assistant casting:

1. Confirm the question and timezone.
2. Run `qi_gua.py` exactly once in live mode.
3. Show the six coin throws and line values.
4. Pass the returned time and lines to `pai_gua.py`.
5. Interpret the resulting chart with the existing limits and safety rules.

Never rerun because the result is inconvenient or because the user wants a
more favorable chart. Script failure before a valid JSON result does not create
a usable cast; report the failure instead of inventing lines.

Assistant casts count toward the same three-per-day limit. Repeated-question
rules apply without exception.

## Interpretation Layers

The hexagram-meaning layer is independent of the user's question:

1. Primary hexagram: original judgment and Great Image, followed by a plain
   modern-Chinese translation.
2. Moving lines: each original moving-line text, followed by a plain
   modern-Chinese translation.
3. Changed hexagram: original judgment and Great Image, followed by a plain
   modern-Chinese translation.

Do not map people, events, motives, advice, or the user's question inside this
layer. Do not add a separate symbolic application paragraph there.

Begin question-specific interpretation only in the Najia analysis. The Najia
analysis and final conclusion continue to use useful spirit, month/day,
Shi/Ying, movement, void/break, real-world facts, and uncertainty.

## Files

- Create `scripts/qi_gua.py` for live and replay casting.
- Create `tests/test_qi_gua.py` for coin mapping, entropy replay, time, JSON,
  and line order.
- Modify `SKILL.md` for the two input paths and interpretation-layer contract.
- Modify `README.md` with assistant-casting usage and transparency notes.
- Extend `tests/test_skill_contract.py` with assistant-casting and output-layer
  requirements.
- Do not change the chart mathematics in `scripts/pai_gua.py`.

## Testing

- Exhaust all eight three-coin combinations and verify the `1:3:3:1` mapping.
- Use fixed entropy to verify exact replay without statistical/flaky tests.
- Verify exactly six throws and bottom-to-top ordering.
- Verify live mode uses the supplied clock abstraction and timezone.
- Verify CLI JSON is UTF-8 and contains the audit fields.
- Verify replay is labeled and cannot be mistaken for a live cast.
- Verify `SKILL.md` requires explicit user intent and prohibits rerolls.
- Verify the hexagram layer contains only original text and plain translation,
  while question-specific application starts in the Najia section.
- Run all existing chart tests and official skill validation.

## Non-Goals

- Do not derive lines from time, question text, two numbers, or Meihua methods.
- Do not claim that software randomness is supernatural or more authoritative
  than a user's physical coin cast.
- Do not add network dependencies or third-party random services.
- Do not merge casting randomness into `pai_gua.py`.
