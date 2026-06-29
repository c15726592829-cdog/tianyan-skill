---
name: tianyan
description: Use when a user asks for 文王六爻、纳甲六爻、铜钱起卦、代起卦、排卦、断卦，or provides a question, cast time, and six bottom-to-top 6/7/8/9 or 老阴/少阳/少阴/老阳 line values for traditional Liuyao analysis.
---

# Tianyan 文王六爻

## Casting Paths

### User-Supplied Casting

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

### Assistant Three-Coin Casting

Use assistant casting only when the user explicitly asks with wording such as
`你帮我起卦`, `代我抛硬币`, or `随机起卦`.

Require a finalized question and a known timezone. Use the script's actual
execution minute as the cast time. Never reuse a time supplied before the
assistant actually casts the coins. Never replace user-supplied lines with an
assistant cast.

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
Assistant casting is an auditable software simulation of the traditional
three-coin method, not a claim of supernatural randomness.

## Accuracy Test Mode

Activate this mode only when the user explicitly calls the session an accuracy
test, benchmark, blind test, or `准确性测试`. State that the mode is active.

Accuracy Test Mode overrides the normal three-new-hexagrams-per-day limit for
clearly identified test cases. It does not override any casting or audit
safeguard:

- assign an immutable case ID and preserve the user's exact question
- treat each materially distinct test prompt as one case
- perform at most one live assistant cast per case
- never reroll, replace supplied lines, or recast the same case
- record cast time, IANA timezone, bottom-to-top values, full chart, and for an
  assistant cast the disclosed entropy and all eighteen coins
- lock the perspective, selected anchor, primary answer, resolution,
  alternatives, evidence for/against, and confidence before ground truth
- keep post-reveal reinterpretation separate from the locked answer and score

Read [references/accuracy-testing.md](references/accuracy-testing.md) before
opening a test case and follow its case ledger and scoring rules. A replay is
audit-only. Content checks validate the protocol structure, not predictive
accuracy.

For calibration from prior blind tests, read
[references/accuracy-retrospectives.md](references/accuracy-retrospectives.md)
as cautionary process guidance only. Retrospectives do not govern chart
judgment, do not prove accuracy, and must not be used as revealed answer keys.

## Manual Casting Input

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

## Assistant Casting Workflow

Resolve paths relative to this `SKILL.md`. From the skill directory, run:

```text
python scripts/qi_gua.py \
  --question "<问题>" \
  --timezone "<IANA timezone>"
```

The script simulates three coins per line and six lines bottom to top:

| Combination | Value | Line |
|---|---:|---|
| 三字 | 6 | 老阴，动 |
| 两字一背 | 7 | 少阳，静 |
| 一字两背 | 8 | 少阴，静 |
| 三背 | 9 | 老阳，动 |

`字面=2` and `背面=3`. The script uses OS-backed entropy, discloses the entropy
and all eighteen coin results, and records the script's actual execution minute.

For a live request, run `qi_gua.py` exactly once. Show the six throws before
chart interpretation. Never rerun because the result is inconvenient or the
user asks for a more favorable chart.

Pass the returned `cast_time`, `timezone`, and `line_values_text` to
`pai_gua.py`. `line_values_text` preserves the six bottom-to-top values as the
comma-separated form required by `--lines`. Never replace user-supplied lines.
If either script fails before returning valid JSON, report the failure instead
of inventing or rerolling lines.

The `--replay-entropy` and `--replay-time` options reproduce a disclosed cast.
Replay output is audit-only, does not count as a new cast, and must never be
interpreted as newly generated divination.

## Usage Discipline

The daily limit below applies outside explicit Accuracy Test Mode. The test-mode
override and unchanged one-cast safeguards are defined above.

- In the visible conversation context, analyze at most three new hexagrams for
  the same user in one natural day.
- If the host environment provides persistent state, record and enforce the
  count by the user's local date.
- If historical count cannot be confirmed, enforce the limit only from visible
  records and do not invent counts.
- Do not recast a materially unchanged question. Return to the original chart
  for clarification or review.
- Assistant live casts count toward the same three-per-day limit.

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

## Reading Contract And Outcome Review

Before interpreting any chart, read
[references/reading-contract-and-review.md](references/reading-contract-and-review.md).
Freeze the exact question, subject, perspective, concrete event, requested time
window, requested and maximum defensible resolution, known facts, and reveal
status before selecting an anchor or useful spirit.

