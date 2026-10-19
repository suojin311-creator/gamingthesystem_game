# Working on this game

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
