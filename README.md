# Gaming the System — Level 1

A standalone, English-language Level 1 workbench. The supplied cinematic opening has **not** been merged or modified. Its office and classroom backgrounds are reused as visual references/assets from the supplied project.

**Just want to play? [Download the playable ZIP (v5)](play/Level1-play-v5.zip?raw=true), extract it, and open `Level1.html` in Chrome or Edge. No developer tools are needed. Sign in to a GitHub account with access to this repository before downloading.**

## Play without installing anything

Open `dist/index.html` in a current desktop browser. The production file contains its own JavaScript, styles, and images, and needs no server or Internet connection. The separately delivered `Gaming-the-System-Level1.html` is the same file with a descriptive name.

Select one of six metrics, write a prediction of up to 100 characters, run the evaluation, observe the selected story placeholder, then compare the result with the prediction. `Try more metrics` finishes Level 1 at a Level 2 handoff placeholder. Level 2 is not implemented.

Version 5 simplifies the post-scene page. The prediction is a quiet reference line. A single classroom observation paragraph (the former details text) appears automatically together with the Students summary, sharing one sound cue. There is no duplicate headline, details toggle, student badge or separate student animation. Management’s view retains its existing score without renewed emphasis.

The classroom observation has 6–8 seconds of visible reading time, based on its English length, before conversation begins. Maya appears above-left, then Alex below-right within the main content column. Each message starts with 650 ms of typing dots and gets 3–5 seconds of visible reading time. The next-step button appears only after the last reply’s reading interval. All revealed information stays available. Hidden tabs, off-screen text, Guide and restart dialogs hold the pending beat; sequences resume automatically when visible again. There are no pause or reveal buttons.

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

## Files

- `src/LevelOne.tsx`: complete decision flow, dashboard, perspectives, dialogue, restart and completion.
- `src/metrics.ts`: six metrics, illustrative scores, behavioural evidence and temporary scene dialogue.
- `src/components/CinematicPlaceholder.tsx`: replaceable three-line interlude for each branch.
- `src/components/Dialogue.tsx`: visible-time chat sequence and typing indicators.
- `src/components/WorkbenchGuide.tsx`: new-run, replayable guide with actual-region spotlights.
- `src/useVisibleDelay.ts`: pausable, visible-time presentation beats.
- `src/readingTime.ts`: text-length-based reading intervals for observations and replies.
- `src/useFeedback.ts`: self-contained, gesture-unlocked sound cues and mute preference.
- `src/state.ts`: in-memory run types and initial state; no save/load API.
- `src/styles.css`: warm paper/office styling, responsive layouts and reduced-motion support.
- `docs/LEVEL1_HANDOFF.md`: scene contract and responsibilities for later integration.
- `tests/smoke.py`: actual Chromium browser checks; requires Python Playwright and Chromium.

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

All six cinematics and the Level 2 entry are explicitly marked placeholders. The story placeholder uses text from Narrative V2 with an existing classroom background. It does not claim to be a finished character animation or video. Interface feedback tones are generated locally; voice acting and cinematic audio remain outside this prototype.
