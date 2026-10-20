import { resolve } from 'node:path';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { viteSingleFile } from 'vite-plugin-singlefile';

if (!process.env.LEVEL2_ANIMATION_SOURCE) throw new Error('Set LEVEL2_ANIMATION_SOURCE to the pinned, read-only Level 2 delivery.');
const root = resolve(process.env.LEVEL2_ANIMATION_SOURCE);
const here = fileURLToPath(new URL('.', import.meta.url));
const replace = (code, from, to) => {
  if (!code.includes(from)) throw new Error('Review the pinned Level 2 presentation adapter: missing ' + from);
  return code.replace(from, to);
};
export default {
  root, base: './',
  resolve: { dedupe: ['react', 'react-dom'], alias: { '@partner': root + '/src', '@partner-assets': root + '/assets' } },
  plugins: [{ name: 'placeholder-only-level2-film', enforce: 'pre', transform(code, id) {
    if (id === root + '/src/main.tsx') return `import ${JSON.stringify(here + 'film-entry.jsx')};`;
    if (id === root + '/src/cinematics/level2/Level2ConsequencesSequence.tsx') {
      // The retained dialogue-only scenes use Alex/hand artwork; wide establishing
      // plates are removed with the trimmed opening, not duplicated in downloads.
      code = code.replace(/^import (visibleClassroom|qualityClassroom|mixedClassroom) from [^\n]+;$/gm, 'const $1 = "";');
      code = replace(code, '<img className="l2-world-plate" src={classroom} alt="Alex, in his rust-orange hoodie, with classmates in a warm sunlit university classroom." />', 'null');
      code = replace(code, 'const cameraDrift = reduced ? 0 : Math.sin(Math.PI * clamp01(elapsed / duration));', 'const cameraDrift = 0;');
      code = replace(code, 'const cameraScale = 1.04 + cameraDrift * 0.045;', 'const cameraScale = 1.025;');
      return replace(code, 'vignette: final ? 0.62 : 0.35', 'vignette: 0');
    }
  } }, viteSingleFile()],
};
