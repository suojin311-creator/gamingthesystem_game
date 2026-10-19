import { resolve } from 'node:path';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { viteSingleFile } from 'vite-plugin-singlefile';
if (!process.env.LEVEL1_ANIMATION_SOURCE) throw new Error('Set LEVEL1_ANIMATION_SOURCE to the unmodified partner checkout.');
const root = resolve(process.env.LEVEL1_ANIMATION_SOURCE);
const here = fileURLToPath(new URL('.', import.meta.url));
export default {
  root, base: './',
  resolve: { alias: { '@partner': root + '/src', '@preview-pacing': here + 'pacing.mjs' } },
  plugins: [{ name: 'independent-level1-film', enforce: 'pre', transform(code, id) {
    if (id === root + '/src/main.tsx') return readFileSync(here + 'cinematic-entry.jsx', 'utf8');
    if (id === root + '/src/cinematics/level1/Level1Composition.tsx') {
      // Supply the authored clock directly. Remotion Freeze would clamp the old
      // 33.4-second clock to the shorter player's duration and truncate the ending.
      const updated = code
        .replace('readonly reducedMotion?: boolean;', 'readonly reducedMotion?: boolean; readonly previewSourceFrame?: number;')
        .replace('reducedMotion = false }: Level1CompositionProps)', 'reducedMotion = false, previewSourceFrame }: Level1CompositionProps)')
        .replace('const frame = useCurrentFrame();', 'const liveFrame = useCurrentFrame(); const frame = previewSourceFrame ?? liveFrame;');
      if (updated === code || !updated.includes('previewSourceFrame ?? liveFrame')) throw new Error('The partner composition signature changed; review the preview adapter.');
      return updated;
    }
  } }, viteSingleFile()],
};
