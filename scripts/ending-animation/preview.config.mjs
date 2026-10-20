import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { viteSingleFile } from 'vite-plugin-singlefile';
import level3Config from '../level3-animation/cinematic.config.mjs';

const root = resolve(process.env.ENDING_ANIMATION_SOURCE || '');
if (!process.env.ENDING_ANIMATION_SOURCE) throw new Error('Set ENDING_ANIMATION_SOURCE to the pinned read-only ending delivery.');
const here = fileURLToPath(new URL('.', import.meta.url));
const replace = (code, from, to) => { if (!code.includes(from)) throw new Error('Review ending adapter: missing ' + from); return code.replace(from, to); };
export default {
  root, base:'./',
  resolve:{dedupe:['react','react-dom'],alias:{'@ending':root+'/src','@ending-assets':root+'/assets','@level3a':resolve(process.env.LEVEL3_ANIMATION_SOURCE)+'/src'}},
  plugins:[{name:'adapt-ending-preview',enforce:'pre',transform(code,id){
    if(id===root+'/src/main.tsx')return `import ${JSON.stringify(here+'preview-entry.jsx')};`;
    const task=level3Config.plugins[0].transform(code,id);
    if(task)return task;
    if(id===root+'/src/cinematics/ending/OfficeReveal.tsx'){
      code=replace(code,"import { Img } from 'remotion';",`import { Img } from ${JSON.stringify(here+'Still.jsx')};`);
      code=replace(code,"import { RecapMemories } from './EndingMemories';",'');
      code=replace(code,'const recap = seconds >= 48.8;','const recap = false;');
      // No invented all-green dashboard for a player who may have low effort.
      const start=code.indexOf('        <svg className="end-office-plane"'),end=code.indexOf('        <EnvironmentMotion',start);
      if(start<0||end<0)throw new Error('Review ending office dashboard.');
      code=code.slice(0,start)+code.slice(end);
      code=code.replace(/^    \{seconds >= 35 && seconds < 43[^\n]+\n/m,'');
      code=replace(code,'“{QUOTE}”','<span className="end-quote-line">“When a measure becomes a target,</span><span className="end-quote-line">it ceases to be a good measure.”</span>');
      code=code.replace(/^    \{recap && <RecapMemories[^\n]+\n/m,'');
      code=code.replace(/^    \{seconds >= 55\.2[^\n]+\n/m,'');
      return code;
    }
    if(id===root+'/src/cinematics/level1/ConsequenceScene.tsx'){
      code=replace(code,"import { Img, interpolate } from 'remotion';",`import { interpolate } from 'remotion'; import { Img } from ${JSON.stringify(here+'Still.jsx')};`);
      const start=code.indexOf('  const cameraPose = {'),end=code.indexOf('\n  };',start);
      if(start<0||end<0)throw new Error('Review ending Level 1 memory camera.');
      return (code.slice(0,start)+'  const cameraPose = { scale: 1.025, x: 0, y: 0, vignette: 0 };'+code.slice(end+'\n  };'.length))
        .replace('<div className="l1-scene-shading" />','').replace('Read Chapter 3','Read the assigned material').replace('Week 3','Coursework').replace('01 / 01','');
    }
    if(id===root+'/src/cinematics/level2/AlexCheckingSequence.tsx')return code.replace(/^import look from [^\n]+;$/m,'const look = "";').replace(/^import reaction from [^\n]+;$/m,'const reaction = "";');
    if(id===root+'/src/cinematics/level2/ChecklistSystem.tsx')return replace(code,'<div className="l2-checklist-tally"><strong>{number(completed)}</strong><span>/ {number(count)}</span></div>','');
  }},viteSingleFile()],
};
