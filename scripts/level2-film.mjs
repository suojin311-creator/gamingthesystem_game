import { createHash } from 'node:crypto';
import { copyFileSync, existsSync, mkdirSync, readFileSync, writeFileSync, readdirSync } from 'node:fs';
import { resolve } from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('../', import.meta.url));
const cache = resolve(root, 'node_modules/.cache/level2-cinematic');
const html = resolve(cache, 'index.html');
const manifest = resolve(cache, 'manifest.json');
const PIN = 'c8c1c83456c4e67cf627df399bfb67b3a9792adb';
const files = readdirSync(resolve(root, 'scripts/level2-animation')).filter(name => /\.(mjs|jsx|css)$/.test(name)).sort().map(name => 'scripts/level2-animation/' + name);
files.push('src/shared/data/cinematicPalette.js');
files.push('scripts/cinematic-dissolve.mjs', 'scripts/cinematic-reading.mjs', 'scripts/metric100-preview/pacing.mjs');
const sha = data => createHash('sha256').update(data).digest('hex');
const fingerprint = () => sha(Buffer.concat(files.map(path => Buffer.concat([Buffer.from(path + '\0'), readFileSync(resolve(root, path)), Buffer.from('\0')]))));
function cached() {
  if (!existsSync(html) || !existsSync(manifest)) return false;
  const saved = JSON.parse(readFileSync(manifest, 'utf8'));
  return saved.sourceSha256 === fingerprint() && saved.htmlSha256 === sha(readFileSync(html)) && saved.partnerSourceCommit === PIN;
}
export function prepareLevelTwoFilm() {
  const supplied = process.env.LEVEL2_CINEMATIC_HTML;
  if (supplied) {
    mkdirSync(cache, { recursive: true });
    if (resolve(supplied) !== html) copyFileSync(resolve(supplied), html);
  } else if (cached()) {
    process.stdout.write('Reusing the verified Level 2 cinematic cache.\n');
    return;
  } else {
    const source = process.env.LEVEL2_ANIMATION_SOURCE;
    if (!source) throw new Error('Prepare Level 2 with LEVEL2_ANIMATION_SOURCE pointing to the pinned read-only delivery; see docs/LEVEL2_ANIMATION_PREVIEW.md.');
    const check = spawnSync('git', ['-C', source, 'rev-parse', 'HEAD'], { encoding: 'utf8' });
    if (check.status !== 0 || check.stdout.trim() !== PIN) throw new Error('Review and pin the changed Level 2 delivery before building.');
    const clean = spawnSync('git', ['-C', source, 'diff', '--quiet', 'HEAD']);
    if (clean.status !== 0) throw new Error('Keep partner tracked files unchanged.');
    const result = spawnSync(process.execPath, [resolve(source, 'node_modules/vite/bin/vite.js'), 'build', '--config', resolve(root, 'scripts/level2-animation/cinematic.config.mjs'), '--outDir', cache, '--emptyOutDir'], { cwd: root, env: process.env, stdio: 'inherit' });
    if (result.error) throw result.error;
    if (result.status !== 0) throw new Error(`Level 2 film build failed (${result.status}).`);
  }
  writeFileSync(manifest, JSON.stringify({ sourceSha256: fingerprint(), htmlSha256: sha(readFileSync(html)), partnerSourceCommit: PIN }, null, 2) + '\n');
}
export function levelTwoFilmPlugin() {
  return { name: 'level-two-cinematic-html', enforce: 'pre',
    resolveId(id) { if (id === 'virtual:level2-cinematic-film') return '\0' + id; },
    load(id) {
      if (id !== '\0virtual:level2-cinematic-film') return;
      const supplied = process.env.LEVEL2_CINEMATIC_HTML;
      if (!supplied && !cached()) throw new Error('The Level 2 film cache is missing or stale; run cinematic:prepare with LEVEL2_ANIMATION_SOURCE.');
      return 'export default ' + JSON.stringify(readFileSync(supplied ? resolve(supplied) : html, 'utf8'));
    },
  };
}
if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) prepareLevelTwoFilm();
