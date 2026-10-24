# Approved chapter handoff, wording and floating Sound removal

- User approved the metric wording preview and requested formal sync plus ZIP.
  Integrate all three pending items: Which metric would tell me the most?;
  0.7-second Level 1 chapter/workbench overlap dissolve with the guide opening
  after 1.05 seconds; remove floating AudioControls on every game page.
- Keep existing header sound toggles, effects-only audio, actual selected metric,
  player name, ending copy and Padlet handoff. Preserve historical Lab package.
- FullGame passes initialGuideDelay only to the first Level 1 workbench; standalone
  entries keep original guide behavior. Guide must not reopen after manual close.
- Refresh the six regular ZIPs and embedded game-server archive together; deliver
  Full-game-play.zip after relevant real handoff, continuation and audio checks.
- These approvals supersede the pending-review restrictions below.

# Approved Level 1 chapter dialogue wording

- User requested sign → metric in the Level 1 chapter teacher bubble only:
  Which metric would tell me the most? Keep original position, type and colors.
- Preview under scripts/level1-dialogue-review/ uses actual ChapterTransition with
  a build-time string substitution. Sample teacher name fei; formal name still
  follows opening input. Screenshot play/Level1-metric-dialogue-preview.png.
- User approved the wording, transition and button removal for formal game sync
  and requested the complete playable ZIP; pending restrictions are superseded.

# Approved Sound button removal and Level 1 handoff

- User requested removal of the floating bottom-right Sound button on every page.
  This refers to the floating AudioControls, not the existing header sound toggle.
- User then deferred ZIP delivery and prioritized a video preview of the Level 1
  chapter → workbench handoff. No formal build or ZIP changed for this review.
- scripts/level1-handoff-review/ uses actual ChapterTransition and Gameplay, keeps
  the two-visible-second chapter hold, overlaps both pages for 0.7 seconds, then
  opens the first-use guide at 1.05 seconds after entry with a soft guide fade.
- Guide delay now uses the production initialGuideDelay prop. It preserves automatic-guide focus,
  real metric selection, player name and guide skipping. Film payloads excluded
  only because this review ends at selection. Not for production packaging.
- Review: play/Level1-handoff-preview.mp4, PNG and LEVEL1_HANDOFF_REVIEW.json.
  All three items are now approved for formal integration and ZIP delivery.

# Current combined release

- User approved the latest Level 1 icon result animation plus earlier opening and
  ending copy previews for formal integration. Preserve actual chosen metric and
  opening player name. Deliver a full-game playable ZIP, with the existing Padlet
  handoff and external-tab fallback. Keep effects only, with no background music.
- Opening subtitle: When you set the metrics, what are you measuring?
- Ending adds the two approved sentences, ceases tense, coral becomes/gold ceases,
  equal-size gold/coral assessment lines, and 37.2-second timeline before Padlet.
- Earlier pending-copy restrictions are superseded by this explicit approval.

# Current audio: effects only

- User requested removal of all current game music. No replacement music is
  selected or authorized. Director no longer imports, bundles or decodes tracks;
  scene calls are compatibility no-ops and saved music settings cannot restore it.
- Keep existing interaction sound effects and their mute/volume controls.
  Remove the nonfunctional music slider and music audition controls.
- Refresh formal game archives and embedded game-server package. Preserve all
  pending visual/copy reviews and historical standalone Lab packages. Padlet stays
  untouched. Do not reintroduce music to satisfy superseded audio tests.

# Approved Level 1 icon-based results

- Latest user request replaces the student percentage chart with one Level 2-style
  metric icon/card. Keep only the Management’s view progressbar. No student
  percentages or numeric improvement report. User approved integration into the
  formal game; selected card/icon and cinematic must follow the actual player choice.
- scripts/level1-icon-review/ reuses actual PerspectivePanel/ManagementSatisfaction.
  Six cards now use the shared metric-selection CSS/markup: original icon backing,
  card radius/shadow, bold name and top-right selection check. Remove the custom
  Selected text and bare icons. Only a slight enlargement on movement; completion
  adopts Level 2 green result palette. Example: Participation → Target met.
