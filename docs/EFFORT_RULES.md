# Level 3 relative effort rules (v20)

The prior release is saved at `archive/pre-relative-effort-v19`. V17–v19
used absolute 25%/67% cutoffs; those rules and reports are historical.

## Compare the complete allocation

Three positive integer weights still total exactly 100%, each at least 1%.
For each task, compare its score weight with each of the other two tasks:

- A difference of at most 10percentage points, inclusively, counts as similar.
- Being more than 10points above an alternative is a higher-reward comparison.
- Being more than 10points below an alternative is a lower-reward comparison.
- More higher than lower comparisons produces high effort; more lower than
  higher produces low effort; a tie produces medium effort.

This compares every task with both alternatives. It gives the three common
patterns without forcing a graduated distribution into a two-group answer:

| Weights | Effort in the same order | Interpretation |
| --- | --- | --- |
|49/26/25|high/low/low|One priority, two similar lower rewards|
|49/27/24|high/low/low|Same pattern; no absolute 24/25cliff|
|45/45/10|high/high/low|Two priorities, one lower reward|
|34/33/33|medium/medium/medium|Three similar rewards|
|65/24/11|high/medium/low|Graduated priorities;24% is medium here|
|40/30/30|medium/medium/medium|All pair differences are within 10|
|40/31/29|high/medium/low|The40vs29difference is11; the raised31stays medium|

The10-point tolerance reuses the game's agreed notion of similar weights. It
is an explicit game-design assumption, not an empirical behavioural threshold
or a formula derived from Goodhart's Law. A categorical model still has
boundaries: crossing a relative-gap boundary may change a category. It does
not claim that every1-point edit leaves the scene unchanged.

Effort labels are qualitative relative responses within the tested trio. They
are neither measured effort percentages nor learning gains or losses. There
is no fixed rule saying 24% means minimum effort. The same 40% is medium in
40/30/30 and high in 40/50/10 because the other rewards differ.

## Stable slider behaviour

Editing a share now preserves the ratio of the other unlocked shares, rounding
the first in card order and assigning the remainder to the other. At least 1%
is reserved for each. With one unlocked alternative, that card receives the
exact remainder. Locked weights and linked-pair confirmation are unchanged.

This matters for relative effort: automatically resetting the other shares
to equal values could change the whole reward structure while the player
only meant to adjust one value. A no-op edit now leaves all values unchanged.
Across all 4,851 valid splits, increasing an edited share cannot reduce its own
effort band, including actual proportional slider reallocations. Equal weights
receive equal bands, and reordering cards cannot alter their behaviour.

## Keep attention and motivation separate

Near-even remains highest minus lowest at most 10points. The pairwise model
naturally yields three medium responses for these allocations; no global
near-even override is applied to individual effort.

Shared attention is acknowledged. The unresolved problem is Alex's reason for
working: he stops after earning the marks he wants. That observation applies
across allocations. Low-effort tasks stay unticked in the existing stopping
sequence; the game does not pretend every criterion was met.

Editor prompts, actual scene requests, result rows, dialogue, coverage ticks
and comparison deltas all read the same `effortAt` function. Comparison labels
still refer to the immediately previous actual test by metric identity.
Changing weights may leave categories unchanged, which must be reported as
Same effort rather than an invented improvement.

## Validation and scope

Current checks and package hashes are in
[LEVEL3_VALIDATION-v20.json](LEVEL3_VALIDATION-v20.json). They include all 4,851
splits, all card permutations,28,518 one-point transfers, proportional slider
edits, 20 trios, short fresh dialogue, two-test completion, optional-third
cancellation, partner requests, offline downloads and responsive layouts.

The two-test path, optional third, positive bounds, opening-name/trio handoff,
authored partner scripts and final theory placeholder remain. There is no
Design Lab navigation. Functional checks do not establish learning efficacy.
