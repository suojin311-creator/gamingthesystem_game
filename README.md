# Gaming the System

An English-language game about measuring engagement. Level 1 and Level 2 gameplay are implemented. The opening and finished cinematics remain the partner's separate work; classroom scenes are clearly labelled, replaceable placeholders.

**[Download the Level 2 preview (v5)](play/Level2-play-v5.zip?raw=true).** Sign in to GitHub with access to this private repository, download and extract the ZIP, then open **Level2.html** in Chrome or Edge. No installation is needed. **Levels1-and-2.html** in the same ZIP starts at Level 1 and continues to Level 2.

Player decisions now use **I**. The reusable `Gameplay` host accepts the name already collected in the opening and carries it through both levels, dialogue labels, avatars and cinematic requests. These standalone previews still use Maya because they omit the opening. See [Opening/name handoff](docs/OPENING_HANDOFF.md) for the integration point in the partner's supplied source.

The saved [Level 1 v7 preview](play/Level1-play-v7.zip?raw=true) is preserved unchanged on `level1-preview` and in `play/`. New development is on `level2-dev`.

## What is playable

**Level 1 — One metric.** Select one of six metrics, write a prediction, watch the illustrative reported score rise, visit the classroom and compare the outcome. The final observation page now has an enabled **Continue to Level 2** button. Completion still reports automatically; navigation waits for that button.

**Level 2 — More metrics.** A dedicated chapter introduction presents the player/Alex conversation, then automatically opens the six working metric cards after the final reply's reading interval. Choose exactly three; the vertical **Alex’s Checklist** records the current selection using the same visual format as the later checklists. Three- and six-metric evaluations show the changing metrics and perspective cards without a duplicate checklist. All 20 trios route to three descriptive outcome groups. Continue from 6 to 10, 25 and 100 requirements, with students moving from completing requirements to managing criteria and optimizing the checklist. Level 3 is reserved.

Level 2 counts requirements; it does not invent numerical learning results or a declining student health score. Level 1's 0–100 reported scores remain illustrative. Neither predictions nor choices are graded or sent to a service.

The gap view emphasizes **3 areas untracked** with larger metric names and a continuous, slow amber border pulse until the missing metrics are added. Reduced motion keeps a static prominent border. Both levels use the same student card content: the observed behaviour has the largest text, with **Learning at risk** as a small supporting label. Level 1 describes skimming, shallow contributions, looking busy, formulaic discussion, safe reflection patterns and box-ticking replies. Each new round clears both cards' old presentation: management awaits its report and students show **Awaiting observation** until current classroom evidence arrives. There is no stale observed-at count or numerical learning penalty.

Results arrive before observations. Level 2 dialogue starts after 1.6–2.8 seconds of visible finding time, with 300 ms typing dots and 1.1–2.2 seconds between messages. Its next button appears with the final reply; all text remains available and the player decides when to continue. At 10, 25 and 100 metrics checklist actions tick sequentially, with the next button about one second after the final item. Level 1 keeps its original 6–8 second finding time, 650 ms typing dots and 3–5 second message intervals. Hidden tabs, off-screen information and restart dialogs hold pending beats. Reduced motion removes movement. Level 2 has no Guide, Pause or Reveal control.

State and sound preference live only in the current page's memory. Moving between levels and scenes retains the open run. Reloading, reopening or restoring the page from the browser back-forward cache starts fresh. No progress or preferences are written to localStorage, sessionStorage or cookies. Each computer runs independently; two students can share one open game. This is not networked multiplayer.

## Develop

Use Node.js 20.19+, 22.12+, or newer (validated with Node 24):

```sh
cd /workspace/gamingthesystem_game
npm ci --cache /tmp/gaming-the-system-npm-cache
npm run dev
```

The default development entry starts at Level 1. To work directly on Level 2:

```sh
npm run dev -- --mode level2
```

Production builds check TypeScript and embed JavaScript, styles and images in one HTML file, with no external fonts, services or runtime network requests:

```sh
npm run build         # dist/index.html: Level 1 → Level 2
npm run build:level2  # dist-level2/index.html: start directly at Level 2
```

## Source layout

```text
src/
  App.tsx                 Standalone preview entry (Maya fallback)
  Gameplay.tsx            Opening-name handoff and in-memory Level 1 → Level 2 navigation
  main.tsx                Bootstrap and shared base stylesheet
  levels/
    level1/               One-metric choices, scores, guide and observations
    level2/
      LevelTwo.tsx        Level 2 gameplay and presentation sequence
      Conversation.tsx   Faster Level 2 pace and next-button arrival callback
      MetricChecklist.tsx Vertical Alex’s Checklist for the current three choices
      Perspectives.tsx   Current-round report and student learning-risk card
      data.ts             Trio branches, expansion stages and scene contract
      CinematicPlaceholder.tsx
      styles.css          Level 2 layouts scoped to .level-two
  shared/
    components/           Icons, timed conversation bubbles and shared student learning-risk presentation
    data/metrics.ts       Six metric names, IDs and descriptions
    hooks/                Audio and visible-time delays
    utils/                Reading-time calculation and player-name fallback
    styles/               Common design tokens, controls and conversation defaults
  assets/                 Office and classroom artwork
```

Each level owns its rules and text. Shared modules do not import level internals. `Gameplay.tsx` connects levels without storage or full-page navigation. The cinematic opening has not been merged. See [Opening handoff](docs/OPENING_HANDOFF.md), [Level 1 handoff](docs/LEVEL1_HANDOFF.md) and [Level 2 handoff](docs/LEVEL2_HANDOFF.md) for the partner integration contracts.

## Validate

With Python Playwright and system Chromium available:

```sh
npm run build
npm run build:level2
python tests/level2.py
python tests/smoke.py --file dist/index.html
python tests/feedback.py --file dist/index.html
python tests/guide.py --file dist/index.html
# With npm run dev running, also check the partner scene contracts:
python tests/level2_integration.py
python tests/player_identity.py
# After packaging the playable ZIP:
python tests/release.py
```

The browser tests serve the exact production HTML bytes through an in-memory test origin with networking disabled. This cloud machine blocks `file://` navigation, so opening the downloaded file in the user's particular browser remains a separate check. Screenshots/results go to ignored `test-results/`.

Checks cover the automatic chapter-dialogue handoff, vertical selection checklist, absence of duplicate evaluation checklists, continuous gap pulse, the 20 trios, complete expansion flow, both levels' handoff, outcome text, timing, selection limits, sound, keyboard controls, restart, fresh-page lifetime and responsive layouts. They are browser functional checks, not a classroom concurrency/load test.

The current results and artifact hashes are recorded in
[LEVEL2_VALIDATION-v5.json](docs/LEVEL2_VALIDATION-v5.json). Earlier previews and
their validation records are preserved. The highlighted narrative ownership
check is in [LEVEL2_NARRATIVE_AUDIT.md](docs/LEVEL2_NARRATIVE_AUDIT.md).
