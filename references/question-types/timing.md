# Timing Module

## Scope

- Category ID: timing
- Chinese label: 时间、应期、多久、何时发生。
- Use when the primary answer requested is a time window or activation point.

## Trigger Questions

- 我的好朋友刘硕士什么时间出发玩的？
- 这件事大概什么时候有消息？
- 他什么时候会联系我？

## Exclusions and Redirects

- If the main question is whether an event succeeds, primary is `outcomes-development`.
- If the main question is contact/action, primary is `contact-actions`.
- If the main question is travel destination, primary is `travel-whereabouts`.

## Question Subject

Define the event whose timing is being judged: departure, reply, result, signing,
payment, return, recovery, or document approval.

## Perspective

State timezone, calendar unit, event scale, and whether the question asks past
time, current timing, or future timing.

## Primary Anchor or Useful Spirit

Use the anchor of the timed event: actor for action, document for approval,
money for payment, traveler for departure/return, or outcome anchor for result.

## Secondary References

Void filling, month break recovery, moving line activation, changed branch,
combination, clash, day/month value, and seasonal support are timing triggers.

## Anchor Conflict Resolution

If several triggers compete, give ranked windows and lower confidence. Do not
select the most attractive date without explaining why it governs.

## Month and Day

Month/day are activation and strength authorities. A selected branch may become
active when valued, clashed, filled, released, or seasonally supported.

## Moving and Changed Lines

Moving lines supply the strongest timing candidates only when they touch the
selected anchor or event process.

## Shi and Ying

For interpersonal timing, decide whether Shi or Ying is the actor. Do not time
the other person's action from Shi's movement alone.

## Branch Structures, Void, Break, Tomb, and Hidden Spirit

Void, break, tomb, hidden spirit, combination, and clash each need a named
activation condition. Branch equality alone is insufficient.

## Hexagram and Trigram Corroboration

Hexagram and trigram images may describe speed or delay but not exact dates.

## Allowed Answer Resolution

Prefer relative speed, window, or competing triggers. Exact date or clock time
is weak unless multiple independent timing rules converge and reality permits.

## Required Contrary Evidence

Report multiple triggers, weak anchor, no movement, void/break, timezone
ambiguity, or event scale mismatch.

## Prohibited Inferences

Do not infer an exact date from one branch matching a day, month, or line.

## Source Rule IDs

- ZYSG-TEXT-001
- ZYSG-XIANG-001
- ZYSG-NATURE-001
- ZYSG-BODY-001
- ZYSG-FAMILY-001

## Worked Structural Examples

- “什么时候联系”：actor anchor plus contact-action evidence; timing from activation of actor/action line.
- “什么时候出发”：traveler anchor must be selected first; departure evidence is not the same as destination.
- “什么时候有结果”：outcome anchor and event scale determine whether timing is days, weeks, or months.
