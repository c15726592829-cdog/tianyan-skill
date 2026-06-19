# Tianyan Original Text Design

## Goal

Place the relevant Zhouyi original text immediately before every hexagram or
moving-line interpretation.

## Output Contract

- Primary hexagram: quote the judgment and Great Image, then explain the
  hexagram meaning.
- Moving lines: quote each actual moving line in bottom-to-top order, then
  explain that line.
- Changed hexagram: quote the judgment and Great Image, then explain the
  changed hexagram and structural transition.
- Do not label paraphrase, reconstructed wording, or modern translation as
  original text. Mark uncertain wording as unverified instead of inventing it.

## Scope

This changes only `SKILL.md`, `README.md`, and the skill contract test. Chart
calculation and Najia analysis remain unchanged.

## Validation

The contract test must verify that each original-text field precedes its
interpretation field. All tests and official skill validation must pass before
the installed copy and GitHub repository are updated.