- Current animation starts with all six metrics in a 3×2 grid. The already
  selected card moves smoothly into the center and enlarges; the other five fade
  without receiving ticks. Then Target met, actual management fill, enabled
  Observe the class. Remove the But question entirely. Replaces Look behind the
  number because this proposal no longer shows student numbers.
- No bottom teacher dialogue. Formal audio remains effects-only; video is silent.
- Review: play/Level1-icon-results-preview.mp4 and PNG; timing/layout checks in
  play/LEVEL1_ICON_RESULTS_REVIEW.json. Preserve the earlier numeric proposal as
  historical; do not promote it instead of this current visual review.

# Historical numeric Level 1 assessment preview (superseded proposal)

- Isolated preview under scripts/level1-assessment-review/. Production source and
  formal packages unchanged. Video play/Level1-assessment-preview.mp4; still PNG
  and validation reports share this basename.
- Remove the Percentage of students meeting the criteria heading and all metric
  name overlays in this result chart. Retain actual before/after numeric data.
- User chose the longer caption: More students met the target for this metric.
  Avoid claims that learning or performance improved. Caption follows number
  growth; management then updates; Management is satisfied. fades in beside its
  panel after the fill completes; But… what changed in the classroom? follows;
  Look behind the number enables 0.5 seconds later. Text areas reserve space.
- Whole main copy uses 28px semibold dark ink; But… is 44px bold brick red.
  Remove the bottom teacher dialogue for this result-page review only.
- Uses actual ResultChart, PerspectivePanel and ManagementSatisfaction via a
  review-only Vite transform. Wait for approval before formal integration.

# Approved Level 1 result copy and teacher strip

- User requested a preview image only: all Level 1 settlement student headlines
  read "Alex focused on only one metric." A teacher-only bubble below reads
  "What if I measured more than one metric?" Retain existing card visuals.
- Source uses an optional PerspectivePanel behaviour override for the settlement;
  do not alter metric-specific cinematic scripts or other observation content.
- Corrected preview: teacher bubble belongs in the separate full-width,
  shaded dialogue strip BELOW the action row, matching the prediction screen. Preserve Your prediction and its original collapsed details;
  preview must use a nonempty prediction so this control is visible.
- Preview: play/Level1-result-copy-preview.png; reproduction under
  scripts/level1-result-copy-review/. TypeScript and actual rendered text checked.
- User approved the corrected preview for the formal game. Refresh regular game
  archives and the game-server package; preserve opening player-name propagation.
  No ZIP delivery requested.

# Approved Level 2 observation copy

- User approved five Students/But they paragraphs and requested a still preview.
  Only the five evidence strings in src/levels/level2/data.ts change; preserve
  renderer, CSS, effects and layout.
- Review sheet: play/Level2-observation-copy-preview.png, generated with the real
  ObservationContent and original CSS via scripts/observation-copy-review/.
  User approved the preview for the formal game. Refresh game/classroom builds
  with these five strings; no ZIP download needs to be sent to the user.

# Current Padlet Design Lab

- User replaced the local Design Lab with Padlet and supplied the live embed:
  https://padlet.com/embed/s024sqd75q7kuy5xciyy . The actual ending button now
  opens a full-viewport board inside the game, without a local API dependency.
- Keep the external-tab fallback, preserve the iframe source/run-token validation,
  and permit the Padlet frame in the local game server CSP. Do not post test data,
  vote, comment or change external board permissions without explicit instruction.
- New full-game HTML requires Internet for Padlet. The optional classroom launcher
  opens /game and prints /game links; its old host controls are not the new flow.
  Standalone Design-Lab-local.zip stays historical; do not delete it or rebuild it.
- Pending opening/ending text previews remain unapproved. Refresh regular game
  archives and the optional game-server archive when releasing this integration.
  Target actual ending handoff with tests/padlet_handoff.py; it only reads the board.
  Direct file:// browser navigation is blocked by this execution environment,
  so validate the standalone HTML via a static server and state that limitation.

