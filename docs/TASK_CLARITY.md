# Level 3 task and comparison clarity

The v14 source and downloads are preserved on `archive/pre-task-clarity-v14` at
`3ffe53588ef599673228b9156c4af975c5aabd68`.

## Task entry point

The one-sentence question now occupies a contrasting card above the weights:
24px on desktop, 21px on phones, with a four-pixel left accent. Each editor
entry pulses its border/glow three times over 2.4 visible seconds, then retains
the static card. Hidden/off-screen time pauses the cue; editing, confirming,
resetting or applying a suggestion ends it immediately. Reduced motion shows
one steady timed outline without a flashing or moving effect.

Questions are shorter and concrete, such as “What if Participation and Peer
response counted more?” The adaptive trial goals and suggested allocations
remain the same.

“Apply suggested weights” is a filled button. Its caption says “Sets the
sliders; you confirm.” Clicking loads editable unconfirmed percentages and
reports “Weights set. Adjust or confirm.” It does not publish or run a trial.
Manual slider edits and Reset remain available.

## Comparison semantics

The former full-cell fill only marked effort-band changes relative to the
immediately preceding test. Since the visible percentages could also change,
this unstated distinction looked inconsistent. The full-cell fill and its
ambiguous changed flag are removed.

Every cell now explicitly states First result, Same effort, More effort or
Less effort, with a matching dash/equal/up/down symbol. Headers name the basis:
Starting observation, Effort vs First test, Effort vs Second test. Percentages
retain their quiet scoring-weight reference. More effort is not labelled better
learning; the qualitative behaviour/risk interpretation stays unchanged.

For the reported 43/29/28 → 34/33/33 → 28/43/29 example:

| Metric | Second vs first | Third vs second |
| --- | --- | --- |
| Preparation | Same effort | Less effort |
| Participation | More effort | Same effort |
| Peer response | More effort | Less effort |

In particular, preparation's 43% → 34% and participation's 33% → 43% change
weights while keeping their current effort band. The explicit Same effort label
makes this distinction visible. Checks also reorder metric IDs between records
to verify that comparisons follow the metric, and cover large weight changes
that stay within an effort band.

## Validation

`LEVEL3_VALIDATION-v15.json` records focused production-browser and component
checks, finite/hidden/reduced-motion attention behaviour, editable suggestion
loading, the exact reported three-trial example, 1366/768/390/320px layouts and
actual ZIP integrity/offline flows. All latest standalone/combined downloads
come from the same final builds. Earlier broader suites remain historical in
v14 and were not rerun in full for this presentation change.
