# Preview releases

- Keep one implementation per level under `src/levels/`; reuse shared modules.
  Individual previews and the combined game must use these same components.
- Current development is on `level3-dev`. Level 3 is reserved until implemented.
- After an approved gameplay change, run `npm run package:previews` to rebuild
  all three latest downloads together. Never update only an individual package
  or only the combined package when they share affected code.
- The fixed latest entries are `play/Level1-play.zip`, `play/Level2-play.zip`
  and `play/Full-game-play.zip`. Keep version-numbered archives unchanged.
- Run `python tests/release.py` against the actual latest ZIPs. Use the relevant
  gameplay suites when behaviour changes. Record current validation/hashes.
- When publishing is authorized, fast-forward the preview branches to the
  approved release as well; do not leave `level1-preview` with stale Level 1
  source or downloads. Check remote changes first and never force-push.
- Use this checkout; do not create a worktree unless the user requests one.