# Current chapter entrance review

- User requested the shared entrance change for all three levels: finish the
  entry animation, hold two visible seconds, then enter the operation interface
  automatically, without the chapter action button. Teacher dialogue must not
  directly address Alex by name; student identity labels and report narration stay.
- These shared source and caption-adapter changes are authorized. The pending
  opening/ending copy review below remains isolated and unapproved.
- User approved this change for the formal game. Refresh all six regular game
  archives plus the combined classroom package; run actual archive/continuation
  and non-loopback LAN checks. Preserve the standalone Lab and stable aliases.
- The focused preview uses the actual shared chapter and workbench components;
  film payloads are excluded because this review ends at metric selection.
  Level 1/2 film adapters also normalize direct teacher address; their verified
  caches are refreshed from the pinned source for the next full build.

# Approved opening/ending copy integration

- User requested independent previews before approval. Use `scripts/copy-review/`;
  read its README for exact copy. Preserve all production source, film caches and
  game/classroom ZIPs. Deliver the opening PNG and ending MP4 for this review.

# Current integrated audio and classroom review

- Classroom LAN compatibility: HTTP addresses other than localhost do not expose
  `crypto.randomUUID`. All four film adapters use `cinematicRunId()` with
  `crypto.getRandomValues`, while preserving iframe-source/run-token validation.
  The user's two-client blank-screen report supersedes the reuse-only note below:
  refresh the six game ZIPs and integrated classroom ZIP for this fix. Do not
  rebuild the unaffected standalone Lab. Run `tests/classroom_lan.py --base-url`
  against an actual non-loopback HTTP address; localhost does not cover this bug.

- Three requested deliverables are documented in `play/DELIVERY_GUIDE.zh-CN.md`.
  The game and combined classroom ZIPs at d5d26fb are already built, verified and
  pushed. Reuse them. Build the current independent Lab with
  `DESIGN_LAB_GO=/workspace/.cache/gts-go/go/bin/go python3 design-lab/package.py --standalone`.
  This uses an ignored build staging directory, shares `/` directly, and preserves
  the integrated `design-lab/web/` and all six game archives. Do not change stable
  aliases or repackage the entire game just to deliver these files.

- User authorized GitHub backup, the approved reflection emphasis, all agreed
  music/feedback, and a review ZIP. Baseline: archive/full-game-before-audio-20261020.
- Work on animation/opening-integration. Preserve stable aliases and independent
  Lab/ending branches. The prior standalone-only restrictions are superseded for
  this merge. Current design is docs/AUDIO_DESIGN.md.
- Level films share music; don't add per-shot effects. Existing timings and
  dialogue stay unchanged. All output goes through src/audio/director.ts.
- Serve the current game at /game and Lab at / in the local classroom executable.
  Package regular HTML archives together, then build Lab, embed gzip game, verify
  Linux service/browser and cross-build play/Gaming-the-System-classroom.zip.
- Never claim native Windows execution on Linux. No hosting/trials required.

# Working on this game

## Current approved 100-metric integration

- The user requested a fresh edit from the pinned original Level 2 delivery,
  not another patch to the integrated 100-metric edit. Work is isolated under
  `scripts/metric100-preview/`. That preview is now approved for the game: the
  default checklist scene directly reuses its `createHundredPacing` timeline.
  This sync updates source/build only; do not regenerate or send ZIPs unless asked.
- Start on the original Criterion 66 pen insert. Keep the complete authored paper,
  Coverage map, evidence slips/references, criterion labels and footer.
- Remove the chapter, stage/title and candidate-credit overlays throughout.
- After the paper finishes, enter the conversation immediately; its first caption
  starts one second after that scene enters, with no additional transition pause.
  End on the final authored dialogue, omitting all priority/extra ending scenes.
- You is warm gold, Alex is light blue; identity centred directly above the
  transparent caption. Preserve authored lines and the standard reading intervals.
