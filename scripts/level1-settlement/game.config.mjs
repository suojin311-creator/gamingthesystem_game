import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { viteSingleFile } from 'vite-plugin-singlefile';
const root = fileURLToPath(new URL('../../', import.meta.url));
export default {
  root, base: './',
  plugins: [{ name: 'independent-level1-settlement', enforce: 'pre',
    resolveId(id) { if (id === 'virtual:level1-settlement-film') return '\0' + id; },
    load(id) { if (id === '\0virtual:level1-settlement-film') {
      if (!process.env.LEVEL1_CINEMATIC_HTML) throw new Error('Set LEVEL1_CINEMATIC_HTML to the built isolated player.');
      return 'export default ' + JSON.stringify(readFileSync(resolve(process.env.LEVEL1_CINEMATIC_HTML), 'utf8'));
    } },
    transform(code, id) { if (id === root + 'src/main.tsx') return "import './previews/level1-settlement/entry';"; },
  }, viteSingleFile()],
  build: { target: 'es2022' },
};
