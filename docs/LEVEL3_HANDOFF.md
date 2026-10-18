# Level 3 — The Weighting Trap

The highlighted priority selector and weight editor use the opening-confirmed
player name. The connected host preselects Level 2’s original three choices;
players may swap them before weighting. A standalone Level 3 starts empty.
The [chapter transition](CHAPTER_TRANSITIONS.md) closes the long checklist and
returns those actual three cards with slider artwork under a large LEVEL 03
title. Without an inherited trio, the artwork shows unassigned priorities. One
teacher line replaces the old opening conversation; an explicit entry button
waits for the player after about three visible seconds. The artwork does not
change selection or allocate weights.

The shared short-name icon cards feed three removable/reviewable selection
slots. Full metric definitions appear in the tray. Alex task vignettes now lead
the results and comparison; they match each row’s existing qualitative effort
category. See [visual operations](VISUAL_PLAY.md).

## Tests and observations

- Three positive integer weights total exactly 100%, each at least 1% and at most 98%. Native and accessible slider bounds reserve 1% for every other unlocked priority; publication rejects zero weights.
- Moving an unlocked slider divides the remainder among other unlocked sliders.
  Confirmed values stay locked, and a one-point remainder follows card order.
- Confirm any first card, then adjust either remaining card. Confirming either
  final card locks both; the other button turns gray and reads Auto-confirmed.
  The 80/10/10 → 80/15/5 case works in every confirmation order.
- Reset weights resets only the current allocation. It sits below the allocation
  bar, above the action row; there is no player Restart-level control or dialog.
- Publication ticks the three weights and waits for Observe the class.
  Management satisfaction starts at Level 2’s final value and rises a little
  after each completed publication, irrespective of the chosen split. The small
  evidence line retains the three priorities and 100% allocation. Replaying or
  comparing adds nothing; near-even weights earn no bonus. See the shared
  [satisfaction checkpoints](MANAGEMENT_SATISFACTION.md).
  Students remains Awaiting
  observation until its current classroom response has been observed.
- The scene has exactly three selected metric/intensity shots, using the 18
  Narrative V2 behaviours. Returning reveals qualitative effort rows, then the
  teacher/Alex conversation; the next action appears with Alex’s second short message. Weight editing, publication and comparison contain no workbench dialogue.
- Results use the three evidence rows without an additional effort-summary box.
  A single neutral table aligns all tests in adjacent columns, with each metric label shown once. Each cell explicitly states First result, Same effort, More effort or Less effort; the second column compares with the first test and the third with the second. Whole-cell highlight fills have been removed; near-even does not receive a success colour. All three player-confirmed attempts remain visible as actual data rows.
- Level 3 action footers have no explanatory left-side captions. Selection
  feedback stays next to the chosen-priorities list; unchanged-allocation
  validation is shown above the weight cards. Replay scene remains a control.
- Table typography is composed for the view: main metric names are 16px,
  comparison names 16px, percentages 20px (18px in comparison) and effort labels 14px
  (13px in comparison, 12px in narrow comparisons) with medium
  weight. Qualitative bars are slimmer. The columns retain aligned headings
  and a quiet divider. There are no invented numerical effort percentages.

Every task uses its own weight for effort: **1–24% low, 25–66% medium and
67–98% high**. Near-even means highest minus lowest at most **10 percentage
points**, including 10. It only describes the allocation and never changes
effort or selects a separate criticism. Thus 38/33/29 and 40/30/30 qualify;
40/31/29 does not, but all three allocations still produce three medium shots.
Changed weights within the same bands are valid unchanged observations. These
categories are narrative choices, not measured learning gains or losses. See
[effort rules](EFFORT_RULES.md).

## Explore, Adjust and Verify

Level 3 has three player-confirmed tests. Each editor asks the player to choose
an aim: give all three attention, shift Alex’s priority, or keep Alex exploring.
No aim is selected automatically. Choosing one preserves the current weights.
The result's short finding and teacher question follow that chosen aim.

Strategy help is collapsed under “Need a hint?”. “Apply suggested weights” only
loads editable unconfirmed values; it never runs a trial. The optional example
responds to the aim and avoids exact prior allocations. Players can ignore it.

Every new positive split can run, including three uneven or three near-even
tests. Verify does not prescribe a pattern, an effort change, or a correct answer.
Exact allocation repeats are rejected; changed weights with unchanged effort
are accepted. Reset restores the immediately previous trial. Comparison contains
First/Second/Third test, each `kind: 'player'`, with no system reference.

After comparing, the player judges whether to keep the latest split or rethink
the setup. Both choices are accepted and the final response acknowledges that
judgment. See [player-led experiments](PLAYER_EXPERIMENTS.md).

These required aims, three attempts and final judgment are the retained v16
flow. Their educational purpose and player path remain under review. The v17
effort correction does not remove these gates or claim that the path is fixed.

## First-use weight guide

The four-step, nonmodal guide appears automatically the first time the editor
opens during a visit: move any slider → confirm the chosen value → adjust and
confirm either remaining value (locking the pair) → Run evaluation. It follows
actual controls, supports keyboard input and does not prescribe percentages.
The same edited/confirmed values become the first actual trial.

Skip guide and Escape close it; Guide in the editor header reopens it at the
current control state. Reset restarts the instructions if the guide is open,
without replaying it automatically on later tests. Reopening the page starts a
fresh visit. The inline guide remains reachable on narrow screens; highlighted
controls retain normal keyboard focus indicators.

## Conversations and final placeholder

