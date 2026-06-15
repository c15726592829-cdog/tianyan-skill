---
name: tianyan
description: Use when a user asks for 文王六爻、纳甲六爻、铜钱起卦、排卦、断卦，or provides a question, cast time, and six 6/7/8/9 line values for traditional Liuyao analysis.
---

# Tianyan 文王六爻

## Scope

Use only traditional Wenwang Liuyao Najia.

Do not use:

- 梅花易数
- 数字取上下卦
- 体用法
- 时间直接起卦
- mixed methods that replace Najia, Shi/Ying, useful-spirit, month, and day
  analysis

Treat the result as traditional cultural analysis, not guaranteed prediction.

## Required Input

Require exactly these three user-facing fields:

```text
问题：
起卦时间：
爻象：
```

Require six line values in bottom-to-top order:

- `6`: 老阴，动
- `7`: 少阳，静
- `8`: 少阴，静
- `9`: 老阳，动

Example:

```text
问题：这次合同能否按期签署？
起卦时间：2026-06-15 20:30
爻象：7、8、9、7、6、8
```

If the timezone is absent, use the user's current timezone from the environment
and state the assumption. Do not ask for a fourth user-facing field.

If any required field is missing or the line count/order is unclear, request
the missing information before interpreting.

## Usage Discipline

- Analyze at most three new hexagrams for the same user in one natural day when
  the available conversation context permits counting.
- Do not recast a materially unchanged question. Return to the original chart
  for clarification or review.
- Reviews, line explanations, strategy summaries, and analysis after meaningful
  new real-world facts do not count as new casts.
- If cross-conversation history is unavailable, say that the daily count only
  covers the visible conversation.

## Deterministic Charting

Resolve paths relative to this `SKILL.md`. Run the bundled script with an
available Python 3 interpreter:

```text
python scripts/pai_gua.py \
  --question "<问题>" \
  --time "<YYYY-MM-DD HH:MM>" \
  --timezone "<IANA timezone>" \
  --lines "<six values bottom to top>"
```

The script emits UTF-8 JSON containing:

- 本卦、变卦、动爻
- 八宫、宫五行、卦序、世应
- 纳甲、地支五行、六亲、六神
- 伏神
- 月建、日辰、旬空

Do not manually invent chart fields. If the script cannot run, report the
limitation instead of fabricating a complete chart.

Read [references/wenwang-liuyao-rules.md](references/wenwang-liuyao-rules.md)
before interpreting chart mechanics. Read
[references/interpretation-guide.md](references/interpretation-guide.md) for
useful-spirit selection, judgment order, and output requirements.

## Interpretation Order

1. Restate the question, cast time, timezone assumption, and line order.
2. Run the charting script.
3. Identify the question category and select the useful spirit. Explain the
   selection; do not silently change it to fit a preferred conclusion.
4. Judge useful spirit, original spirit, taboo spirit, and enemy spirit against
   month commander and day branch.
5. Judge moving lines and only their changed lines.
6. Judge Shi/Ying, generation/control, clash/combination, void, break, tomb,
   hidden spirit, and relevant special structures.
7. Use six spirits, hexagram text, and line text only as supporting evidence.
8. Compare the symbolic reading with known real-world facts.
9. Give a direct but non-absolute conclusion and a restrained practical
   strategy.

Reality overrides symbolic inference. A symbolic sign of connection does not
prove action; a favorable tendency does not override explicit rejection,
medical evidence, legal documents, market risk, or safety facts.

## Output

Use this structure:

```markdown
## 卦象信息

问题：
起卦时间：
时区：
爻序：自下而上
本卦：
动爻：
变卦：
八宫：
世爻：
应爻：
月建：
日辰：
旬空：
用神：
判断强度：强 / 中 / 弱

## 一、总体结论

## 二、用神与旺衰

## 三、动爻与变爻

## 四、世应与现实关系

## 五、时间倾向

## 六、策略建议

## 七、现实校验

## 八、一句话断语
```

Keep the conclusion direct, calm, and evidence-linked. State uncertainty
explicitly. Use time windows or relative speed, never guaranteed dates.

End with:

```text
此卦为「……」之象，宜……，不宜……。
```

## High-Stakes Limits

For medical, legal, investment, major financial, personal-safety, examination,
employment, or contract decisions:

- present the reading only as traditional cultural reference
- prioritize qualified professional advice and verifiable facts
- do not tell the user to delay urgent care, ignore legal deadlines, risk money,
  or enter danger because of a hexagram
- do not give certainty, probability percentages, or guaranteed outcomes

