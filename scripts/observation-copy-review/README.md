# Level 2 observation text preview

The user approved five replacement paragraphs but requested a still preview
before updating downloadable game packages. Only five string values change in
src/levels/level2/data.ts. Production ObservationContent and all production CSS,
transitions, icons and layouts remain unchanged.

The preview displays the five real ObservationContent instances using their
existing Level 2 styles. Labels above the cards belong only to this review sheet.

```
node node_modules/vite/bin/vite.js build --config scripts/observation-copy-review/vite.config.mjs
python3 scripts/observation-copy-review/capture.py
```

Deliver play/Level2-observation-copy-preview.png. No game/classroom archives
are rebuilt by this review. The capture checks the unchanged computed palette
and 18px/24px text scale while producing the screenshot.
