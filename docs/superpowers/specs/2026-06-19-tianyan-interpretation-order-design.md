# Tianyan Interpretation Order Design

## Goal

Make every complete Tianyan reading explain the Zhouyi meaning before applying
Wenwang Liuyao Najia mechanics to the user's question.

## Required Order

1. Present the deterministic chart result.
2. Explain the hexagram meaning in this exact order:
   - primary hexagram
   - each moving line, from bottom to top
   - changed hexagram
3. Perform the Najia analysis:
   - useful-spirit selection
   - month and day strength
   - Shi/Ying and six-relative relationships
   - moving and changed-line effects
   - void, break, combination, clash, tomb, and hidden spirits when relevant
4. Give the conclusion for the user's question.

## Layer Boundary

The hexagram-meaning section explains the original symbolic meaning only. It
does not identify real people, infer their thoughts, or turn the line text into
advice for the user. Application to the concrete question begins in the Najia
analysis.

For a static hexagram, state that there are no moving lines and omit the
changed-hexagram interpretation. For a moving hexagram, explain only the lines
that actually move.

## Output Contract

The output template gains a dedicated `卦意解读` section between `排盘结果` and
`纳甲分析`, with these required subsections:

```text
## 二、卦意解读

### 本卦
### 动爻
### 变卦
```

The existing useful-spirit and technical judgment material becomes one
`纳甲分析` section after it. The final conclusion remains last.

## Scope

- Update `SKILL.md` and `README.md` only; chart calculation does not change.
- Add a contract test that verifies the required section order and the layer
  boundary language.
- Keep the existing input, usage-limit, and safety rules unchanged.

## Validation

- The contract test must fail against the current skill before the edit.
- All unit tests must pass after the edit.
- The official skill validator must pass for the repository and installed copy.
- The installed `tianyan` copy must match the repository version.
