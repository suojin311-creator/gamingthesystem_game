# Learning-focused gameplay revision

The v11 baseline is preserved on `archive/pre-learning-optimizations-v11` at
`fc279fc38c2a8ce4d913317b4f2102fae44d78c8`, including the previous downloads.
This revision implements the four approved gameplay changes. Opening animation
integration and the Level 1 opening handoff remain a separate next step.

## Positive scoring weights

Every selected Level 3 priority receives at least 1%; all three still total
exactly 100%. A single shared lower bound controls allocation, available maxima,
validation and native/accessible slider bounds. The first priority can reach
98%, reserving 1% for each other priority. After confirming 61%, either remaining
slider can reach at most 38%, producing 61/38/1. The final linked pair still
confirms in either order. Zero-weight runs cannot pass publication validation.
Near-even still means a highest-minus-lowest spread of at most ten points.

## Predict, observe, compare

After confirming weights, Make a prediction opens a short three-card forecast.
The player selects one or more priorities expected to receive Alex’s highest
effort, then runs the evaluation. There is no text entry, preselected answer or
correctness reward. Returning to weights and re-entering the forecast clears
the unsubmitted prediction. Each explicit system reference also requires a fresh
forecast before publication.

Result rows place the recorded prediction beside the actual qualitative effort.
Highest observed effort follows the categories actually shown: for 61/38/1,
Preparation and Participation can both be Steady while Focus is Minimum; both
Steady rows therefore share the highest observed band. Near-even shows three
Steady rows. The game does not invent precise numerical effort percentages.
Forecasts never affect weights, effort categories, reference selection,
management satisfaction or the narrative outcome.

`WeightRun.predictedMetricIds?: MetricId[]` is an additive partner/result field.
All new internal runs include it. `copyRun`, scene requests, comparison snapshots
and completion results copy its array independently. Legacy external runs may
omit it. Replays retain the original recorded forecast.

## A scoring routine spreads between students

The six-metric placeholder replaces its prior explanatory paragraph and three
teacher/Alex lines with a three-beat illustrated peer interaction:

1. Alex passes along a discussion phrase card that earns a tick.
2. A classmate copies the phrase, then asks why the lesson idea is true.
3. Alex redirects both students to completing the scored phrase. Both get ticks;
   the content question remains visibly open.

This shows institutional criteria acting through a shared tool and peer routine,
rather than treating the presence of character dialogue as sufficient social
interaction. The classmate is a separate speaker and portrait position. The
ordinary three/final-checklist scenes retain their existing contracts.
`level2.six` now supplies optional `peerInteraction` action/text beats for a
finished partner animation; the current preview remains an illustrated story
placeholder, not a claim that finished video assets have been produced.

## One continuous escalation

After the six-metric observation, Add more metrics starts the whole 10 → 25 →
100 sequence. Each milestone keeps its real count, report-triggered satisfaction
checkpoint and growing paper stack. A short illustrated Alex action replaces
the former three-sentence checklist: checking boxes, reusing one answer across
criteria, then doing just enough for every tick. The first two milestones move
on after their visible action; there are no repeated Add clicks. At 100, Observe
the class still waits for the player. Hidden/off-screen presentation holds;
reduced motion removes movement while retaining each milestone and outcome.

## Relationship to the submitted design

| Dimension | Concrete experience |
| --- | --- |
| Game mechanics | Choose criteria, allocate a limited total, confirm decisions, forecast and observe distinct consequences |
| Narrative | The teacher changes the assessment system; students adapt to its rewards and stopping conditions |
| Cognitive foundation | Make a prediction, inspect evidence, contrast two actual tests and reconsider the scoring model |
| Sociocultural foundation | Management expectations shape criteria; students share a scoring tool and reproduce a classroom routine |
| Levels | Single metric → more metrics → weighting, with the existing distinct chapter transitions and inherited choices |

These describe implemented design opportunities; functional checks do not
establish measured learning effectiveness. Fresh rule, forecast/peer-contract,
offline-browser, dialogue, partner and actual-ZIP checks are recorded in
`LEVEL3_VALIDATION-v12.json`. Earlier broader reports remain historical.