- Approved review: `play/Level2-100metrics-preview.zip`; original source remains
  read-only at `c8c1c83456c4e67cf627df399bfb67b3a9792adb`.
  See `docs/METRIC100_ANIMATION_PREVIEW.md` for build and targeted checks.

## Current ending preview

- The user approved an office reflection opening, three short memories and a
  plain-language closing. Remove the repeated You/Alex question and the three-window
  convergence montage. See `docs/ENDING_ANIMATION_PREVIEW.md`.
- The Level 3 comparison action reads "Step back and reflect" with the arrow
  icon, shared by standalone Level 3 and the complete game.
- The user approved this ending for the game. The default comparison entry now
  plays the full-screen film and holds its accepted Design Lab entry page, replacing
  the comparison/theory placeholders. Custom partner renderers retain their contract.
  Refresh all six game ZIPs together for this integration. The independent ending
  review ZIP remains a historical approved artifact.
- Entry fills the browser viewport, preserving the full composition. You is warm
  gold; Alex is light blue; labels are centred immediately above transparent captions.
- Ending never displays the top-left metric heading, including in Level 3 memory.
  Keep that heading in the separate Level 3A task film; do not change its renderer.
- The user rejected the standalone aphorism/short decorative rule as unclear.
  End with a Design Lab entry: destination, invitation to share what real
  learning looks like, and button. The user removed the two explanatory prose
  blocks (connection to Alex and reflection/read/vote steps).
  Use the office scene beside left-aligned copy; no decorative short rule.
  The handoff page fills the viewport with readable responsive type, while the
  earlier film keeps its complete 16:9 composition. Cover that aspect-ratio
  change with a full-viewport dissolve, including the outgoing matte. Title and
  button mount together and share one fade; never delay the action and recenter
  the text. The reflection question is centred without You, gently fades in,
  then fades away as the office darkens. The opening still uses the You label.
  Do not reveal the Goodhart name or quote here; the formal reveal belongs after
  Design Lab. Its accepted quote is the short "When a measure becomes a target…"
  version, not the 1975 wording. See `docs/ENDING_DESIGN_LAB_COPY.md`.
  Level 3 recap: "The weights changed. Learning still came second."
  Restore the earlier
  dark office; the user rejected the olive full-screen treatment. Use the opening
  office's Georgia/warm-white type and directly import its brick-red opening-action
  button style. No oversized uppercase title or glowing gold button.
  The user now authorized the game/Lab merge: embedded ending sends enter-lab to its validated parent, which opens the local classroom Lab; independent film previews stay display-only.
- Pinned ending delivery: `e467998dfb07abc028e4e0fcb5567006e4eaa07d`.
  Keep it read-only and reuse only the approved 3A task renderer, never 3B.
  Game film: `scripts/ending-film.mjs`, prepared with the pinned ending and 3A
  sources. The same runtime/composition serves preview and embedded modes; embedded
  mode receives actual history via a source-checked handshake and hides review controls.
  Keep `onDesignLab` reserved: the classroom service remains a separate local program.
  Independent review build remains `npm run package:ending-preview`.

## Animation review delivery

- The user reverted to ZIP delivery because the hosting setup requested a trial.
  Deliver updated animation/game ZIPs for review. Do not ask the user to enable
  Pages, start a trial or configure hosting. The web export is an unused snapshot.
- Target visual checks to the changed shots. Do not rerun full game paths for
  these animation tweaks: the user explicitly waived those checks.

## Current Level 3A integration

- Before this merge, the complete Level 2 integration and six game ZIPs were
  verified and saved at `archive/before-level3a-integration-20261020`, commit
  `2411baa78192d764d07a8d3952ebb5d4f02a878c`.
- Use only the partner's Level 3A metric-adaptations delivery at `ba9f81e`.
  Replace `level3.weights`; comparison and theory keep their existing placeholders.
  Do not import Level 3B or impose its conclusion/branching logic.
