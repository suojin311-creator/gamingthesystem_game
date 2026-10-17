# Level 2 — More metrics

- `LevelTwo.tsx`: complete 3 → 6 → 10 → 25 → 100 flow, in-memory state and paced presentation.
- `Conversation.tsx`: faster Level 2 dialogue and finding pace; the last message releases the next action immediately.
- `Notebook.tsx`: passive choice record and three/six requirement checks. Selection starts directly on the metric cards.
- `data.ts`: three combination branches, evidence, checklists and integration types.
- `Perspectives.tsx`: same-round report, awaiting-observation state, prominent student behaviour and a smaller learning-risk label.
- `CinematicPlaceholder.tsx`: replaceable three-metric, six-metric and final story slots.
- `styles.css`: layout scoped to `.level-two`.

Default App starts at Level 1 and continues here. `npm run dev -- --mode level2`
opens this level directly; `npm run build:level2` produces its self-contained preview.

Use the six common definitions, conversation bubbles, audio and visible-time
utilities from `../../shared/`. Do not import Level 1's component internals.
The optional `previousMetricId` prop carries the prior choice in memory.

See [LEVEL2_HANDOFF.md](../../../docs/LEVEL2_HANDOFF.md) for cinematic IDs,
completion data and boundaries. Level 3 is reserved, not implemented.
