import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { viteSingleFile } from 'vite-plugin-singlefile';
if(!process.env.LEVEL2_ANIMATION_SOURCE)throw new Error('Set LEVEL2_ANIMATION_SOURCE to the pinned read-only original.');
const root=resolve(process.env.LEVEL2_ANIMATION_SOURCE),here=fileURLToPath(new URL('.',import.meta.url));
const replace=(code,from,to)=>{if(!code.includes(from))throw new Error('Review the original 100-metric adapter: '+from);return code.replace(from,to);};
export default {root,base:'./',resolve:{dedupe:['react','react-dom'],alias:{'@partner':root+'/src','@partner-assets':root+'/assets','@partner-scenes':root+'/docs/visual-style/references/Level 2 - More Metrics Consequences'}},plugins:[{name:'original-hundred-metric-review',enforce:'pre',transform(code,id){
  if(id===root+'/src/main.tsx')return `import ${JSON.stringify(here+'entry.jsx')};`;
  if(id===root+'/src/cinematics/level2/Level2ConsequencesSequence.tsx'){
    code=code.replace(/^import (visibleClassroom|qualityClassroom) from [^\n]+;$/gm,'const $1 = "";');
    code=replace(code,'const cameraDrift = reduced ? 0 : Math.sin(Math.PI * clamp01(elapsed / duration));','const cameraDrift = 0;');
    code=replace(code,'const cameraScale = 1.04 + cameraDrift * 0.045;','const cameraScale = 1.025;');
    code=replace(code,'vignette: final ? 0.62 : 0.35','vignette: 0');
    // Remove the original overlay nodes, never any of the authored paper text.
    code=code.replace(/^      <div className="l2-chapter">[^\n]+\n/m,'');
    code=code.replace(/^      \{CAPTIONS\[id\][^\n]+\n/m,'');
    code=code.replace(/^      <span className="l2-reference-credit">[^\n]+\n/m,'');
    const start=code.indexOf('      {dialogue && <div'),end=code.indexOf('\n      {id === \'priority\' && <p',start);
    if(start<0||end<0)throw new Error('Review original dialogue adapter.');
    return code.slice(0,start)+code.slice(end);
  }
}},viteSingleFile()]};
