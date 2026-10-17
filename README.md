# Gaming the System

One English-language game project, organised by level. Level 1 is implemented; Level 2 has a reserved source folder. The supplied cinematic opening has **not** been merged or modified. Its office and classroom backgrounds are reused as visual references/assets from the supplied project.

**Just want to play? [Download the playable ZIP (v7)](play/Level1-play-v7.zip?raw=true), extract it, and open `Level1.html` in Chrome or Edge. No developer tools are needed. Sign in to a GitHub account with access to this repository before downloading.**

## Play without installing anything

Open `dist/index.html` in a current desktop browser. The production file contains its own JavaScript, styles, and images, and needs no server or Internet connection. The separately delivered `Gaming-the-System-Level1.html` is the same file with a descriptive name.

Select one of six metrics, write a prediction of up to 100 characters, run the evaluation, observe the selected story placeholder, then compare the result with the prediction. Level 1 ends on that observation page. After the final reply’s reading interval, a disabled Continue to Level 2 button appears there and all four progress steps are marked done. No click is required to finish Level 1, and the current build stays on this page. Replay scene and the header Restart remain available.

Version 7 replaces the final completion label with **Continue to Level 2 →**, reserved as a disabled button until the next level is ready.

The prediction page removes the duplicate Back to metrics control: use Change beside the selected metric. The Run evaluation button stays on the right. The former next-level screen is reserved separately in `src/levels/level2/LevelTwoEntryPlaceholder.tsx` and is not mounted or included in this playable flow.

The post-scene page stays simple. The prediction is a quiet reference line. A single classroom observation paragraph (the former details text) appears automatically together with the Students summary, sharing one sound cue. There is no duplicate headline, details toggle, student badge or separate student animation. Management’s view retains its existing score without renewed emphasis.

The classroom observation has 6–8 seconds of visible reading time, based on its English length, before conversation begins. Maya appears above-left, then Alex below-right within the main content column. Each message starts with 650 ms of typing dots and gets 3–5 seconds of visible reading time. The reserved next-level button appears only after the last reply’s reading interval. All revealed information stays available. Hidden tabs, off-screen text, Guide and restart dialogs hold the pending beat; sequences resume automatically when visible again. There are no pause or reveal buttons.

The score's Target 70 label sits directly below the 70-point marker at every screen size. The finding fades in once; the student card changes quietly as its summary. The evaluation’s management highlight ends after 1.6 visible seconds. Reduced-motion preferences remove movement while retaining the reading intervals and sequence.

Web Audio tones mark the rising score, target achievement, the combined classroom finding/student update, and arriving replies. Data cues remain more audible than v2, with reply pips softer. The header’s **Sound on / Sound off** control changes sound only for the current run; a new run starts with sound on. Audio starts after a user gesture. Unsupported audio falls back to visual feedback.

A short, skippable four-step guide appears at the start of every run. Use **Guide** to reopen it. It highlights decisions, the reported score, student response and conversation without revealing the lesson’s conclusion.

Scores are illustrative 0–100 indices. Each metric has a stable before/after pair and an illustrative target of 70. Predictions are never graded or sent to a service. Moodle references are fictional game content; no Moodle or AI connection is required.

Game state lives only in the current page’s React memory. No game progress, guide marker, or sound preference is written to localStorage, sessionStorage or cookies. Old saved data is ignored. Refreshing, closing and reopening, opening another tab, or returning through the browser back-forward cache starts a new run with no selected metric or prediction. Restart also starts a fresh run and shows the guide again. Moving between the workbench and its cinematic within the open page preserves the current run.

The integrated full game must use the same lifetime rule: initialise the opening and player identity on a new page, and keep data only while that page is open. Mount the Level 1 component once during its workbench/cinematic sequence; pass the current player name and completion callback in memory.

## Develop

Use Node.js 20.19+, 22.12+, or a newer compatible version (validated here on Node.js 24).

```sh
cd /workspace/gamingthesystem_game
npm ci
npm run dev
```

Use the address printed by Vite. For a production build:

```sh
npm run build
```

The build checks TypeScript and creates a self-contained `dist/index.html`. `vite-plugin-singlefile` embeds the assets so this first prototype can be shared as one HTML file. No external fonts, runtime network calls, or secret variables are needed.

## Source layout

```text
src/
  main.tsx                 Browser bootstrap; loads shared base styles
  App.tsx                  Game entry; currently opens Level 1
  levels/
    level1/
      LevelOne.tsx         Implemented Level 1 flow
      metrics.ts           Choices, scores and narrative observations
      state.ts             Level 1 in-memory state
      components/          Level 1 dialogue, guide and cinematic placeholder
      styles.css           Scoped Level 1 layouts
    level2/
      LevelTwoEntryPlaceholder.tsx
      styles.css           Reserved Level 2 entry styles
      README.md            Development boundary for the next level
  shared/
    components/            Common icons, independent of level data
    hooks/                 Audio and visible-time delays
    utils/                 Reading-time calculation
    styles/base.css        Design tokens, resets and common controls
  assets/                  Office and classroom artwork
```

Open [Level 1](src/levels/level1/), [Level 2](src/levels/level2/), or
[shared code](src/shared/) to work on that area. Each has a short README.

Keep each level's rules, text and state in its own folder. Shared modules do not
import level internals. `App.tsx` owns the application entry and is where future
level navigation will be connected. Level 2 is not mounted yet, and the next-level
button remains reserved. The cinematic opening has not been merged.

`main.tsx` imports the shared base stylesheet once before App. Each level imports
its own stylesheet. Level 1 selectors are scoped to `.level-one`, and the reserved
Level 2 entry selectors to `.level-two-entry`, so level layouts can evolve separately.

[LEVEL1_HANDOFF.md](docs/LEVEL1_HANDOFF.md) documents scene integration and result
callbacks. Existing playable ZIPs in `play/` remain saved previews; the current
source still builds into one self-contained HTML file with `npm run build`.

## Validate

With the Vite development server running and Python Playwright available:

```sh
python tests/smoke.py
python tests/smoke.py --file dist/index.html
python tests/feedback.py
python tests/feedback.py --file dist/index.html
python tests/guide.py --file dist/index.html
```

Pass `--chromium /path/to/chromium` if needed. Test results and screenshots are written to ignored `test-results/`.

The `--file` check runs the exact built HTML with networking disabled through an in-memory test origin, because this cloud machine's managed Chromium blocks `file://` navigation. It validates the single-file artifact and embedded assets offline; opening a downloaded file in a specific user's browser remains a separate check.

Checks cover all six branches, matching story content and scores, prediction validation, fresh-page and tab lifecycle behaviour, keyboard interactions, restart confirmation, reduced motion, unavailable storage and desktop/touch layouts. This is browser functional validation, not a classroom concurrency or network-capacity test.

## Current scope

The reported score and the student's qualitative evidence remain visible together after observation. Student learning is not represented by an invented declining numerical score. Purple author/narration notes are absent from the player interface; an amber observation card provides the intended point of tension after the story.

All six cinematics are explicitly marked placeholders. The future Level 2 entry is retained only as source for later integration; it is absent from the current player flow. The story placeholder uses text from Narrative V2 with an existing classroom background. It does not claim to be a finished character animation or video. Interface feedback tones are generated locally; voice acting and cinematic audio remain outside this prototype.
