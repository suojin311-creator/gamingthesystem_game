# Level 1 assessment visual review

Preview only. Production source and formal packages are unchanged.
The Vite transform exports the actual ResultChart solely for review, removes its
metric name and duplicate subtitle. The heading is Percentage of students meeting
the criteria. The bridge reads Learning performance looks better. Management is
satisfied. But… inside a centered, lightly shaded chart-card footer above the Look behind the number button.

Build with `node node_modules/vite/bin/vite.js build --config scripts/level1-assessment-review/vite.config.mjs`, then run `python3 scripts/level1-assessment-review/capture.py`.

Video: `PLAYWRIGHT_BROWSERS_PATH=/workspace/.cache/gts-playwright python3 scripts/level1-assessment-review/record.py`.
The video reuses ResultChart, PerspectivePanel, ManagementSatisfaction and Dialogue.
It demonstrates counting, management update, bridge reveal, But emphasis/button
availability in that order. Original teacher dialogue is retained, fei is a sample
player name, and the film button remains preview-only (no movie is launched).
