# Opening animation

Imported from the user's `gaming-the-system-main (1).zip` supplied for
`Mg614/gaming-the-system`. Original archive SHA-256:
`47f743de944f21a6c7f830f5accfd1f2db4999ad0e2489918dcf6a6928e413e3`.
The five production PNGs retain their original bytes and filenames. The earlier
unmodified review ZIP remains `play/Opening-animation-preview.zip`.

The user's approved integration changes add visual email/student targets,
three-person completion feedback, larger Look around text and shorter waits.
Normal inspections use a smaller 1.28x zoom: 900ms approach, a 1700ms reading
hold after arrival, and 850ms return (about 3.45s). Motion completion callbacks
advance phases and unlock input; movement is not timed out mid-flight. One plain
glowing arrow points to the next unseen student. Three unframed portrait/check
indicators show progress. Leaving unlocks after all three. Reading the email
and choosing actions still wait for input.

The classroom fades out before the office camera is reset behind an opaque
cover. The office fades in fully, then shows two brief teacher reflections.
After the final fade, onComplete passes the confirmed name to FullGame. The
shared ChapterTransition first introduces LEVEL 01 / One metric against a faint
office backdrop. Choose a metric then mounts Gameplay once for the three levels.
Opening styles/variables are scoped to `.opening-scene`; shared feedback owns
the mute preference. Restoring a closed page starts at title with a fresh name.

Use `npm run dev` for the opening and connected game. The `dev:level1`,
`dev:level2`, `dev:level3` entries remain direct standalone levels.
All work stays on `animation/opening-integration` until the user requests merging.
