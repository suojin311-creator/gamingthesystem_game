# Level 1 — One metric

This folder owns the implemented Level 1 gameplay:

- `LevelOne.tsx`: entry component and decision flow; imports its own stylesheet.
- `metrics.ts`: six choices, scores, observations and temporary scene text.
- `state.ts`: in-memory state for one open game.
- `components/`: Level 1 dialogue, guide and replaceable cinematic placeholder.
- `styles.css`: Level 1 layouts and animations, scoped to `.level-one`.

Import shared base styles once in the application entry point. Reuse icons, audio,
visible-time delays and reading-time utilities from `../../shared/`.

The cinematic and completion contracts are documented in
[LEVEL1_HANDOFF.md](../../../docs/LEVEL1_HANDOFF.md).

The existing [v7 playable ZIP](../../../play/Level1-play-v7.zip?raw=true) remains
the saved Level 1 preview. The current App opens this level directly.

This folder in `level3-dev` contains the later Level 1 updates included in the
accepted Level 1 + Level 2 v6 release. The older `level1-preview` branch retains
the standalone v7 version and was not separately updated during Level 2 work.
See the [repository guide](../../../docs/REPOSITORY_GUIDE.md) for the current
source and saved preview locations.
