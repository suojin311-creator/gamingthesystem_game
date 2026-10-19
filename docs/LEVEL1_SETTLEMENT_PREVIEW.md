# Independent Level 1 result-settlement preview

The user's requested experiment lives on `preview/level1-settlement`, based on
`32a91fe4bfb1cb193040410c846ebc165f8b9d5d`. The opening integration and stable game
branches and all their existing playable ZIPs remain unchanged. This review is
not a replacement for the approved complete game.

## Preview flow

Choose the metric that will count towards students’ marks → read its assessment
criteria and predict students’ response → View assessment results → watch the
before/after class percentages → Look behind the result → play the selected
consequence, office email and teacher thoughts → show the results settlement.
The shared Common Ending / Alex line is omitted, as requested.

The numbers represent the illustrative percentage of students meeting the chosen
metric’s assessment criteria, not individual grades or a measured learning score.
They remain the same fixed story values for each branch. The prediction page
shows a criterion for each of the six metrics, matching the retained scene:

| Metric | Assessment criteria |
| --- | --- |
| Preparation | Complete the preparation checklist. |
| Participation | Make at least one contribution in class. |
| Focus | Be recorded as on task during classroom checks. |
| Discussion | Ask a follow-up question and build on a classmate’s point. |
| Reflection | Use the reflection format: describe your thinking before and after. |
| Peer response | Include a specific suggestion and a follow-up question in your response. |

The report's two columns are **First assessment** (the recorded baseline) and
**Second assessment** (after the metric counts towards students’ marks), making
the numbering explicit without a new page. There is no extra assessment-period
eyebrow or marks explanation above the report. The prediction question stays
screen-reader-only; its visible criteria and existing page heading remain.
The report label is **Percentage of students meeting the criteria**; values and scale endpoints
carry percentages. The numerical target, threshold marker and target-met
heading are absent. The original increasing bars and button alignment remain.
The report and the classroom show the same assessment period; the classroom
reveals how students attained the reported result.

The original four steps stay Choose / Predict / Evaluate / Observe. Both the
animation and the final settlement belong to Observe; there is no Results step.
The animation occupies the former classroom placeholder, below the visible
workbench heading and stepper. View assessment results stays on the right, as in the
original game.

The settlement reuses the original Level 1 PerspectivePanel: Management’s view,
Satisfaction, Satisfied and the satisfaction bar; Students, its existing
branch-specific behaviour and Learning at risk. Management’s view has no bottom
evidence text in this preview, including its choose, predict and report pages. The two
wide, equally weighted cards sit under the selected metric.
Original final values and copy remain. Management’s view is static at its final
report value, without a second bar rise or attention animation. Students keeps
its waiting view during the brief recap uncover and a 250ms visible pause, then
reveals the branch's behaviour, risk and compact portrait/notebook illustration.
Only the Students border pulses, three slow amber/rust pulses over 2.25 seconds,
to emphasize the negative outcome. Reduced motion uses a steady outline instead.
There are no unselected-metric icons; the small neutral check denotes completing
a checklist. Text and picture sit beside each other without changing card height.
The shared status component's default behaviour in other levels is unchanged.
The redundant “What changed?” heading is removed; the selected metric leads the
page and the region retains an accessible name and focus target.
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
The existing completion guard remains. The optional settlement path enables
the assessment-report wording and percentages; legacy callers keep their original
copy and target display. Shared components and values are reused; there is no
copied gameplay implementation. The existing completion payload is unchanged.

## Animation and pacing

The original partner source is pinned at
`Mg614/gaming-the-system@1bdd0c442c4b345b3bd37d6f541742d4e55c732f`
(`feature/cinematic-level1-consequences`). No upstream writes are made. The
94 files from the downloaded archive retain their exact bytes.

The external cinematic build imports the partner's original artwork, content
constants and ConsequenceScene prop animation into an isolated iframe. Styles do
not leak into the workbench. `presentation.jsx` assembles one fully opaque shot at
a time: selected branch → office email. The last branch line gets its normal
reading hold and a short settling beat. An eased flat cover (about 640ms) buffers the scene change. The office
mounts only after the cover’s real transitionend, followed by two painted frames
before uncovering; dropped composition frames cannot bypass the protected swap. The email is already complete when the
cover lifts; its sender, greeting, body and signature appear together. The green
Selected metric / TARGET ACHIEVED block is removed. Photos never dissolve through
one another. A final cover hands off to the same-colour recap uncover.
Camera poses are fixed within each shot. A build-only adapter freezes
ConsequenceScene's framing without changing the partner checkout. The office
retains its original laptop geometry and three thought/bridge lines. The first
thought is singular: “The number looks great... but something still feels wrong.”
There are no overlapping scene dissolves, repeated zooms, Alex memory overlay or
six-metric text montage. Subtitle gradient/shade layers and the extra vignette
are removed. Teacher dialogue and thoughts use warm gold; Alex uses pale blue.
Speaker labels match their captions, with a dark text outline and small shadow
for readability on the artwork, without a subtitle background layer.

The presentation clock skips the removed common ending and office approach,
retaining source timings for the selected branch and office thoughts. Per-line
English reading holds remain (roughly 220 words/minute plus a settling margin).
The teacher's first thought appears two seconds after the email uncover actually
finishes, using the visible playback clock so hidden tabs do not consume the wait.
The remaining dialogue holds stay unchanged; the bridge reads “What if I measured
more than one?” The six timelines span about 20.1–21.3 seconds; no global
playback multiplier is used. Both required images are decoded before playback
so the transition does not expose an unloaded shot. Predictions stay on the
settlement, without competing with the thought captions.

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
