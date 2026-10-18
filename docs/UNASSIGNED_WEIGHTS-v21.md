# Level 3: unassigned first allocation (v21)

Saved before this change: `archive/pre-unassigned-weights-v21` at
`2d91487e87d73e77987424580016d0fb10406a43`. That checkpoint includes the accepted
Level 3 relative effort model and the latest Level 2 experiment framing.

## First action belongs to the player

The first weight editor displays **— / — / —**, with all sliders at the start.
It contains no preselected 34/33/33 split. Confirm and Run are disabled until
the player moves a slider. The first question is **How would you split the
100%?**. Collapsed help says **Move any slider to start. Confirm your weights,
then watch Alex.** The guide explains this same operation without entering
values, asking for a practice action or prescribing a pattern.

Moving any card creates the first positive allocation: its requested value is
bounded to 1–98 and the remaining percentage is divided between the other two
cards, differing by at most one rounding point. Nothing is confirmed. The
player may edit any card before confirming; all subsequent changes preserve
the existing proportional redistribution and linked-pair confirmation.

The unassigned editor is `null` state, not a zero-valued `WeightRun`. Native
range controls use zero solely as their unassigned starting position and name
it **Not assigned** accessibly. Once initialized their minimum becomes 1.
Only a valid positive total of 100 with all confirmations can be published.
Unassigned controls never enter effort calculation, animations, comparison,
completion callbacks or the attempt count.

Reset before the first publication clears back to unassigned. On subsequent
trials it restores the most recent actual allocation and clears confirmations.
Guide, hints, waiting, reset and optional-third cancellation create no record.

## Evidence, rather than an obligatory balanced solution

The experiment path is unchanged: free first observation, a new second split,
comparison after two observations and an optional cancellable third. An equal
or near-even split is allowed in any test but never required to complete.

- If an observed task receives little attention, the next question names it.
  Optional help asks what changing its share does to the other tasks; it does
  not fill numbers or prescribe balancing.
- If all tasks receive attention, the next question asks whether new weights
  help Alex go further. The preceding observation retains score-based stopping.
- If new numbers leave all effort bands unchanged, the comparison says Same
  effort. It does not invent a shift to make the experiment dramatic.
- Final dialogue uses only actual observations. Two uneven trials can reach
  Alex's response and the theory without a reference example, and the game
  never claims an untested balanced allocation was disproved.

These are intended opportunities for player reasoning, not evidence of an
observed psychological or learning effect. The v20 relative effort calculation,
ten-point tolerance, illustrated stopping concern and authored dialogue remain.

## Level 2 stays in this release

Level 1, Level 2 and shared product source are unchanged from the saved v21
baseline. The current standalone Level 2 and full game still show **Would more
metrics help Alex learn?** with the 6 → ? diagram, the explicit **Test more
metrics** action, continuous 10 → 25 → 100 growth and **More metrics. Still
chasing marks.** at the final observation. The existing 3.5-second holds and
0.7-second anticipated turns are retained.

No opening merge or new partner animation script is included. The original
Level 2 choices, supplied player name, sound, scene requests, copied run/result
payloads and final theory placeholder remain compatible. No Design Lab
navigation is added.

## Verification

Current checks and hashes are in
[LEVEL3_VALIDATION-v21.json](LEVEL3_VALIDATION-v21.json). They cover the first
action from every card, real keyboard and pointer input, initial and later
Reset, guide/hint neutrality, positive allocation bounds, first-even and
never-even paths, unchanged effort, optional third cancellation, responsive
layouts, actual ZIPs and the connected three-level flow. The standalone and
combined downloads are rebuilt from the same source.
