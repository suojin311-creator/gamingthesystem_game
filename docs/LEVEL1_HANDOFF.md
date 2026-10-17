# Level 1 handoff and narrative boundaries

## Selected workflow

Opening returns to office → mount Level 1 → select one metric → predict → run evaluation → see dashboard success → explicitly observe classroom → play exactly one selected cinematic → return to the same in-memory workbench → compare prediction with observed behaviour → finish Level 1 on the same observation page.

The opening remains a separate project in the supplied ZIP. No opening scenes have been spliced into this implementation. Each cloud task is already isolated; use the existing checkout and do not create another Git worktree unless explicitly requested.

## Who displays what

The workbench owns the six cards, prediction input, illustrative numerical result and animation, `Target achieved`, both perspective panels, and the post-observation comparison. It retains the original prediction and displays it after observation without evaluating it for correctness.

The cinematic owns Maya/Alex's descriptive actions and dialogue for the selected metric. It does not need to display or interpret a score or receive the prediction. The workbench's bottom dialogue supplies short transitions without repeatedly opening a separate cinematic. Formal audio and new character actions remain the cinematic creator's responsibility.

## Component contract

`LevelOne` lives in `src/levels/level1/LevelOne.tsx` and imports its own scoped styles. Import `src/shared/styles/base.css` once in the host entry before the level. `src/App.tsx` is the current game entry.

`LevelOne` is a React component. Its default player name is Maya; the later host can pass the name already collected in the opening. Every mount starts a new in-memory run. The component never restores progress or preferences from browser storage.

