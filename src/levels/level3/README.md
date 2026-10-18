# Level 3 — The Weighting Trap

- `LevelThree.tsx`: chapter entry, editable inherited trio, linked confirmation,
  publication, evidence-led return to editing, two-test comparison and optional
  third trial.
- `experiments.ts`: adaptive questions, optional verbal hints, actual-observation
  context and distinct-allocation validation. No required experiment aims or
  numerical suggestions.
- `ExperimentPrompt.tsx`: short evidence-led question, finite visible-time
  attention pulses and collapsed Need a hint? text.
- `WeightGuide.tsx`: four static spotlight steps with Next, Back, Skip and Escape;
  explains controls without practice or changing weights.
- `weights.ts`: exact positive allocation, locked-value invariants, per-item
  effort thresholds and descriptive near-even classification.
- `dialogue.ts`: concise observed-result exchanges and final cinematic dialogue;
  editing, publication and comparison operations remain silent.
- `data.ts`: 18 Narrative V2 behaviours, copied runs, cinematic and result types.
- `CinematicPlaceholder.tsx`: three selected shots, Alex's comparison response
  and theory slot; custom partner scenes replace the full placeholder.
- `styles.css`: scoped `.level-three` layout, ranges, observations and responsive
  two-/three-test comparison; `guide.css` owns the modal spotlight presentation.

The Gameplay host passes the opening-confirmed name, original Level 2 trio and
page-local sound setting. `initialMetricIds` preselects the cards without
preventing changes; standalone Level 3 starts empty. The standalone Level 1/2
entries still stop at their respective endings.

The first allocation is free. The second editor keeps the last observation in
view and asks a question based on its actual effort bands. Every new valid
split is accepted, even when the bands remain unchanged. After two observed
tests the player can compare and Watch Alex's response, or optionally Test
another idea. The latter adds one third test, not a reference or a compulsory
pattern. No aim radios or keep/rethink judgment gate remain.

Weights total 100% and reserve at least 1% for each task. Effort follows only
each task's own weight: 1–24% minimum, 25–66% steady and 67–98% intense.
Near-even means a highest-to-lowest spread of at most ten percentage points;
it does not override effort. Thus 40/30/30 → 40/31/29 leaves three steady
responses. Findings must not invent a changed effort band from changed weights.

The scoring stopping rule is independent of that label. All-steady runs show
criteria/ticks/packing up; low-effort tasks remain unticked. Improved coverage
can be acknowledged without claiming deeper learning or measured learning loss.
Comparison explicitly labels First result / Same effort / More effort / Less
effort against the immediately previous test. It keeps all actual trials and
does not display a system reference or aim headings.

The current UI does not populate the legacy optional `WeightRun.intent`,
cinematic `decision` or optional result `decision`. Completion fires once on
Watch Alex's response after two or three observations and copies all runs.
`compared` remains a near-even/uneven pair or null for uniform-pattern histories.
The scene chain ends at the final theory placeholder. `onDesignLab` is reserved
and never called; no player Restart control is present.

Run `npm run dev -- --mode level3` for direct development,
`npm run build:level3` for its HTML, or `npm run package:previews` to refresh all
latest individual/combined downloads together. Latest standalone entry:
`play/Level3-play.zip`.

See [player path](../../../docs/LEVEL3_PLAYER_PATH.md),
[partner handoff](../../../docs/LEVEL3_HANDOFF.md),
[player-led experiments](../../../docs/PLAYER_EXPERIMENTS.md) and
[effort rules](../../../docs/EFFORT_RULES.md). Current validation:
[v18](../../../docs/LEVEL3_VALIDATION-v18.json); v17 and earlier are historical.
