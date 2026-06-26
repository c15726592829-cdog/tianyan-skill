# Travel and Whereabouts Module

## Scope

- Category ID: travel-whereabouts
- Chinese label: 出行、行踪、去向、路线、返回。
- Use when the main question concerns a person's travel or whereabouts.

## Trigger Questions

- 我的好朋友刘硕士去哪玩了？
- 他这趟出门去了什么地方？
- 她什么时候出发去玩的？

## Exclusions and Redirects

- Pure direction belongs to `location-direction`.
- Pure departure/return time belongs to `timing`.
- Companion identity belongs to `people-identity`.

## Question Subject

Fix traveler, trip phase, and requested resolution: departure, current location,
destination, route, companion, return, or safety.

## Perspective

For named friends or outsiders, anchor the traveler at Ying. State known home
base, likely travel frame, and whether candidate cities were predeclared.

## Primary Anchor or Useful Spirit

Use Ying as named traveler anchor; use movement/change and location evidence
for trip state. Use companion or timing modules only as secondary if asked.

## Secondary References

Direction, inner/outer, road/water/mountain/fire imagery, branch movement,
combination/clash, and real travel constraints can corroborate.

## Anchor Conflict Resolution

If traveler evidence and destination imagery conflict, prioritize traveler
state and downgrade destination specificity.

## Month and Day

Month/day indicate whether travel line is active, blocked, delayed, returning,
or hidden. They can trigger timing but not name the city alone.

## Moving and Changed Lines

Relevant movement may show departure, transit, return, route change, or activity
around the traveler. Movement of unrelated lines is not travel evidence.

## Shi and Ying

Ying is normally the named outside traveler. Shi may show asker's knowledge or
relation to the trip but not the destination by itself.

## Branch Structures, Void, Break, Tomb, and Hidden Spirit

Combination/clash can show route binding, separation, movement, or obstruction
only when relevant branches are present and strong. Void can hide whereabouts.

## Hexagram and Trigram Corroboration

Trigram direction and natural images may describe travel environment or broad
direction. They do not produce a modern city without independent support.

## Allowed Answer Resolution

Allowed: trip phase, broad direction, environment class, likely range, or ranked
candidate if the candidate set was fixed. Named city is weak in open-world tests.
For destination questions, lock direction and environment before considering a
name. If no candidate set exists, give ranked candidates only as speculation.

## Required Contrary Evidence

Report missing candidate set, contradictory direction, weak traveler anchor,
void/hiding, and real-world travel constraints.

## Prohibited Inferences

Do not derive a city from water/fire/wood structure, three-combination, or
single trigram image. Do not claim safety status from one symbol.

## Source Rule IDs

- ZYSG-TEXT-001
- ZYSG-NATURE-001
- ZYSG-BODY-001
- ZYSG-XIANG-001
- ZYSG-FAMILY-001

## Worked Structural Examples

- “刘硕士去哪玩”：Ying anchors Liu硕士; direction/environment may be answerable, exact city is speculative unless candidate frame exists.
- “什么时候出发”：primary should be `timing`; traveler module supplies actor and trip phase.
- “和谁去”：primary should be `people-identity`; travel module supplies context only.
