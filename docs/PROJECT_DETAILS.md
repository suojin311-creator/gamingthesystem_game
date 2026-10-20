# Gaming the System

> 当前动画整合版位于 `animation/opening-integration`，包含开头、Level 1／2 动画和三关。
> 最新下载及备份以 [play/README.md](../play/README.md) 为准；下方部分玩法展示和稳定分支下载说明保留较早状态。

For the latest one-ZIP download containing the full game and all three standalone
levels, use [the download guide](../play/README.md). This page retains the detailed
gameplay and development explanation from the preceding repository home.
For the current daily/release commands, follow [Development workflow](DEVELOPMENT_WORKFLOW.md).

An English-language game about measuring engagement. Levels 1, 2 and 3 are playable. On animation/opening-integration, the partner’s opening now precedes real Gameplay with visual click cues and shorter interactions. Later story slots still use replaceable placeholders; the approved game branches remain separate.

Download the [Level 3 + full-game review ZIP](https://github.com/suojin311-creator/gamingthesystem_game/blob/level3-dev/play/Level3-and-Full-game-play.zip?raw=true) for both requested versions in one archive: `Level3/Level3.html` and `Full-game/Gaming-the-System.html`.

The latest combined and individual previews live together on **level3-dev**:

| Latest preview | Download | Open after extracting |
| --- | --- | --- |
| **Levels 1 → 2 → 3** | [Full-game-play.zip](https://github.com/suojin311-creator/gamingthesystem_game/blob/level3-dev/play/Full-game-play.zip?raw=true) | Gaming-the-System.html |
| **Level 1 only** | [Level1-play.zip](https://github.com/suojin311-creator/gamingthesystem_game/blob/level3-dev/play/Level1-play.zip?raw=true) | Level1.html |
| **Level 2 only** | [Level2-play.zip](https://github.com/suojin311-creator/gamingthesystem_game/blob/level3-dev/play/Level2-play.zip?raw=true) | Level2.html |
| **Level 3 only** | [Level3-play.zip](https://github.com/suojin311-creator/gamingthesystem_game/blob/level3-dev/play/Level3-play.zip?raw=true) | Level3.html |

Sign in with access to this private repository, download and extract the ZIP, then open its HTML in Chrome or Edge. No installation is required; the downloaded game runs offline. These fixed paths are updated together. Version-numbered ZIPs preserve older releases.

The approved Level 3 baseline is preserved at [`level3-approved-v20`](https://github.com/suojin311-creator/gamingthesystem_game/tree/level3-approved-v20). Current development is on **level3-dev**. The existing level1-preview, level2-preview and level2-dev branches are synchronized for this release. Use [play/](../play/README.md) as the single place to find current individual and combined downloads. See [GitHub 使用说明](REPOSITORY_GUIDE.md).

## Playable flow

**Level 1 — One metric.** Choose one of six plausible indicators, write a prediction, watch an illustrative score rise, then observe a selected classroom story and its unintended behaviour. The comparison keeps the prediction, one evidence paragraph and the player/Alex conversation. Alex replies in two grouped bubbles with distinct emoji. The standalone entry stops here; the combined game enables Continue to Level 2.

**Level 2 — More metrics.** A three-second chapter break carries forward the actual Level 1 card and its unintended behaviour, then files the card away and unfolds three empty slots. The large LEVEL 02 title and a single teacher line replace the old three-message introduction. Choose three metrics explicitly opens the selection page for three of the same six metrics. A three-slot Alex’s Checklist records those choices. Three/six-metric icon/check reports avoid duplicate checklists. All 20 trios route to descriptive branches; missing areas receive a continuous amber warning. Classroom scenes remain replaceable slots for the existing authored animations; the extra peer demonstration and generated peer-story fields have been withdrawn. After the six-item observation, the page asks **Would more metrics help Alex learn?** with a **6 → ?** diagram. The question is interface content, independent of dialogue, and replaces the generic observation heading. One **Test more metrics** action then runs a continuous 10 → 25 → 100 escalation, filling a checkbox field and growing a paper pile. Brief illustrated actions replace the repeated checklist paragraphs and Add clicks. A stable desk keeps the counter, matrix and paper mounted throughout. Completed 10/25 actions hold for 3.5 visible seconds, preview the next milestone and use a 0.7-second paper turn without automatic scrolling; Observe the class still waits at 100. Its final observation reads **More metrics. Still chasing marks.**, linking the result back to the experiment. The standalone entry ends here; the combined game enables Continue to Level 3.

**Level 3 — The weighting trap.** The long checklist closes and the original three selected cards return with slider artwork beneath a prominent LEVEL 03 title. A short teacher line and explicit Review priorities / Choose priorities action end the chapter break. The combined game preselects Level 2’s three metrics; players may swap them before weighting. Standalone Level 3 starts with an empty selection. Its first weight editor is unassigned: three dashes and sliders at the start, with Confirm and Run unavailable. Moving any slider creates the first positive allocation; the other two share the remainder. No values are supplied before this action. Allocate exactly 100% across three priorities using positive weights of at least 1% each (up to 98% for one priority). Native slider bounds reserve the minimum for all unlocked priorities, and publication rejects zero weights. Confirm one card, then adjust either remaining slider; confirming either final card locks the pair and marks the other Auto-confirmed. Reset weights sits above the action row. A once-per-visit four-step spotlight guide explains the controls with Next, Back, Skip and Escape; it does not require practice or change weights. Guide in the editor header reopens it. Confirmed weights run directly into publication. The redundant Level 3 prediction page and result markers have been removed; comparison uses the actual observed trial records. Player/Alex conversations use a separate bottom region. Publication stays visible with both perspective cards until the player clicks Observe the class. Results reveal three qualitative responses with aligned, divided columns.

The first allocation is a free experiment. Reset returns to unassigned before the first run and restores the last observed split on later tests. Near-even weights are a possible route, never a required step or an inferred untested result. The second editor carries forward a compact Last observation with each task’s actual effort, then asks a short question based on that evidence. Optional Need a hint? text suggests what to observe; it supplies no numerical answer and never sets sliders. There are no aim radios, automatic examples or compulsory weight patterns. After two distinct, confirmed and observed allocations, Compare the results opens the real results side by side. Step back and reflect continues directly; Test another idea optionally opens a third experiment, with Back to comparison available before publication. The third allocation may leave the effort bands unchanged, and its findings must say so. Comparison keeps all two or three actual trials without a system reference or keep/rethink gate. See the [Level 3 player path](LEVEL3_PLAYER_PATH.md).

Effort now follows the complete relative allocation. Compare each task with both alternatives: a difference up to ten percentage points counts as similar. More clearly higher comparisons gives high effort, more lower comparisons gives low effort, and a tie gives medium effort. Thus 49/26/25 and 49/27/24 both produce high/low/low, 45/45/10 produces high/high/low, 34/33/33 produces three medium responses, and 60/30/10 produces high/medium/low. There is no absolute 24/25 cutoff. These are qualitative relative responses, not measured effort percentages. The ten-point tolerance is a game-design assumption. Edited weights preserve the other unlocked shares' ratio rather than automatically equalizing them; increasing the edited share cannot lower its own effort. Shared attention and score-based stopping remain separate observations. See [effort rules](EFFORT_RULES.md).

The neutral comparison table keeps all actual tests in adjacent columns, with each metric name once per row and explicit effort changes against the previous trial. Repeated effort-summary boxes, aim headings and comparison footnotes are removed. Level 3 action footers contain controls without explanatory captions. Teacher and Alex use ordinary speech bubbles; each observation ends with one teacher question and two short Alex replies. Weight editing, publication and comparison have no workbench dialogue. Alex’s response and Goodhart’s theory reveal remain replaceable cinematics; this preview stops at the final theory frame without a Design Lab transition.

The opening owns name entry. `Gameplay` accepts its confirmed `playerName`, forwards it through all three levels and scene requests, and preserves it through in-page transitions. Standalone previews use Maya because they omit the opening. All player decisions use I. Authored dialogue emoji remain distinct. Teacher and student have different portrait icons, independent of their displayed names.

Chapter breaks preserve the prior green report alongside its unresolved student consequence. They take about three visible seconds and wait for an entry click. A short paper movement and a low, descending, unresolved tone mark the new chapter; there is no reward cue. The same page-local, gesture-unlocked audio context continues across levels, and Sound off silences both cues. Standalone previews work without autoplay permission. Hidden or off-screen chapters pause; reduced motion removes the card movement. See [chapter transitions](CHAPTER_TRANSITIONS.md).

Information arrives in visible-time beats with local Web Audio cues. Hidden tabs, off-screen timed information and the Level 1 guide hold pending beats; reduced motion removes animation. No Pause or extra Reveal button is used. All text remains available. Student cards show the specific behaviour prominently, with a small Learning at risk label. Weight percentages describe scoring, and qualitative effort categories follow the narrative; no numerical learning loss or learning gain is invented.

The Restart control and its dialogs are removed in all three levels. Administrator access is deferred. Reset weights only resets the current allocation. Each page is one independent game. Closing, reopening, reloading or restoring from the back-forward cache starts fresh. Choices, names and sound preferences are not saved in browser storage or sent to a service. Two students can share one open game; there is no multiplayer server.

## Develop and package

Use Node.js 20.19+, 22.12+ or newer (validated with Node 24), plus Python 3 for ZIP packaging:

```sh
cd /workspace/gamingthesystem_game
npm ci --cache /tmp/gaming-the-system-npm-cache
npm run dev                     # Combined game, starts at Level 1
npm run dev -- --mode level3     # Work directly on Level 3
```

Level 1/2 standalone development uses `--mode level1` or `--mode level2`. Builds check TypeScript and inline JavaScript, CSS and artwork into one HTML:

```sh
npm run build                   # dist/index.html: Levels 1 → 2 → 3
npm run build:level1             # dist-level1/index.html: Level 1 only
npm run build:level2             # dist-level2/index.html: Level 2 only
npm run build:level3             # dist-level3/index.html: Level 3 only
npm run package:previews         # Rebuild and package all four latest entries
```

After an approved change, rebuild all previews and the two-version review ZIP together, validate the packages and synchronize the preview branches. `play/LATEST.json` records source and artifact hashes. Keep version-numbered historical ZIPs unchanged.

## Source layout and partner integration

```text
src/
  App.tsx                 Combined / individual preview entry
  Gameplay.tsx            Opening-name handoff and Level 1 → 2 → 3 navigation
  levels/
    level1/               Choices, prediction, score, guide and observations
    level2/               Three-metric branches and 6 → 10 → 25 → 100 expansion
    level3/
      LevelThree.tsx      Priority choices, locked weights, run history and comparison
      weights.ts          Exact allocation and relative effort rules
      data.ts             Narrative responses and cinematic/result contracts
      CinematicPlaceholder.tsx
      styles.css          Layout scoped to .level-three
  shared/                 Metric definitions, icons, conversations, sounds and timing
  assets/                 Office and classroom artwork
scripts/package_previews.py
play/                     Latest downloads and historical archives
```

Each level owns its rules and text. Shared modules never import level internals. [Typography](TYPOGRAPHY.md) documents shared sizes for equivalent content across the three levels. Partner contracts are documented in [Opening handoff](OPENING_HANDOFF.md), [Level 1](LEVEL1_HANDOFF.md), [Level 2](LEVEL2_HANDOFF.md) and [Level 3](LEVEL3_HANDOFF.md).

## Validate

```sh
npm run package:previews
node tests/level3_rules.mjs
node tests/learning_contracts.mjs
node tests/experiment_rules.mjs
node tests/player_dialogue.mjs
python tests/player_experiments.py
python tests/task_clarity.py
node tests/dialogue_emojis.mjs
node tests/dialogue_narrative.mjs
python tests/release.py
# With npm run dev running:
python tests/level3_integration.py
```

The current Level 3 checks cover allocation invariants, observed-evidence prompts, the two-test completion path and optional third trial, spotlight-guide controls, actual cinematic shots, copied results, name/completion contracts and responsive layouts. There is no aim or verdict selection in the current UI. The shared [management satisfaction](MANAGEMENT_SATISFACTION.md) and [visual operations](VISUAL_PLAY.md) documents cover their own checkpoints and illustrations. The release test reads all four individual/combined ZIPs, verifies the two-version review ZIP against those exact builds, and plays across all three chapters. [LEVEL3_VALIDATION-v21.json](LEVEL3_VALIDATION-v21.json) records the current unassigned-start release, including the latest Level 2 framing. [v20](LEVEL3_VALIDATION-v20.json) records the approved relative-effort baseline. [v19](LEVEL3_VALIDATION-v19.json) records the preceding copy/layout checkpoint. [v18](LEVEL3_VALIDATION-v18.json) records the complete player-path revision. [v17](LEVEL3_VALIDATION-v17.json) records the earlier absolute effort-rule correction; [v16](LEVEL3_VALIDATION-v16.json) retains the now-superseded aim-selection and judgment checks. Reports v15 and earlier, [Scaffolding](SCAFFOLDING.md), [earlier gameplay corrections](LEARNING_OPTIMIZATIONS.md) and versioned ZIPs remain historical records. Behaviour checks do not establish classroom learning effectiveness.

Offline browser tests serve exact production HTML through an in-memory HTTPS origin because managed Chromium blocks local file navigation. Opening the downloaded file in the user’s particular browser remains a separate check. Test outputs/screenshots go to ignored test-results/. These are functional checks, not a classroom load test.

The current Level 3 task is a prominent short-question card with three visible-time pulses (one steady outline with reduced motion), paired on later tests with the preceding observation. Strategy hints are optional verbal help. The comparison uses explicit More/Less/Same effort labels with a named prior-test reference, replacing ambiguous whole-cell fills. [Task clarity](TASK_CLARITY.md) documents the earlier presentation revision; its old numerical suggestion control is no longer present.

See [player-led experiments](PLAYER_EXPERIMENTS.md) for the current flow and compatibility contract; the compared near-even/uneven pair can be null for uniform-pattern histories. The relative rules are documented in [effort rules](EFFORT_RULES.md). Level 2’s additional growth framing is now complete; opening integration is reviewed separately on animation/opening-integration.

The v19 editor simplifies the all-covered question to “Can new weights make Alex go further?”, removes the small prompt headings and the redundant 100% allocation strip, and keeps hints on one line where space permits. Last observation retains the honest effort bands alongside an amber reminder that Alex stopped after earning the marks he wanted. The subsequent v20 revision replaces the old 25%/67% cutoffs with whole-allocation relative effort. See [v19 details](LEVEL3_FEEDBACK-v19.md).

The preceding earlier-level framing release is recorded in [LEVEL2_VALIDATION-v7.json](LEVEL2_VALIDATION-v7.json). It verifies the six-metric question, continuous growth and result, the retained Level 1 Enter/closing pace fixes, connected handoff and actual ZIPs. [Level 2 framing](LEVEL2_FRAMING.md) records that release’s scope; its Level 2 changes remain included. The next authorized Level 3 revision starts unassigned, documented in [Unassigned weights](UNASSIGNED_WEIGHTS-v21.md).
