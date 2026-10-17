# Level 3 — The Weighting Trap

## Gameplay and narrative ownership

The highlighted Screens 1–2 are implemented as the playable priority selector
and weighting dashboard. Both use the current opening-supplied player name and
first-person player decisions. The revised game-side lines are:

- Chapter introduction: “I’ll choose three priorities and decide how much each one counts.”
- Weight dashboard: “I’ll test whether these weights change how Alex spends his effort.”

The first makes the choice and meaning of a weight explicit. The second asks
about observable effort, rather than claiming a measured change in learning.
Alex’s introduction uses two short messages, typing dots and one new distinct
emoji. The chapter waits for its lower-right Choose priorities button (Review priorities when the Level 2 trio is inherited). Separate bottom conversations explain weight tests, Alex’s choices and the optional nearly-equal balance check.

The teammate’s Screens 3–5 and final reveal remain replaceable story readings.
The weight scene plays exactly three selected metric shots, using Narrative V2’s
18 low/medium/high actions and lines. The comparison reading retains the
document’s exchange about following percentages. Goodhart’s Law appears only in
the final story slot, after the player has tested both patterns. The opening and
finished videos have not been merged.

## Weight rules

- Choose any three different metrics from the shared six. Selected cards enter
  the dashboard in catalog order; later tests keep those same three metrics.
- The connected game preselects the actual Level 2 trio. Players can deselect and swap before entering the editor. The standalone entry starts empty. Restart restores the inherited starting trio and clears the Level 3 tests.
- Every selected metric starts at 34/33/33 and can receive 0–100%. The former prototype’s 10% minimum was removed to support splits such as 80/15/5.
- Sliders use whole percentage points. Moving an unlocked slider divides the remainder among other unlocked sliders; a one-point remainder goes in card order. Totals always equal 100%, with confirmed values untouched.
- Each slider shares a visual 0–100 scale. After the first confirmation, the actual remaining maximum appears on unlocked cards and in accessibility attributes. Both unlocked sliders remain editable, including when their current values match.
- The first confirmation locks one card. Confirming either remaining card locks both; the other button is gray and reads Auto-confirmed. Both buttons remain available before that choice so confirmation order is free. Reset weights restores the current round’s baseline and clears confirmations. Run requires a valid, fully confirmed allocation and the current round’s goal.
- Reset sits below the allocation bar, above the action row. Teacher/Alex bubbles have a separate bottom region, matching the earlier levels. Repeated instructions and the illustrative-behaviour note are removed. Shared metric name typography and aligned Score weight/Alex’s response columns apply to all layouts.
- Publishing ticks the three weights in sequence and stays on screen with Management and Students perspectives. The player clicks Observe the class to open the three-shot classroom slot. Students remains Awaiting observation until the current round’s classroom responses are available. Returning reveals three qualitative responses, then the teacher/Alex exchange; the next action appears with Alex’s last message.

Near-even means highest minus lowest is at most five percentage points. All
three story shots are medium in that case, including 34/33/33. Otherwise,
0–33% produces low, 34–66% medium and 67–100% high effort in this editor.
These are deterministic narrative categories, not measured learning outcomes.
The prototype’s invented numerical effort transform is not presented as data.

## Adaptive paths

| First run | Second task | Then |
| --- | --- | --- |
| Near-even | Create a contrast, spread at least 20 points | Compare the two actual runs |
| Uneven | Rebalance, with a smaller spread than the first run | Compare if near-even |
| Uneven, then improved but still uneven | Explicit Test 34 / 33 / 33 action publishes a third balance check | Compare the original uneven run with that tested balance check |

The 34/33/33 check is not an automatic reset after two attempts: it appears only if both tested splits are still uneven. The player first says “It’s still uneven. I’ll test a nearly equal split.” A click publishes a third run, followed by the same manual Observe flow. If both patterns have already been tested, the game goes straight to comparison.

The compare view identifies each run and distinguishes the system’s balance
check from a player-selected test. Run snapshots are copied before sharing.
Near-even visibly improves effort distribution; the remaining concern is that
the scoring rules still direct Alex’s choices. No declining student health or
unsupported learning percentage is shown.

## Integration

`Gameplay` connects Level 1 → Level 2 → Level 3 in page memory. Its required
`playerName` comes from the opening once; there is no second name form. The host
accepts `renderLevelThreeCinematic`, `onLevelThreeComplete` and `onDesignLab`:

```tsx
<Gameplay
  playerName={playerName}
  renderLevelThreeCinematic={(request, complete) => (
    <PartnerScene request={request} onComplete={complete} />
  )}
  onLevelThreeComplete={result => setWeightingResult(result)}
  onDesignLab={() => setCurrentScene('design-lab')}
/>
```

The replaceable renderer receives:

```ts
{
  sceneId: 'level3.weights' | 'level3.compare' | 'theory.reveal',
  kind: 'weights' | 'comparison' | 'theory',
  playerName: string,
  runs: Array<{
    round: number,
    kind: 'player' | 'balance-check',
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

`shots` contains three entries for a weight scene and is empty for comparison
and theory. Call `complete()` at the end of the full scene, keeping LevelThree
mounted. A weight scene returns to its observation; comparison leads to theory;
theory goes directly to Design Lab. There is no experiment-complete page.

`onComplete` / `onLevelThreeComplete` reports the completed experiment once after
both patterns have been compared. The payload contains `selectedMetricIds`, all
`runs`, and `compared: { nearEven, uneven }`. Clicking the comparison’s next
button also settles the callback before leaving if its reading delay has not
finished. Replay never reports it twice. The optional `onDesignLab` callback runs once automatically when `theory.reveal` calls `complete()`, including when a renderer accidentally calls twice. The host should route straight to its Design Lab. Without that host route, previews show a minimal Design Lab destination; the lab’s interactions are still reserved.

LevelTwo now has an optional `onContinue(result)` callback. The combined host
supplies it, retains `result.selectedMetricIds` in page memory and enables Continue to Level 3. The standalone Level 2 entry leaves
it absent, so that download still ends at Level 2. Level 1 standalone behaviour
is unchanged. Audio preference carries across all three levels during one run.

## Lifetime and accessibility

All state lives in memory. Reload, reopen and restored pages restart. Restart
clears Level 3 tests and restores the inherited starting choices while keeping the opening-supplied name. Hidden
tabs, off-screen timed information and restart dialogs hold pending beats.
Keyboard-operated cards/sliders/buttons, focus return, reduced motion, no-audio
fallback and 320px layouts are covered by browser checks.

## Build and checks

`npm run build:level3` creates the self-contained Level 3 entry. Run
`npm run package:previews` to rebuild all three standalone ZIPs and the combined
three-level game together. Latest artifact hashes are in `play/LATEST.json`.

```sh
node tests/level3_rules.mjs
python tests/level3.py
python tests/level3_feedback.py
# With npm run dev running:
python tests/level3_integration.py
python tests/level2_integration.py
python tests/player_identity.py
python tests/release.py
node tests/dialogue_emojis.mjs
```

The offline checks serve exact production HTML through an in-memory HTTPS
origin; managed Chromium blocks local file navigation. They are functional
checks, not a classroom load test. Results and artifact hashes are recorded in
`docs/LEVEL3_VALIDATION-v2.json`.