- Game `request.shots[].effort` chooses Low/Medium/High. Never classify from a
  percentage in film code. Keep actual metric order and use the game's current
  `weightedSceneReply` captions, including medium criteria/stopping behaviour.
- Omit numeric entry/exit sheets, the rejected standalone Alex portrait, peer-only
  opening crops, classmate reactions, empty establishing views and hand-only cuts.
  Keep useful task/criteria actions. Show the current full metric name top-left.
  Alex captions/label are blue; player/teacher labels are You and warm gold when
  present. Captions are transparent and use the shared Level 1 palette.
- Internal Level 1/2/3 joins now cross-dissolve a frozen outgoing frame into the
  decoded live scene via `scripts/cinematic-dissolve.mjs`; no internal black cover.
  Level 2 content is otherwise paused at the backed-up version.
- Build with `LEVEL3_ANIMATION_SOURCE` pointing to the pinned read-only delivery.
  Review ZIP: `play/Level3A-animation-preview.zip`. See `docs/LEVEL3A_ANIMATION.md`.
- The complete ZIP shares its full-game HTML across the standalone launchers to
  keep duplicated artwork below the GitHub file limit. Individual ZIPs retain
  their self-contained single-HTML format and existing entry behaviour.

## Current Level 2 animation integration

- The user requested direct integration after trimming/review. Before changes,
  source and all six game ZIPs were backed up and verified on
  `archive/before-level2-animation-integration-20261020` at `762ce7e`.
- Replace only the existing three-metric, six-metric and final checklist
  placeholders. The final placeholder starts on the Criterion 66 pen insert,
  then retains the full Coverage map and completion before entering reflection
  with a one-second subtitle lead-in. Omit the silent perfect/reaction hold.
  Omit the earlier establishing view and final priority page.
  The approved 100-metric edit ends on its last authored line without an extra
  reaction hold or final fade covering the subtitle.
  Ignore separate 10/25 clips and checking studies; the game owns growth and Level 3 entry.
- Visible/Quality/Mixed start at "I’ve completed all three requirements!".
  Films retain dialogue, Alex/You labels and authored checklist item/group text.
  Checklist text is an explicit exception to the overlay-text removal rule.
  The 100-metric paper must stay intact: working-notes/title/tally, evidence
  slips, E1/E2/E3 row references, gaps and footer all remain visible.
  Reuse the Level 1 palette,
  reading holds, transparent captions, fixed framing and soft scene dissolves.
- Final 100-metric reflection cuts must commit the new caption and portrait
  together during the dissolve; never reveal the new portrait with stale dialogue.
- Level 2 post-film pages have no teacher/Alex chat: existing observation above
  two equal perspective cards, with existing copy/actions and no added text.
  Students uses the Level 1 red outline: three 0.75-second pulses on observation,
  with a static outline for reduced motion.
- Cover the gaps goes directly to the six-card evaluation. The original three
  stay checked/locked; the player checks the remaining three. Observe enables
  only when all six are checked. No automatic six-metric ticks or separate
  gaps/Add remaining metrics page. Remove Illustrative outcomes from Level 2;
  do not add this label to other levels.
- See `docs/LEVEL2_ANIMATION_PREVIEW.md` for pins, build and boundaries. The
  review ZIP shows the exact adapted film; normal game delivery uses the full
  six-ZIP pipeline. Keep partner source read-only and push only this branch.

## Current opening + Level 1 integration

- The user approved merging the Level 1 preview into the opening + three-level
  version. Work and publish only on `animation/opening-integration`; preserve
  `preview/level1-settlement` at its approved saved version.
- Before merging, the original source and all original playable archives were
  backed up on `archive/opening-before-level1-merge-20261020` at `32a91fe`.
- Integrated ZIP releases use the regular four-entry/six-ZIP pipeline on this branch.
  Keep stable game branches and their aliases unchanged. Every visible playable
  change must include updated downloadable ZIPs for the user's review.
- Reuse the approved iframe cinematic through the shared LevelOneExperience.
  Keep partner source read-only, and carry the opening's confirmed playerName
  through Gameplay, the operating UI and cinematic request without re-entry.

