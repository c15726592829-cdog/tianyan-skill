# Tianyan Accuracy Testing Protocol

This protocol tests whether a pre-reveal interpretation matches later disclosed
ground truth. It does not validate supernatural causation and must not turn
retrospective pattern fitting into a scored prediction.

## Activation

Activate this mode only when the user explicitly says the session is an
`准确性测试`, `accuracy test`, benchmark, blind test, or equivalent. State that
the mode is active before casting or interpreting.

Each materially distinct test prompt is a new case. Preserve the user's exact
question; do not rewrite it into a leading yes/no question or insert an answer
candidate that was not supplied.

## Daily-Limit Override

Accuracy Test Mode may exceed the normal three-new-hexagrams-per-day limit
because repeated cases are the declared task. This override applies only to
clearly identified test cases.

All other safeguards remain active:

- one live assistant cast per case
- no reroll because the result is inconvenient
- no duplicate live cast for the same case ID
- replay is audit-only
- supplied lines are never replaced
- every timestamp and timezone is recorded

## Case Identifier

Assign an immutable ID before the cast, such as `TY-20260622-001`. Never reuse
an ID for a different question, and never overwrite the original record.

Record case status as one of:

```text
opened -> cast -> locked -> revealed -> scored
```

## Reproducibility Record

Before interpretation, record:

- case ID
- exact user question and stated region
- cast path: user-supplied or assistant three-coin simulation
- local cast time, IANA timezone, and line order
- six values from bottom to top
- for assistant casting: entropy disclosure/hash and all eighteen coin results
- primary/changed hexagrams, moving lines, palace, Shi/Ying, month, day, xunkong
- script names and, when available, file hashes or version identifiers

Store the chart JSON or all fields required to recreate it. A replay must return
the same throws and six line values; otherwise mark the case invalid.

## Pre-Reveal Record

Before the user reveals the answer, lock a record containing:

1. perspective and selected anchor/useful spirit
2. chart facts
3. classical rules applied
4. inference chain
5. contrary evidence
6. primary answer at a stated resolution
7. at most three ranked alternatives, if alternatives are requested
8. confidence: strong, medium, or weak
9. explicit conditions that would make the case unscorable
10. the **locked scoring dimensions** applicable to this case: exact identity,
    category, direction, date, and/or time-window, including the match rule for
    each dimension

The lock boundary is the assistant message containing the answer. Later edits,
new candidates, and changed anchors belong only in the post-reveal analysis.

## Locked Answer Contract

Use this compact record:

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

The primary answer must be singular enough to score. A list such as `城市A、
城市B、城市C、其他同省城市` is not an exact-city prediction. Broad classes and
ranked alternatives may be useful, but they are scored separately and cannot
inflate primary exact accuracy.

## Post-Reveal Scoring

First preserve the user's ground truth verbatim. Then normalize only with an
alias map fixed before scoring, for example `物品A` and a predeclared equivalent
`物品A-细分类`. Do not invent an alias merely to create a match.

Score each case deterministically:

- **Exact primary hit**: locked primary equals truth at the same resolution;
  primary score `1`.
- **Primary miss**: locked primary differs; primary score `0`.
- **Ranked-alternative coverage**: truth appears in the locked top three; record
  its rank, but primary score remains `0`.
- **Category-only match**: a broader locked category contains the truth; record
  category coverage, but do not call it an exact hit.
- **Direction**: score only a predeclared directional vocabulary and tolerance,
  such as eight trigrams or cardinal/intercardinal sectors.
- **Date**: score exact-date equality only when an exact date was locked; a
  nearby date is a miss unless a tolerance was fixed before reveal.
- **Time-window**: score containment in the locked start/end interval using the
  recorded timezone; an open-ended phrase is not a scorable window.
- **Unscorable**: truth is not revealed, ambiguous, contradictory, or the case
  record was not locked before reveal; exclude it from the denominator.

A possibility added after reveal **does not count as a hit**. A vague statement
that could fit many outcomes also does not count as an exact hit.

Report at least:

```text
primary exact accuracy = exact primary hits / scored cases
top-3 coverage = truth present in locked primary or alternatives / scored cases
category coverage = broad category matches / scored cases
direction accuracy = direction matches / direction-scored cases
date accuracy = exact date matches / date-scored cases
time-window accuracy = contained truths / time-window-scored cases
unscorable count
```

Never claim predictive accuracy from a small retrospective fixture set.

## Running Ledger

Maintain an append-only table:

| Case ID | Question | Cast time | Locked primary | Resolution | Confidence | Truth | Primary score | Alt rank | Category match | Failure class |
|---|---|---|---|---|---|---|---:|---:|---|---|

Aggregate only cases using the same protocol version. Show the denominator and
keep unscorable cases visible.

## Failure Analysis

After scoring a miss, assign one or more failure classes without changing the
score:

- question rewritten or perspective error
- wrong person/matter anchor
- useful-spirit selection error
- chart or calendar error
- movement/static misuse
- branch-structure overreach
- named-entity over-specificity
- timing trigger unsupported
- alternatives too broad
- real-world contradiction ignored
- genuinely ambiguous under the locked rules

Use misses to revise general rules only when the change can be stated before the
next cases and applied symmetrically to successes and failures.

## Replay and Reinterpretation

Replay reproduces a disclosed assistant cast using the recorded entropy and
time. It is not a new cast and does not create a second scored answer.

Post-reveal reinterpretation is allowed for diagnosis, but label it
`retrospective analysis`. Preserve the locked answer and original score. Never
replace the pre-reveal record, and never use a better retrospective fit as
evidence that the original answer was correct.
