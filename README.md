# Gaming the System

An English-language game about measuring engagement. Level 1 and Level 2 gameplay are implemented. The opening and finished cinematics remain the partner's separate work; classroom scenes are clearly labelled, replaceable placeholders.

The latest combined and individual previews live together on **`level3-dev`**:

| Latest preview | Download | Open after extracting |
| --- | --- | --- |
| **Level 1 + Level 2** | [Full-game-play.zip](https://github.com/suojin311-creator/gamingthesystem_game/blob/level3-dev/play/Full-game-play.zip?raw=true) | `Gaming-the-System.html` |
| **Level 1 only** | [Level1-play.zip](https://github.com/suojin311-creator/gamingthesystem_game/blob/level3-dev/play/Level1-play.zip?raw=true) | `Level1.html` |
| **Level 2 only** | [Level2-play.zip](https://github.com/suojin311-creator/gamingthesystem_game/blob/level3-dev/play/Level2-play.zip?raw=true) | `Level2.html` |

Sign in to GitHub with access to this private repository, download and extract the ZIP, then open its HTML in Chrome or Edge. No installation is needed. These fixed download paths are updated together; version-numbered ZIPs preserve older releases.

Player decisions now use **I**. The reusable `Gameplay` host accepts the name already collected in the opening and carries it through both levels, dialogue labels, avatars and cinematic requests. These standalone previews still use Maya because they omit the opening. See [Opening/name handoff](docs/OPENING_HANDOFF.md) for the integration point in the partner's supplied source.

New work continues on **`level3-dev`**, with Level 3's folder at [`src/levels/level3/`](src/levels/level3/README.md). The current playable build contains Level 1 and Level 2; Level 3 is being prepared. The latest standalone Level 1 includes the changes made during Level 2 development, including clearer student behaviour and the two-message Alex replies.

| Branch | Purpose |
| --- | --- |
| `level1-preview` | Refreshed source and latest standalone Level 1 download |
| `level2-preview` | Current preview release, with combined and individual downloads |
| `level2-dev` | Earlier development branch, synchronized for this release; new work uses `level3-dev` |
| **`level3-dev`** | **Current development: complete game source plus the Level 3 workspace** |

All four branches are synchronized for this preview release. Use `level3-dev/play/` as the single place to find the latest downloads. See the [repository guide / GitHub 使用说明](docs/REPOSITORY_GUIDE.md). Historical [Level 1 v7](play/Level1-play-v7.zip?raw=true) and [Level 1 + Level 2 v6](play/Level2-play-v6.zip?raw=true) archives remain available; their versioned links preserve those releases.

## What is playable

**Level 1 — One metric.** Select one of six metrics, write a prediction, watch the illustrative reported score rise, visit the classroom and compare the outcome. The combined game enables **Continue to Level 2** on the final observation page; the Level 1-only preview leaves it reserved and disabled. Both entries use the same `LevelOne` component. Completion reports automatically; navigation waits for that button when connected.

**Level 2 — More metrics.** A dedicated chapter introduction presents the player/Alex conversation, then shows a lower-right **Choose three metrics** button with Alex's final message. The introduction stays until the player chooses to continue. Choose exactly three; the vertical **Alex’s Checklist** records the current selection using the same visual format as the later checklists. Three- and six-metric evaluations show the changing metrics and perspective cards without a duplicate checklist. All 20 trios route to three descriptive outcome groups. Continue from 6 to 10, 25 and 100 requirements, with students moving from completing requirements to managing criteria and optimizing the checklist. Level 3 is reserved.

Level 2 counts requirements; it does not invent numerical learning results or a declining student health score. Level 1's 0–100 reported scores remain illustrative. Neither predictions nor choices are graded or sent to a service.

The gap view emphasizes **3 areas untracked** with larger metric names and a stronger continuous 1.25-second border pulse, wider outer glow and synchronized warning icon until the missing metrics are added. Reduced motion keeps a static prominent border. Both levels use the same student card content: the observed behaviour has the largest text, with **Learning at risk** as a small supporting label. Level 1 describes skimming, shallow contributions, looking busy, formulaic discussion, safe reflection patterns and box-ticking replies. Each new round clears both cards' old presentation: management awaits its report and students show **Awaiting observation** until current classroom evidence arrives. There is no stale observed-at count or numerical learning penalty.

Results arrive before observations. Level 2 dialogue starts after 1.6–2.8 seconds of visible finding time, with 300 ms typing dots and 1.1–2.2 seconds between messages. Its next button appears with the final reply; all text remains available and the player decides when to continue. At 10, 25 and 100 metrics checklist actions tick sequentially, with the next button about one second after the final item. Level 1 starts dialogue 3.5 seconds earlier: its finding interval is now 2.5–4.5 visible seconds, followed by the same 650 ms typing dots and 3–5 second message intervals. Its prediction page keeps the example and input without a repeated visible prompt/helper; the input retains an accessible label. Hidden tabs, off-screen information and restart dialogs hold pending beats. Reduced motion removes movement. Level 2 has no Guide, Pause or Reveal control.

State and sound preference live only in the current page's memory. Moving between levels and scenes retains the open run. Reloading, reopening or restoring the page from the browser back-forward cache starts fresh. No progress or preferences are written to localStorage, sessionStorage or cookies. Each computer runs independently; two students can share one open game. This is not networked multiplayer.

Alex now replies in two consecutive short messages. The three-metric conversation explicitly refers to the other three areas; the six-metric reply answers the proposal to add metrics. All 16 dialogue emoji are distinct. Consecutive messages from one character share a visible name/avatar, and a newly arrived reply scrolls into view when needed. The approved text is recorded in [Dialogue review](docs/DIALOGUE_REVIEW.md).

## Develop

Use Node.js 20.19+, 22.12+, or newer (validated with Node 24):

```sh
cd /workspace/gamingthesystem_game
npm ci --cache /tmp/gaming-the-system-npm-cache
npm run dev
```

The default development entry starts at Level 1 and continues to Level 2. For a standalone level:

```sh
npm run dev -- --mode level1
npm run dev -- --mode level2
```

Production builds check TypeScript and embed JavaScript, styles and images in one HTML file, with no external fonts, services or runtime network requests:

```sh
npm run build         # dist/index.html: Level 1 → Level 2
npm run build:level1  # dist-level1/index.html: Level 1 only
npm run build:level2  # dist-level2/index.html: start directly at Level 2
npm run package:previews # rebuild and package all three fixed download entries
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
    level3/
      README.md           Level 3 development location and existing handoff context
  shared/
    components/           Icons, timed conversation bubbles and shared student learning-risk presentation
    data/metrics.ts       Six metric names, IDs and descriptions
    hooks/                Audio and visible-time delays
    utils/                Reading-time calculation and player-name fallback
    styles/               Common design tokens, controls and conversation defaults
  assets/                 Office and classroom artwork
```

Each level owns its rules and text. Shared modules do not import level internals. `Gameplay.tsx` connects levels without storage or full-page navigation. The cinematic opening has not been merged. See [Opening handoff](docs/OPENING_HANDOFF.md), [Level 1 handoff](docs/LEVEL1_HANDOFF.md) and [Level 2 handoff](docs/LEVEL2_HANDOFF.md) for the partner integration contracts.

The Level 3 folder currently documents the integration context and planned module layout. Its gameplay, preview entry and Level 2 continuation will be connected during implementation.

After changes to either level or shared modules, use `npm run package:previews` to rebuild all three latest downloads together. `play/LATEST.json` records their source and artifact hashes. Validate the packages before publishing and synchronize the preview branches with the approved release; keep version-numbered archives unchanged.

## Validate

With Python Playwright and system Chromium available:

```sh
npm run package:previews
python tests/level2.py
python tests/smoke.py --file dist/index.html
python tests/smoke.py --file dist-level1/index.html --standalone
python tests/feedback.py --file dist/index.html
python tests/guide.py --file dist/index.html
# With npm run dev running, also check the partner scene contracts:
python tests/level2_integration.py
python tests/player_identity.py
node tests/dialogue_emojis.mjs
# After packaging the playable ZIP:
python tests/release.py
```

The browser tests serve the exact production HTML bytes through an in-memory test origin with networking disabled. This cloud machine blocks `file://` navigation, so opening the downloaded file in the user's particular browser remains a separate check. Screenshots/results go to ignored `test-results/`.

Checks cover the player-controlled chapter-dialogue handoff, vertical selection checklist, absence of duplicate evaluation checklists, continuous gap pulse, the 20 trios, complete expansion flow, both levels' handoff, outcome text, timing, selection limits, sound, keyboard controls, restart, fresh-page lifetime and responsive layouts. They are browser functional checks, not a classroom concurrency/load test.

The preview refresh checks and hashes are recorded in
[PREVIEW_VALIDATION.json](docs/PREVIEW_VALIDATION.json). The combined and Level 2 production HTML remain byte-identical to the accepted v6 builds, whose broader gameplay checks are recorded in
[LEVEL2_VALIDATION-v6.json](docs/LEVEL2_VALIDATION-v6.json). Earlier previews and
their validation records are preserved. The highlighted narrative ownership
check is in [LEVEL2_NARRATIVE_AUDIT.md](docs/LEVEL2_NARRATIVE_AUDIT.md).
