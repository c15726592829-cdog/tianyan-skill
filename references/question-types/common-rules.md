# Common Question-Routing Rules

These rules apply before any question-specific module. They are intended to
make interpretation reproducible and to prevent post-reveal anchor switching.

## Mandatory Decision Order

```text
exact question and perspective
-> primary category and redirects
-> primary anchor/useful spirit
-> month/day
-> relevant movement/change
-> Shi/Ying
-> branch structures and hidden spirits
-> six spirits
-> trigram corroboration
-> real facts
-> confidence and resolution cap
```

## Source Priority

1. Deterministic chart facts from `scripts/pai_gua.py`.
2. Category module rules with source IDs marked `A` or `B`.
3. Common Liuyao mechanics only from source records that are marked `A` or `B`.
4. Shuo Gua trigram/body/family/nature images as corroboration, not as primary
   useful-spirit selection.
5. Real-world facts and high-stakes safety constraints override symbolic
   optimism.

Records marked `C`, including unaudited `HZL-*`, `ZSBY-*`, and `BSZZ-*`
records, are navigation-only and must not govern a strong conclusion.

## Evidence Independence

Do not count the same fact twice. For exact modern object, named city, exact
companion, exact identity, or exact date, require at least two independent
evidence groups, such as:

- selected useful spirit or person anchor;
- month/day strength or activation;
- directly relevant moving or changed line;
- Shi/Ying relation;
- branch structure with required participants present;
- trigram/body image;
- predeclared candidate set or real-world constraint.

Two phrasings of the same trigram image are one evidence group.

## Classification Confidence

Use:

- `high`: one clear category, no material redirect dispute.
- `medium`: one primary category is likely, but a secondary dimension affects
  the answer.
- `low`: question is broad, mixed, or asks for exact modern resolution without
  enough framing.

Low classification confidence caps answer confidence.

## Conflict Logging

For every material conclusion, record:

- selected primary category;
- selected primary anchor or useful spirit;
- rejected alternative anchors;
- governing source IDs;
- contrary evidence;
- maximum defensible resolution.

Do not switch category or anchor after the truth is revealed.

## Forced-Guess Separation

If the user asks for likely options in a test, separate:

1. primary answer;
2. ranked alternatives;
3. speculative guesses;
4. evidence for and against each.

Speculative guesses remain speculative after reveal.

## Accuracy-Test Locking

In explicit accuracy testing, lock these fields before accepting the revealed
answer:

- exact user question;
- cast record;
- primary category;
- secondary categories;
- perspective;
- useful spirit or anchor;
- primary answer;
- alternatives;
- confidence;
- evidence for and against;
- scoring match rules.

Post-reveal reinterpretation must be recorded separately.

## Prohibited Shortcuts

1. Do not infer gender or relationship identity from `妻财` or `官鬼` alone.
2. Do not infer absence from static lines.
3. Do not infer action, success, or existence from movement alone.
4. Do not derive a modern city from a three-combination or trigram image alone.
5. Do not derive an exact date from branch equality alone.
