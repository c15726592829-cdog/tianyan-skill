# Tianyan Input Boundaries Design

## Goal

Make `tianyan` stricter and more practical for Wenwang Liuyao use by tightening
input boundaries, clarifying scope rules, and adding repository quality checks.

## Decisions

- Enforce cast time as `YYYY-MM-DD HH:MM` or `YYYY/MM/DD HH:MM`, with `T`
  allowed between date and time. Reject date-only, hour-only, seconds, and
  malformed inputs before datetime parsing.
- Continue accepting a trailing IANA timezone in `--time`, but validate the
  time portion before using it.
- Keep `--timezone` required at the script layer. In `SKILL.md`, default to the
  user's environment timezone when available, then `Asia/Shanghai`; ask for a
  timezone when the matter clearly belongs elsewhere.
- Accept Chinese line names in `parse_line_values`: `老阴`, `少阳`, `少阴`, and
  `老阳`, in addition to `6`, `7`, `8`, and `9`.
- Reject numeric or Meihua-style two-number casts in the skill instructions.
- Scope the one-day-three-casts rule to visible conversation context unless the
  host provides persistent state.
- Spell out repeated-question criteria and allowed follow-up cases.
- Add `README.md`, `pyproject.toml`, and GitHub Actions tests because this
  repository is also distributed through GitHub, not only as an installed skill.

## Non-Goals

- Do not add Meihua Yi or number-derived hexagram support.
- Do not rename existing reference files; current names are clearer and already
  linked from `SKILL.md`.
- Do not make the script infer timezone silently. Skill instructions may choose
  the default, but the script remains explicit and deterministic.

## Validation

- Unit tests must cover rejected incomplete times, accepted slash and trailing
  timezone formats, Chinese line aliases, invalid line values, Zi-hour day
  rollover, and solar-term month boundaries.
- `python -m unittest discover -s tests -v` must pass.
- Official skill validation must pass for the repo and installed copy.
