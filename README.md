# Gaming the System

An English-language game about measuring engagement. Levels 1, 2 and 3 are playable. The partner’s opening and finished cinematics remain separate; story slots use replaceable placeholders.

Download the [Level 3 + full-game review ZIP](https://github.com/suojin311-creator/gamingthesystem_game/blob/level3-dev/play/Level3-and-Full-game-play.zip?raw=true) for both requested versions in one archive: `Level3/Level3.html` and `Full-game/Gaming-the-System.html`.

The latest combined and individual previews live together on **level3-dev**:

| Latest preview | Download | Open after extracting |
| --- | --- | --- |
| **Levels 1 → 2 → 3** | [Full-game-play.zip](https://github.com/suojin311-creator/gamingthesystem_game/blob/level3-dev/play/Full-game-play.zip?raw=true) | Gaming-the-System.html |
| **Level 1 only** | [Level1-play.zip](https://github.com/suojin311-creator/gamingthesystem_game/blob/level3-dev/play/Level1-play.zip?raw=true) | Level1.html |
| **Level 2 only** | [Level2-play.zip](https://github.com/suojin311-creator/gamingthesystem_game/blob/level3-dev/play/Level2-play.zip?raw=true) | Level2.html |
| **Level 3 only** | [Level3-play.zip](https://github.com/suojin311-creator/gamingthesystem_game/blob/level3-dev/play/Level3-play.zip?raw=true) | Level3.html |

Sign in with access to this private repository, download and extract the ZIP, then open its HTML in Chrome or Edge. No installation is required; the downloaded game runs offline. These fixed paths are updated together. Version-numbered ZIPs preserve older releases.

Current development is on **level3-dev**. The existing level1-preview, level2-preview and level2-dev branches are synchronized for this release. Use [play/](play/README.md) as the single place to find current individual and combined downloads. See [GitHub 使用说明](docs/REPOSITORY_GUIDE.md).

## Playable flow

**Level 1 — One metric.** Choose one of six plausible indicators, write a prediction, watch an illustrative score rise, then observe a selected classroom story and its unintended behaviour. The comparison keeps the prediction, one evidence paragraph and the player/Alex conversation. Alex replies in two grouped bubbles with distinct emoji. The standalone entry stops here; the combined game enables Continue to Level 2.

**Level 2 — More metrics.** A separate chapter conversation introduces choosing three of the same six metrics. A three-slot Alex’s Checklist records those choices. Three/six-metric icon/check reports avoid duplicate checklists. All 20 trios route to descriptive branches; missing areas receive a continuous amber warning. Expanding from 6 to 10, 25 and 100 requirements fills a checkbox field and grows a paper pile as students move from completing requirements to managing and optimizing a checklist. The standalone entry ends here; the combined game enables Continue to Level 3.

**Level 3 — The weighting trap.** The combined game preselects Level 2’s three metrics; players may swap them before weighting. Standalone Level 3 starts with an empty selection. Allocate exactly 100% across three priorities using 0–100% sliders. Confirm one card, then adjust either remaining slider; confirming either final card locks the pair and marks the other Auto-confirmed. Reset weights sits above the action row. Player/Alex conversations use a separate bottom region. Publication stays visible with both perspective cards until the player clicks Observe the class. Results reveal three qualitative responses with aligned, divided columns and the same metric font size used in Levels 1–2.

The second test freely changes the split; it is not required to become more even. Near-even means a highest-to-lowest spread of at most ten percentage points. If the two player tests contain only one pattern, a clearly identified system reference supplies the missing pattern: What if they counted equally? or What if one counted more? The comparison keeps every tested run, including both player attempts and any reference. Repeated effort-summary boxes and comparison footnotes are removed. Level 3 action footers contain their controls without explanatory captions. Teacher and Alex use ordinary speech bubbles with connected questions and replies. The result/compare tables use a calmer hierarchy of metric names, readable percentages and medium-weight effort labels. Alex has two short messages at each workbench beat. Alex’s response and Goodhart’s theory reveal remain replaceable cinematics; this preview stops at the final theory frame without a Design Lab transition.

The opening owns name entry. `Gameplay` accepts its confirmed `playerName`, forwards it through all three levels and scene requests, and preserves it through in-page transitions. Standalone previews use Maya because they omit the opening. All player decisions use I. The 25 authored dialogue emoji are distinct.

Information arrives in visible-time beats with local Web Audio cues. Hidden tabs, off-screen timed information and the Level 1 guide hold pending beats; reduced motion removes animation. No Pause or extra Reveal button is used. All text remains available. Student cards show the specific behaviour prominently, with a small Learning at risk label. Weight percentages describe scoring, and qualitative effort categories follow the narrative; no numerical learning loss or learning gain is invented.

The Restart control and its dialogs are removed in all three levels. Administrator access is deferred. Reset weights only resets the current allocation. Each page is one independent game. Closing, reopening, reloading or restoring from the back-forward cache starts fresh. Choices, names and sound preferences are not saved in browser storage or sent to a service. Two students can share one open game; there is no multiplayer server.

## Develop and package

Use Node.js 20.19+, 22.12+ or newer (validated with Node 24), plus Python 3 for ZIP packaging:

```sh
cd /workspace/gamingthesystem_game
npm ci --cache /tmp/gaming-the-system-npm-cache
npm run dev                     # Combined game, starts at Level 1
npm run dev -- --mode level3     # Work directly on Level 3
```

Level 1/2 standalone development uses `--mode level1` or `--mode level2`. Builds check TypeScript and inline JavaScript, CSS and artwork into one HTML:

```sh
npm run build                   # dist/index.html: Levels 1 → 2 → 3
npm run build:level1             # dist-level1/index.html: Level 1 only
npm run build:level2             # dist-level2/index.html: Level 2 only
npm run build:level3             # dist-level3/index.html: Level 3 only
npm run package:previews         # Rebuild and package all four latest entries
```

After an approved change, rebuild all previews and the two-version review ZIP together, validate the packages and synchronize the preview branches. `play/LATEST.json` records source and artifact hashes. Keep version-numbered historical ZIPs unchanged.

## Source layout and partner integration

```text
src/
  App.tsx                 Combined / individual preview entry
  Gameplay.tsx            Opening-name handoff and Level 1 → 2 → 3 navigation
  levels/
    level1/               Choices, prediction, score, guide and observations
    level2/               Three-metric branches and 6 → 10 → 25 → 100 expansion
    level3/
      LevelThree.tsx      Priority choices, locked weights, run history and comparison
      weights.ts          Exact allocation and adaptive-path rules
      data.ts             Narrative responses and cinematic/result contracts
      CinematicPlaceholder.tsx
      styles.css          Layout scoped to .level-three
  shared/                 Metric definitions, icons, conversations, sounds and timing
  assets/                 Office and classroom artwork
scripts/package_previews.py
play/                     Latest downloads and historical archives
```

Each level owns its rules and text. Shared modules never import level internals. [Typography](docs/TYPOGRAPHY.md) documents shared sizes for equivalent content across the three levels. Partner contracts are documented in [Opening handoff](docs/OPENING_HANDOFF.md), [Level 1](docs/LEVEL1_HANDOFF.md), [Level 2](docs/LEVEL2_HANDOFF.md) and [Level 3](docs/LEVEL3_HANDOFF.md).

## Validate

```sh
npm run package:previews
node tests/level3_rules.mjs
python tests/level3.py
python tests/level3_feedback.py
python tests/management_satisfaction.py
python tests/visual_play.py
python tests/typography.py
# With npm run dev running:
python tests/level3_integration.py
python tests/level2_integration.py
python tests/player_identity.py
python tests/release.py
node tests/dialogue_emojis.mjs
```

The Level 3 checks cover allocation invariants, all 20 trios, three adaptive routes, actual cinematic shot selection, compared snapshots, name/completion contracts, chapter handoff, real-time audio and sequential updates, no player Restart controls and 320–1366px layouts. The shared [management satisfaction](docs/MANAGEMENT_SATISFACTION.md) checks cover report-triggered increases, chapter baselines, replay stability, standalone previews and the one-second fill animation. [Visual operations](docs/VISUAL_PLAY.md) add checks for compact cards, removable slots, illustrated evidence, checklist growth and matching Alex poses. The release test reads all four individual/combined ZIPs, verifies the two-version review ZIP against those exact builds, and plays across all three chapters. [LEVEL3_VALIDATION-v7.json](docs/LEVEL3_VALIDATION-v7.json) records this release. Earlier validation reports and versioned ZIPs are historical records.

Offline browser tests serve exact production HTML through an in-memory HTTPS origin because managed Chromium blocks local file navigation. Opening the downloaded file in the user’s particular browser remains a separate check. Test outputs/screenshots go to ignored test-results/. These are functional checks, not a classroom load test.
