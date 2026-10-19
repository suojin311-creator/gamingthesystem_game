// Independent review only; never build the gameplay release with this config.
// Set LEVEL1_ANIMATION_SOURCE to the downloaded partner checkout, then run its
// Vite binary with --config <this file> --outDir <external output folder>.
import { resolve } from 'node:path';
import { viteSingleFile } from 'vite-plugin-singlefile';
if (!process.env.LEVEL1_ANIMATION_SOURCE) throw new Error('Set LEVEL1_ANIMATION_SOURCE to the unmodified animation checkout.');
const root = resolve(process.env.LEVEL1_ANIMATION_SOURCE);
export default {
  root, base: './',
  plugins: [{
    name: 'enable-authored-level1-review-entry', enforce: 'pre',
    transform(code, id) {
      if (id === root + '/src/main.tsx') return code.replaceAll('import.meta.env.DEV', 'true');
    },
  }, viteSingleFile()],
};
