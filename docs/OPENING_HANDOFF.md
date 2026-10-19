# Opening → gameplay: current animation branch

The user requested separate animation development. `animation/opening-integration`
contains the opening and its real Level 1 handoff; `level3-dev` retains the approved
game version. Review bundles are built and published only on the animation branch
until the user requests merging. See [animation integration](ANIMATION_INTEGRATION.md).

## Actual entry and completion

`src/App.tsx` routes the three standalone modes directly to their respective
levels. Its default full-game entry renders `src/FullGame.tsx`, which starts with
`src/cinematics/opening/Opening.tsx`. The opening keeps its original identity
form, office email, classroom observations and return to the office.

After all three students are observed and RETURN TO OFFICE completes, officeEnd
shows LEVEL 01 / One metric. Choose a metric calls `onComplete(playerName)` once
with the trimmed, confirmed name. FullGame mounts `<Gameplay playerName={name} />`;
Gameplay stays mounted across Levels 1, 2 and 3. The existing Level 1 workbench
guide teaches controls without adding another story opening or name form.

Closing/reloading starts at the title. A restored page (`pageshow.persisted`)
clears the current name and game and returns to the opening. No identity, choices
or sound preference are stored in browser storage or sent to a service.

## Requested opening adjustments

- The urgent email has a pointing arrow and gentle card emphasis until clicked.
  It never opens automatically; screen-reader text identifies the email button.
- Each unobserved student has a pointing arrow. On return to the wide view,
  completed students have checks and outstanding arrows remain. Three connected
  portrait indicators show the group’s completion without written instructions.
- Look around remains visible between observations and is larger. Existing
  student lines are retained. Every normal-motion inspection takes 450ms approach,
  1500ms response and 450ms return (about 2.4s); overlapping input is locked.
- All three distinct students are required before leaving. Revisiting one does
  not replace observing another. The final thought and return action remain.
- Other automatic camera holds and transitions are shorter. Email reading and
  every decision still wait indefinitely for the player. Reduced motion keeps
  static arrows/checks and removes camera movement.

## Assets, styles and sound

Source is the uploaded `gaming-the-system-main (1).zip` from Mg614’s repository;
archive SHA-256 is recorded in [the opening README](../src/cinematics/opening/README.md).
Five runtime PNGs retain their original bytes. The original review download is
kept as `play/Opening-animation-preview.zip`, with its original source manifest.
Imported runtime code lives together under `src/cinematics/opening/`.

Every opening selector and its colour variables are scoped to `.opening-scene`.
The game’s fonts, primary buttons and level styles retain their own values after
handoff. The office handoff button uses the game’s coral style.

The partner’s optional audio-file hook shares the in-memory mute preference with
`useFeedback`. Existing audio is stopped on handoff/unmount. No missing audio is
requested and no replacement soundtrack was invented. Start/name/click gestures
unlock the shared audio context for the later game. Newly supplied audio can use
the partner’s existing file names inside the opening’s `assets/audio/` folder.

## Later scenes and player identity

The same confirmed playerName reaches all three levels, teacher labels and
cinematic requests; Alex remains Alex. Role portraits are independent of names.
Standalone entries retain their default preview name and omit the opening.

Later classroom and final cinematics still use their existing renderer slots;
this opening work does not replace them or alter the approved level rules.
`Gameplay` accepts `renderLevelOneCinematic`, `renderLevelTwoCinematic` and
`renderLevelThreeCinematic`. Renderers receive the actual request/playerName and
complete callback. Keep Gameplay mounted and call complete only when that scene
ends. See [Level 1](LEVEL1_HANDOFF.md), [Level 2](LEVEL2_HANDOFF.md) and
[Level 3](LEVEL3_HANDOFF.md). The final endpoint remains the theory reveal; no
Design Lab navigation or administrator Restart control was added.

## Verification and previews

Use `npm run dev` for the complete opening and game, or `dev:level1/2/3` for a
standalone level. `tests/opening_integration.py` exercises real-time desktop
visual cues, actual inspection timing, all-three gating, name handoff, styles,
restored-page reset, touch and reduced motion. With `--packaged` it exercises the
actual full-game ZIP bytes offline. The release suite also completes the
opening → Levels 1 → 2 → 3 route and verifies all standalone entries. Current
results and hashes belong in [PREVIEW_VALIDATION.json](PREVIEW_VALIDATION.json).
