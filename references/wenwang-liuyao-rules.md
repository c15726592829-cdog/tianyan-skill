# 文王六爻纳甲规则

## Contents

1. Method boundary
2. Line encoding
3. Calendar conventions
4. Chart fields
5. Five-element relations
6. Branch relationships
7. Moving and hidden lines
8. Mechanical safeguards

## Method Boundary

Use the Wenwang Liuyao Najia system:

- six supplied lines form the primary hexagram
- old yin and old yang form moving lines and the changed hexagram
- determine the eight-palace affiliation and palace element
- install Shi/Ying, Najia, six relatives, six spirits, month commander, day
  stem-branch, xunkong, and hidden spirits

Do not derive upper/lower trigrams from numbers. Do not use Meihua Ti-Yong.

## Line Encoding

Read the six values from bottom to top:

| Value | Line | Motion | Changed line |
|---|---|---|---|
| `6` | yin | moving | yang |
| `7` | yang | static | yang |
| `8` | yin | static | yin |
| `9` | yang | moving | yin |

Never reverse the user-provided order silently.

## Calendar Conventions

- Use the supplied local time and an IANA timezone.
- If no timezone appears in the user's three fields, use the current user
  timezone and state it.
- Change the Liuyao day at local `23:00` (start of Zi hour).
- Calculate the month commander from solar-term Jie boundaries:

| Boundary | Month branch |
|---|---|
| 小寒 | 丑 |
| 立春 | 寅 |
| 惊蛰 | 卯 |
| 清明 | 辰 |
| 立夏 | 巳 |
| 芒种 | 午 |
| 小暑 | 未 |
| 立秋 | 申 |
| 白露 | 酉 |
| 寒露 | 戌 |
| 立冬 | 亥 |
| 大雪 | 子 |

The bundled script calculates apparent-solar-longitude boundaries and supports
years 1800 through 2200. Times close to a solar-term boundary carry greater
calendar sensitivity; state the boundary time when it could change the month.

## Chart Fields

Treat script output as deterministic chart data:

- `primary` and `changed`: hexagram names and trigram structure
- `palace`: eight-palace affiliation, palace element, and generation
- `shi_line` and `ying_line`: one-based line positions
- `calendar`: month commander, day, sexagenary index, xunkong
- `lines`: line value, yin/yang, motion, Shi/Ying, Najia, branch element, six
  relative, six spirit, changed data, and optional hidden spirit

Changed-line relatives remain measured against the primary hexagram's palace
element.

## Five-Element Relations

Generation:

```text
木生火，火生土，土生金，金生水，水生木
```

Control:

```text
木克土，土克水，水克火，火克金，金克木
```

Six relatives are assigned from the palace element:

| Relation to palace element | Six relative |
|---|---|
| same element | 兄弟 |
| palace generates line | 子孙 |
| line generates palace | 父母 |
| palace controls line | 妻财 |
| line controls palace | 官鬼 |

## Branch Relationships

Six clashes:

```text
子午、丑未、寅申、卯酉、辰戌、巳亥
```

Six combinations:

```text
子丑、寅亥、卯戌、辰酉、巳申、午未
```

Three combinations:

```text
申子辰合水
亥卯未合木
寅午戌合火
巳酉丑合金
```

Tombs:

```text
水土墓辰，木墓未，火墓戌，金墓丑
```

Use combinations only when the participating branches and strength conditions
are actually present. Do not treat every pair as a completed transformation.

## Month, Day, Void, And Break

- Month commander is the seasonal authority and a primary measure of strength.
- Day branch can support, control, combine, clash, fill void, or trigger a
  static line.
- A branch opposite the month commander is month-broken.
- Xunkong weakens manifestation but is not automatic nonexistence. Consider
  moving, filling, clashing, seasonal strength, and timing.
- A day clash of a strong static line may indicate hidden movement. A weak,
  empty, or broken line struck by the day may remain damaged rather than active.

Do not reduce strength to a single keyword. Weigh month, day, movement,
generation, control, combination, clash, void, and break together.

## Moving And Changed Lines

- Moving lines are the active changes in the cast.
- Judge the moving line first, then the branch and relative it changes into.
- Changed-line return generation supports the moving line.
- Changed-line return control restrains the moving line.
- Advance/retreat and repetition structures require matching branch sequences;
  do not label them from general optimism or pessimism.
- Do not interpret changed data on a static line as an actual transformation.

When several lines move, identify which moving lines directly affect the useful
spirit, Shi, Ying, or the central matter. Do not narrate every line at equal
weight.

## Hidden Spirits

When a needed six relative is absent from visible lines, inspect `hidden` data
derived from the palace's pure hexagram.

Judge:

- whether the hidden spirit is useful
- whether the flying spirit generates, controls, drains, or conceals it
- whether month/day support emergence
- whether void, break, tomb, clash, or movement prevents manifestation

A hidden useful spirit is not automatically favorable and not automatically
unavailable.

## Six Spirits

Use six spirits as secondary imagery only:

- 青龙: benefit, celebration, refinement
- 朱雀: speech, writing, dispute, messages
- 勾陈: delay, attachment, land, old matters
- 螣蛇: uncertainty, entanglement, alarm, strange conditions
- 白虎: pressure, injury, severity, force
- 玄武: concealment, ambiguity, private matters, loss

Never let a six spirit override useful-spirit strength, month/day, or moving
lines.

## Mechanical Safeguards

- Use script output for names, palace, Shi/Ying, Najia, relatives, spirits,
  calendar, void, and hidden spirits.
- Do not fill missing data from memory when the script reports an error.
- State calendar assumptions near solar-term and Zi-hour boundaries.
- Separate chart facts from interpretive inferences.

