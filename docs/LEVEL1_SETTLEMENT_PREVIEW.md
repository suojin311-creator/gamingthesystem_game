# Independent Level 1 result-settlement preview

The user's requested experiment lives on `preview/level1-settlement`, based on
`32a91fe4bfb1cb193040410c846ebc165f8b9d5d`. The opening integration and stable game
branches and all their existing playable ZIPs remain unchanged. This review is
not a replacement for the approved complete game.

## Preview flow

Choose one of the existing six metrics → write a prediction → Run evaluation →
play that metric's complete authored animation → show the results settlement.
The full animation includes both the common ending and Something Feels Wrong.
It finishes before the settlement appears. There is no separate pre-animation
score dashboard in this preview.

The settlement records the selected metric, its existing illustrative before and
after scores and target, and the matching qualitative classroom consequence.
Measured results and classroom results sit beside each other. Predictions remain
available in a collapsed reference; they are not graded. There is no new learning
percentage or claim that a score measures real learning. The former review chat,
long evidence panel and duplicate sidebars do not appear. Replay keeps the actual
choice and prediction; Try another metric starts a fresh Level 1 run. The preview
stops at Level 1 and provides these review controls instead of navigating onward.

`LevelOne` has one optional `renderSettlement` seam. Without it the existing
selection → prediction → score result → observe → review-chat path stays intact.
With it, the actual cinematic completion callback opens the settlement and reports
the existing result once. Replay does not report the result again. The shared
component and rules are reused; there is no copied gameplay implementation.

## Animation and pacing

The original partner source is pinned at
`Mg614/gaming-the-system@1bdd0c442c4b345b3bd37d6f541742d4e55c732f`
(`feature/cinematic-level1-consequences`). No upstream writes are made. The
94 files from the downloaded archive retain their exact bytes.

The external cinematic build imports the original composition and artwork into
an isolated iframe. Its styles do not leak into the workbench. A build-only clock prop supplies a monotonic source frame directly to the
authored composition (without Remotion Freeze clamping the longer source clock).
The mapping preserves the entire original branch/common/office sequence, while
shortening empty shots and transitions. Speech holds depend on each English
line's length (roughly 220 words/minute plus a settling margin). The target
result has 0.2 seconds of fade-in followed by 2.4 seconds fully visible. Thought
fades are shortened to keep their words clear. The six authored playback timelines now
span about 25.4–26.6 seconds instead of 33.4 seconds; no global playback multiplier
is used. Predictions are kept on the settlement rather than competing with the
animation's thought captions. Player controls allow pause and scrubbing.

The parent validates the iframe source and the current run token. Only the real
player `ended` event and its closing fade complete the scene. Hidden-page playback
pauses; returning leaves the player paused for the viewer to resume. Reduced
motion uses the original composition's motion option and retains reading holds.
No new music or voice recording is added to this review.

## Build and check

Keep the partner checkout outside the game repository. Install its exact lockfile
with `npm ci --ignore-scripts --cache /tmp/gaming-level1-preview-npm-cache`, then run
its typecheck. Set `LEVEL1_ANIMATION_SOURCE` to that checkout's absolute path.

```sh
npm run check
node "$LEVEL1_ANIMATION_SOURCE/node_modules/vite/bin/vite.js" build --config scripts/level1-settlement/cinematic.config.mjs --outDir /tmp/level1-film-review
LEVEL1_CINEMATIC_HTML=/tmp/level1-film-review/index.html node node_modules/vite/bin/vite.js build --config scripts/level1-settlement/game.config.mjs --outDir /tmp/level1-settlement-review
python3 scripts/level1-settlement/package.py /tmp/level1-settlement-review/index.html
node tests/level1_settlement_pacing.mjs
python3 tests/level1_settlement_preview.py
```

The separate ZIP contains `START-HERE.html`, `Level1-settlement.html` and
`Current-Level1.html`. The latter is byte-identical to the previously published
standalone Level 1. Review hashes and browser verification belong in
`play/LEVEL1_SETTLEMENT_PREVIEW.json`, not the approved game's release report.
