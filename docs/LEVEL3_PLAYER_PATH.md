# Level 3 player path (v18)

Saved baseline: `archive/pre-level3-path-v17` at
`5d56d4cbb763b039b4a8a7a4c3bceb7932f303b2`.

## What this revision addresses

The previous editor required an abstract aim before every trial, supplied
numerical examples and required three tests plus a final judgment. That could
ask the player to repeat operations without obtaining different evidence.
The current path connects each return to editing with the last observation,
while allowing the player to reach the comparison after two tests.

1. **Choose priorities.** In the combined game, the original Level 2 trio is
   already selected and can be changed. Standalone Level 3 starts empty.
2. **Try an allocation.** Allocate positive integers totaling 100%, confirm the
   cards and run. The spotlight guide teaches only controls.
3. **Observe.** Publication waits for Observe the class. The selected shots,
   qualitative effort rows and short teacher/Alex exchange show the result.
4. **Try a change.** The second editor retains the last observation and asks a
   short question based on its actual bands. Need a hint? gives verbal help,
   never an automatic split. The player decides the values.
5. **Compare.** After the second observation, show both actual trials side by
   side. The primary Watch Alex's response action continues directly.
6. **Optional verification.** Test another idea returns from comparison to a
   third editor. Back to comparison cancels this optional test without adding a result. After a third observation, comparison includes all three real
   tests. It does not add a system reference or allow a fourth trial.
7. **Final scene slots.** Alex's response leads to `theory.reveal`. The preview
   remains on the final theory placeholder and never navigates to Design Lab.

## Player-route checks

| Starting observation | Context for another experiment | What the next result must acknowledge |
| --- | --- | --- |
| One or more tasks receive minimum effort | Keep those actual task names and effort visible; ask about changing the allocation | If attention improves, acknowledge it; do not label every adjustment a failure |
| A near-even split gives three steady responses | Acknowledge shared attention; retain the observed score-based stopping and ask whether new weights help Alex go further | The first balanced allocation was legitimate; scoring-directed stopping remains a separate observation |
| An uneven split gives three steady responses | Use the same actual bands, rather than treating the uneven label as low attention | Near-even is descriptive metadata, not a second behaviour rule |
| New values leave every effort band unchanged | Describe no observed band change and let the player compare or optionally investigate further | Do not claim attention shifted merely because the numerical weights changed |

The questions do not require a prescribed answer, near-even split, band change
or numerical example. Exact allocation repeats are rejected, but changed values
with identical bands remain valid observations.

## Controls and evidence

The four-step guide is a modal spotlight like Level 1's introduction: slider,
Confirm, linked remaining pair, Run. Next/Back advance the explanation;
Skip/Escape close it. The final action is Try your weights. No practice action
or percentage change is required, and Guide can reopen it during editing.

Comparison cells label First result, Same effort, More effort or Less effort.
Every later column compares qualitative effort with the immediately previous
test by metric identity. Weight percentages are quiet reference values, not
effort percentages. No aim heading, result-summary box or keep/rethink gate is
inserted.

The retained per-item bands are 1–24% minimum, 25–66% steady and 67–98% intense.
Highest minus lowest at most ten points describes near-even weights without
overriding the bands. Any all-steady result can show criteria → ticks → packing
up; minimum-effort tasks stay unticked. Shared attention can improve while
stopping at the scoring requirement remains visible. Neither observation is a
measurement of learning gain or loss.

## Compatibility and boundaries

Completion fires once when Watch Alex's response is chosen after two or three
observed tests. Actual runs and the compared near-even/uneven pair are copied;
that pair is null if both classes are not present. Optional legacy intent and
decision fields remain accepted but the current UI does not populate them.
Player name, original metric inheritance, scene IDs, custom renderer replacement
and the reserved unused Design Lab callback are preserved.

This revision is limited to Level 3. It neither merges the opening nor changes
the partner's authored animation scripts or Level 2's growth sequence. Functional
path, accessibility and packaging checks are recorded in
[LEVEL3_VALIDATION-v18.json](LEVEL3_VALIDATION-v18.json); classroom efficacy and
the best possible learning design are not established by those checks.