```tsx
import LevelOne from './levels/level1/LevelOne';

<LevelOne
  playerName={playerName}
  showIntro={false}
  renderCinematic={(request, complete) => (
    <YourClassroomScene
      metricId={request.metricId}
      onComplete={complete}
    />
  )}
  onComplete={(result) => setLevelOneResult(result)}
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

If no renderer is supplied, a clearly labelled classroom placeholder plays three manually advanced lines from the corresponding Narrative V2 branch. Refreshing during an interlude starts a new game at metric selection, with the guide shown again. `Replay scene` replays the same selected branch within the open game.

After the final Alex reply has received its reading interval, `onComplete` automatically receives:

```ts
{
  metricId: 'prep',
  prediction: 'Students will arrive ready to discuss the reading.',
  reportedScore: { before: 34, after: 88, target: 70 }
}
```

The standalone view stays on the observation page and shows a disabled Continue to Level 2 button with a right arrow; all four progress steps are done. The button is a reserved entrance; Level 2 is not mounted. There is no separate completion/Level 2 page. The callback fires once per run after the final dialogue reading interval. Replaying the cinematic does not fire it again; Restart, reload or remount starts a new run. The current host should retain the result in memory without navigating. Later Level 2 integration can choose how and when to use it.

## Narrative adjustments for the highlighted operations

1. Six cards appear in an independent office-themed workbench instead of requiring tiny interactions on a perspective-skewed laptop or a new whiteboard shot.
2. Maya: “Where should I start?”
3. Prediction prompt: “What do you expect students to do?” Supporting text asks the player to imagine the metric as the main target.
4. `Run evaluation` shows the illustrative score rising. Management’s view and Target met status then update automatically with a success chime. The Target 70 label is aligned to the real threshold marker.
5. Maya: “Looking good. Let’s check the classroom.” Player chooses `Observe the class`.
6. The selected branch cinematic plays. The existing placeholder is replaced here.
7. Completing the cinematic returns to a compact, static prediction reference. After 1000 ms of visible time, the classroom observation and student uncertainty appear together, with one shared observation cue. Show only `metric.evidence` under IN THE CLASSROOM: the former details paragraph. Do not add the old takeaway headline or details toggle. Students is a quiet summary: no NEW badge, separate sound, pulse or forced sidebar scroll. Management’s view retains the already reported score.
8. Give the observation 6–8 seconds of visible reading time before Maya: “The score is up. What about learning?” Alex then replies with the selected branch quote. Both bubbles sit within the main content column, Maya above-left and Alex below-right. Each starts with 650 ms of typing dots, followed by 3–5 seconds to read. Keep all messages visible. Wait for the final reply’s reading interval before showing the reserved Continue to Level 2 button on this page and reporting completion once. Replies wait until the chat is on screen. Guide and restart dialogs suspend reading and typing; closing them resumes automatically. There is no Pause / Resume control.
9. The former “What if we measured more than one?” screen, More metrics card and “Maybe one metric is too narrow” bridge are reserved in `src/levels/level2/LevelTwoEntryPlaceholder.tsx` for the future Level 2 host. LevelOne never imports or renders this component. Any future management-email scene remains the narrative host’s responsibility.
10. The prediction page has one Change button beside the selected metric; the duplicate Back to metrics link is removed. Run evaluation remains right-aligned.

Do not display Goodhart's Law in Level 1. All six choices are plausible educational indicators. Behaviour improves in the measured respect, while deeper engagement remains uncertain. There is no fixed student-health penalty, no right/wrong grading of predictions, and no conversion of qualitative evidence into an unsupported learning percentage.

## Deployment and integration notes

- React 19, TypeScript 5.9 and Vite 7 match the opening's toolchain family. Framer Motion is not needed for these operations.
- The independent build is portable. The later combined app can use ordinary asset chunks instead of single-file bundling.
- Shared base styles live in `src/shared/styles/base.css`; Level 1 layout is scoped to `.level-one` in its own folder. Reconcile the shared global resets/tokens with the opening's base styles when merging, then load the shared base once. Level 1 component styles are imported by the component.
- Keep keyboard focus, reduced-motion handling and the in-page state lifetime when replacing the placeholder.
- There are no live processes, credentials or external services required by the finished HTML. For source development, restart Vite with `npm run dev` in the project directory.
- Each browser is one independent game. Two students may share that game; no room server or multiplayer connection is implied.

## Interface feedback and orientation (v7)

The dashboard owns locally synthesized Web Audio cues: count ticks, an ascending success chime, one shared classroom-observation/student-summary cue, and softer message pips. No audio files, network calls, or credentials are needed. Sound is unlocked by pointer/keyboard interaction, can be muted immediately for the current run, and resets to sound on for a new run. Hidden tabs stop pending sounds. Voice acting, ambience and cinematic audio remain with the cinematic creator.

The host can preserve these interface cues or coordinate them with its eventual audio system. Neither qualitative student uncertainty nor sound is a numerical learning penalty. The in-memory run contains `resultReported` and `reviewStep` so scene transitions retain completed presentation beats. Reloads reset both, and older saved data is ignored. The cinematic renderer contract is unchanged. The completion payload is unchanged, but its trigger is now automatic after the final reply’s reading interval, once per run.

The guide appears for every new run, with no persistent completion marker. Completing or skipping it hides it for this run; Guide reopens it without changing current choices. Pass `showIntro={false}` if the integrated host provides the introduction. Guide and restart dialogs hold the presentation. The guide follows actual region positions and supports keyboard navigation, Escape, touch layouts and reduced motion.

The automatic recap uses visible-time delays. Hidden tabs, off-screen text, an open guide and the restart dialog suspend the pending beat. There is no manual pause control. Reading time is 1000 ms + 300 ms per English word, bounded to 6000–8000 ms for evidence and 3000–5000 ms for replies. Reduced motion keeps these intervals. The data-cue master gain is 0.13 (v2: 0.045); reply envelopes remain softer. The finding fades in once. The evaluation management highlight clears after 1600 visible ms; the recap never re-highlights it. No sound files or network calls are required.

## Run lifetime

A page opening is a new game: selection, prediction, result, inspected/review stages, guide position and mute state start fresh. There is no `persist` prop and no load/save path. Closing/reloading the page ends that run; a pageshow event restored from the back-forward cache also resets it. Existing old-version keys have no effect. A separate tab starts its own independent game. The host must initialise the full opening/name state afresh for the integrated game too.

Keep the same LevelOne instance mounted while its renderer plays the selected cinematic. Its completion callback still receives the current metric, prediction and illustrative score in memory, enabling the next scene within that open game. Do not persist the callback payload to restore later runs.
