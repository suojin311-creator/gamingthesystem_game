# Working on this game

## Current ending preview

- The user approved a universal opening with no assumed near-even trial; use the
  three lines and real last-trial shots in `docs/ENDING_ANIMATION_PREVIEW.md`.
- This is an independent animation preview, not yet a replacement for the game
  theory/comparison placeholders. Keep the six current game ZIPs unchanged.
- Entry fills the browser viewport, preserving the full composition. You is warm
  gold; Alex is light blue; labels are centred immediately above transparent captions.
- Stop at the enlarged two-line Goodhart quote, split after the comma. Remove
  later recap/handoff scenes. The user's latest request adds a prominent gold
  Design Lab button here; it is display-only and must not launch Design Lab yet.
- Pinned ending delivery: `e467998dfb07abc028e4e0fcb5567006e4eaa07d`.
  Keep it read-only and reuse only the approved 3A task renderer, never 3B.
  Build with `npm run package:ending-preview`; deliver `play/Ending-animation-preview.zip`.

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
  then retains the full Coverage map, completion and reaction before reflection.
  Omit the earlier establishing view and final priority page.
  Shorten nonverbal holds (the reaction is 0.4 seconds).
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
