# Gaming the System — Level 1

A standalone, English-language Level 1 workbench. The supplied cinematic opening has **not** been merged or modified. Its office and classroom backgrounds are reused as visual references/assets from the supplied project.

**Just want to play? [Download the playable ZIP (v3)](play/Level1-play-v3.zip?raw=true), extract it, and open `Level1.html` in Chrome or Edge. No developer tools are needed. Sign in to a GitHub account with access to this repository before downloading.**

## Play without installing anything

Open `dist/index.html` in a current desktop browser. The production file contains its own JavaScript, styles, and images, and needs no server or Internet connection. The separately delivered `Gaming-the-System-Level1.html` is the same file with a descriptive name.

Select one of six metrics, write a prediction of up to 100 characters, run the evaluation, observe the selected story placeholder, then compare the result with the prediction. `Try more metrics` finishes Level 1 at a Level 2 handoff placeholder. Level 2 is not implemented.

Version 3 introduces a short, skippable four-step guide on the first visit to the decision board. Use **Guide** to reopen it. The guide highlights decisions, university score, student response and conversation, without revealing the lesson's conclusion. It pauses the underlying presentation.

The evaluation and post-scene recap now advance automatically. After the score rises, the university card updates. After the cinematic ends, the original prediction returns, the classroom finding appears, the student card updates, and Maya/Alex reply in order. No extra reveal buttons are required. Each update has an entrance animation and a distinct cue, remains on screen, and waits if its information is off screen or the tab is hidden. On small screens the presentation brings the next region into view. **Pause / Resume** controls the sequence; opening More context pauses it for reading. Players still choose the metric, write the prediction, run the evaluation, enter the classroom and choose when to proceed to Level 2.

The score's Target 70 label sits directly below the 70-point marker at every screen size. Card entrances, selection confirmation, the growing result bar, revealed observations and the student signal use restrained animations. Reduced-motion preferences remove movement while retaining the order.

More audible Web Audio tones mark the rising score, university success, observation, student update and arriving replies. Data cues use a higher output level than v2, with reply pips kept softer. The header’s **Sound on / Sound off** control remembers the preference. Audio starts after a user gesture; a refreshed page waits for another gesture. Unsupported audio falls back to the visual feedback. Reduced-motion mode preserves the order with static dots and immediate score changes.

Scores are illustrative 0–100 indices. Each metric has a stable before/after pair and an illustrative target of 70. Predictions are never graded or sent to a service. Moodle references are fictional game content; no Moodle or AI connection is required.

Progress is saved locally in this browser when storage is available. Shared computers share this local save. Use **Restart** before another player/group begins. Different computers do not share or synchronise progress. Browsers may handle local-file storage differently; a hosted HTTPS version is preferred for classroom distribution.

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
- `src/components/WorkbenchGuide.tsx`: first-visit, replayable guide with actual-region spotlights.
- `src/useVisibleDelay.ts`: pausable, visible-time presentation beats.
- `src/useFeedback.ts`: self-contained, gesture-unlocked sound cues and mute preference.
- `src/state.ts`: versioned, validated local saves with an in-memory fallback.
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

Checks cover all six branches, matching story content and scores, prediction validation, persistence and recovery, keyboard interactions, restart confirmation, reduced motion, unavailable storage and desktop/touch layouts. This is browser functional validation, not a classroom concurrency or network-capacity test.

## Current scope

The university score and the student's qualitative evidence remain visible together after observation. Student learning is not represented by an invented declining numerical score. Purple author/narration notes are absent from the player interface; an amber observation card provides the intended point of tension after the story.

All six cinematics and the Level 2 entry are explicitly marked placeholders. The story placeholder uses text from Narrative V2 with an existing classroom background. It does not claim to be a finished character animation or video. Interface feedback tones are generated locally; voice acting and cinematic audio remain outside this prototype.
