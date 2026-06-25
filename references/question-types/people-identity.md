# People Identity Module

## Scope

- Category ID: people-identity
- Chinese label: 人物身份、同伴、对象是谁。
- Use when the main answer requested is a person, companion, role, or identity.

## Trigger Questions

- 我今天和谁一起吃的晚饭？
- 我的好朋友刘硕士和谁一起玩的？
- 刚才陪我逛街的人是谁？

## Exclusions and Redirects

- If the question asks what the person thinks, route primary to `thoughts-intentions`.
- If it asks whether the person will contact or act, route primary to `contact-actions`.
- If it asks relationship outcome, route primary to `romance-marriage`.

## Question Subject

Identify the named person or identity slot before reading six relatives. For a
friend or outsider, the person anchor is normally Ying; the unknown companion
is a candidate identity attached to that person's situation.

## Perspective

State whether the asker is asking about self, a named third party, or an
unknown person connected with a named third party. Do not rewrite the question
after reveal.

## Primary Anchor or Useful Spirit

Use Shi for the asker. Use Ying for a named outside person or target side.
Use matter-specific relatives only after fixing whose person or companion is
being identified.

## Secondary References

Six relatives can suggest role class: peers, resources, authority, documents,
children/juniors, or pressure. Trigram family images are secondary only.

## Anchor Conflict Resolution

If Ying and a six-relative candidate conflict, preserve Ying as the named-person
anchor and lower the exact-identity resolution unless a predeclared candidate
set or independent evidence supports the relative.

## Month and Day

Judge whether the person anchor and candidate identity lines are supported,
controlled, void, broken, tombed, or activated by month/day.

## Moving and Changed Lines

Movement can show activity or connection involving a person, but it does not
prove exact identity. Read only moving lines that touch Shi, Ying, the person
anchor, or candidate identity evidence.

## Shi and Ying

Shi is the asker's side. Ying is normally the external person or counterpart.
For named friends and outsiders, start with Ying before considering six-relative
role imagery.

## Branch Structures, Void, Break, Tomb, and Hidden Spirit

Hidden or void candidate lines can show concealed, delayed, or unmanifest
identity information; they do not prove absence.

## Hexagram and Trigram Corroboration

Trigram family images may suggest elder/younger, male/female symbolic position,
or household role only as corroboration. They cannot decide exact identity.

## Allowed Answer Resolution

Prefer broad role class, bounded category, or ranked candidate. Exact named
identity is weak unless candidates were fixed before the cast and at least two
independent evidence groups converge.

## Required Contrary Evidence

List any anchor ambiguity, weak or void person line, conflicting Shi/Ying
relation, or missing candidate set.

## Prohibited Inferences

Do not infer gender, boyfriend, girlfriend, spouse, or exact companion from
妻财、官鬼、trigram family image, or a single moving line alone.

## Source Rule IDs

- ZYSG-TEXT-001
- ZYSG-NATURE-001
- ZYSG-BODY-001
- ZYSG-FAMILY-001
- ZYSG-XIANG-001

## Worked Structural Examples

- “刘硕士和谁一起玩”：刘硕士 is the outside named subject, so start from Ying; companion identity is secondary and cannot be upgraded to exact boyfriend/girlfriend without independent support.
- “我和谁吃饭”：asker-side event starts from Shi plus relevant companion/counterpart evidence.
- “刚才那个人是谁”：if candidate set was not fixed, output role class and ranked speculation, not a scored exact claim.
