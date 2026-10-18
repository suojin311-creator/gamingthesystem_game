# Level 3 — The Weighting Trap

The connected host preselects Level 2's original three choices with the same
opening-confirmed player name. Players may swap those choices before weighting;
standalone Level 3 starts empty. The chapter transition closes the long
checklist and returns the three actual cards with slider artwork and LEVEL 03.
Its entry waits after about three visible seconds. Without inherited choices,
artwork shows unassigned priorities. It never allocates weights.

Short-name icon cards feed removable selection slots; full definitions stay in
the tray. Alex task vignettes lead results and comparison and follow each task's
actual qualitative effort. See [visual operations](VISUAL_PLAY.md).

## Current player path

1. Choose or review the three priorities, then make a free first allocation.
2. Confirm and publish the weights. Observe the class is a manual action.
3. Watch the selected classroom shots and read the three effort rows and brief
   teacher/Alex exchange.
4. Return to editing for a second allocation. The editor retains Last observation
   with all three actual task/effort pairs. Its short question follows neglected
   tasks, shared attention or unchanged effort, not a required aim.
5. After the second observation, Compare the results shows both actual trials.
   Watch Alex's response continues directly without a keep/rethink question.
6. Test another idea optionally returns from comparison for a third experiment.
   After its observation, comparison retains all three tests. No fourth is added.
7. Alex's response leads to the theory reveal. The preview stops there.

Need a hint? is optional, collapsed verbal support. It offers no numbers and
cannot set sliders. There are no goal radios, numerical suggestions, system
references, prescribed patterns or repeated aim/finding boxes. A near-even first
allocation is legitimate evidence. Changed values with the same effort bands
are accepted and described as unchanged, not a failed or newly changed result.
Exact repeats of earlier allocations are rejected. Reset restores the previous
observed allocation, or unassigned dashes before the first test.

See [player path](LEVEL3_PLAYER_PATH.md) and
[player-led experiments](PLAYER_EXPERIMENTS.md). The preceding v16/v17 gates are
historical; they are not prerequisites in this revision.

## Allocation, reports and evidence

- The first editor has no allocation (`null` locally): three dashes, sliders at the start, Confirm and Run disabled. A deliberate move of any slider creates positive weights and divides the remainder between the other two. Unassigned range positions are not zero-valued trial weights and never enter callbacks or effort calculations.
- Three positive integer weights total exactly 100%; each is 1–98%. Native and
  accessible range bounds reserve the minimum for other unlocked priorities.
  Publication rejects zero weights.
- Moving an unlocked slider preserves the ratio of other unlocked shares,
  with positive integer rounding in card order. Confirmed values stay locked.
- Confirm any first card, then adjust either remaining card. Confirming either
  final card locks both, with the other button gray and Auto-confirmed. The
  80/10/10 → 80/15/5 case works in every confirmation order.
- Reset weights resets only the current editor. It sits below the weight cards and above the action row. There is no player Restart-level control.
- Publication ticks three weights and waits for Observe the class. Management
  satisfaction begins at Level 2's final checkpoint and rises slightly with
  completed publications, irrespective of the split. Replays and comparison add
  nothing; near-even receives no bonus. Its evidence line retains three
  priorities and 100% allocation. See [satisfaction](MANAGEMENT_SATISFACTION.md).
- The Students card stays Awaiting observation until the current response is
  observed. The result reveals three qualitative rows, then the conversation.
  The next action appears with Alex's second short message. Editing, publication
  and comparison contain no workbench dialogue.
- One neutral table keeps the two or three actual tests in adjacent columns and
  each metric name once per row. Cells label First result, Same effort, More
  effort or Less effort. Later columns name the immediately previous test as
  their comparison basis; metric identity is retained when comparing records.
  Weight changes alone are not effort changes. No full-cell change fills, aim
  headings, system-reference column or summary footnotes are added.
- Percentages are quiet scoring references. Illustrated actions and qualitative
  effort remain the main evidence; there are no numerical effort percentages.
  Level 3 action footers carry controls without explanatory left-side captions.

Each task compares its reward with both alternatives, treating differences up to
10 percentage points as similar. More clearly higher comparisons gives high
effort, more lower comparisons gives low effort, and a tie gives medium.
49/26/25 and 49/27/24 both yield high/low/low; 45/45/10 yields high/high/low;
34/33/33 yields medium/medium/medium; 60/30/10 yields high/medium/low.
Near-even still means highest minus lowest at most 10points. There is no global
override or absolute 24/25cutoff. These are qualitative relative categories and
the tolerance is a game rule, not an empirical effort or learning model.
See [effort rules](EFFORT_RULES.md).

## First-use weight guide

The four-step modal spotlight appears once when the editor first opens during a
visit. It points to a slider, Confirm, the linked remaining pair and Run. Next
and Back move through static explanations; Try your weights closes the last
step. Skip guide and Escape close it early. Guide in the editor header reopens
it. The guide neither asks for practice nor changes or confirms any percentage.
It explains controls, not which allocation to use.

