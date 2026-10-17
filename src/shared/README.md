# Shared game code

- `components/Icon.tsx`: presentation icons, independent of level data types.
- `hooks/useFeedback.ts`: local interface sounds and per-run mute state.
- `hooks/useVisibleDelay.ts`: delays that wait for visible information.
- `utils/readingTime.ts`: reading durations based on text length.
- `styles/base.css`: global resets, design tokens, common buttons and motion preferences.

Shared modules do not import from `levels/`. Keep a feature in its level folder
until there is a real reason for multiple levels to share it. In particular,
Level 1 dialogue and guide remain local because their text and selectors belong
to that level.
