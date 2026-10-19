# Opening animation

Imported from the user's `gaming-the-system-main (1).zip` supplied for
`Mg614/gaming-the-system`. Original archive SHA-256:
`47f743de944f21a6c7f830f5accfd1f2db4999ad0e2489918dcf6a6928e413e3`.
The five production PNGs retain their original bytes and filenames. The earlier
unmodified review ZIP remains `play/Opening-animation-preview.zip`.

The user's approved integration changes add visual email/student targets,
three-person completion feedback, larger Look around text and shorter waits.
Each normal-motion inspection is 450ms approach + 1500ms response + 450ms return.
Unseen students keep arrows; inspected students have checks; leaving unlocks
after all three. Reading the email and choosing actions still wait for input.

At officeEnd, a short LEVEL 01 / One metric handoff calls onComplete with the
confirmed player name. `FullGame` mounts Gameplay once for the three levels.
Opening styles/variables are scoped to `.opening-scene`; shared feedback owns
the mute preference. Restoring a closed page starts at title with a fresh name.

Use `npm run dev` for the opening and connected game. The `dev:level1`,
`dev:level2`, `dev:level3` entries remain direct standalone levels.
All work stays on `animation/opening-integration` until the user requests merging.
