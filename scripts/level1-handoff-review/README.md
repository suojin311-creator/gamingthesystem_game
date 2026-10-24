# Level 1 chapter-to-workbench handoff review

Independent preview only; formal source and game packages unchanged.
Uses actual ChapterTransition, Gameplay and first-use WorkbenchGuide. Existing
chapter reading hold is unchanged. On entry, both chapter and workbench overlap
for a 0.7-second dissolve, with no extra click or black screen. The original first
use guide is delayed until 1.05 seconds after workbench mount, then fades in.
Its automatic-focus behavior and Skip guide action remain intact.

The guide delay is injected only by this review's Vite transform. Film payloads
are excluded because this scope ends at the actual six-metric selection screen.
No new production game entry or divergent rules are introduced.

Build: `node node_modules/vite/bin/vite.js build --config scripts/level1-handoff-review/vite.config.mjs`
Record: `PLAYWRIGHT_BROWSERS_PATH=/workspace/.cache/gts-playwright python3 scripts/level1-handoff-review/record.py`
Artifacts: play/Level1-handoff-preview.mp4, PNG and LEVEL1_HANDOFF_REVIEW.json.
