# Gaming the System

An English-language game about measuring engagement. Levels 1, 2 and 3 are playable. The partner’s opening and finished cinematics remain separate; story slots use replaceable placeholders.

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

**Level 2 — More metrics.** A separate chapter conversation introduces choosing three of the same six metrics. The vertical Alex’s Checklist records those choices. Three/six-metric evaluations avoid duplicate checklists. All 20 trios route to descriptive branches; missing areas receive a continuous amber warning. Expanding from 6 to 10, 25 and 100 requirements reveals how students move from completing requirements to managing and optimizing a checklist. The standalone entry ends here; the combined game enables Continue to Level 3.

**Level 3 — The weighting trap.** Choose any three priorities, allocate exactly 100% and confirm each weight. Confirmed values lock; other unlocked sliders automatically share the remainder. Each metric has a 10% minimum from the supplied prototype. Sliders share the same visual 0–100 scale, display their actual available maximum, and use whole percentage points to keep the total exact. Publishing automatically opens the selected three-shot classroom placeholder, then reveals the three qualitative responses one at a time.

An uneven first run leads to Rebalance; a near-even first run leads to Create a contrast. If the second test is still uneven, an explicit 34/33/33 balance check completes the comparison. Near-even means a spread of at most five points, with all three story shots medium. The side-by-side comparison uses actual tested snapshots. Balancing improves effort distribution while the percentages still guide Alex’s choices. Comparison and theory cinematics remain placeholders. Design Lab is reserved.

The opening owns name entry. `Gameplay` accepts its confirmed `playerName`, forwards it through all three levels and scene requests, and preserves it through in-page transitions. Standalone previews use Maya because they omit the opening. All player decisions use I. The 17 authored dialogue emoji are distinct.

Information arrives in visible-time beats with local Web Audio cues. Hidden tabs, off-screen timed information and restart dialogs hold pending beats; reduced motion removes animation. No Pause or extra Reveal button is used. All text remains available. Student cards show the specific behaviour prominently, with a small Learning at risk label. Weight percentages describe scoring, and qualitative effort categories follow the narrative; no numerical learning loss or learning gain is invented.

Each page is one independent game. Closing, reopening, reloading or restoring from the back-forward cache starts fresh. Choices, names and sound preferences are not saved in browser storage or sent to a service. Two students can share one open game; there is no multiplayer server.

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

After an approved change, rebuild all previews together, validate the packages and synchronize the preview branches. `play/LATEST.json` records source and artifact hashes. Keep version-numbered historical ZIPs unchanged.

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

Each level owns its rules and text. Shared modules never import level internals. Partner contracts are documented in [Opening handoff](docs/OPENING_HANDOFF.md), [Level 1](docs/LEVEL1_HANDOFF.md), [Level 2](docs/LEVEL2_HANDOFF.md) and [Level 3](docs/LEVEL3_HANDOFF.md).

## Validate

```sh
npm run package:previews
node tests/level3_rules.mjs
python tests/level3.py
# With npm run dev running:
python tests/level3_integration.py
python tests/level2_integration.py
python tests/player_identity.py
python tests/release.py
node tests/dialogue_emojis.mjs
```

The new Level 3 checks cover allocation invariants, all 20 trios, three adaptive routes, actual cinematic shot selection, compared snapshots, name/completion contracts, chapter handoff, real-time audio and sequential updates, restart and 320–1366px layouts. The release test reads the real four ZIPs and plays across all three chapters. [LEVEL3_VALIDATION-v1.json](docs/LEVEL3_VALIDATION-v1.json) records this release. Earlier validation reports and versioned ZIPs are historical records.

Offline browser tests serve exact production HTML through an in-memory HTTPS origin because managed Chromium blocks local file navigation. Opening the downloaded file in the user’s particular browser remains a separate check. Test outputs/screenshots go to ignored test-results/. These are functional checks, not a classroom load test.
