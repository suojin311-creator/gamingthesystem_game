# Pending opening and ending copy review

This is an isolated review, pending user approval. Production source, cinematic
caches, six game ZIPs and the classroom ZIP remain unchanged.

- Opening: When you set the metrics, what are you measuring?
- After the current learning/numbers question, the new paragraphs read:
  - When a number becomes a measure, it ceases to be a good measure.
  - Your assessment doesn’t just measure learning, it shapes how students learn.
- The user explicitly corrected ceased to ceases; retain their measure wording.
- Opening only replaces the subtitle at build time. It imports the current
  Opening component without changing it.
- Ending uses local review copies of the current composition/timeline, extends
  the film to 37.2 seconds and keeps the existing actual-history memories.
  The new pages share the office background and gentle fades. The final
  invitation/title/button remain together after the two new sentences.
- No speaker labels, formal Goodhart title or decorative rule on the new pages.

Build with ENDING_ANIMATION_SOURCE and LEVEL3_ANIMATION_SOURCE pointing at the
unchanged pinned e467998 and ba9f81e deliveries, respectively:

```
node node_modules/vite/bin/vite.js build --config scripts/copy-review/ending.config.mjs --outDir /workspace/gamingthesystem_game/node_modules/.cache/copy-review/ending --emptyOutDir
node node_modules/vite/bin/vite.js build --config scripts/copy-review/opening.config.mjs --outDir /workspace/gamingthesystem_game/node_modules/.cache/copy-review/opening --emptyOutDir
PLAYWRIGHT_BROWSERS_PATH=/workspace/.cache/gts-playwright python3 scripts/copy-review/capture.py
```

The capture checks exact wording, ordering, labels and fade opacity, then records
real autoplay from the built review, using the existing system FFmpeg for MP4.
Deliver play/Opening-title-copy-preview.png and play/Ending-copy-preview.mp4.
The ending recording is a visual review without a soundtrack. Existing game
music is not changed. Original interactive independent ending ZIP is preserved.

Latest typography review: all three reflection pages share Georgia 400, 3.6cqw body size and 1.65 line height. The question and principle highlights use a common 1.16 emphasis scale. Only becomes is coral and ceases gold on the principle page; number returns to body white. The assessment page uses two equal-size lines, gold then coral. Principle lasts 5.1 seconds instead of 7.1; subsequent sections shift two seconds earlier. Use capture.py --ending-only to preserve the unchanged opening screenshot.