Teacher and Alex use ordinary speech bubbles throughout. The cloud-outline
mode, circular tails and Thinking labels are removed from the shared component.
Teacher and student portraits replace initial-letter avatars across all chapters,
including classroom notebook and checklist illustrations. Player names still
come from the opening-supplied prop, independently of the role artwork.

Each observation has one concise teacher question and two short Alex replies.
Weight editing, publication and the comparison table have no workbench dialogue;
the final response cinematic develops the scoring-system conclusion once.
`workbenchDialogue` receives the run history but returns lines only for `result`.
Questions follow actual effort changes, including an unchanged routine when the
weights changed within the same bands.

Any all-medium allocation shows a visible-time sequence: checking criteria,
collecting ticks and packing up. This includes uneven splits such as 40/31/29;
the split label does not select the sequence. The student card describes the
scoring stopping rule, while actual effort bands determine its contextual
wording. An uneven or low-effort run still exposes score-directed stopping,
without claiming that all tasks received attention or all requirements were
met. Neglected low-effort tasks receive no completion tick. The risk concerns
stopping at scoring requirements, not a claimed learning loss or a special
penalty for balancing. The sequence holds while hidden or off-screen; reduced
motion removes movement.

`weightedSceneReply(request, shotIndex)` keeps repeat observations fresh and
replays deterministic. `weightedSceneAction(request, shotIndex)` supplies the
task/criterion/stop behaviour for each metric. Medium-shot criteria actions and
replies apply to every all-medium run, independently of near-even classification.
Custom animation hosts can use both helpers. Existing scene IDs and prop shapes
are unchanged; the per-item effort threshold changed in v17. The contract below
retains trial aims and the final judgment. The partner's finished videos and
authored scripts remain separate and unchanged.

`comparisonDialogue(playerName, runs, decision)` has three brief lines and describes the
player’s keep/rethink judgment without treating it as a correctness test. Its
summary follows the observed effort bands: a history with unchanged bands must
not claim that Alex's effort moved with each new split. Comparison trial headings and weight-pattern labels are larger: 12px on
desktop and 11px at phone widths. All authored emoji remain distinct. `tests/dialogue_narrative.mjs` checks 8,640 complete combination paths
for repeated lines/emoji; Replay scene intentionally preserves its established
lines. See [Level 3 focus revision](LEVEL3_FOCUS.md) for the saved baseline and
accepted visual/narrative scope.

The replaceable scene chain is `level3.weights` for each test, then
`level3.compare` for Alex’s response, then `theory.reveal`. The final theory
placeholder stays on its last frame. There is no completion page or Design Lab
transition. The existing `onDesignLab` prop is reserved and never invoked in
this revision, including after duplicate theory callbacks.

## Partner contracts

`Gameplay` passes `playerName`, Level 2’s original `selectedMetricIds`, sound
preference and any `renderLevelThreeCinematic` to Level 3. Direct hosts can pass
`initialMetricIds`. A custom scene renderer receives this shape:

```ts
{
  sceneId: 'level3.weights' | 'level3.compare' | 'theory.reveal',
  kind: 'weights' | 'comparison' | 'theory',
  playerName: string,
  decision?: 'keep' | 'revise',
  runs: Array<{
    round: number,
    kind: 'player' | 'balance-check' | 'contrast-check',
    metricIds: MetricId[],
    weights: [number, number, number],
    intent?: 'attention' | 'priority' | 'exploration'
  }>,
  shots: Array<{
    sceneId: string, // e.g. level3.prep.high
    metricId: MetricId,
    weight: number,
    effort: 'low' | 'medium' | 'high'
  }>
}
```

`shots` has three entries for weight scenes and is empty for comparison/theory.
Keep LevelThree mounted during a scene. Its completion callback returns weight
scenes to results and advances comparison to theory; a theory callback does not
advance to another screen. The finished opening/cinematics remain separate.

`onComplete` / `onLevelThreeComplete` fires once on Watch Alex’s response,
after all three observations and an explicit keep/rethink judgment. It returns
`selectedMetricIds`, all copied `runs`, `decision: 'keep' | 'revise'` and
`compared: { nearEven, uneven } | null`. A mixed history retains the copied pair;
a history without both patterns returns `null`, so hosts must handle that case.
The table and all-runs payload always retain all three actual tests.

## Lifetime and validation

All state stays in page memory. Reload, reopen and restored pages start fresh;
there is no persistence or administrator/login implementation. Hidden tabs and
off-screen timed information hold their remaining delay. The Level 1 guide also
holds that level’s pending information. Player Restart controls are removed
across all three chapters; Reset weights is retained.

`npm run package:previews` builds all four entries plus
`play/Level3-and-Full-game-play.zip`, containing standalone Level 3 and connected
Levels 1–3. `play/LATEST.json` records source, build, ZIP and bundle hashes.
`tests/release.py` verifies the actual downloads and their complete flows.
Current checks are recorded in [LEVEL3_VALIDATION-v17.json](LEVEL3_VALIDATION-v17.json); v16 retains the preceding player-led-flow checks, and v15/v14 retain their broader checks; older reports and
versioned ZIPs are historical. Managed Chromium tests exact offline HTML bytes
through an in-memory HTTPS origin; direct file opening in the user browser and
classroom load capacity are not claimed as tested.

The v12 Level 3 forecast page and prediction/result fields have been withdrawn. Confirmed weights run directly into publication; all three player-confirmed tests publish directly after Run evaluation. The positive-weight rule remains. See [current feedback corrections](LEARNING_OPTIMIZATIONS.md).
