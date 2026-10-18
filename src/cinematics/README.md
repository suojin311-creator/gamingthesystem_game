# Finished animation integration

This folder is the destination for the partner's finished animation components
and their scene-local assets. No new animation script or placeholder is added.

Add the corresponding folders when their actual source is imported:

```text
cinematics/
  opening/        opening, existing name entry and its assets
  level1/         the six selected-metric scenes
  level2/         three-metric branches, six-metric and final checklist scenes
  level3/         weighted task shots, Alex's response and theory reveal
```

Keep each delivery's necessary relative imports/assets together. Expose one
adapter per supplied scene family and use the existing callbacks from
`src/Gameplay.tsx`; do not copy level rules into this folder. The actual adapters
will be implemented against the delivered source rather than guessed now.

Start with [Animation integration](../../docs/ANIMATION_INTEGRATION.md).
Use [Development workflow](../../docs/DEVELOPMENT_WORKFLOW.md) to preview only
the affected entry; build all downloadable versions when preparing a release.
