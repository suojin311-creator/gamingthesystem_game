import { defineConfig } from 'vite';
import { viteSingleFile } from 'vite-plugin-singlefile';
import { levelOneFilmPlugin } from './scripts/level1-film.mjs';

export default defineConfig({
  base: './',
  plugins: [levelOneFilmPlugin(), viteSingleFile()],
  build: { target: 'es2022' },
});
