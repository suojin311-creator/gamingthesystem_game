// Export the exact adapted film used by the game's Level 2 placeholder adapter.
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { viteSingleFile } from 'vite-plugin-singlefile';
import { levelTwoFilmPlugin } from './level2-film.mjs';

const root = fileURLToPath(new URL('../', import.meta.url));
export default {
  root, base: './',
  plugins: [{ name: 'placeholder-film-review-entry', enforce: 'pre', transform(code, id) {
    if (id === resolve(root, 'src/main.tsx')) return `import ${JSON.stringify(resolve(root, 'scripts/level2-review-entry.jsx'))};`;
  } }, levelTwoFilmPlugin(), viteSingleFile()],
};
