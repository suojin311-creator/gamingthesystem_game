# Current audio: sound effects only

User requested removal of all existing game music. The shared director no longer
imports, bundles, decodes or plays the five background cues. Saved music settings
are ignored and cannot restore playback. Scene adapters retain a no-op setScene
interface so gameplay and film timing stay unchanged. Music UI/audition controls
are removed. Existing effects, effect volume, mute and visibility handling remain.

Actual built-game Web Audio output and prior saved music=1 are checked in
`tests/audio_effects_only.py`; actual six-archive integrity is checked separately.
Formal game packages and embedded game-server HTML are refreshed together.
Pending visual previews, Padlet and the historical independent Lab stay untouched.

# Historical integrated sound preview (superseded music plan)

The original complete-game baseline is saved on GitHub at
`archive/full-game-before-audio-20261020` (`33a10e9`). The approved two-line ending
reflection is merged from `preview/ending-reflection-emphasis` (`04445a5`).

## Score and feedback

The three level films deliberately share one continuous music theme, rather than
per-shot effects. Interface music is quieter; Level 2's film is slightly stronger.
The opening uses a sparse office arrangement; ending reflection lowers the music
under the central learning/numbers question; the invitation and Lab share a quiet
focus arrangement. The Lab's two questions become silent, followed by a single,
slowly unfolding Goodhart reveal cue. The static ranking remains unchanged.

Five original instrumental cues are rendered by `scripts/render_score.py` using
synthesized felt-piano-like partials, soft sustained chords and a short room tail.
No commercial recordings, sampled music, vocals, subscription or runtime download
is used. Source and durations are in `src/audio/assets/SCORE.json`.

Selection/tick, paper, notification, results, chapter, submission, warning and vote
sounds share `src/audio/director.ts`. Both voting choices use the exact same neutral
confirmation. No repeating subtitle notifications, countdown or ranking scan audio.

One AudioContext per document owns music and effects separately. Film iframes
report playback state to their validated parent; they never play competing music.
Music keeps playing across ordinary shots. New scenes crossfade, film pause resumes
its saved musical position, hidden tabs become silent, and preferences persist
through the transition to Lab. Browsers require the first click to unlock sound.
The Sound panel controls music/effects separately and has a master mute.

## Integrated classroom review

The local Go classroom now embeds the approved complete game at `/game` and Lab
at `/`. The host shares `/game`; the ending invitation opens the same classroom's
Lab. No name, metric or weight transfer is needed. Participants join the Lab at
that point; the teacher starts writing once everyone is there. The writing prompt
is: What is one change you would make to help Alex learn more deeply?

The teacher opens `Start-Gaming-the-System.exe`. `/host` includes an explicit
music/effects audition link (`/game?soundcheck=1`) and a game link. The sound-check
page also links directly to all three levels. Host controls themselves are silent
so they don't duplicate the display/participant soundtrack.

`play/Gaming-the-System-classroom.zip` is the integrated review download. The six
regular HTML archives still work offline for individual play; their ending button
explains how to use the classroom executable when no classroom service is present.
The standalone film ZIP remains an approved historical review.

## Validation notes

Use `tests/audio_classroom.py` against the embedded Linux service. It captures the
actual Web Audio output through an analyser, checks all five score cues, pause,
master mute, independently zeroed music/effects, visibility and the real Level 3
ending-to-Lab handoff. The zero-volume path cancels prior AudioParam automation
and sets exact zero, preventing a previously silent graph from reviving an old
bus level on the next effect. The full game release browser checks and the
21-participant Lab checks are preserved as separate reports; after audio-only
changes, repeat the audio checks and actual ZIP integrity rather than replaying
unchanged game allocation rules. `tests/release.py --integrity-only` validates all
six final archives without relying on a browser transfer of large HTML via CDP.
