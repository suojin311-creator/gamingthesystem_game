# Level 1 handoff and narrative boundaries

## Selected workflow

Opening returns to office → mount Level 1 → select one metric → predict → run evaluation → see dashboard success → explicitly observe classroom → play exactly one selected cinematic → return to the same saved workbench → compare prediction with observed behaviour → finish Level 1.

The opening remains a separate project in the supplied ZIP. No opening scenes have been spliced into this implementation. Each cloud task is already isolated; use the existing checkout and do not create another Git worktree unless explicitly requested.

## Who displays what

The workbench owns the six cards, prediction input, illustrative numerical result and animation, `Target achieved`, both perspective panels, and the post-observation comparison. It retains the original prediction and displays it after observation without evaluating it for correctness.

The cinematic owns Maya/Alex's descriptive actions and dialogue for the selected metric. It does not need to display or interpret a score or receive the prediction. The workbench's bottom dialogue supplies short transitions without repeatedly opening a separate cinematic. Formal audio and new character actions remain the cinematic creator's responsibility.

## Component contract

`LevelOne` is a React component. Its default player name is Maya; the later host can pass the name already collected in the opening. Local persistence can be disabled when the host owns saves.

```tsx
import LevelOne from './LevelOne';

<LevelOne
  playerName={playerName}
  persist={false}
  renderCinematic={(request, complete) => (
    <YourClassroomScene
      metricId={request.metricId}
      onComplete={complete}
    />
  )}
  onComplete={(result) => enterLevelTwo(result)}
/>
```

The renderer receives `{ sceneId, metricId }`, then calls `complete()` when the scene ends. No score or prediction is needed to choose the branch. Mount the Level 1 component once through the interlude to retain its session. Names for the current slots:

| Metric ID | Scene ID | Metric |
| --- | --- | --- |
| `prep` | `level1.prep` | Pre-class Preparation |
| `part` | `level1.part` | In-class Participation |
| `focus` | `level1.focus` | On-task Focus |
| `discuss` | `level1.discuss` | In-class Discussion Quality |
| `reflect` | `level1.reflect` | Learning Reflection Quality |
| `peer` | `level1.peer` | Online Peer Response Quality |

If no renderer is supplied, a clearly labelled classroom placeholder plays three manually advanced lines from the corresponding Narrative V2 branch. Refreshing an interlude starts that branch again while preserving the metric and prediction. `Replay scene` replays the same selected branch.

After `Try more metrics`, `onComplete` receives:

```ts
{
  metricId: 'prep',
  prediction: 'Students will arrive ready to discuss the reading.',
  reportedScore: { before: 34, after: 88, target: 70 }
}
```

The standalone view shows a Level 1 completion / Level 2 placeholder. The host should navigate to its next scene in `onComplete`. The callback fires on explicit completion; reloading the standalone completed view does not automatically fire a navigation callback again.

## Narrative adjustments for the highlighted operations

1. Six cards appear in an independent office-themed workbench instead of requiring tiny interactions on a perspective-skewed laptop or a new whiteboard shot.
2. Maya: “Where should I start?”
3. Prediction prompt: “What do you expect students to do?” Supporting text asks the player to imagine the metric as the main target.
4. `Run evaluation` shows the illustrative score rising. `See university response` explicitly reveals the green university score and Target met status with a success chime.
5. Maya: “Looking good. Let’s check the classroom.” Player chooses `Observe the class`.
6. The selected branch cinematic plays. The existing placeholder is replaced here.
7. Back at the workbench, `You expected` shows the original prediction. `Reveal observation` shows a short classroom finding; full behavioural context is available under More context. `See student response` then reveals the amber student uncertainty with a separate cue. These steps wait for clicks instead of disappearing on a timer.
8. Maya: “The score is up. What about learning?” Then Alex replies with the selected branch quote. Maya appears above-left, Alex below-right; each message starts with 650 ms of typing dots. The first message stays visible during a reading pause before the second types. Replies wait until the chat is on screen, and pause in hidden tabs. Read replies scrolls to the chat if needed.
9. The standalone completion bridge uses “Maybe one metric is too narrow.” The final management-email scene can be inserted by the narrative host around this bridge. It is not recreated as a second finished cinematic here.

Do not display Goodhart's Law in Level 1. All six choices are plausible educational indicators. Behaviour improves in the measured respect, while deeper engagement remains uncertain. There is no fixed student-health penalty, no right/wrong grading of predictions, and no conversion of qualitative evidence into an unsupported learning percentage.

## Deployment and integration notes

- React 19, TypeScript 5.9 and Vite 7 match the opening's toolchain family. Framer Motion is not needed for these operations.
- The independent build is portable. The later combined app can use ordinary asset chunks instead of single-file bundling.
- The stylesheet includes standalone page/base styles. Reconcile these with the opening's global styles when merging; importing both global stylesheets unchanged is not the integration plan.
- Keep keyboard focus, reduced-motion handling and local-save boundaries when replacing the placeholder.
- There are no live processes, credentials or external services required by the finished HTML. For source development, restart Vite with `npm run dev` in the project directory.
- Each browser is one independent game. Two students may share that game; no room server or multiplayer connection is implied.

## Interface feedback (v2)

The dashboard owns quiet synthesized Web Audio cues: count ticks, an ascending success chime, an observation cue, a softer two-note student update, and message pips. No audio files, network calls, or credentials are needed. Sound is unlocked by pointer/keyboard interaction, can be muted immediately, and remembers mute independently from the game save. Hidden tabs stop pending sounds. Voice acting, ambience and cinematic audio remain with the cinematic creator.

The host can preserve these interface cues or coordinate them with its eventual audio system. Neither qualitative student uncertainty nor sound is a numerical learning penalty. Save data now includes `resultReported` and `reviewStep` so reloads retain acknowledged reveal steps. Older saves migrate to a valid first reveal. The cinematic renderer and completion callback contracts are unchanged.