Ask one focused question only when ambiguity would materially change the
category, anchor, useful spirit, time window, or scoring resolution. Otherwise
state the smallest reasonable assumption and proceed. External information is
reality evidence or contrary evidence only; it cannot import Meihua external
omens, trigger a recast, or override Najia through `舍卦从应`.

When ordinary post-outcome feedback arrives, preserve the original conclusion
and use the reference's diagnostic review. Do not score hindsight or promote a
retrospective pattern without future unrevealed testing.

## Question Classification

Before chart interpretation, read
[references/question-types/index.md](references/question-types/index.md) and
[references/question-types/common-rules.md](references/question-types/common-rules.md).
Select exactly one primary category and zero to two secondary categories. Load
the primary module under `references/question-types/` and only the secondary
modules needed by the user's wording.

Preserve the exact question, then lock:

- primary category and classification confidence
- question subject and perspective
- primary anchor or useful spirit
- rejected alternative anchors
- loaded source rule IDs
- requested resolution and maximum defensible resolution

Use source records marked `A` or `B` as governing rules. Source records marked
`C` are navigation-only. If the question asks for an exact modern object, named
city, exact companion, exact identity, or exact date, require independent
support and apply the resolution caps in the loaded module.

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
useful-spirit selection, judgment order, and output requirements. Read
[references/classical-interpretation-rules.md](references/classical-interpretation-rules.md)
for perspective, evidence labels, third-party anchors, object/location/timing
limits, and confidence resolution.

## Interpretation Order

1. Restate and lock the exact question, subject, perspective, concrete matter,
   requested time window and resolution, known facts, reveal status, cast time,
   timezone assumption, and line order.
2. Run the charting script.
3. Present the Zhouyi text without applying it to the question:
   - `本卦`: original judgment and Great Image, then a plain modern-Chinese
     translation.
   - `动爻`: each actual moving-line text in bottom-to-top order, then a plain
     modern-Chinese translation.
   - `变卦`: original judgment and Great Image, then a plain modern-Chinese
     translation.
4. Classify the question through the question-type index and loaded module.
5. Fix the question perspective, person/matter anchor, and useful spirit before
   reading individual symbols.
6. Judge the useful spirit and supporting/opposing roles against month and day.
7. Judge moving lines and only their actual changed lines; static is not absent
   and moving is not automatic success or presence.
8. Judge Shi/Ying and the named third party from the fixed perspective.
9. Judge relevant branch structures, void, break, tomb, and hidden spirit.
10. Use six spirits only as secondary imagery.
11. Use hexagram and trigram images only as corroboration; exact objects,
    modern cities, relationship identities, and dates require independent
    support and must be labeled speculative when support is insufficient.
12. Compare the inference only with external facts recorded under the reading
    contract and state contrary evidence; verified reality governs practical
    advice.
13. Give a bounded conclusion with resolution and confidence.

The `卦意解读` layer contains only original text and plain translation. It
只解释卦爻本义，不得映射到用户、对方或现实事件。Do not infer a person's
thoughts, describe symbolic application, or give advice inside `本卦`, `动爻`,
or `变卦`. Question-specific interpretation begins in `纳甲分析`.

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
- 白话文：

### 动爻

- 爻辞原文：
- 白话文：

### 变卦

- 卦辞与大象原文：
- 白话文：

## 三、纳甲分析

### 问题分类

- Exact question:
- Locked before interpretation:
- Concrete matter or event:
- Requested time window:
- Known real-world facts:
- Outcome already revealed:
- Primary category:
- Secondary categories:
- Classification confidence:
- Question subject:
- Perspective:
- Primary anchor or useful spirit:
- Rejected alternative anchors:
- Loaded rule IDs:
- Requested resolution:
- Maximum defensible resolution:

### 用神选择

- 所问事项：
- 取用神：
- 取用理由：

### 旺衰与作用

- 用神旺衰：
- 世应用神关系：
- 动爻及变爻作用：
- 空破墓绝合冲刑害：

### 证据分层

- 排盘事实：
- 古典规则：
- 推断：
- 反证：
- 猜测或候选：
- 结论分辨率与信心：

## 四、结论

- 直接判断：
- 时间提示：
- 行动建议：
- 不确定点：
- 现实校验：
- 一句话断语：
```

In Accuracy Test Mode, append the locked-answer contract before asking for or
accepting the reveal:

```text
Case ID:
Primary answer:
Resolution:
Ranked alternatives (optional, maximum 3):
Confidence:
Evidence for:
Evidence against:
Scoring dimensions and match rules:
Lock time and timezone:
```

After reveal, preserve the truth verbatim and report primary score, alternative
rank, category coverage, and failure class. Never replace the locked record.

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
