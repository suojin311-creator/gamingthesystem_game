# Typography across Levels 1–3

Shared interface roles use responsive tokens in `src/shared/styles/base.css`.
The ordinary metric name is now 16px in all three levels, in selection cards and main result lists. Level 3’s compact comparison uses 15px metric names for its own layout. Deliberate warning emphasis is retained: Level 2’s
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
| Management satisfaction state | 30px | 25px |
| Management report evidence | 11px | 10px |
| Student behaviour | 25px | 21px |
| Evidence paragraph | 22px | 20px |
| Cinematic spoken caption | 26px | 23px |

All three chapter titles use 25px below 350px. On short desktop viewports the
shared section heading uses 26px. A tablet primary action uses the shared
responsive button rules. These changes depend on viewport, not chapter.

The Level 3 tables have been revised for visual balance rather than forcing
all content into a single size. Readable 22px sans-serif percentages, 16px
medium-weight effort labels and slim bars replace the earlier tiny numbers
and oversized bold labels. Main metric names are 16px; compact comparison
names are 15px. Repeated summaries and card footnotes are removed. Headings,
columns and row spacing align across all displayed attempts.

`tests/typography.py` measures the actual production DOM at 1366px, 390px and
320px, verifies equality across chapters for ordinary interface roles, verifies
16px metric names, and checks that selection layouts do not overflow. Current
measurements are included in the release validation report. Narrative intro
text is intentionally larger than ordinary workbench dialogue.

Management satisfaction uses the same component and stylesheet in all three
chapters. Its initial Awaiting results state uses 25px desktop / 22px phone.
Report numbers are supporting evidence, not the main display.
