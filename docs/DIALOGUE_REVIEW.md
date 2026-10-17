# Gameplay dialogue review

This revision follows the proposed line-by-line review and the user's response
that emoji must not repeat. All 16 emoji have one source location across the
gameplay code. `node tests/dialogue_emojis.mjs` checks that inventory.

## Clarity and character

The three-metric exchange previously asked “Other parts?” without naming those
parts in the preceding line. It now explicitly identifies the other three areas.
The six-metric Alex reply previously answered a learning question from another
scene rather than the player's immediate proposal to add metrics. It now responds
to that proposal. Post-observation replies use everyday wording instead of
assessment jargon, while showing how Alex responds to the scoring system.

Alex sends two short, successive messages. Each has its own typing indicator;
only the first shows his name/avatar visibly. The second keeps the speaker label
for screen readers. Revealed messages remain available. New replies move into
view when needed. Emoji add a playful tone without replacing the meaning.

## Level 1 post-observation replies

The player asks: **“The score went up. What did you learn?”**

| Branch | Alex, first message | Alex, second message |
| --- | --- | --- |
| Preparation | I finished the whole list! 📋 | The reading? I mostly skimmed it 😬 |
| Participation | I put my hand up! 🙋 | I… didn’t really have an explanation 🤷 |
| Focus | I kept the page open! 💻 | That counts as staying focused… right? 👀 |
| Discussion | I used all the right phrases! 💬 | A new idea? Umm… 🤔 |
| Reflection | I followed the example! 📝 | I just used the same pattern again 🔁 |
| Peer response | A suggestion and a question! 🎯 | I use that pattern every time 🤭 |

The branch's observed classroom evidence stays visible. The dialogue illustrates
the behaviour behind the reported result without asserting a measured learning
loss. The existing final completion callback still waits for the last message's
reading interval.

## Level 2 exchanges

| Stage | Player | Alex, first message | Alex, second message |
| --- | --- | --- | --- |
| Chapter introduction | One metric wasn’t enough. What if I tracked three? | Three? Easy 😎 | Just tell me what gets the points. |
| Three metrics observed | These three look better. What about the other three? | Are those worth any points? 🧐 | I only worked on the three you picked 😇 |
| Six metrics observed | What if I added even more metrics? | Even more? 😅 | Okay… just tell me what gets the points. |

The final Level 2 player question, “What if some metrics mattered more than
others?”, already introduces the next weighting stage clearly and is retained.
The short Level 1 choice/prediction/result thoughts are also retained.

Choose three metrics appears with the chapter's second Alex message and waits
for the player's click. The three- and six-metric next actions also appear with
the second Alex message. Final result reporting retains its reading interval.

This review covers the gameplay bubbles. The supplied Narrative V2 classroom
readings remain temporary placeholders for the partner's finished cinematics;
this change does not edit or replace the partner's video assets.
