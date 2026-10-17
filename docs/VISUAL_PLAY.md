# Visual operations across Levels 1–3

All three levels use `shared/components/MetricSelection.tsx`. The six cards show
one large category icon and its short name. Full official metric names remain
the accessible button labels and appear, with the original description, in the
selection tray after choosing a card. Review a filled slot to inspect another
selected metric; its separate × button removes it. No information depends on
hover. Pointer and keyboard selection use the same controls and rules.

Level 1 has one slot and supports direct replacement. Levels 2 and 3 have three
slots and retain the exactly-three limit and deselect-to-swap behaviour. Level 2
labels its tray Alex’s Checklist. Level 3 starts with the actual Level 2 trio in
the connected game; the tray remains editable. A short card flight and slot
arrival provide feedback without delaying the next action. Reduced motion
shows the filled slot immediately. Transient flights are removed on completion
or unmount. At tablet/phone widths the tray moves above the card grid.

Repeated left-side action-footer captions are removed across all three levels,
including selection counts, repeated current metric labels, evaluation-ready
messages and cover-all-six instructions. The buttons retain their meaningful
labels and disabled states. Necessary selection-limit feedback appears beside
the tray. Replay scene and Reset weights remain working controls.

`ObservationContent.tsx` replaces the single oversized text block with a small
illustrated notebook, a quieter observation and an emphasized behavioural
consequence. Level 1 retains each original evidence statement. Level 2’s three
branches and six/final observations use shorter, concrete two-part copy. Its
notebook shows the actual tracked categories, with untracked categories faded
outside it; observing all six removes the outside group.

Level 2 evaluations use short metric names and large icon/check cards. The
10/25/100 requirement field fills with checks, and the student checklist gains
decorative paper layers as requirements grow. These layers illustrate growing
administrative work; they are not literal page counts. The three original
checklist actions still reveal and tick one at a time. No duplicate checklist
is added to the three/six-metric evaluation dashboards.

`TaskEffort.tsx` adds an Alex desk vignette to Level 3 results and comparison:
intense effort writes rapidly beside a paper stack, steady effort works on a
single task, and minimum effort has a relaxed pose beside a checked sheet.
These are qualitative pictures driven by the same tested effort category as
the existing labels, bars and cinematic shots. Weight numbers are smaller;
short names and their familiar icons identify each task. Full metric names
remain in accessible row/slider labels. Both player attempts and any reference
retain their exact weights. Visual responses appear with the existing observed
rows, after the manual Observe action, never during allocation/publication.

The shared satisfaction milestones, actual selection/weight mechanics,
prediction input, teacher/Alex speech bubbles, opening-name handoff and partner
scene contracts are retained. These interface illustrations do not replace the
partner’s finished cinematic assets. There are no numerical learning or effort
scores, extra rewards for balanced weights, player Restart or Design Lab route.

`tests/visual_play.py` exercises all three production entries at 1366/768/390/
320px, including keyboard selection, removable/reviewable slots, exact choices,
empty/filled states, short cards with accessible definitions, footer removal,
illustrated evidence, paper growth, matching Alex poses and comparison records.
