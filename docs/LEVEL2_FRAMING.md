# Earlier-level follow-up: Level 2 framing

The user approved Level 3 at `cdcff6ed5e34b4e09bd0998788152174ec71e04e`.
GitHub tag `level3-approved-v20` preserves that source and those downloads.
The Level 3 folder, Level 1 and shared gameplay modules are unchanged here.

## The missing link

The six-metric observation showed checklist behaviour and then offered Add more
metrics, but the interface never made the player's next hypothesis explicit.
The growth could read as a demonstration the player was obliged to watch.

The six-metric page now asks **Would more metrics help Alex learn?**, paired
with a small non-interactive **6 → ?** paper diagram. This replaces the generic
Look a little closer heading. It is visible before the review dialogue, not
buried in a character line. **Test more metrics** waits for an explicit click
after the final reply. No extra question page, mandatory answer or explanation
paragraph is added.

The growth heading stays **Testing more metrics.** through the continuous
10 → 25 → 100 sequence. The completed 100-item observation says **More metrics.
Still chasing marks.**, answering the initial question through the observed
behaviour. It does not invent a measured learning score or a scientific claim
that every use of more metrics fails.

## Earlier requests retained and checked

- Level 1 retains the original Run evaluation button plus Enter submission,
  whitespace rejection, Shift+Enter newline and IME handling.
- Its ending retains one teacher question, two grouped Alex replies and the
  brisk Level 2 pace. Continue appears with the last reply.
- Report updates retain their three attention pulses. Player Restart controls
  and action-footer helper captions remain absent.
- Level 2 keeps the previously implemented 3.5-second visible holds and
  0.7-second anticipated paper turns. Counter, matrix and paper stay mounted;
  hidden time pauses progression, and 100 waits for Observe the class.
- The original trio, opening name and sound continue into approved Level 3.
  Classroom scene IDs and authored partner scripts are unchanged; no extra
  peer interaction or replacement animation is generated.

The opening animation import and its Level 1 connection remain the previously
separated integration step. This work does not introduce a competing opener.

## Verification

`tests/level2_framing.py` exercises the production Level 1 controls/ending,
all three Level 2 narrative families, explicit hypothesis timing, desktop and
phone layout, normal/reduced motion, hidden-page holds and continuous growth.
`tests/level3_integration.py` exercises the actual partner and connected host;
only its Level 2 action label is updated. `tests/release.py` checks the actual
individual and connected ZIPs. Current results and artifact hashes are in
[LEVEL2_VALIDATION-v7.json](LEVEL2_VALIDATION-v7.json).
