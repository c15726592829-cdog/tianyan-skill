# Accuracy Retrospectives

This file stores calibration lessons from user-supplied blind-test summaries.
It is not a source book, not a governing Liuyao rule, and not a predictive accuracy proof.

## Use Boundary

- **Prospective-only**: use these notes to design future blind tests, set
  resolution caps, and prevent repeated reasoning errors before a reveal.
- Do not use a revealed truth as evidence for the same case.
- Do not convert post-reveal explanations into scored hits.
- Do not score revealed-answer reinterpretations.
- Do not promote a retrospective pattern into a governing rule unless future
  unrevealed cases validate it under the same protocol.
- Keep source-book rules and deterministic chart facts above retrospective
  notes in priority.

## 2026-06-23 User Blind-Test Summary

User file: `tianyan_6爻测试_20cases总结.txt`. The reported set contained 20
cases, with several cases explicitly marked as not interpreted before reveal.
The scoring summary itself has inconsistent denominators, so it must not be
used as a formal benchmark statistic without cleaning the ledger.

Reusable observation:

- YES/NO questions performed materially better than open-ended exact questions.
- Broad province/direction answers were more defensible than city/county names.
- Exact objects, colors, modern cities, companions, and motives failed often
  when inferred from one vivid image.
- Some post-reveal readings were plausible but remain hindsight unless tested
  prospectively.

## Context Isolation

For every accuracy test case, answer this before locking:

```text
If the prior conversation were hidden and only this question plus this chart
remained, would I still produce the same answer?
```

If not, label the answer contaminated and lower confidence. Do not reuse:

- earlier case facts;
- the user's revealed answers;
- the user's descriptive wording from prior cases;
- the assistant's previous guesses;
- unstated candidate geography from the conversation.

## Resolution Limits

Use different match rules by question shape:

| Question shape | Safer output | Strong-answer requirement |
|---|---|---|
| YES/NO | yes/no with conditions and contrary evidence | clear actor/action/window and relevant movement or textual support |
| broad direction/province | direction, region, province candidate | fixed reference point plus stable direction evidence |
| open-ended exact questions | class or ranked candidates | at least two independent evidence groups and predeclared candidates |
| city/county/place name | broad direction/environment first | candidate set plus independent geographic signals |
| exact object/product | object class or function first | independent material/function/body signal beyond one trigram |
| companion/identity | broad role class first | predeclared candidates plus person-anchor support |

County-level and product-level answers are normally beyond the defensible
resolution of one open-world chart. State the cap instead of forcing a name.

## Retrospective Failure Modes to Guard Against

1. **Single-image lock**: reading one body image as a specific device, one
   mountain image as a specific landmark, or one vehicle image as a specific
   transport setting. Use broad class first and require another independent
   signal for exact identity.
2. **Modern geography overfit**: mapping trigram or branch images directly to a
   named city. Lock direction/environment first; city names need candidates.
3. **Text layer skipped**: ignoring the direct sense of the hexagram name,
   judgment, or actual moving-line text when the question is YES/NO or motive.
   Treat text as one evidence layer, not as an automatic override.
4. **Color priority confusion**: when a color is asked, six-spirit evidence
   directly on the selected object line can outrank broad trigram color;
   broad trigram color can outrank loose Najia element color. If the selected
   object line is unclear, lower confidence.
5. **伏神 overclaim or avoidance**: hidden spirits can be part of the matter,
   but do not turn them into a complete answer unless the primary anchor also
   supports it.
6. **Multi-moving-line noise**: three or more moving lines often produce
   conflicting direction and event signals. Prefer wider resolution.

## Prospective Test Design

Future tests should be scored only from locked pre-reveal records:

- assign case ID before casting;
- write requested resolution and match criteria before answering;
- separate primary answer, ranked alternatives, and speculative guesses;
- score YES/NO separately from open-ended exact questions;
- record whether the candidate set was open-world or predeclared;
- after reveal, record failure class without changing the locked answer.

## Promotion Rule

A retrospective hypothesis can move into a question module only after it is
validated on future unrevealed cases. Until then, write it as:

```text
Retrospective hypothesis; use only as a caution or secondary check.
```
