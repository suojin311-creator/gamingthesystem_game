# Independent Level 1 result-settlement preview

The user's requested experiment lives on `preview/level1-settlement`, based on
`32a91fe4bfb1cb193040410c846ebc165f8b9d5d`. The opening integration and stable game
branches and all their existing playable ZIPs remain unchanged. This review is
not a replacement for the approved complete game.

## Preview flow

Choose one of the existing six metrics → write a prediction → Run evaluation →
watch the original before/after score animation and Target achieved report →
Observe the class → play that metric's complete authored animation → show the
results settlement. The full animation includes both the common ending and
Something Feels Wrong. It finishes before the settlement appears.

The original four steps stay Choose / Predict / Evaluate / Observe. Both the
animation and the final settlement belong to Observe; there is no Results step.
The animation occupies the former classroom placeholder, below the visible
workbench heading and stepper. Run evaluation stays on the right, as in the
original game.

The settlement reuses the original Level 1 PerspectivePanel: Management’s view,
Satisfaction, Satisfied, the satisfaction bar and Reported score / target met;
Students, its existing branch-specific behaviour and Learning at risk. The two
wide, equally weighted cards sit under the selected metric.
Original final values and copy remain. The recap opt-in replays the satisfaction
bar from its initial awaiting position to the same final value. The game value is
never incremented again. Students initially keeps its original waiting view.
The actual width-transition completion starts a 250ms visible pause, then reveals
the branch's student behaviour, risk and compact portrait/notebook illustration.
There are no unselected-metric icons; the small neutral check denotes completing
a checklist. Text and picture sit beside each other without changing card height.
The shared status component's default behaviour in other levels is unchanged.
Reduced motion completes the sequence without relying on a transitionend event.
The former large IN THE CLASSROOM evidence panel and review chat are absent.
The metric ribbon, coloured card borders, paired layout and compact student
illustration retain visual weight without adding a second explanation of the movie.
Predictions remain available in a collapsed, ungraded reference.

The replay button is removed. Try another metric starts a fresh Level 1 run.
The preview stops at Level 1 and provides that review control instead of
navigating onward.

`LevelOne` has one optional `renderSettlement` seam. Both modes preserve the
original selection → prediction → score result → observe path. Without the seam,
the legacy review chat follows the cinematic. With it, the actual cinematic
completion callback opens the settlement and reports the existing result once.
The existing completion guard remains. The shared component and rules are
reused; there is no copied gameplay implementation.

## Animation and pacing

The original partner source is pinned at
`Mg614/gaming-the-system@1bdd0c442c4b345b3bd37d6f541742d4e55c732f`
(`feature/cinematic-level1-consequences`). No upstream writes are made. The
94 files from the downloaded archive retain their exact bytes.

The external cinematic build imports the partner's original artwork, content
constants and ConsequenceScene prop animation into an isolated iframe. Styles do
not leak into the workbench. `presentation.jsx` assembles one fully opaque shot at
a time: branch → shared Alex line → office. A 320ms flat cover, including a fully
opaque middle, buffers each scene change. The previous line gets a brief stable
hold, and the next line starts after the new shot is clear. Photos never dissolve
through one another. A final cover hands off to the same-colour recap uncover.
Camera poses are fixed within each shot. A build-only adapter freezes ConsequenceScene's framing without changing
the partner checkout. The office retains its original laptop geometry, email,
selected result and three thought/bridge lines. There are no overlapping scene
dissolves, repeated zooms, Alex memory overlay or six-metric text montage.
Subtitle gradient/shade layers and the extra vignette are removed. Captions sit
directly on the original art, using the opening's light text-shadow style.

The monotonic presentation clock still covers the full authored script. Per-line
English reading holds remain (roughly 220 words/minute plus a settling margin),
including 2.4 seconds of clear target-result display. The removed memory gap is
shortened so it does not leave a lingering empty beat. The six timelines span
about 25.8–27.0 seconds instead of 33.4 seconds; no global playback multiplier is
used. The three required images are decoded before playback so cuts do not expose
an unloaded next shot. Predictions stay on the settlement, without competing
with the thought captions.

The player starts automatically and has no visible controls, timeline, timecode,
click-to-pause or spacebar playback shortcut. The actual ended event commits a
fully covered frame before handing off. The parent validates the iframe source and current run token; only the actual player `ended`
event completes the scene, once. Playback pauses when the page becomes hidden
and resumes on return, so removing controls cannot strand a hidden-tab pause.
Reduced motion retains readable holds and the same fixed framing. No new music
or voice recording is added.

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
standalone Level 1. Archive hashes and matching browser verification belong in
`play/LEVEL1_SETTLEMENT_PREVIEW.json`, not the approved game's release report.
