# Level 2 handoff

## Flow and ownership

The game owns choosing exactly three metrics, evaluating, identifying the missing
three, expanding the system and displaying classroom evidence/checklist changes.
The partner owns finished cinematics. The opening remains separate.

Level 2 begins with a dedicated introduction carrying the visible LEVEL 2
label and the player/Alex conversation. Typing and reading intervals run in
sequence. The lower-right Choose three metrics button appears with Alex's final
message, and the introduction stays on screen until the player clicks it. The
same level instance then opens the six working metric cards. It replays on a level restart or a fresh page.
Hidden tabs, off-screen dialogue and restart dialogs suspend this sequence.

On the selection page, the vertical **Alex’s Checklist** records exactly the
current choices using the later checklists' paper, heading and checkbox styles.
Its checks mean selected, not completed or learned; its counter says N / 3
selected. Only the six metric cards are selection controls. On narrow screens
the checklist follows the cards and precedes Run evaluation. The optional
previousMetricId appears as a quiet reference on the choice page.

Three- and six-metric evaluation screens display their sequential metric results
and current-round perspectives without a second checklist. Alex's physical
three/six-item checklist actions remain part of the partner's classroom scenes;
the temporary scene describes the six-item action. The game uses the same
Alex’s Checklist heading for the selection summary and 10/25/100 action lists.

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
Continue to Level 3 is enabled by the combined host's optional onContinue
callback. The standalone Level 2 entry leaves it reserved and disabled.

## Component contract

Import shared base CSS once in the host, before mounting levels:

```tsx
import LevelTwo from './levels/level2/LevelTwo';

<LevelTwo
  playerName={playerName}
  previousMetricId={levelOneResult?.metricId}
  renderCinematic={(request, complete) => (
    <PartnerScene sceneId={request.sceneId} playerName={request.playerName} onComplete={complete} />
  )}
  onComplete={result => setLevelTwoResult(result)}
  onContinue={() => setCurrentLevel(3)}
/>
```

Keep the LevelTwo instance mounted while its cinematic renderer is active.
The renderer receives:

```ts
{
  sceneId: 'level2.three.mixed',
  playerName: 'Jordan',        // confirmed in the opening, replaces Maya's display name
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
The explicit Continue to Level 3 action settles completion once before calling
onContinue(result), including when clicked before the final reading delay ends.

The shared `Gameplay` host forwards the opening's name to all three levels and their
scene requests. See [Opening handoff](OPENING_HANDOFF.md). Player decisions use
“I”; the older narrative's “we” is adapted to the player's first-person role.

## Presentation and lifetime

The central content is the reading focus. The right-hand cards summarize the
same current round. Starting a round hides the previous report until the new
evaluation finishes and resets students to **Awaiting observation**. The student
card shows the current behaviour with a small **Learning at risk** label only
when the current observation arrives. Behaviour is the main type; risk is secondary. Both levels render the shared LearningRisk component and stylesheet to keep this hierarchy identical.
Do not retain an observed-at count from an earlier round. The risk is a
qualitative interpretation of the story; actual learning gains remain unverified.
No sidebar badges, extra student sound or independently pulsing update competes
with the central content. The Level 2 header has Sound and Restart controls;
there is no Guide button or guide dialog.

| Metric count | Main student behaviour description |
| --- | --- |
| 3 | Untracked areas get overlooked. |
| 6 | Meeting criteria becomes the goal. |
| 10 | Ticking boxes takes priority. |
| 25 | Optimizing for the criteria takes priority. |
| 100 | Doing the minimum becomes the strategy. |

The gap view keeps tracked areas quiet and emphasizes the other three with
larger names, an amber border, **3 areas untracked**, and a stronger continuous 1.25-second border-colour pulse, 5px outer ring, 18px soft glow and synchronized warning-icon pulse. Text and panel layout stay stationary; adding the remaining metrics removes the gap panel and ends the pulse. Reduced motion retains a static amber border.
Untracked areas are blind spots; no declining learning score is inferred.

Core metrics turn green one at a time, followed by the report cue. After each
scene, the observation and student summary appear together with one evidence
cue. Level 2 waits 1.6–2.8 visible seconds before dialogue, uses 300 ms typing dots,
and 1.1–2.2 second message intervals. The next action appears with the final
message, including Alex's last reply on the three- and six-metric pages. The
shared Conversation's optional onLastMessage callback releases the action;
onSettled still waits for the final reading interval before reporting completion.
Level 1 retains its 650ms typing and 3–5 second reply intervals; its finding interval is now 3.5 seconds shorter (2.5–4.5 seconds). All revealed text remains available.
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

The player and Alex dialogue uses the approved [Dialogue review](DIALOGUE_REVIEW.md). Alex sends two consecutive short messages at the chapter introduction and three/six-metric observations; the next action appears with the second reply. The shared conversation groups consecutive messages under one visible name/avatar and brings new replies into view when needed.
