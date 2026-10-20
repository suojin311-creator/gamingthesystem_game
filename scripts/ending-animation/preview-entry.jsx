import React, { useEffect, useMemo, useRef, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { preloadAdaptationArt } from '@level3a/cinematics/level3/MetricAdaptationScene';
import { branches } from '@ending/cinematics/level1/level1Content';
import office from '@ending-assets/backgrounds/BG_Office_FirstPerson_v01.png';
import hand from '@ending-assets/characters/alex-rig/production/actions/checking/ALEX-HAND-CHECKING.png';
import { endingInputFromRuns } from '../../src/cinematics/ending/input';
import { dissolveFrame } from '../cinematic-dissolve.mjs';
import Composition from './Composition';
import { DURATION, SECTIONS, actualShotAt, sectionAt } from './timeline.mjs';

const CASES = {
  changed: { title:'Effort changes · no near-even trial', metrics:['prep','discuss','peer'], weights:[[60,30,10],[10,60,30]] },
  unchanged: { title:'Same effort · no near-even trial', metrics:['part','focus','reflect'], weights:[[60,30,10],[62,28,10]] },
  three: { title:'Three actual trials', metrics:['peer','reflect','discuss'], weights:[[60,30,10],[45,45,10],[34,33,33]] },
};
function Preview() {
  const params = new URLSearchParams(location.search), initialCase = CASES[params.get('case')] ? params.get('case') : 'changed';
  const [caseId,setCaseId] = useState(initialCase), [ready,setReady] = useState(false), [error,setError] = useState(false);
  const [time,setTime] = useState(0), [playing,setPlaying] = useState(true), [speed,setSpeed] = useState(1), [completed,setCompleted] = useState(0);
  const reducedMotion = params.get('reduced') === '1' || matchMedia('(prefers-reduced-motion:reduce)').matches;
  const surface=useRef(null),clock=useRef(0),changing=useRef(false),transition=useRef(null),done=useRef(false),currentKey=useRef('opening');
  const input=useMemo(()=>{
    const example=CASES[caseId];
    return endingInputFromRuns(example.metrics[0],example.weights.map((weights,index)=>({round:index+1,kind:'player',metricIds:example.metrics,weights})));
  },[caseId]);
  // Decode every image once, including lazy recollection artwork, before autoplay.
  useEffect(()=>{let live=true;const urls=[office,hand,...Object.values(branches).map(branch=>branch.plate)];Promise.all([preloadAdaptationArt(),...urls.map(url=>{const image=new Image();image.src=url;return image.decode();})]).then(()=>{if(live)setReady(true);},()=>{if(live)setError(true);});return()=>{live=false;};},[]);
  const keyAt=t=>{const section=sectionAt(t);return section.id==='level3'?section.id+':'+actualShotAt(input,t-section.start).sceneId:section.id;};
  const seek=(next,resume=false)=>{
    transition.current?.cancel();changing.current=false;
    const t=Math.max(0,Math.min(DURATION,next));clock.current=t;currentKey.current=keyAt(t);setTime(t);setPlaying(resume);
    if(t<DURATION)done.current=false;
  };
  useEffect(()=>{
    if(!ready||!playing)return;
    let raf=0,last=performance.now();
    const tick=now=>{
      if(!document.hidden&&!changing.current){
        const next=Math.min(DURATION,clock.current+Math.min(100,now-last)/1000*speed),key=keyAt(next);
        const commit=()=>{clock.current=next;currentKey.current=key;setTime(next);};
        if(key!==currentKey.current){changing.current=true;transition.current=dissolveFrame(surface.current,commit,{duration:520,reducedMotion});transition.current.finished.then(()=>{changing.current=false;});}
        else commit();
        if(next>=DURATION){setPlaying(false);if(!done.current){done.current=true;setCompleted(n=>n+1);}return;}
      }
      last=now;raf=requestAnimationFrame(tick);
    };
    raf=requestAnimationFrame(tick);return()=>cancelAnimationFrame(raf);
  },[ready,playing,speed,input,reducedMotion]);
  useEffect(()=>()=>transition.current?.cancel(),[]);
  const pause=()=>{setPlaying(false);transition.current?.pause();};
  const play=()=>{setPlaying(true);transition.current?.play();};
  const reset=()=>{seek(0,true);setCompleted(0);done.current=false;};
  return <>
    <div className="ending-viewport" data-completions={completed} data-case={caseId}><div className="ending-screen">
      <Composition {...{input,time,reducedMotion,surface}} />
      {!ready&&<div className="ending-loading" role="status">{error?'The animation could not load. Please reopen the preview.':'Preparing the ending…'}</div>}
    </div></div>
    <details className="ending-review-controls"><summary>预览控制</summary><div>
      <button type="button" disabled={!ready} onClick={()=>playing?pause():play()}>{playing?'Pause':'Play'}</button>
      <button type="button" onClick={reset}>Replay</button>
      <label>History <select aria-label="History" value={caseId} onChange={e=>{seek(0,false);setCaseId(e.target.value);setCompleted(0);done.current=false;setPlaying(true);}}>{Object.entries(CASES).map(([key,value])=><option key={key} value={key}>{value.title}</option>)}</select></label>
      <label>Scene <select aria-label="Scene" value={sectionAt(time).id} onChange={e=>seek(SECTIONS.find(s=>s.id===e.target.value).start)}>{SECTIONS.map(s=><option key={s.id} value={s.id}>{s.title}</option>)}</select></label>
      <label>Speed <select aria-label="Speed" value={speed} onChange={e=>setSpeed(Number(e.target.value))}>{[1,2,4].map(n=><option key={n}>{n}</option>)}</select></label>
      <label className="ending-scrub">Time <input aria-label="Preview time" type="range" min="0" max={DURATION} step=".05" value={time} onChange={e=>seek(Number(e.target.value))}/></label>
      <output>{time.toFixed(1)} / {DURATION}s</output>
    </div></details>
  </>;
}
createRoot(document.getElementById('root')).render(<Preview/>);
