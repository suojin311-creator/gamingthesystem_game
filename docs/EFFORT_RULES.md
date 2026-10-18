# Level 3 effort rules (introduced v17, retained v18)

The pre-change v16 source and downloads are frozen on
`archive/pre-effort-rules-v16` at
`69f2bb4906a6d6c85442686180e49dc6a0800291`.

The v17 revision fixed the relation between weights, observed effort and
narrative feedback. Those rules remain in v18; the subsequent
[player-path revision](LEVEL3_PLAYER_PATH.md) removes the aim and judgment gates
and allows completion after two observations, with an optional third.

## One per-item rule

Three positive integer weights total exactly 100%. Each lies between 1% and
98%, reserving at least 1% for the other tasks. Locked weights and linked-pair
confirmation keep their existing behaviour.

| A task's weight | Observed effort | Story intensity |
| --- | --- | --- |
| 1–24% | Minimum effort | low |
| 25–66% | Steady effort | medium |
| 67–98% | Intense effort | high |

Each task uses only its own weight to select its effort band. Increasing that
weight cannot reduce its effort band. These are qualitative illustrative rules,
not measured percentages of effort, learning gains or learning losses.

## Near-even is a description

An allocation is near-even when its highest and lowest weights differ by at
most **10 percentage points**, including the boundary. That classification
never overrides effort, awards a success state or triggers special criticism.
All valid near-even allocations naturally fall into three medium bands under
the rule above; uneven allocations can also have three medium bands.

For example, 40/30/30 is near-even, while 40/31/29 is uneven. Both produce three
steady responses. Moving between them is an unchanged-effort observation, not
an improvement, deterioration or new discovery merely because a label changed.
The comparison and final dialogue must preserve that distinction.

## Stopping at the scoring requirements

Alex's attention may become more evenly distributed. That change should be
acknowledged. It does not by itself establish deeper learning or exploration.
Stopping once scoring requirements are satisfied is a separate narrative
observation across allocations, including uneven ones.

Every all-medium run uses the criteria → ticks → packing-up sequence and the
medium-shot criteria actions/replies, independently of its near-even label.
The effort illustrations and summaries still follow the actual bands. When
some tasks receive minimum effort, those tasks remain unticked: the visual
must not imply that all requirements were met. The stopping-rule observation
must not accuse a near-even allocation of a defect that disappears solely when
its split label changes.

Findings, teacher questions, Alex replies and the final comparison summary use
actual effort bands and their changes. Three changed allocations with identical
bands are valid evidence of no observed band change. They must not produce a
summary claiming that effort moved each time.

## Scope and compatibility

The current flow uses a free first allocation, an evidence-led second editor,
comparison after two observations and an optional third experiment. Strategy
help is verbal and optional, without numerical examples. Required aims and the
keep/rethink gate have been removed. Level 1 and Level 2 behaviour is unchanged.

Existing cinematic IDs, prop shapes, opening-name routing and endpoint remain
the same: weighted observations → Alex's response → `theory.reveal`. The game
stays at the final theory placeholder, with no Design Lab navigation. The
partner's authored animation scripts are unchanged; custom renderers continue
to replace the entire placeholder.

Current validation is recorded in
[LEVEL3_VALIDATION-v18.json](LEVEL3_VALIDATION-v18.json). The
[v17 report](LEVEL3_VALIDATION-v17.json) preserves the original rule correction;
the v16 report, older archives and versioned ZIPs stay historical. Behaviour and
packaging checks do not establish classroom learning effectiveness.
