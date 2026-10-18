# Level 3 — The Weighting Trap

The highlighted priority selector and weight editor use the opening-confirmed
player name. The connected host preselects Level 2’s original three choices;
players may swap them before weighting. A standalone Level 3 starts empty.

The shared short-name icon cards feed three removable/reviewable selection
slots. Full metric definitions appear in the tray. Alex task vignettes now lead
the results and comparison; they match each row’s existing qualitative effort
category. See [visual operations](VISUAL_PLAY.md).

## Tests and observations

- Three integer weights total exactly 100%, each allowed from 0–100%.
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
  A single neutral table aligns all tests in adjacent columns, with each metric label shown once. Cells with changed effort have a restrained marker; near-even does not receive a success colour. Both player attempts and
  any system reference remain visible as actual data rows.
- Level 3 action footers have no explanatory left-side captions. Selection
  feedback stays next to the chosen-priorities list; unchanged-allocation
  validation is shown above the weight cards. Replay scene remains a control.
- Table typography is composed for the view: main metric names are 16px,
  comparison names 16px, percentages 20px (18px in comparison) and effort labels 14px
  (13px in comparison, 12px in narrow comparisons) with medium
  weight. Qualitative bars are slimmer. The columns retain aligned headings
  and a quiet divider. There are no invented numerical effort percentages.

Near-even means highest minus lowest at most **10 percentage points**, including
10. Thus 38/33/29 and 40/30/30 qualify; 40/31/29 does not. Near-even produces three
medium story shots. Otherwise 0–33% is low, 34–66% medium and 67–100% high effort.
These categories are narrative choices, not measured learning gains or losses.

## Free second attempt and a missing reference

After the first observation, Try another split opens the editor. The only extra
requirement is to change the allocation. Neither the title, teacher dialogue nor
Run gate requires the player to make it more even or reach a specific spread.

| Two player tests | Next |
| --- | --- |
| One near-even, one uneven | Compare the two actual player tests |
| Both uneven | What if they counted equally? offers a 34/33/33 system reference |
| Both near-even | What if one counted more? offers a 70/20/10 system reference |

The reference is explicitly identified, requires a click, and uses the same
publication → Observe → classroom → results flow. The comparison displays all
actual runs in order: Your first test, Your second test, and System reference
when present. No second player test is omitted. On narrow layouts each metric label spans the table, followed by the same two or three trial columns. All actual records remain visible. The concern remains that scoring rules guide
Alex’s choices even when effort is distributed more evenly.

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

Near-even effort stays medium on all three metrics. It also shows a visible-time
sequence: checking criteria, collecting ticks and packing up. The student card
reads “Stops when the criteria are met.” The first near-even review asks about
exploring further; Alex asks whether that earns extra points and says he is done
if it does not. The risk concerns the stopping rule, not a claimed learning loss.
The sequence holds while hidden or off-screen; reduced motion removes movement.

`weightedSceneReply(request, shotIndex)` keeps repeat observations fresh and
replays deterministic. `weightedSceneAction(request, shotIndex)` supplies the
near-even task/criterion/stop behaviour for each metric. Custom animation hosts
can use both helpers. Existing scene IDs, effort thresholds and result payloads
are unchanged. The partner's finished videos remain separate.

`comparisonDialogue(playerName, runs)` has three brief lines and describes the
actual final pattern in either experiment order. All authored emoji remain
distinct. `tests/dialogue_narrative.mjs` checks 8,640 complete combination paths
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
  runs: Array<{
    round: number,
    kind: 'player' | 'balance-check' | 'contrast-check',
    metricIds: MetricId[],
    weights: [number, number, number]
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

`onComplete` / `onLevelThreeComplete` fires once when the comparison is read or
its next action is clicked. It returns `selectedMetricIds`, every copied `run`
and `compared: { nearEven, uneven }`. The compared pair remains compatible while
the UI and all-runs payload also retain the second test and any reference.

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
Current checks are recorded in `LEVEL3_VALIDATION-v9.json`; older reports and
versioned ZIPs are historical. Managed Chromium tests exact offline HTML bytes
through an in-memory HTTPS origin; direct file opening in the user browser and
classroom load capacity are not claimed as tested.
