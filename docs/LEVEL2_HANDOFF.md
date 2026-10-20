# Level 2 handoff

> Current animation-branch presentation: `LevelTwoCinematic` now replaces only
> the existing three/six/final placeholders. Post-film results omit the review
> conversation and arrange the existing observation above two equal perspective
> cards. The old conversation/replay-text details below are historical; current
> presentation and backup are in [Level 2 animation integration](LEVEL2_ANIMATION_PREVIEW.md).
> Request shapes, actual selected trio, explicit Observe actions and game-owned
> 10 → 25 → 100 growth remain unchanged.

## Flow and ownership

The game owns choosing exactly three metrics, evaluating, identifying the missing
three, expanding the system and displaying classroom evidence/checklist changes.
The partner owns finished cinematics. The opening remains separate.

Level 2 begins with a [chapter transition](CHAPTER_TRANSITIONS.md): a brief
hold on the prior target met / actual student consequence, a single metric card
filing away into three empty slots, and a prominent LEVEL 02 title. One teacher
line replaces the former three-message opening. After about three visible
seconds, the lower-right Choose three metrics button appears. The chapter stays
on screen until the player clicks it; the working metric selection starts empty.
The optional previousMetricId and previousObservation carry the real Level 1
card and student behaviour. Without that context, the standalone intro uses
“One metric” and “Learning still unclear.” rather than fabricating a choice.
Hidden tabs and off-screen chapters pause their beats and movement.

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
The six-metric observation asks **Would more metrics help Alex learn?** as the
page heading, with a non-interactive **6 → ?** paper diagram. This is visible
independently of the teacher/Alex exchange. Its **Test more metrics** action
appears with the existing final reply and waits for the player; the heading
replaces Look a little closer rather than adding a new page or paragraph.
One Test more metrics action runs the 10 → 25 → 100 sequence. Each milestone
changes the count/matrix and reveals a short illustrated checklist action. After
the 10- and 25-item actions finish, each holds for 3.5 visible seconds before
a 0.7-second paper turn. A persistent counter, matrix and paper surface prevents page replacement; the next milestone lights before the count changes. Internal transitions retain scroll position and paper height. Hidden/off-screen time does not consume either hold or turn. No repeated Add
click is required.
At 100, Observe the class plays the final scene. The last dashboard stays at
100 with **More metrics. Still chasing marks.**, answering the preceding
experiment through the observed checklist behaviour. The existing final
dialogue asks about relative importance as the bridge into Level 3.
Continue to Level 3 is enabled by the combined host's optional onContinue
callback. The standalone Level 2 entry leaves it reserved and disabled.

## Component contract

Import shared base CSS once in the host, before mounting levels:

```tsx
import LevelTwo from './levels/level2/LevelTwo';

<LevelTwo
  playerName={playerName}
  previousMetricId={levelOneResult?.metricId}
  previousObservation={levelOneMetric?.studentBehaviour}
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

Replay does not repeat completion. Player Restart controls are removed. Every fresh
page starts a new run. The callback does not automatically navigate to Level 3.
The explicit Continue to Level 3 action settles completion once before calling
onContinue(result), including when clicked before the final reading delay ends.

The shared `Gameplay` host forwards the opening's name to all three levels and their
scene requests. See [Opening handoff](OPENING_HANDOFF.md). Player decisions use
“I”; the older narrative's “we” is adapted to the player's first-person role.

## Presentation and lifetime

The shared short-name icon cards feed a three-slot Alex’s Checklist tray.
Players can review full selected definitions or remove a slot; the exactly-three
rules are unchanged. Core reports use icon/check cards; observations use shorter
two-part evidence beside the actual tracked/untracked notebook categories.
The 10/25/100 expansions add physical paper layers and check fields. Repeated
left-footer captions are removed. See [visual operations](VISUAL_PLAY.md).

The central content is the reading focus. Management’s view shows cumulative
satisfaction, retaining the previous value while a new evaluation is pending.
Each completed 3/6/10/25/100-metric report raises it once and shows its tracked
count as small evidence. It starts at Level 1’s final satisfaction and ends at
Level 3’s initial value, including standalone previews. See the shared
[satisfaction checkpoints](MANAGEMENT_SATISFACTION.md).
Starting a round resets students to **Awaiting observation**. The student
card shows the current behaviour with a small **Learning at risk** label only
when the current observation arrives. Behaviour is the main type; risk is secondary. Both levels render the shared LearningRisk component and stylesheet to keep this hierarchy identical.
Do not retain an observed-at count from an earlier round. The risk is a
qualitative interpretation of the story; actual learning gains remain unverified.
No sidebar badges, extra student sound or independently pulsing update competes
with the central content. The Level 2 header has a Sound control;
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
Level 1’s closing review now shares the brisk 300 ms typing, 1.1–2.2 second reply intervals and 1.6–2.8 second finding wait. Its earlier single workbench lines retain the original defaults. All revealed text remains available.
The 10/25/100 illustrations complete their checkmarks at 300 ms intervals, then
hold 3.5 visible seconds at 10/25. The next milestone highlights and the current
illustration fades out over a 700 ms paper turn; the same mounted counter runs
upwards and the next illustration fades in. The paper surface keeps its height
and no repeated automatic scrolling occurs. At 100 the final Observe action
waits for the player. Hidden/off-screen time pauses the sequence and its paper
animation. Reduced motion removes movement while retaining readable holds and
milestone cues. Sound preference carries between levels in page memory.

No game storage, runtime server, API key or multiplayer service is used.
Two students at one computer share one run. Classroom network capacity and
finished-video delivery should be checked separately when hosting is chosen.

The player and Alex dialogue uses the approved [Dialogue review](DIALOGUE_REVIEW.md). Alex sends two consecutive short messages at the three/six-metric observations and final weighting bridge; the next action appears with the second reply. The three-metric exchange uses the actual selected trio and branch, while the final cinematic and workbench have different lines. The shared conversation groups consecutive messages under one visible name/avatar and brings new replies into view when needed.

Equivalent typography now shares responsive tokens with Levels 1 and 3, including 16px ordinary metric names. There is no player Restart button or dialog; administrator functionality is deferred. See [Typography](TYPOGRAPHY.md).

The added v12 peer demonstration, generated peer narrative and `peerInteraction` field are withdrawn. The original classroom placeholder/dialogue and request schema are restored. The user’s existing finished-animation script owns classroom events. A custom `renderCinematic` replaces the entire placeholder; no second peer panel is rendered before or after it.

## Current checkpoint

The approved Level 3 is frozen at Git tag `level3-approved-v20`
(`cdcff6ed5e34b4e09bd0998788152174ec71e04e`). This framing release changes only
Level 2's six-metric question, small diagram, expansion action and growth/final
headings. It preserves the approved Level 3 folder, Level 1, shared components,
all partner scene scripts/IDs and timing logic. See
[Level 2 framing](LEVEL2_FRAMING.md) and
[LEVEL2_VALIDATION-v7.json](LEVEL2_VALIDATION-v7.json).
