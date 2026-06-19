---
name: tianyan
description: Use when a user asks for 文王六爻、纳甲六爻、铜钱起卦、排卦、断卦，or provides a question, cast time, and six bottom-to-top 6/7/8/9 or 老阴/少阳/少阴/老阳 line values for traditional Liuyao analysis.
---

# Tianyan 文王六爻

## Input Template

Ask the user to provide exactly this format:

```text
问题：
起卦时间：
爻象：
```

Example:

```text
问题：这件事近期是否会有进展？
起卦时间：2026-06-16 15:30
爻象：7 8 9 7 8 6
```

Accept Chinese line names too:

```text
爻象：少阳、少阴、老阳、少阳、少阴、老阴
```

The line order is always bottom to top. Never reverse it silently.

## Scope

Use only traditional Wenwang Liuyao Najia.

Do not use:

- 梅花易数
- 数字取上下卦
- 体用法
- 时间直接起卦
- mixed methods that replace Najia, Shi/Ying, useful-spirit, month, and day
  analysis

If the user only provides two numbers such as `3 和 7` or `72 和 81`, do not
cast a chart with this skill. Explain that the input belongs to digital or
Meihua-style casting, not Wenwang Liuyao Najia. If they want that method, they
need a separate Meihua Yi skill.

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

Also accept `老阴`、`少阳`、`少阴`、`老阳` directly.

Example:

```text
问题：这次合同能否按期签署？
起卦时间：2026-06-15 20:30
爻象：7、8、9、7、6、8
```

Normalize the cast time before calling the script. The script accepts
`YYYY-MM-DD HH:MM` or `YYYY/MM/DD HH:MM`, with a space or `T` between date and
time. Do not accept a date without hour and minute.

If the timezone is absent, use the user's current timezone from the environment
when available and state the assumption. If no environment timezone is
available, default to `Asia/Shanghai`. If the question clearly occurs in
another region, ask for the timezone before interpreting. Do not ask for a
fourth user-facing field unless the timezone is materially ambiguous.

If any required field is missing or the line count/order is unclear, request
the missing information before interpreting.

## Usage Discipline

- In the visible conversation context, analyze at most three new hexagrams for
  the same user in one natural day.
- If the host environment provides persistent state, record and enforce the
  count by the user's local date.
- If historical count cannot be confirmed, enforce the limit only from visible
  records and do not invent counts.
- Do not recast a materially unchanged question. Return to the original chart
  for clarification or review.

Treat these as repeated questions:

1. Same subject and same matter, with only wording changed.
2. Nearby time window while still asking the same event development.
3. Asking `她会不会联系我` and then `她今天会不会找我` without new facts.
4. Asking `这件事成不成` and then `有没有希望` about the same object.

Do not treat these as repeated questions:

1. Meaningful new real-world facts appeared.
2. The time window clearly changed.
3. The object of the question changed.
4. The user shifts from outcome judgment to action advice, such as from
   `会不会联系我` to `我现在怎么办`.

Reviews, line explanations, strategy summaries, and reinterpretation after new
facts do not count as new casts.

## Deterministic Charting

Resolve paths relative to this `SKILL.md`. Run the bundled script with an
available Python 3 interpreter:

```text
python scripts/pai_gua.py \
  --question "<问题>" \
  --time "<YYYY-MM-DD HH:MM>" \
  --timezone "<IANA timezone>" \
  --lines "<six values or Chinese line names bottom to top>"
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
3. Explain the Zhouyi meaning before applying Najia mechanics:
   - `本卦`: quote the original judgment and Great Image first, then explain
     the hexagram's original meaning and overall structure.
   - `动爻`: quote each actual moving line first, in bottom-to-top order, then
     explain its original line meaning.
   - `变卦`: quote the original judgment and Great Image first, then explain
     the changed hexagram and the structural transition from the primary.
4. Begin the Najia analysis only after the hexagram-meaning section:
   - identify the question category and select the useful spirit
   - judge useful spirit, original spirit, taboo spirit, and enemy spirit
     against month commander and day branch
   - judge moving lines and only their changed lines
   - judge Shi/Ying, generation/control, clash/combination, void, break, tomb,
     hidden spirit, and relevant special structures
5. Compare the Najia judgment with known real-world facts.
6. Give a direct but non-absolute conclusion and a restrained practical
   strategy.

The `卦意解读` layer only explains the original hexagram and line meanings. It
只解释卦爻本义，不得映射到用户、对方或现实事件。Do not infer a person's
thoughts or give question-specific advice inside `本卦`, `动爻`, or `变卦`.
Application to the concrete question begins in `纳甲分析`.

For a static hexagram, write `无动爻` and omit a separate changed-hexagram
interpretation. For a moving hexagram, explain only the lines that actually
move.

For quoted original text:

- preserve the source order and do not silently rewrite it as modern Chinese
- include a moving line's Small Image only when it is used in the explanation
- 不得把转述或白话释义标为原文
- if exact wording cannot be verified, write `原文未核实` instead of inventing
  or reconstructing a quotation

Reality overrides symbolic inference. A symbolic sign of connection does not
prove action; a favorable tendency does not override explicit rejection,
medical evidence, legal documents, market risk, or safety facts.

## Output

Use this structure:

```markdown
## 一、排盘结果

- 问题：
- 起卦时间：
- 时区：
- 爻序：自下而上
- 本卦：
- 变卦：
- 动爻：
- 八宫：
- 世爻：
- 应爻：
- 月建：
- 日辰：
- 旬空：

## 二、卦意解读

### 本卦

- 卦辞与大象原文：
- 卦意：

### 动爻

- 爻辞原文：
- 爻意：

### 变卦

- 卦辞与大象原文：
- 卦意：
- 本卦至变卦的结构变化：

## 三、纳甲分析

### 用神选择

- 所问事项：
- 取用神：
- 取用理由：

### 旺衰与作用

- 用神旺衰：
- 世应用神关系：
- 动爻及变爻作用：
- 空破墓绝合冲刑害：

## 四、结论

- 直接判断：
- 时间提示：
- 行动建议：
- 不确定点：
- 现实校验：
- 一句话断语：
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
