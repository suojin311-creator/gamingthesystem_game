# Chapter breaks without a victory cue

The prior experiment has met its reported target, while the student consequence
remains unresolved. Levels 2 and 3 therefore open as a new experiment, with a
prominent chapter title and a physical change on the same desk. They do not use
congratulations, rewards, confetti, a score bonus or an ascending success sound.

The previous release is preserved on `archive/pre-chapter-transitions-v10`, at
`78df0ead3d52bf692292399988a7f0ff0b9aff26`, including all five prior downloads.

| Visible beat | Duration | Level 1 → 2 | Level 2 → 3 |
| --- | --- | --- | --- |
| Hold | 900 ms | Actual single metric card; Target met alongside its actual student behaviour | Completed checklist; 100 requirements tracked alongside Chasing ticks |
| Turn | 1,000 ms | Single card files away; three empty slots unfold | Checklist closes away; the original three chosen cards return with slider artwork |
| Chapter | 1,100 ms | LEVEL 02 · More metrics. | LEVEL 03 · The weighting trap. |
| Entry | Until click | One teacher line; Choose three metrics | One teacher line; Review priorities, or Choose priorities in the standalone entry |

These replace the earlier three-message introductions. The ordinary workbench
chapter header and stepper appear after entry, avoiding a duplicate chapter
title. The last report / student consequence stays at the top of the break.
The teacher uses the opening-confirmed name and the existing portrait/speech
bubble. The chapter adds no Alex reply or additional explanation paragraph.

`ChapterTransition` accepts existing metric identities as presentation data.
It never selects or confirms a metric, assigns a weight, or changes satisfaction.
Level 2 still starts with three empty slots. Level 3 still preselects the actual
original Level 2 trio, and permits editing after entry. Its three slider drawings
are decorative. Standalone Level 3 uses unassigned priority cards and an empty
working selection. Standalone Level 2 uses a generic single metric / unresolved
learning recap because it has no actual preceding Level 1 run.

A 240 ms filtered paper sound accompanies the movement. Two soft low tones
(196 → 174.61 Hz, about 660 ms total) accompany the chapter title. Both are local
Web Audio synthesis, with no asset download or background loop. Sound off stops
active cues and suppresses future cues. The page retains one gesture-unlocked
audio context across level mounts; each level stops its own voices on unmount.
An isolated chapter without a prior gesture can remain silent under browser
autoplay policy, while the complete visual sequence still works. No autoplay
retry or extra audio-permission button blocks play.

Timers and card animations pause when the page is hidden or the chapter is off
screen. Reduced motion keeps the same information and click gate without
animation. The new heading receives focus when revealed; the entry button is a
normal keyboard-operable button. The layout keeps all three cards visible at
320, 390, 768 and 1366 px widths.

`tests/chapter_transitions.py` checks exact production HTML offline, including
three-second pacing, explicit entry, empty standalone selections, the real Level
1 card/consequence handoff, gesture-unlocked chapter audio, mute/active sound
stopping, hidden/off-screen pause, reduced motion and responsive layouts.
`tests/level3_integration.py` checks the real Gameplay host carrying the original
non-default Level 2 trio, supplied player name and sound preference into Level 3,
and still allows swaps. `tests/release.py` exercises the actual packaged entries.