The spotlight follows its target on desktop and narrow screens. Dialog focus
stays within the guide while it is open, and closing returns focus to the editor.
Reopening the page starts a fresh visit. State remains page-local.

## Conversations and scene slots

Teacher and Alex use ordinary speech bubbles. Distinct role portraits replace
initial-letter avatars, independently of the player name. Every observation has
one concise teacher question and two short Alex replies. Questions and findings
follow actual effort bands and changes, including improved coverage or an
unchanged routine. Replays remain deterministic.

Any all-medium allocation shows criteria → ticks → packing up in visible time,
including uneven splits such as 40/31/29. Low-effort tasks remain unticked. The
risk concerns stopping at scoring requirements; it must not imply that every
requirement was met in neglected tasks, measured learning loss or a special
penalty for balancing. Improved attention and score-directed stopping can both
be acknowledged. Hidden or off-screen sequences hold; reduced motion removes
movement.

`weightedSceneReply(request, shotIndex)` and
`weightedSceneAction(request, shotIndex)` supply the task/criterion/stop context.
Medium criteria actions apply to all-medium runs regardless of near-even.
`comparisonDialogue(playerName, runs, decision?)` retains compatibility with old
hosts, while the current UI does not supply a decision. Its three brief lines
follow the two- or three-test evidence. Unchanged-band histories must not claim
that effort moved with every new split.

The replaceable chain is `level3.weights` for each trial, then `level3.compare`
for Alex's response, then `theory.reveal`. Custom renderers replace the complete
placeholder. No partner-authored script or opening asset is changed. The theory
placeholder remains on its last frame; there is no completion page or Design
Lab navigation. Reserved `onDesignLab` is never called, including after duplicate
final callbacks.

## Partner contracts

`Gameplay` passes `playerName`, Level 2's original `selectedMetricIds`, sound
preference and any `renderLevelThreeCinematic`. Direct hosts can pass
`initialMetricIds`. A custom renderer receives:

```ts
{
  sceneId: 'level3.weights' | 'level3.compare' | 'theory.reveal',
  kind: 'weights' | 'comparison' | 'theory',
  playerName: string,
  decision?: 'keep' | 'revise', // legacy context; not populated by current UI
  runs: Array<{
    round: number,
    kind: 'player' | 'balance-check' | 'contrast-check',
    metricIds: MetricId[],
    weights: [number, number, number],
    intent?: 'attention' | 'priority' | 'exploration' // legacy; not populated
  }>,
  shots: Array<{
    sceneId: string, // e.g. level3.prep.high
    metricId: MetricId,
    weight: number,
    effort: 'low' | 'medium' | 'high'
  }>
}
```

New trials always have `kind: 'player'`. The older kind/intent/decision fields
remain accepted for host compatibility. `shots` has three entries for weight
scenes and is empty for comparison/theory. Keep LevelThree mounted during a
scene. Complete callbacks return weight scenes to results, comparison to theory
and leave theory at its endpoint.

`onComplete` / `onLevelThreeComplete` fires once on Watch Alex's response after
**two or three observed tests**, without a judgment gate. It returns:

```ts
{
  selectedMetricIds: MetricId[],
  runs: WeightRun[],
  compared: { nearEven: WeightRun, uneven: WeightRun } | null,
  decision?: 'keep' | 'revise' // omitted by current UI
}
```

The arrays, tuples and compared pair are copied. `compared` is null if the
history lacks either pattern class; hosts must support that. The all-runs
payload and table retain every actual test and are authoritative. No completion
fires merely for opening comparison or opting into the third experiment.

## Lifetime and validation

All state stays in page memory. Reload, reopen and restored pages start fresh;
there is no persistence, login or administrator implementation. No player
Restart control is present. Names and sound routing remain shared in the
combined game; standalone entries use their existing defaults.

`npm run package:previews` builds all four entries and
`play/Level3-and-Full-game-play.zip`. That review archive contains standalone
Level 3 and connected Levels 1–3 from the same builds. `play/LATEST.json` records
source/build/ZIP hashes. `tests/release.py` verifies the actual downloads.
Current checks are recorded in [LEVEL3_VALIDATION-v21.json](LEVEL3_VALIDATION-v21.json).
The v17 report preserves the effort-rule correction; v16 and older reports and
versioned ZIPs remain historical. Managed Chromium tests exact offline bytes
through an in-memory HTTPS origin. Direct file opening in a particular user's
browser, classroom load capacity and learning effectiveness are not established
by those checks.

This scope adds an unassigned first editor while retaining the relative effort
model and free two-/three-test path. Level 2's additional growth framing is
included in the current packages; opening integration remains separate. The withdrawn
v12 prediction page and extra peer-script prototype are not reintroduced.
