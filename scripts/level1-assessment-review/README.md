# Level 1 assessment visual review

Preview only. Production sources and formal packages are unchanged.
The review-only Vite transform exports actual ResultChart and removes its metric
name and duplicate percentage heading. It adds the metric-target caption below
numeric results. Actual PerspectivePanel and ManagementSatisfaction are reused.

Sequence: numeric growth; More students met the target for this metric.; management
status/fill update; Management is satisfied.; But… what changed in the classroom?;
Look behind the number enables after 0.5 seconds. No bottom teacher dialogue.
The preview button demonstrates availability and does not launch a movie.

Build: `node node_modules/vite/bin/vite.js build --config scripts/level1-assessment-review/vite.config.mjs`
Still: `python3 scripts/level1-assessment-review/capture.py`
Video: `PLAYWRIGHT_BROWSERS_PATH=/workspace/.cache/gts-playwright python3 scripts/level1-assessment-review/record.py`
