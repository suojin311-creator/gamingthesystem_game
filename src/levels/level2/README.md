# Level 2 — Reserved

Put Level 2 gameplay, rules, data, dialogue and level-specific components here.
Its gameplay is not implemented yet.

`LevelTwoEntryPlaceholder.tsx` preserves the previously agreed next-level
introduction. It imports `styles.css` and is not mounted by the current App.

Use shared modules from `../../shared/`. Keep Level 2 rules and state in this
folder, rather than importing Level 1 internals. Connect the finished level
through `../../App.tsx` and pass any previous-level result through props or the
in-memory game host. The current Level 1 next-level button stays disabled.

Global design tokens and common buttons come from the shared base stylesheet;
Level 2 layout belongs in this folder's scoped stylesheet.
