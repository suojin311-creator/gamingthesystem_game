# Shared game code

- `components/Icon.tsx`: presentation icons, independent of level data types.
- `components/Conversation.tsx`: chronological bubbles, typing dots and visible reading intervals; each level supplies its own lines.
- `data/metrics.ts`: the six common metric definitions; scores and outcomes stay in their respective levels.
- `hooks/useFeedback.ts`: local interface sounds and per-run mute state.
- `hooks/useVisibleDelay.ts`: delays that wait for visible information.
- `utils/readingTime.ts`: reading durations based on text length.
- `styles/base.css`: global resets, design tokens, common buttons and motion preferences.

Shared modules do not import from `levels/`. Keep a feature in its level folder
until there is a real reason for multiple levels to share it. In particular,
Level 1 dialogue text and guide remain local because their content and selectors
belong to that level. Mute preference is shared in page memory across level mounts.
