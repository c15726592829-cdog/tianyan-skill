# Location and Direction Module

## Scope

- Category ID: location-direction
- Chinese label: 方位、位置、方向、地点类别。
- Use when the main answer requested is where something or someone is.

## Trigger Questions

- 我的钥匙在什么方位？
- 她现在大概在哪个方向？
- 朋友这次玩的地方偏哪个方向？

## Exclusions and Redirects

- Travel itinerary or whereabouts belongs to `travel-whereabouts`.
- Lost or held object identification belongs to `objects-lost-property`.
- Exact departure or arrival time belongs to `timing`.

## Question Subject

Fix what or who is being located: self, named person, object, travel place, or
document/property. Then choose the person or matter anchor.

## Perspective

State the reference point for direction: asker location, known home base, last
known place, or candidate area. Without a reference point, exact direction is
low confidence.

## Primary Anchor or Useful Spirit

Use Ying for a named outside person. Use the object/matter useful spirit for
lost property, document, money, house, or travel matter. Use Shi only for the
asker's own location.

## Secondary References

Use inner/outer placement, branch direction, trigram direction, movement,
changed line, and known geographic constraints as separate evidence layers.

## Anchor Conflict Resolution

If branch direction and trigram direction conflict, report both and prefer the
anchor directly tied to the selected person/object. Lower resolution to broad
direction or environment.

## Month and Day

Month/day can activate, clash, fill void, or damage the location anchor. Use
them to judge whether location evidence is current, hidden, delayed, or moving.

## Moving and Changed Lines

Moving location anchor may show travel, relocation, exposure, or changing place.
Changed direction is corroboration only if the moving line is relevant.

## Shi and Ying

Shi/Ying positions distinguish asker's side from external side. Ying can mark
outside place or counterpart's direction; Shi can mark local/near place.

## Branch Structures, Void, Break, Tomb, and Hidden Spirit

Void or hidden anchor suggests concealed, hard-to-find, delayed, or unclear
location. Combination and clash need actual participating branches and strength.

## Hexagram and Trigram Corroboration

Use Shuo Gua direction and natural images to describe broad setting. Do not map
a trigram or three-combination directly to a named city.

## Allowed Answer Resolution

Allowed: broad direction, near/far, inside/outside, environment class, or ranked
candidate among predeclared places. Open-world named city is weak speculation.

## Required Contrary Evidence

Report missing reference point, conflicting direction layers, weak/void anchor,
known travel constraints, or open-world candidate space.

## Prohibited Inferences

Do not translate a three-combination, branch, six spirit, or trigram image into
a specific modern city without independent support.

## Source Rule IDs

- ZYSG-XIANG-001
- ZYSG-NATURE-001
- ZYSG-TEXT-001
- ZYSG-FAMILY-001
- ZYSG-BODY-001

## Worked Structural Examples

- “钥匙在哪”：first anchor object; then read object line, position, direction, and trigram image.
- “朋友去哪玩”：if asking named destination, route to `travel-whereabouts`; location module supplies direction only.
- “在哪个方向”：answer from a stated reference point; otherwise say the reference is underdetermined.