## Saved independent Level 1 experiment

- The user asked to preview a new Level 1 results page without overwriting the
  existing version. That approved experiment is saved on
  `preview/level1-settlement`; its saved baseline is `32a91fe`.
- Follow `docs/LEVEL1_SETTLEMENT_PREVIEW.md` for this experiment. Its separate
  entry uses the shared LevelOne with an opt-in `renderSettlement` callback;
  defaults preserve the existing game. Partner source is read-only.
- When working on that independent experiment, build through `scripts/level1-settlement/` and package
  `play/Level1-settlement-preview.zip`. Do not run the normal six-ZIP publishing
  pipeline for this experiment: the user explicitly requested preserving them.
- The user reviews this preview through downloaded ZIPs. Visible UI changes must
  include an updated independent ZIP in the same delivery, rather than requiring
  a separate packaging request after source changes.
- The original rules below still govern the stable game and opening integration.


- The user requested separate animation development. Current opening integration
  work belongs on `animation/opening-integration` in this checkout. Keep the
  approved game branch `level3-dev` unchanged; do not create a worktree unless asked.
- Keep one implementation per level under `src/levels/`. All playable entries
  reuse these components. Existing gameplay and authored animation scripts are
  approved; integrate finished scenes through `Gameplay` renderer props.
- For animation work, start with `docs/ANIMATION_INTEGRATION.md` and
  `src/cinematics/README.md`. Read a level’s handoff only when that scene needs it.
  Use `docs/DEVELOPMENT_WORKFLOW.md` for current commands. Historical design
  reports are references, not instructions to restore superseded gameplay.

# Daily development

- Use `npm run dev` or `npm run dev:level1`, `dev:level2`, `dev:level3` for the
  affected entry. Use the running Vite server rather than rebuilding downloads
  for each visual/timing adjustment.
- Run `npm run check` for TypeScript changes and the relevant behaviour checks.
  Do not run every historical test suite or recheck unchanged allocation rules
  for an animation/style-only change. See the workflow’s check-selection table.
- Documentation-only changes need relevant link/content checks, not builds.
- Commit and push daily work to `level3-dev`. Do not routinely synchronize all
  preview branches, rebuild ZIPs or create numbered reports for minor edits.
- For the current animation task, commit/push only `animation/opening-integration`.
  Review packages on that branch include the integrated opening. Do not merge
  into `level3-dev` or update stable preview aliases until the user requests it.
- Keep a concrete baseline before a substantial gameplay change or animation
  merge; an already-pushed commit is a saved baseline. Extra archive tags are
  not required for every small change.

# Playable releases

- When a ZIP/review version is requested or a playable release is being made,
  run `npm run package:previews` once. It type-checks once, builds all four
  entries, then generates all six current archives together.
- Fixed latest entries: `play/Level1-play.zip`, `play/Level2-play.zip`,
  `play/Level3-play.zip`, `play/Full-game-play.zip`,
  `play/Level3-and-Full-game-play.zip`, `play/Gaming-the-System-complete.zip`.
  Never replace only part of a release. Keep numbered archives unchanged.
- Run `npm run test:release` against the actual ZIPs. Record current checks and
  hashes in `docs/PREVIEW_VALIDATION.json`; keep old versioned reports historical.
- Check remote changes, then fast-forward `level1-preview`, `level2-preview`
  and `level2-dev` to the same tested release as `level3-dev`. Never force-push.
  The repository’s current default branch is the `level1-preview` release alias;
  daily development may be ahead on `level3-dev` until the next release.
- The animation branch is a separate review line: build and check its ZIPs there,
  then push only that branch. Its artifacts do not replace the stable game release.
- Reuse a verified build/package until relevant source changes. Do not repeat
  broad testing after it passes unless a change or unresolved failure warrants it.
- Preserve history, tags and existing download links. Do not rewrite Git history
  or move historical binary archives as routine cleanup.
