import { createHash } from 'node:crypto';
import { existsSync, mkdirSync, readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
const root=fileURLToPath(new URL('../',import.meta.url));
const cache=resolve(root,'node_modules/.cache/ending-cinematic'),html=resolve(cache,'index.html'),manifest=resolve(cache,'manifest.json');
const sources=[['ENDING_ANIMATION_SOURCE','e467998dfb07abc028e4e0fcb5567006e4eaa07d'],['LEVEL3_ANIMATION_SOURCE','ba9f81ee619c14b3342104228cdd2a5cc2bc2b3b']];
const paths=[...readdirSync(resolve(root,'scripts/ending-animation')).sort().map(n=>'scripts/ending-animation/'+n),'scripts/ending-film.mjs','scripts/cinematic-dissolve.mjs','scripts/level3-animation/cinematic.config.mjs','src/cinematics/opening/styles.css','src/cinematics/ending/input.ts','src/cinematics/level3/mapping.mjs','src/shared/data/cinematicPalette.js','src/levels/level3/data.ts','src/levels/level3/weights.ts','src/levels/level3/dialogue.ts','src/shared/data/metrics.ts'];
const sha=b=>createHash('sha256').update(b).digest('hex');
const fingerprint=()=>sha(Buffer.concat(paths.map(p=>Buffer.concat([Buffer.from(p+'\0'),readFileSync(resolve(root,p))]))));
function cached(){if(!existsSync(html)||!existsSync(manifest))return false;const m=JSON.parse(readFileSync(manifest));return m.sourceSha256===fingerprint()&&m.htmlSha256===sha(readFileSync(html))&&JSON.stringify(m.sources)===JSON.stringify(sources.map(([source,commit])=>({source,commit})));}
export function prepareEndingFilm(){
  if(cached()){process.stdout.write('Reusing the approved ending cinematic cache.\n');return;}
  for(const [env,pin]of sources){
    const dir=process.env[env];if(!dir)throw new Error('Prepare the ending with '+env+' pointing to its pinned read-only delivery.');
    const result=spawnSync('git',['-C',dir,'rev-parse','HEAD'],{encoding:'utf8'});
    if(result.status!==0||result.stdout.trim()!==pin||spawnSync('git',['-C',dir,'diff','--quiet','HEAD']).status!==0)throw new Error('Use the unchanged pinned source: '+env);
  }
  const result=spawnSync(process.execPath,[resolve(root,'node_modules/vite/bin/vite.js'),'build','--config',resolve(root,'scripts/ending-animation/preview.config.mjs'),'--outDir',cache,'--emptyOutDir'],{cwd:root,env:{...process.env,VITE_ENDING_EMBEDDED:'1'},stdio:'inherit'});
  if(result.error)throw result.error;if(result.status!==0)throw new Error('Ending film build failed.');
  mkdirSync(cache,{recursive:true});writeFileSync(manifest,JSON.stringify({sources:sources.map(([source,commit])=>({source,commit})),sourceSha256:fingerprint(),htmlSha256:sha(readFileSync(html))},null,2)+'\n');
}
export function endingFilmPlugin(){return{name:'ending-cinematic-html',enforce:'pre',resolveId(id){if(id==='virtual:ending-cinematic-film')return'\0'+id;},load(id){if(id!=='\0virtual:ending-cinematic-film')return;if(!cached())throw new Error('Ending cache is stale; run cinematic:prepare with the pinned ending and Level 3A sources.');return'export default '+JSON.stringify(readFileSync(html,'utf8'))+';';}};}
if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url))prepareEndingFilm();
