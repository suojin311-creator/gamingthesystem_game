# Typography across Levels 1–3

Equivalent content uses the same responsive token in `src/shared/styles/base.css`.
The ordinary metric name is now 16px in all three levels, including selection
cards and result lists. Deliberate warning emphasis is retained: Level 2’s
untracked metrics are 18px, bold, with the amber warning treatment.

| Content role | Desktop | 390px phone |
| --- | --- | --- |
| Chapter title | 31px | 29px |
| Step label | 12px | 9px |
| Metric name | 16px | 16px |
| Metric description | 11px | 11px |
| Main section heading | 29px | 28px |
| Primary action | 12px | 11px |
| Ordinary conversation | 15px | 15px |
| Level 2/3 chapter introduction conversation | 22px | 20px |
| Perspective heading | 12px | 11px |
| Perspective label | 11px | 10px |
| Student behaviour | 25px | 21px |
| Evidence paragraph | 22px | 20px |
| Cinematic spoken caption | 26px | 23px |

All three chapter titles use 25px below 350px. On short desktop viewports the
shared section heading uses 26px. A tablet primary action uses the shared
responsive button rules. These changes depend on viewport, not chapter.

The Level 3 result table deliberately distinguishes different roles: a repeated
score weight uses muted 18px text, while Alex’s effort uses bold 20px text and
larger qualitative bars. They are not quantitative effort percentages.

`tests/typography.py` measures the actual production DOM at 1366px, 390px and
320px, verifies equality across chapters for ordinary interface roles, verifies
16px metric names, and checks that selection layouts do not overflow. Current
measurements are included in the release validation report. Narrative intro
text is intentionally larger than ordinary workbench dialogue.
