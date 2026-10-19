import { resolve } from 'node:path';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { viteSingleFile } from 'vite-plugin-singlefile';
if (!process.env.LEVEL1_ANIMATION_SOURCE) throw new Error('Set LEVEL1_ANIMATION_SOURCE to the unmodified partner checkout.');
const root = resolve(process.env.LEVEL1_ANIMATION_SOURCE);
const here = fileURLToPath(new URL('.', import.meta.url));
export default {
  root, base: './',
  resolve: {
    dedupe: ['react', 'react-dom', 'remotion', '@remotion/player'],
    alias: { '@partner': root + '/src', '@partner-assets': root + '/assets', '@preview-pacing': here + 'pacing.mjs', '@preview-presentation': here + 'presentation.jsx', '@preview-transitions': here + 'transitions.mjs' },
  },
  plugins: [{ name: 'independent-level1-film', enforce: 'pre', transform(code, id) {
    if (id === root + '/src/main.tsx') return readFileSync(here + 'cinematic-entry.jsx', 'utf8');
    if (id === root + '/src/cinematics/level1/ConsequenceScene.tsx') {
      // Freeze framing in this review build only; keep original prop animations.
      const start = code.indexOf('  const cameraPose = {');
      const end = code.indexOf('\n  };', start);
      if (start < 0 || end < start) throw new Error('Review the partner camera adapter: source structure changed.');
      return code.slice(0, start) + '  const cameraPose = { scale: 1.025, x: 0, y: 0, vignette: 0 };' + code.slice(end + '\n  };'.length).replace('<div className="l1-scene-shading" />', '');
    }
  } }, viteSingleFile()],
};
