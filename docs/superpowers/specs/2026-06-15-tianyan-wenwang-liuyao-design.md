# Tianyan Wenwang Liuyao Design

## Goal

Replace the current draft with an installable Codex skill named `tianyan` that
supports only traditional Wenwang Liuyao Najia analysis.

## User Input

Require exactly three user-facing fields:

```text
问题：
起卦时间：
爻象：
```

The six line values must use `6/7/8/9` and be listed from the first line to the
sixth line, bottom to top:

- `6`: old yin, moving
- `7`: young yang, static
- `8`: young yin, static
- `9`: old yang, moving

Require a date, time, and timezone. If the timezone is omitted, use the user's
current timezone and state that assumption.

## Scope

Use Wenwang Liuyao Najia only. Do not use Meihua Yishu, number-to-trigram
divination, or Ti-Yong reasoning.

The deterministic charting layer produces:

- primary and changed hexagrams
- upper and lower trigrams
- eight-palace affiliation
- palace element
- Shi and Ying positions
- Najia stems and branches
- six relatives
- six spirits
- month commander
- day stem-branch
- xunkong

The interpretive layer follows this order:

1. Clarify the question and select the useful spirit.
2. Evaluate month and day strength.
3. Evaluate moving and changed lines.
4. Evaluate Shi/Ying relationships.
5. Evaluate generation, control, clash, combination, void, break, tomb, and
   exhaustion where the available chart data supports them.
6. Use six spirits, hexagram text, and line text only as supporting evidence.
7. Compare the reading with known real-world facts.

## Safety And Discipline

- Limit new readings to three per user per natural day when conversation
  context allows counting.
- Do not recast the same materially unchanged question.
- Present tendencies, not guaranteed predictions.
- Treat medical, legal, investment, financial, and personal-safety questions
  as cultural reference only; real-world professional judgment takes priority.
- Never invent missing chart data.

## Repository Structure

```text
SKILL.md
agents/openai.yaml
scripts/pai_gua.py
references/wenwang-liuyao-rules.md
references/interpretation-guide.md
tests/test_pai_gua.py
```

The root `SKILL.md` remains concise and routes detailed rules to references.
The Python charting script uses only the standard library and emits JSON.

## Verification

- Unit tests cover input validation, moving-line transformation, hexagram
  identification, eight-palace/Shi-Ying assignment, Najia, six relatives, six
  spirits, day stem-branch, month commander, and xunkong.
- CLI smoke tests verify valid JSON and clear errors.
- Codex skill validation checks frontmatter and naming.
- A final repository scan confirms that Meihua, number divination, and Ti-Yong
  instructions are absent.
