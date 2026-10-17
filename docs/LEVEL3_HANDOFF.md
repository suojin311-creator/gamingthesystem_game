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
  teacher/Alex conversation; the next action appears with Alex’s second message.
- Results use the three evidence rows without an additional effort-summary box.
  Comparison cards have no repeated prose footnotes. Both player attempts and
  any system reference remain visible as actual data rows.
- Level 3 action footers have no explanatory left-side captions. Selection
  feedback stays next to the chosen-priorities list; unchanged-allocation
  validation is shown above the weight cards. Replay scene remains a control.
- Table typography is composed for the view: main metric names are 16px,
  compact names 15px, percentages 20px (19px compact) and effort labels 14px
  (13px phone) with medium
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
when present. No second player test is omitted. On narrow layouts cards wrap or
stack; typography is retained. The concern remains that scoring rules guide
Alex’s choices even when effort is distributed more evenly.

## Conversations and final placeholder

Teacher and Alex use ordinary speech bubbles throughout. The cloud-outline
mode, circular tails and Thinking labels are removed from the shared component.
Teacher and student portraits replace initial-letter avatars across all chapters,
including classroom notebook and checklist illustrations. Player names still
come from the opening-supplied prop, independently of the role artwork.

Level 3 conversations use submitted run snapshots and earlier trials. Publication
plans distinguish one higher reward, two higher rewards and near-even weights;
the second publication also recognizes whether the leading priorities changed.
Result questions describe actual increases/decreases in qualitative effort, or
acknowledge when changed weights left the effort bands unchanged. Each workbench
exchange gives Alex two short replies. Teacher questions and reactions advance
from planning to observed behaviour to comparing goals.

`workbenchDialogue` receives the full run history. `weightedSceneReply(request,
shotIndex)` varies a repeated metric/intensity reply according to earlier shots;
replaying that request keeps the same words. `comparisonDialogue(playerName,
runs)` describes the final actual pattern, including near-even-first trials and
both system references. It never assumes rebalancing happened in a particular
direction. Custom animation renderers can use these same narrative helpers.
Scene IDs, shot actions, intensity rules and result payloads are unchanged.

Level 1 has six metric-specific review questions. Level 2's three-metric exchange
uses the selected trio and its visible/quality/mixed branch. The final cinematic
and returned conversation make different points before leading into weighting.
All authored emoji remain distinct. `tests/dialogue_narrative.mjs` checks 8,640
complete three-level story paths for repeated dialogue/emoji, along with pattern
boundaries, unchanged effort bands and both comparison orders. Intentional
Replay scene repeats are exempt from that no-repeat story-path check.

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
Current checks are recorded in `LEVEL3_VALIDATION-v8.json`; older reports and
versioned ZIPs are historical. Managed Chromium tests exact offline HTML bytes
through an in-memory HTTPS origin; direct file opening in the user browser and
classroom load capacity are not claimed as tested.
