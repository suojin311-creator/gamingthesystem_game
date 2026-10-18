# Current gameplay and feedback corrections

The v12 prototype is preserved on `archive/pre-feedback-cleanup-v12` at
`031bbb0a737990294258ae97c86ad1badb43b5af`, including its original downloads.
The following corrections supersede the forecast and peer-scene additions
introduced in v12. Versioned validation reports remain historical records.

## Scoped chapter styles

The chapter-transition stylesheet used `.chapter-heading`, which already named
Level 1’s workbench title. Its hidden state, 56px font and reserved title area
leaked into Level 1. At 1366px the affected header measured 163px and its title
was hidden. Scoping every transition selector under `.chapter-transition`
restores the visible 31px workbench title and its 71px header. Tests explicitly
check visible chapter titles and compact headers in all three levels at
1366/768/390/320px, alongside the existing transition checks.

## Direct weight trials

The Level 3 prediction page and prediction/result markers have been removed.
Forecasting which task receives effort after showing its scoring weight mostly
repeated an already apparent relationship. Confirmed weights run directly into publication. Level 3 now uses three player-led Explore/Adjust/Verify trials, as described in [scaffolding](SCAFFOLDING.md). The comparison retains all three actual attempts.

The positive-weight rule stays: each priority receives at least 1%, the total
is exactly 100%, and a priority can reach 98% while reserving 1% for each other
priority. After confirming 61%, either remaining slider can reach at most 38%,
producing 61/38/1. Native/accessible bounds and publication validation agree.

Level 1 retains its original prediction. Level 3’s cognitive work remains the
comparison of actual observations and the tension between meeting reported
criteria and score-directed classroom behaviour. There is no new forecast task,
correctness reward or invented learning score.

## Existing authored animations own classroom action

The added peer-passing-card demonstration, new peer narrative module and
`peerInteraction` request field are withdrawn. The original simple Level 2
classroom placeholder/dialogue and request schema are restored. The user’s
existing formal scripts and animation files have not been edited.

`renderCinematic(request, complete)` owns the entire classroom scene slot. When
provided, its output replaces the entire placeholder, so no duplicate visual
panel or extra peer story appears before/after it. The final authored animation
will carry its own events; the interface does not generate an additional social
scene or reinterpret that script.

## Slower continuous escalation

One Add more metrics action still runs 10 → 25 → 100. Each milestone retains its
real count, growing paper stack, short caption and report-triggered management
satisfaction checkpoint. The completed actions at 10 and 25 now each remain
visible for **3.5 seconds**, followed by a 0.7-second anticipated paper turn on the same mounted surface. Hidden/off-screen time does not
consume that hold. At 100, Observe the class still waits for a click.

## Validation and scope

Current checks cover compact visible headers, the retained positive-weight
bounds, three player-led trial flows, original animation-request contracts,
replacement without duplicate content, longer visible holds, three-level
handoff, dialogue consistency and exact packaged offline HTML. They are recorded
in `LEVEL3_VALIDATION-v14.json`. Earlier broader reports were not rerun in full.
Opening-animation integration and the Level 1 opening handoff remain a separate
next step; this correction does not merge or rewrite the authored opening.
