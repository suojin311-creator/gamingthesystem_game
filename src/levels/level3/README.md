# Level 3 — Gameplay workspace

This is the Level 3 development folder on `level3-dev`. The branch starts from
the accepted Level 1 + Level 2 v6 version (`336c59f`), also saved unchanged on
`level2-preview`. Both earlier levels, shared modules, artwork and playable ZIPs
are included in this branch.

## Current state

Only the folder and integration notes are prepared. There is no Level 3 gameplay
component or playable Level 3 preview yet. `Gameplay.tsx` still connects Level 1
and Level 2, and Level 2's final Continue to Level 3 action remains reserved.
No earlier gameplay, scene, dialogue, dependency or build configuration changed
as part of this repository organization.

## Implementation location

The planned modules belong here as the level is implemented:

| Planned module | Responsibility |
| --- | --- |
| `LevelThree.tsx` | Level 3 gameplay, state and presentation |
| `data.ts` | Level-specific choices, outcomes and scene contracts |
| `styles.css` | Styles scoped to `.level-three` |
| `CinematicPlaceholder.tsx` | Replaceable story slots for partner cinematics |

The filenames above are a layout plan, not existing working components. Reuse
the common metric IDs, conversation bubbles, icons, audio, visible-time delays
and learning-risk presentation from `../../shared/`. The current six core
metrics keep their IDs: `prep`, `part`, `focus`, `discuss`, `reflect`, `peer`.

## Existing handoff context

Level 2 ends after 100 tracked requirements, with the player's question:
“What if some metrics mattered more than others?” The earlier narrative reserves
priority choices for the next stage. Its detailed rules and presentation will
be implemented from the supplied mechanics and Narrative V2 documents.

The existing `LevelTwoResult` completion value is:

```ts
{
  selectedMetricIds: ['prep', 'part', 'discuss'],
  branch: 'mixed',
  metricsTracked: 100
}
```

The host in `src/Gameplay.tsx` is the integration point for the later Level 2 →
Level 3 transition. Carry the opening's confirmed `playerName` through that host,
the same way as the first two levels. Player decisions use I, all authored game
text stays in English, Alex's emoji remain distinct, and new scenes can use
placeholders until the cinematics are ready. Game progress and sound preferences
remain in the current page's memory.

See [repository guide](../../../docs/REPOSITORY_GUIDE.md),
[Level 2 handoff](../../../docs/LEVEL2_HANDOFF.md) and
[opening/name handoff](../../../docs/OPENING_HANDOFF.md).
