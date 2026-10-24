# Automatic chapter entrance review

Current shared source changes apply to all three levels, not just the recorded
example. Wait for the final chapter dialogue animation to end, hold two visible
seconds, then call the real existing onStart continuation exactly once. Reduced
motion starts the two-second hold without waiting for a nonexistent animation.
Hidden/off-screen chapters pause through the existing visible-time hook.

Teacher questions in the six Level 1 branches, Level 2 dialogue and chapter
introductions no longer directly name Alex. The shared teacherSpeech policy also
covers imported teacher captions and legacy dialogue renderers. Student identity
labels remain Alex. Level 2/3 teacher-style result questions use generic wording.

The focused harness imports the real ChapterTransition, Gameplay and Level 2/3
components. Its virtual films are excluded to keep a chapter-only review small;
it never enters or verifies a film. The real Level 2 metric selection interface
is the recorded destination. Level 1 still uses its existing first-use guide.
The standard pinned-source Level 1/2 film builds validate the changed caption
adapters separately; regular game ZIPs are deliberately not regenerated here.

```
node node_modules/vite/bin/vite.js build --config scripts/chapter-review/vite.config.mjs
PLAYWRIGHT_BROWSERS_PATH=/workspace/.cache/gts-playwright python3 scripts/chapter-review/capture.py
npm run check
```

Capture checks levels 1, 2 and 3, the carried-priorities case, reduced motion,
background pause and actual teacher data. It records one normal-motion Level 2
chapter and its automatic entry to the six available metric cards. The MP4 is a
silent visual review. No pending opening/ending copy is merged by this work.
