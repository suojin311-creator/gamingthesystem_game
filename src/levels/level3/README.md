# Level 3 — The Weighting Trap

- `LevelThree.tsx`: chapter introduction, editable inherited three-metric selection, linked confirmation, publication, player-led tests, evidence judgment and complete run history.
- `experiments.ts`: evidence-based Explore/Adjust/Verify tasks, player-chosen aims, optional editable examples, findings and unrestricted third-test validation.
- `ExperimentPrompt.tsx`: compact aim choices, three finite visible-time pulses and collapsed strategy hints; applying an example still requires confirmation.
- `WeightGuide.tsx`: four steps driven by actual slider/confirmation state; skippable and reopenable without resetting choices.
- `weights.ts`: deterministic allocation, locked-value invariants, independent per-item effort thresholds and descriptive near-even classification.
- `dialogue.ts`: concise observation exchanges and final cinematic dialogue; editing/publication/comparison operations remain silent.
- `data.ts`: 18 Narrative V2 behaviours, immutable runs, cinematic and completion contracts.
- `CinematicPlaceholder.tsx`: the selected three shots, comparison dialogue and final theory slots, all replaceable by the partner.
- `styles.css`: office layout, ranges, sequential observations and responsive comparison, scoped to `.level-three`.

The shared Gameplay host connects Level 2 here with the same opening-confirmed
name, three selected metrics and sound preference. `initialMetricIds` preselects the trio without preventing changes. The `level3` build mode mounts this component directly.
The standalone Level 1/2 modes still end at their own level.

Run `npm run dev -- --mode level3` for direct development,
`npm run build:level3` for its HTML, or `npm run package:previews` to refresh
all individual and combined downloads. Latest entry: `play/Level3-play.zip`.

See [Level 3 handoff](../../../docs/LEVEL3_HANDOFF.md) for mechanics, highlighted
narrative adjustments, scene IDs and result payloads. The preview stops at the final theory placeholder. `onDesignLab` is reserved and is not called. All three player-confirmed test snapshots are displayed; no system reference is inserted. No player Restart control is available.

Weights reserve at least 1% for each priority. The v12 forecast page and result markers are withdrawn: confirmed weights run directly, and the comparison retains actual observed trials.

Effort follows each task's own weight: 1–24% minimum, 25–66% steady and 67–98% intense. Near-even means a highest-to-lowest spread of at most ten percentage points; it only names the split and does not override effort. All near-even splits naturally have three steady responses, as do some uneven splits. Thus 40/30/30 → 40/31/29 leaves all three effort bands unchanged. This is an observation, not a new discovery or a failed adjustment.

The scoring stopping rule is independent of the split label. Any all-steady run uses the criteria/ticks/packing-up sequence and medium-shot criteria actions/replies. Low-effort tasks remain unticked; uneven runs must not imply that every requirement was met. Findings, dialogue and final summaries follow the actual effort bands, including histories with no band changes. See [effort rules](../../../docs/EFFORT_RULES.md).

Comparison cells explicitly label First result / Same effort / More effort / Less effort. Column headings name the previous test used for comparison; weight changes alone do not become effort changes. Whole-cell highlight fills are removed.

See [player-led experiments](../../../docs/PLAYER_EXPERIMENTS.md) for the retained v16 aim/judgment flow and nullable compared-pair completion contract. All three uneven or near-even trials can finish. The required aims, three attempts and final judgment are pending a separate player-path redesign; v17 changes the rules and evidence rather than those gates. Current validation: [v17](../../../docs/LEVEL3_VALIDATION-v17.json); v16 remains historical.
