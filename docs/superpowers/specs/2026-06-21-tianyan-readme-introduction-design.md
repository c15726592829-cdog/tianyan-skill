# Tianyan README Introduction Design

## Goal

Give the repository a concise identity that connects its traditional Liuyao
foundation with its engineering standards and preserves human agency.

## Placement

Replace the existing one-line summary immediately below `# Tianyan Skill` with
the approved introduction. Keep `## 支持范围` and every following section
unchanged.

## Content

Use a Markdown blockquote for the project motto:

> 大道五十，天衍四九，人遁其一。  
> 天行健，君子以自强不息。

Follow it with three short paragraphs:

1. Define Tianyan as a Wenwang Liuyao Najia charting and analysis skill. State
   that it observes structure, change, and tendency without treating a chart as
   an unchangeable command.
2. Explain that the knowable forty-nine belongs to analysis, while the missing
   one belongs to human wisdom, courage, ability, and action. The chart informs;
   the person chooses.
3. Connect the philosophy to implementation: deterministic charting, auditable
   three-coin simulation, explicit analytical boundaries, reproducible results,
   and reality taking priority over symbolic inference.

## Approved Copy

```markdown
> 大道五十，天衍四九，人遁其一。  
> 天行健，君子以自强不息。

**Tianyan** 是一个面向文王六爻的纳甲排盘与分析 Skill。它以传统卦理观察事物的结构、变化与趋势，却不把卦象视为不可更改的命令。

“四十九”代表可以推演和认识的部分；遁去的“一”，则留给人的智慧、勇气、实力与行动。卦象提供参考，选择仍归于人。所谓自强不息，正是在看见局势之后，仍以自身行动开辟可能。

在工程实现上，Tianyan 使用确定性排盘、可审计的三硬币模拟和明确的分析边界，力求让每一项排盘结果可复核、每一层判断有依据，并始终将现实事实置于象数推演之上。
```

## Validation

- Verify the motto and all three paragraphs appear before `## 支持范围`.
- Verify the old one-line summary does not remain as duplicate copy.
- Preserve `## 支持范围` and every following README section unchanged.
- Run the existing unit test suite to ensure repository behavior is unchanged.
- Run `git diff --check` to catch Markdown whitespace errors.
