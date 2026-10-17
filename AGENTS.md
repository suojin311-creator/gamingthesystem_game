# Preview releases

- Keep one implementation per level under `src/levels/`; reuse shared modules.
  Individual previews and the combined game must use these same components.
- Current development is on `level3-dev`. Levels 1–3 are playable; Design Lab is reserved.
- After an approved gameplay change, run `npm run package:previews` to rebuild
  all latest downloads and the two-version review ZIP together. Never update only an individual package
  or only the combined package when they share affected code.
- The fixed latest entries are `play/Level1-play.zip`, `play/Level2-play.zip`,
  `play/Level3-play.zip`, `play/Full-game-play.zip` and
  `play/Level3-and-Full-game-play.zip`. The last archive contains both Level 3
  and the connected three-level game from those same production builds. Keep version-numbered archives unchanged.
- Run `python tests/release.py` against the actual latest ZIPs. Use the relevant
  gameplay suites when behaviour changes. Record current validation/hashes.
- When publishing is authorized, fast-forward the preview branches to the
  approved release as well; do not leave `level1-preview` with stale Level 1
  source or downloads. Check remote changes first and never force-push.
- Use this checkout; do not create a worktree unless the user requests one.
