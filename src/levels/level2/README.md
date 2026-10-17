# Level 2 — More metrics

- `LevelTwo.tsx`: complete 3 → 6 → 10 → 25 → 100 flow, in-memory state and paced presentation.
- `Conversation.tsx`: faster Level 2 dialogue and finding pace; the last message releases the next action immediately.
- Shared `MetricSelection.tsx`: short icon cards and a three-slot Alex’s Checklist; selected definitions are reviewed in the tray. Evaluations do not duplicate it.
- `data.ts`: three combination branches, evidence, checklists and integration types.
- `Perspectives.tsx`: same-round report, awaiting-observation state, prominent student behaviour and a smaller learning-risk label.
- `CinematicPlaceholder.tsx`: replaceable three-metric, six-metric and final story slots.
- `styles.css`: layout, icon/check reports and growing checklist paper pile, scoped to `.level-two`.

Default App starts at Level 1 and continues here. A dedicated player/Alex chapter conversation stays on screen until the player clicks its lower-right Choose three metrics button. Alex’s final message releases that action. `npm run dev -- --mode level2`
opens this level directly; `npm run build:level2` produces its self-contained preview.

Use the six common definitions, conversation bubbles, audio and visible-time
utilities from `../../shared/`. Do not import Level 1's component internals.
The optional `previousMetricId` prop carries the prior choice in memory.

See [LEVEL2_HANDOFF.md](../../../docs/LEVEL2_HANDOFF.md) for cinematic IDs,
completion data and boundaries. The combined host enables Continue to Level 3 through the optional onContinue callback. The standalone Level 2 entry leaves that callback absent and stops here.
