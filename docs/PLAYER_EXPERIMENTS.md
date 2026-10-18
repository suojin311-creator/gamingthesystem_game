# Player-led experiments (v18 path, v20 relative effort)

The pre-change source and downloads are frozen on
`archive/pre-level3-path-v17` at
`5d56d4cbb763b039b4a8a7a4c3bceb7932f303b2`.
The v17 effort rules remain; this revision replaces the required aim selector,
three-test gate and final keep/rethink judgment. Level 1, Level 2 and the
partner's authored animation scripts are unchanged.

## Follow evidence rather than a prescribed allocation

The first confirmed allocation is free. The second editor carries forward the
last actual observation, with the selected task names and their qualitative
effort. A short question responds to neglected tasks or shared attention,
rather than asking the player to pick an abstract aim. A near-even first
allocation is legitimate evidence; it is not marked wrong or forced onto a
different route.

Need a hint? is collapsed verbal help. It suggests what could be observed and
leaves the numerical choice to the player. There is no Apply suggested weights
control, automatic allocation, system reference or required pattern. Changed
weights with the same effort bands remain valid evidence of unchanged effort;
exact repeats of an earlier allocation are rejected.

The first-use guide only explains controls. Its four static spotlight steps use
Next, Back, Skip and Escape, ending with Try your weights. It does not ask for
practice, move sliders or confirm values. Guide reopens it during editing.

## Two observations, with room for one more

After the first result, the next action returns to the editor to try a change.
After the second observed result, Compare the results opens a table containing
both real experiments. Its primary Watch Alex's response action continues
without a judgment question. Test another idea optionally opens a third editor.
Back to comparison abandons unsubmitted edits without adding a trial.
After a third observation the comparison retains all three tests and offers the
same direct continuation. There is no fourth experiment.

The second or third allocation does not have to be near-even, uneven or cross
an effort threshold. Each is a new positive integer split totaling 100%,
confirmed by the player and actually observed before it can be compared.
No additional aim selection is needed before Run evaluation.

## Evidence and stopping are different observations

Results retain the effort illustrations and one teacher question with two short
Alex replies. They do not add aim headings or repeated result-summary boxes.
Questions and final dialogue use the actual effort bands and their changes:
improved coverage is acknowledged, while unchanged bands are described as
unchanged. Different numerical weights are not automatically a new finding.

Stopping at the scoring requirements remains a separate narrative observation.
Every all-steady allocation uses criteria → ticks → packing up, independently
of the near-even label. Low-effort tasks remain unticked. The rule is not a
special punishment for a balanced split or evidence of measured learning loss.
Replay preserves the established result; it does not create another trial.

The replaceable scene chain remains weighted observations → Alex's response →
`theory.reveal`. Custom renderers replace the complete placeholder. There is no
Design Lab navigation, additional ending page or player Restart control.

## Contracts and compatibility

- New trial records have `kind: 'player'` and do not populate the legacy optional
  `WeightRun.intent`. Older host fixtures may still provide that field.
- The optional `LevelThreeCinematicRequest.decision` remains accepted for older
  hosts, but the current game has no decision gate and does not populate it.
- Completion fires once on Watch Alex's response after two or three observed
  tests. It returns copied `selectedMetricIds`, copied actual `runs` and
  `compared: { nearEven, uneven } | null`. `LevelThreeResult.decision` is optional
  and omitted by this UI.
- A mixed history retains a copied near-even/uneven pair. Without both pattern
  classes, `compared` is null. Consumers must use the all-runs payload as the
  authoritative two- or three-test history.
- Weighted shot IDs, player-name routing, renderer props and final theory
  endpoint remain compatible. See [Level 3 handoff](LEVEL3_HANDOFF.md).

## Validation and scope

[LEVEL3_PLAYER_PATH.md](LEVEL3_PLAYER_PATH.md) describes the two main player
routes and their limits. [LEVEL3_VALIDATION-v20.json](LEVEL3_VALIDATION-v20.json)
records the current checks and downloadable builds. The v17 report preserves
the effort-rule correction; v16 and earlier reports describe previous flows,
including removed aims, numerical examples and judgments.

These checks verify behaviour and packaging. They do not establish that this
is the best possible design or that classroom learning outcomes have improved.
Opening integration and Level 2's additional growth framing remain separate
work; neither is added by this Level 3 revision.
