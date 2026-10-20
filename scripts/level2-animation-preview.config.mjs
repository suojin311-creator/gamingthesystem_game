// Independent review export. The partner checkout and game entries stay unchanged.
// LEVEL2_ANIMATION_SOURCE=/absolute/partner node <partner>/node_modules/vite/bin/vite.js
// build --config scripts/level2-animation-preview.config.mjs --outDir /tmp/level2-review
import { resolve } from 'node:path';
import { viteSingleFile } from 'vite-plugin-singlefile';

if (!process.env.LEVEL2_ANIMATION_SOURCE) throw new Error('Set LEVEL2_ANIMATION_SOURCE to the read-only Level 2 partner checkout.');
const root = resolve(process.env.LEVEL2_ANIMATION_SOURCE);
export default {
  root, base: './',
  plugins: [{
    name: 'export-authored-level2-review', enforce: 'pre',
    transform(code, id) {
      if (id === root + '/src/main.tsx') return `
import React from 'react';
import { createRoot } from 'react-dom/client';
import Level2DevPreview from './cinematics/level2/Level2DevPreview';
import './styles.css';
createRoot(document.getElementById('root')).render(
  <React.StrictMode><Level2DevPreview /></React.StrictMode>
);`;
      if (id === root + '/src/cinematics/level2/Level2DevPreview.tsx') {
        const original = '<a href="/">Opening</a>';
        if (!code.includes(original)) throw new Error('Review the partner preview navigation before exporting.');
        return code.replace(original, '<a href="./START-HERE.html">All previews</a>');
      }
    },
  }, viteSingleFile()],
};
