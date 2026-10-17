# Gameplay dialogue review

Dialogue is tied to the selected metrics and submitted run history. It stays in
short spoken exchanges, with ordinary speech bubbles and separate teacher and
student portrait icons. The player label uses the opening-supplied name; it is
independent of either portrait. All authored emoji are distinct, as checked by
`node tests/dialogue_emojis.mjs`.

## Clarity and character

Each beat has a purpose: planning before publication, actual behaviour after
observation, changes between experiments during comparison, then the scoring
system's effect during the theory reveal. The teacher asks about something the
player can see. Alex answers that question before adding a playful follow-up.
Names and percentages are not recited again when the table already shows them.

Alex sends two short successive messages in workbench exchanges. Each has its
own typing indicator; only the first visibly repeats the name and portrait.
The second retains the speaker label for screen readers. Messages remain
available and scroll into view when necessary. Replaying a scene intentionally
keeps that scene's established dialogue.

## Level 1

Each metric has its own teacher review question, defined beside Alex's two
replies in `src/levels/level1/metrics.ts`. Preparation asks how Alex got through
the reading so quickly; participation asks what he was adding to the lesson;
focus asks how he used the time; discussion asks what the familiar phrases
helped him work out; reflection asks how he chose what to write; peer response
asks how he wrote the replies so fast.

The earlier classroom scene and later review use different lines. Evidence
stays visible and does not assert a measured learning loss. Completion still
waits for the final message's reading interval.

## Level 2

`src/levels/level2/dialogue.ts` supplies both classroom and observation dialogue.
The three-metric exchange uses the actual selected trio and its visible,
quality or mixed branch. It names the areas being discussed so references like
“the rest” have a clear context. The six-metric exchange asks whether Alex is
learning more or keeping up; he admits he is getting quick at ticking boxes.

At the end, the cinematic notices that adding requirements has not changed
what Alex is chasing. The returned workbench asks whether changing what counts
most would change his time allocation. Alex asks about the reward and offers
to make a plan. This replaces the question previously repeated verbatim at the
end of the cinematic and on the workbench.

The chapter introduction still waits for Choose three metrics. Observation
next actions appear with Alex's second message; final result reporting retains
its reading interval. The 10/25/100 stages continue to show checklist actions.

## Level 3

`src/levels/level3/dialogue.ts` supplies plans, reviews and comparisons from
immutable submitted runs. One higher reward, two higher rewards and near-even
weights have distinct plans and teacher questions. Later trials recognize
changed leading priorities, changes in qualitative effort, and unchanged effort
bands despite changed weights. A repeated metric/intensity shot has a fresh
follow-up line, without changing its scene ID or behavioural action.

Both player attempts and any system reference remain visible. Final dialogue
describes the actual order: a concentrated second trial is not described as an
improvement in balance. The comparison advances to the Goodhart theory
placeholder and stops there.

`node tests/dialogue_narrative.mjs` checks 8,640 complete combination paths for
repeated dialogue and emoji, plus every integer split's classification. The
production browser checks in `tests/dialogue_browser.py` read all three plans,
teacher reviews, unchanged effort, repeated scene replies and reversed trial
order, including role portraits on desktop and at 320px.

The partner's finished opening and video assets remain separate. The temporary
readings implement this dialogue; partner renderers receive playerName and run
history and can reuse the narrative helpers. The formal Goodhart quote stays
unchanged.
