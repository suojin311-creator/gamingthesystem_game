# Player-led experiments (retained v16 flow, v17 rules)

The v15 source and downloads are frozen on `archive/pre-player-experiments-v15`
at `d3075b72950e8bf9a0f693d15cf37b95440cfe7d`.

The v16 source and downloads are frozen on `archive/pre-effort-rules-v16`
at `69f2bb4906a6d6c85442686180e49dc6a0800291`. The current revision corrects
the effort and narrative rules described in [effort rules](EFFORT_RULES.md).
It retains the aim selector, three required attempts and final judgment below.
Their player-path design remains unresolved and is a separate next task.

## Choose a purpose, then investigate

Each of the three weight editors asks the player to choose an aim: give all
three tasks attention, shift Alex’s priority, or keep Alex exploring. There is
no default and no scored correct choice. Choosing an aim does not move sliders
or clear confirmed values. The aim is recorded in that actual trial.

Explore / Adjust / Verify remain the three stages, but Verify no longer
requires a prescribed weight pattern. Every new positive integer split totaling
100 is accepted. Exact repeated allocations ask the player to reset and try a
new split. Different weights with identical effort bands remain valid evidence.
Three uneven or three near-even trials can reach comparison and completion.
No system reference trial is inserted, and no fourth trial is implied.

The first-use guide still teaches only controls: slide, confirm, adjust the
remaining pair, then run. Strategy help is collapsed under “Need a hint?”. After
choosing an aim, a player may read a goal-specific hint and explicitly apply an
editable example. Applying it never confirms or runs it. Suggestions are
examples, not progression requirements or a winning weighting.

## Feedback follows the player's question

Each result keeps the existing effort illustrations and adds one short finding
under the chosen aim. Shared attention can be acknowledged; moving a priority
can be distinguished from changing weights within the same effort bands. The
exploration aim remains unproven by score-directed effort, with the near-even
and other all-steady allocations showing a criteria → ticks → packing-up
sequence. This now depends on actual effort bands, not the near-even label.
Low-effort tasks remain unticked; a neglected task must not be presented as
meeting all requirements. Scoring-directed stopping is an independent narrative
observation across allocations, rather than a special punishment for balancing.

There is still only one teacher question and two short Alex replies per result.
The teacher follows the selected aim; the replies reflect the actual pattern.
Third-test language no longer assumes priorities necessarily changed. Uniform
effort histories are described as unchanged, even if their weights or
near-even labels differ. Repeat all-steady observations have different scene
replies without inventing new evidence.
Replay remains deterministic. No extra editing or publication dialogue is added.

## Judge the evidence

The comparison retains all three actual trials, their aims and explicit
More / Less / Same effort labels relative to the preceding trial. It asks whether
the player would keep the latest split for now or rethink the setup. Neither
choice is marked correct, given a score or blocked. The chosen judgment must
precede the final response, whose opening question acknowledges it.

The same replaceable scene chain ends at `theory.reveal`. No authored animation
scripts or opening assets are edited. Custom renderers still replace the entire
placeholder. There is no Design Lab navigation or player restart.

## Contract changes

- `WeightRun.intent?: 'attention' | 'priority' | 'exploration'` is set for every
  new player-confirmed trial. It is optional in the type for older host fixtures.
- `LevelThreeCinematicRequest.decision?: 'keep' | 'revise'` is supplied after the
  player's final judgment. Scene IDs, weighted shots and player-name routing stay
  the same. A custom renderer may use this additional context.
- Completion fires once on Watch Alex’s response after the three observations
  and explicit judgment. It returns the copied trials and `decision`.
- `compared` retains `{ nearEven, uneven }` for mixed histories. It is `null` for
  histories without both patterns; consumers must handle this. The all-runs
  payload and table are authoritative and always contain the three actual trials.

## Validation

[LEVEL3_VALIDATION-v17.json](LEVEL3_VALIDATION-v17.json) records the current
effort-rule correction and release validation.
`LEVEL3_VALIDATION-v16.json` is the historical report for
free third allocations, optional hints, aim-specific findings, both judgments,
uniform-pattern completion, partner callbacks and names, chapter handoff,
visible-time timing, responsive layouts and actual downloadable ZIPs. Dialogue
checks include all 20 metric trios and representative uniform/mixed histories
under all 27 purpose sequences. Existing v15/v14 reports remain historical.
These checks verify game behaviour rather than measured learning effectiveness.

## Pending player-path design

The three aims are not equivalent controllable outcomes: weight changes can
alter attention or priority but cannot guarantee exploration. Different aims
can still suggest the same weights, and three required trials can still yield
the same observed effort. The final keep/rethink gate also remains in place.
The v17 correction makes those observations causally consistent; it does not
claim that these flow problems have been solved. No new trial count, forced
contrast route, overlay guide or opening/cinematic integration is implemented
as part of this rule-only change.
