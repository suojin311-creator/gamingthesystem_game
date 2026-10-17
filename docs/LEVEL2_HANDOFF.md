# Level 2 handoff

## Flow and ownership

The game owns choosing exactly three metrics, evaluating, identifying the missing
three, expanding the system and displaying classroom evidence/checklist changes.
The partner owns finished cinematics. The opening remains separate.

The first six metrics retain the Level 1 IDs and names. Expansion past six counts
additional requirements; these are not 94 invented named educational indicators.
The matrix is a visual count, not a learning score. No student health percentage,
right/wrong answer, theory explanation or Level 3 weighting is introduced.

| First choice | Branch | Result |
| --- | --- | --- |
| prep + part + focus | visible | The class looks more engaged. |
| discuss + reflect + peer | quality | The work looks stronger. |
| Other 18 distinct trios | mixed | The dashboard looks convincing. |

After the first observation, Cover the gaps displays the exact other three.
Adding them gives six green ticks, followed by the shared six-metric scene.
The player then adds more requirements: 6 → 10 → 25 → 100. Each increase first
changes the count and matrix, then automatically reveals Alex's checklist.
At 100, Observe the class plays the final scene. The last dashboard stays at
100 with qualitative evidence and the question about relative importance.
Continue to Level 3 is disabled until the next level exists.

## Component contract

Import shared base CSS once in the host, before mounting levels:

```tsx
import LevelTwo from './levels/level2/LevelTwo';

<LevelTwo
  playerName={playerName}
  previousMetricId={levelOneResult?.metricId}
  renderCinematic={(request, complete) => (
    <PartnerScene sceneId={request.sceneId} onComplete={complete} />
  )}
  onComplete={result => setLevelTwoResult(result)}
/>
```

Keep the LevelTwo instance mounted while its cinematic renderer is active.
The renderer receives:

```ts
{
  sceneId: 'level2.three.mixed',
  kind: 'three',               // 'three' | 'six' | 'checklist'
  branch: 'mixed',             // 'visible' | 'quality' | 'mixed'
  selectedMetricIds: ['prep', 'part', 'discuss'], // original trio, retained
  metricCount: 3               // 3 | 6 | 100
}
```

| Scene ID | Trigger |
| --- | --- |
| level2.three.visible | Three visible-behaviour metrics |
| level2.three.quality | Three quality-oriented metrics |
| level2.three.mixed | Any mixed trio |
| level2.six | All six evaluated |
| level2.checklist | Final 100-requirement observation |

Call `complete()` at the actual end of the scene. The dashboard then presents its
observation automatically; do not require a separate reveal click. Without a
renderer, a clearly labelled temporary classroom reading fills each slot.
Cinematics do not need to explain dashboard numbers or run the 10/25 checklists.

After the last finding and Maya reply have received visible reading time,
`onComplete` fires once per run:

```ts
{
  selectedMetricIds: ['prep', 'part', 'discuss'],
  branch: 'mixed',
  metricsTracked: 100
}
```

Replay does not repeat completion. Restart permits a new completion. Every fresh
page starts a new run. The callback does not automatically navigate to Level 3.

## Presentation and lifetime

The central content is the reading focus. The right-hand cards summarize the
same current round. Starting a round hides the previous report until the new
evaluation finishes and resets students to **Awaiting observation**. The student
card changes to **Learning at risk** only when the current observation arrives.
Do not retain an observed-at count from an earlier round. The risk is a
qualitative interpretation of the story; actual learning gains remain unverified.
No sidebar badges, extra student sound or independently pulsing update competes
with the central content. The Level 2 header has Sound and Restart controls;
there is no Guide button or guide dialog.

| Metric count | Description below Learning at risk |
| --- | --- |
| 3 | Untracked areas get overlooked. |
| 6 | Meeting criteria becomes the goal. |
| 10 | Ticking boxes takes priority. |
| 25 | Optimizing for the criteria takes priority. |
| 100 | Doing the minimum becomes the strategy. |

The gap view keeps tracked areas quiet and emphasizes the other three with
larger names, an amber border, **3 areas untracked**, and a single arrival pulse.
Untracked areas are blind spots; no declining learning score is inferred.

Core metrics turn green one at a time, followed by the report cue. After each
scene, the observation and student summary appear together with one evidence
cue, followed by 6–8 seconds to read. Dialogue uses 650 ms typing dots and
3–5 seconds per message; the next action follows the final reading interval.
The 10/25/100 checklist uses action items, rather than questions. Each item
appears 550 ms after the previous one and its checkbox ticks. The ticks represent
Alex completing checklist actions, not demonstrating learning. The next button
opens after 1000 ms of visible time following the final item. All items remain
visible and the player decides when to continue. Restart dialogs, hidden
tabs and off-screen text hold these sequences. Reduced motion removes movement
but keeps the sequence and waits. Sound preference carries between levels in page
memory.

No game storage, runtime server, API key or multiplayer service is used.
Two students at one computer share one run. Classroom network capacity and
finished-video delivery should be checked separately when hosting is chosen.
