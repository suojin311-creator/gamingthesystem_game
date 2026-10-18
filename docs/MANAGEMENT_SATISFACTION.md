# Management’s view

All three chapters use the same `ManagementSatisfaction` component: a qualitative
state, green progress bar and small line of report evidence. The bar represents
management’s reaction to meeting reporting requirements, not measured learning
or an extra player objective. Its internal position is never printed as a
satisfaction percentage.

| Latest completed report | Internal bar position | Visible state |
| --- | --- | --- |
| No report | 12 | Awaiting results |
| Level 1 target met | 44 | Satisfied |
| Level 2: 3 metrics | 60 | Satisfied |
| Level 2: 6 metrics | 70 | Very satisfied |
| Level 2: 10 metrics | 77 | Very satisfied |
| Level 2: 25 metrics | 82 | Very satisfied |
| Level 2: 100 metrics | 86 | Very satisfied |
| Level 3: first publication | 90 | Very satisfied |
| Level 3: second publication | 93 | Delighted |
| Level 3: reference publication, if needed | 95 | Delighted |

Positions are derived from completed reports, so there is no separate counter
to increment twice. Level 1 updates when its target result is reported; Level 2
updates when each new metric evaluation finishes; Level 3 updates after all
three weights have been published. Weight allocation is the evidence for that
publication, not a claim about learning. All allocations receive the same
management response; near-even weights earn no extra increase.

The chapter handoffs match exactly: Level 1 ends at 44 and Level 2 starts there;
Level 2 ends at 86 and Level 3 starts there. Standalone previews enter at the
same chapter baseline. Choosing/swapping metrics, moving/confirming/resetting
sliders, observing, replaying and opening the comparison do not raise the bar.
It stays at the preceding report while another evaluation is pending. Fresh
visits use the existing fresh-session behaviour.

The bar fills over one second after a new report and never replays its fill on
ordinary remounts. Reduced-motion users see the new value immediately. A
labelled progressbar exposes the qualitative state to assistive technology.
The student card retains specific observed behaviour and Learning at risk.

A new report also gives the whole management card three green outline pulses
(650 ms each). The shared indicator responds to an actual increase, including
updates within the same qualitative label. It holds while the card is off-screen
or the page hidden, and resumes when visible. Remounts/replays at the same value
and fresh-session decreases do not pulse. Reduced motion uses a single steady
outline for the same total duration. This attention cue does not change any
satisfaction values or block the next action.
