import { createHash } from 'node:crypto';
import { existsSync, mkdirSync, readFileSync, writeFileSync, readdirSync } from 'node:fs';
import { resolve } from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
const root=fileURLToPath(new URL('../',import.meta.url));
const cache=resolve(root,'node_modules/.cache/level3-cinematic'),html=resolve(cache,'index.html'),manifest=resolve(cache,'manifest.json');
const PIN='ba9f81ee619c14b3342104228cdd2a5cc2bc2b3b';
const files=readdirSync(resolve(root,'scripts/level3-animation')).filter(n=>/\.(mjs|jsx|css)$/.test(n)).sort().map(n=>'scripts/level3-animation/'+n);
files.push('scripts/cinematic-dissolve.mjs','src/cinematics/level3/mapping.mjs','src/shared/data/cinematicPalette.js');
const sha=b=>createHash('sha256').update(b).digest('hex');
const fingerprint=()=>sha(Buffer.concat(files.map(path=>Buffer.concat([Buffer.from(path+'\0'),readFileSync(resolve(root,path)),Buffer.from('\0')]))));
function cached(){if(!existsSync(html)||!existsSync(manifest))return false;const m=JSON.parse(readFileSync(manifest));return m.sourceSha256===fingerprint()&&m.htmlSha256===sha(readFileSync(html))&&m.partnerSourceCommit===PIN;}
export function prepareLevelThreeFilm(){
  if(cached()){process.stdout.write('Reusing the verified Level 3A cinematic cache.\n');return;}
  const source=process.env.LEVEL3_ANIMATION_SOURCE;
  if(!source)throw new Error('Prepare Level 3A with LEVEL3_ANIMATION_SOURCE pointing to the pinned read-only delivery.');
  const pin=spawnSync('git',['-C',source,'rev-parse','HEAD'],{encoding:'utf8'});
  if(pin.status!==0||pin.stdout.trim()!==PIN)throw new Error('Use the pinned Level 3A branch, not Level 3B.');
  if(spawnSync('git',['-C',source,'diff','--quiet','HEAD']).status!==0)throw new Error('Keep partner source unchanged.');
  const result=spawnSync(process.execPath,[resolve(root,'node_modules/vite/bin/vite.js'),'build','--config',resolve(root,'scripts/level3-animation/cinematic.config.mjs'),'--outDir',cache,'--emptyOutDir'],{cwd:root,env:process.env,stdio:'inherit'});
  if(result.error)throw result.error;if(result.status!==0)throw new Error('Level 3A film build failed.');
  mkdirSync(cache,{recursive:true});writeFileSync(manifest,JSON.stringify({sourceSha256:fingerprint(),htmlSha256:sha(readFileSync(html)),partnerSourceCommit:PIN},null,2)+'\n');
}
export function levelThreeFilmPlugin(){return{name:'level-three-cinematic-html',enforce:'pre',resolveId(id){if(id==='virtual:level3-cinematic-film')return'\0'+id;},load(id){if(id!=='\0virtual:level3-cinematic-film')return;if(!cached())throw new Error('The Level 3A film cache is stale; run cinematic:prepare with LEVEL3_ANIMATION_SOURCE.');return'export default '+JSON.stringify(readFileSync(html,'utf8'))+';';}};}
if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url))prepareLevelThreeFilm();
