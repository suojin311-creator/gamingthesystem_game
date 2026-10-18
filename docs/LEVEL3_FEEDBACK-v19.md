# Level 3 feedback and copy (v19)

Previous release saved before editing: `archive/pre-level3-feedback-v18` at
`25bc397aec1bad90158f318d1a0efbfd6a953509`.

- Remove every small heading above the editor question, including Follow the
  evidence and An optional check.
- Use “Can new weights make Alex go further?” after a fully covered first test.
- Remove the editor's allocation strip and 100% allocated label. Positive
  weights still total exactly 100%; confirmation and publication are unchanged.
- Shorten optional hints and remove the arbitrary paragraph-width limit.
  Desktop hints fit one line; narrow layouts wrap naturally without clipping.
- Keep Last observation's actual effort bands. Add the observed limitation:
  “Stopped after earning the marks he wanted.” This describes the existing
  stopping sequence across allocations, rather than pretending shared attention
  failed or predicting that another split will fix the stopping rule.

The effort model is unchanged: each task is minimum at 1–24%, steady at
25–66%, and intense at 67–98%. These cutoffs are implementation presets with
no derivation from Goodhart's Law or empirical effort data. They create a
known 24/25 display cliff. A continuous effort model remains a proposal to
agree with the user, not an implemented part of this release.

The two-test comparison, optional cancellable third, standalone/connected
entries, dynamic name handoff and final theory placeholder are unchanged.
Current checks and package hashes are in
[LEVEL3_VALIDATION-v19.json](LEVEL3_VALIDATION-v19.json).
