# Level 2 highlighted narrative audit

The user's latest highlighted screenshot defines gameplay ownership. Narrative
screens are story beats; they do not require separate full-page click-throughs.
All player-facing content stays in English. The opening remains separate and
finished partner cinematics still use replaceable scene renderers.

The latest identity revision adapts the original collective player line to
“One metric wasn’t enough. What if I tracked three? Which ones should I choose?”
Other player decisions also use “I”. Maya is an internal role; the opening's
confirmed playerName replaces its displayed name in both levels and scene
requests. See [Opening handoff](OPENING_HANDOFF.md). Original source quotes below
are retained to identify the highlighted requirements, not current display text.

| Highlighted requirement | v2 gap | v3 implementation |
| --- | --- | --- |
| Choose three of the same six metrics | Implemented after an unnecessary introduction page | Level 2 immediately opens the six working metric cards; no extra entry click |
| Maya: “One metric wasn’t enough. What if we tracked three? Which ones would you choose?” | Last question missing | Complete line appears on the actual selection page |
| Alex: “Three metrics now? Okay, I can handle that!” | Missing | Alex replies in the same selection conversation |
| Alex opens a new notebook | No dedicated game-side representation | Passive three-entry notebook records the current choices; it is not a selection control |
| Run; three metrics turn green sequentially | Implemented | Retained, with three corresponding notebook checks |
| Add Remaining Metrics; all six metrics turn green | Implemented under a different button label | Add remaining metrics adds exactly the missing three; all six become green |
| Alex unfolds a longer checklist and checks six items | Only descriptive text in a placeholder | The game-side notebook expands to six entries and ends with six visible checks; the original three remain completed while the added three tick |

The notebook is an interface representation of Alex's actions. Finished shots of
Alex at the desk, character performance, voiced lines and camera work remain
with the cinematics creator.

The unhighlighted Three Metrics, Three Patterns scene remains the partner's
three branch slots. Its existing reading placeholder is still temporary. The
unhighlighted six-metric scene and Perfect Checklist scene remain partner slots
as documented in LEVEL2_HANDOFF.md. Their renderers do not need to explain
reported dashboard values.

The three Priority Slots and Set Priorities action are not highlighted in the
supplied screenshot and introduce the next weighting stage. They remain reserved
for Level 3. This revision does not implement weighting choices or add a dead
priority-selection page to Level 2.

The existing 10 → 25 → 100 expansion stages remain gameplay. Each checklist item
continues to tick in sequence. Post-scene next actions now appear with the final
reply; completion callbacks still wait for that reply's short reading interval.
