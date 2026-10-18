# Continuous escalation and purposeful experiments

The v13 baseline is frozen on `archive/pre-scaffolding-v13` at
`d10e09bc7a34cae462ea594bce09f4fc8671f593` with its existing downloads.

## Level 2

10 → 25 → 100 stays on one mounted desk: counter, matrix and paper retain their
identity and stable geometry. A completed 10/25 action holds 3.5 visible seconds,
the next milestone lights and the paper turns over 700 ms. The same counter then
runs up to the next count; the new action fades in. Internal count changes do
not focus/scroll the heading. Hidden/off-screen intervals pause the hold, turn
and paper animation. Narrow layouts reserve caption and perspective-card space to avoid page-height changes. The 320px regression allows at most 8px of native viewport settling while requiring identical paper height. Reduced motion keeps the milestones and readable delays
without moving paper. At 100, Observe the class still requires a click.

## Level 3

Three actual player-confirmed trials replace the conditional system reference:

1. Explore: freely allocate weights in response to the experiment's opening question.
2. Adjust: respond to the actual neglected tasks or the near-even stopping rule.
3. Verify: fill a missing contrast, or redirect reward to a previously neglected task.

Second-test guidance is a question, not a fixed allocation. The third task
requires its intended contrast so three identical behaviours cannot satisfy it.
An optional starting-point button loads editable, unconfirmed values; players
can choose different values. Previously tested allocations cannot be repeated.
Reset restores the immediately previous run. The final table contains all three
actual trials and each scene/completion request copies the same immutable runs.
No extra prediction page or correctness reward is introduced.

The nonmodal first-use guide follows the actual operation: slider → Confirm
weight → remaining pair → Run evaluation. It preserves the player's values and
supports keyboard input, Skip, Escape, reset and manual reopening. It does not
auto-open during later tests. Teacher/Alex reviews remain one question plus two
short replies, with fresh third-test wording; no extra editing conversation is
added. All existing scene IDs and partner slots remain, ending at the theory
placeholder. Existing formal animation scripts and opening integration remain
outside this change.

See `LEVEL3_VALIDATION-v14.json` for the final build, package, dialogue,
three-trial, guide and transition checks. Functional validation is not a claim
of measured learning effectiveness or classroom hosting capacity.
