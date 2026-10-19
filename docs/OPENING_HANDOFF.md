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

After all three students are observed, BACK TO OFFICE waits for the exit camera
and classroom fade to complete. The hidden office camera resets behind an
opaque cover before the office fades in. Two successive thoughts appear:
“They’re here, but they’re not really engaged.” and “What should I measure first?”
After the last thought and fade, `onComplete(playerName)` fires once with the
trimmed confirmed name. FullGame shows the shared Level 1 ChapterTransition,
with the office image fading into the paper presentation. Only Choose a metric
mounts `<Gameplay playerName={name} />`; Gameplay stays mounted across all three
levels. The existing workbench guide teaches controls after this chapter entry.

Closing/reloading starts at the title. A restored page (`pageshow.persisted`)
clears the current name and game and returns to the opening. No identity, choices
or sound preference are stored in browser storage or sent to a service.

## Requested opening adjustments

- The urgent email has a pointing arrow and gentle card emphasis until clicked.
  It never opens automatically; screen-reader text identifies the email button.
- One unobserved student at a time has a plain glowing arrow, without a circle
  frame or an outline around the student. The arrow moves to the next unseen
  student after an observation. Players may still choose a different student;
  keyboard focus can move the cue. Three unframed portraits become checks as
  observations complete, showing progress without a written checklist.
- The invitation reads Come closer to take a look at the students. Existing
  student lines are retained. The normal camera uses a smaller 1.28x zoom over
  900ms, then a 1700ms reading hold and an 850ms return. Phase changes and input
  unlocking wait for actual animation completion rather than an independent
  timer. Duplicate input remains locked during movement and reading.
- All three distinct students are required before leaving. Revisiting one does
  not replace observing another. The final classroom thought and back action
  remain, followed by the office reflection and a complete Level 1 chapter entry.
- Camera motion, opaque fades, reading holds and action waits have separate
  responsibilities. Visible reading time pauses on a hidden page. Reduced motion
  keeps static arrows and removes camera movement while preserving the sequence.

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
