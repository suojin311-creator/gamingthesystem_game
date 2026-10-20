import { defineConfig } from 'vite';
import { fileURLToPath } from 'node:url';
export default defineConfig({
  root: fileURLToPath(new URL('.', import.meta.url)),
  base: '/',
  server: { host: '127.0.0.1', port: 5185, proxy: { '/api': 'http://127.0.0.1:3000' } },
  build: { outDir: 'web', emptyOutDir: true, target: 'es2022' },
});
