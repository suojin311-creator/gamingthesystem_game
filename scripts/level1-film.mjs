import { createHash } from 'node:crypto';
import { copyFileSync, existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('../', import.meta.url));
const cache = resolve(root, 'node_modules/.cache/level1-cinematic');
const html = resolve(cache, 'index.html');
const manifest = resolve(cache, 'manifest.json');
const sourceFiles = [
  'scripts/level1-settlement/cinematic.config.mjs', 'scripts/level1-settlement/cinematic-entry.jsx',
  'scripts/level1-settlement/presentation.jsx', 'scripts/level1-settlement/content.mjs',
  'scripts/level1-settlement/pacing.mjs', 'scripts/level1-settlement/transitions.mjs',
  'src/shared/data/cinematicPalette.js',
];
const sha = data => createHash('sha256').update(data).digest('hex');
const fingerprint = () => sha(Buffer.concat(sourceFiles.map(path => Buffer.concat([Buffer.from(path + '\0'), readFileSync(resolve(root, path)), Buffer.from('\0')]))));
function cached() {
  if (!existsSync(html) || !existsSync(manifest)) return false;
  const saved = JSON.parse(readFileSync(manifest, 'utf8'));
  return saved.sourceSha256 === fingerprint() && saved.htmlSha256 === sha(readFileSync(html));
}

export function prepareFilm() {
  const supplied = process.env.LEVEL1_CINEMATIC_HTML;
  if (supplied) {
    mkdirSync(cache, { recursive: true });
    if (resolve(supplied) !== html) copyFileSync(resolve(supplied), html);
  } else if (cached()) {
    process.stdout.write('Reusing the verified Level 1 cinematic cache.\n');
    return;
  } else {
    const source = process.env.LEVEL1_ANIMATION_SOURCE;
    if (!source) throw new Error('Prepare Level 1 with LEVEL1_ANIMATION_SOURCE pointing to the pinned read-only partner checkout; see docs/ANIMATION_INTEGRATION.md.');
    const vite = resolve(source, 'node_modules/vite/bin/vite.js');
    const result = spawnSync(process.execPath, [vite, 'build', '--config', resolve(root, 'scripts/level1-settlement/cinematic.config.mjs'), '--outDir', cache, '--emptyOutDir'], { cwd: root, env: process.env, stdio: 'inherit' });
    if (result.error) throw result.error;
    if (result.status !== 0) throw new Error(`Level 1 cinematic build failed (${result.status}).`);
  }
  writeFileSync(manifest, JSON.stringify({ sourceSha256: fingerprint(), htmlSha256: sha(readFileSync(html)), partnerSourceCommit: '1bdd0c442c4b345b3bd37d6f541742d4e55c732f' }, null, 2) + '\n');
}

export function levelOneFilmPlugin() {
  return { name: 'level-one-cinematic-html', enforce: 'pre',
    resolveId(id) { if (id === 'virtual:level1-settlement-film') return '\0' + id; },
    load(id) {
      if (id !== '\0virtual:level1-settlement-film') return;
      const supplied = process.env.LEVEL1_CINEMATIC_HTML;
      if (!supplied && !cached()) throw new Error('The Level 1 film cache is missing or stale. Run npm run cinematic:prepare with LEVEL1_ANIMATION_SOURCE.');
      return 'export default ' + JSON.stringify(readFileSync(supplied ? resolve(supplied) : html, 'utf8'));
    },
  };
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) prepareFilm();
