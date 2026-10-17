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
emoji. The chapter waits for its lower-right Choose priorities button.

The teammate’s Screens 3–5 and final reveal remain replaceable story readings.
The weight scene plays exactly three selected metric shots, using Narrative V2’s
18 low/medium/high actions and lines. The comparison reading retains the
document’s exchange about following percentages. Goodhart’s Law appears only in
the final story slot, after the player has tested both patterns. The opening and
finished videos have not been merged.

## Weight rules

- Choose any three different metrics from the shared six. Selected cards enter
  the dashboard in catalog order; later tests keep those same three metrics.
- Every selected metric starts at 34/33/33, can receive 10–80%, and must be
  confirmed separately. The 10% minimum comes from the supplied HTML prototype.
- Sliders use whole percentage points. Moving an unlocked slider divides the
  remainder among other unlocked sliders; a one-point remainder goes in card
  order. Totals always equal 100%, with confirmed values untouched.
- Each slider shares a visual 0–100 scale. The actual available maximum appears
  on its card and in accessibility attributes. Values clamp to the available
  allocation. A final remaining slider is fixed but still needs confirmation.
- Confirming locks only that card. Reset weights restores the current round’s
  baseline and clears confirmations. Run requires all three confirmations.
- Publishing ticks the three weights in sequence, then automatically opens the
  classroom slot. Returning reveals three qualitative responses in sequence.
  Each update has an audio cue; all information stays available afterward.

Near-even means highest minus lowest is at most five percentage points. All
three story shots are medium in that case, including 34/33/33. Otherwise,
10–33% produces low, 34–66% medium and 67–80% high effort in this editor.
These are deterministic narrative categories, not measured learning outcomes.
The prototype’s invented numerical effort transform is not presented as data.

## Adaptive paths

| First run | Second task | Then |
| --- | --- | --- |
| Near-even | Create a contrast, spread at least 20 points | Compare the two actual runs |
| Uneven | Rebalance, with a smaller spread than the first run | Compare if near-even |
| Uneven, then improved but still uneven | Explicit Test 34 / 33 / 33 action publishes a third balance check | Compare the original uneven run with that tested balance check |

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
theory leads to the ending/Design Lab handoff.

`onComplete` / `onLevelThreeComplete` reports the completed experiment once after
both patterns have been compared. The payload contains `selectedMetricIds`, all
`runs`, and `compared: { nearEven, uneven }`. Clicking the comparison’s next
button also settles the callback before leaving if its reading delay has not
finished. Replay never reports it twice. The optional Design Lab callback runs
only from its final button; without a callback that button remains reserved.

LevelTwo now has an optional `onContinue(result)` callback. The combined host
supplies it and enables Continue to Level 3. The standalone Level 2 entry leaves
it absent, so that download still ends at Level 2. Level 1 standalone behaviour
is unchanged. Audio preference carries across all three levels during one run.

## Lifetime and accessibility

All state lives in memory. Reload, reopen and restored pages restart. Restart
clears Level 3 choices and tests while keeping the opening-supplied name. Hidden
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
`docs/LEVEL3_VALIDATION-v1.json`.
