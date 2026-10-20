import { useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import film from 'virtual:ending-cinematic-film';
import type { MetricId } from '../../shared/data/metrics';
import type { WeightRun } from '../../levels/level3/data';
import { endingInputFromRuns } from './input';
import './styles.css';
import { audioDirector } from '../../audio/director';
import { cinematicRunId } from '../../shared/utils/cinematicRunId';

/** The approved film holds its final page; it never opens the old theory slot. */
export default function EndingCinematic({ levelOneMetricId, runs }: { levelOneMetricId: MetricId; runs: WeightRun[] }) {
  const frame=useRef<HTMLIFrameElement>(null),runId=useRef(cinematicRunId());
  const [input]=useState(()=>endingInputFromRuns(levelOneMetricId,runs));
  const [finished,setFinished]=useState(false);
  const [labNote,setLabNote]=useState(false),[leaving,setLeaving]=useState(false);
  const navigating=useRef(false),navigationTimer=useRef(0);
  useEffect(()=>()=>clearTimeout(navigationTimer.current),[]);
  useEffect(()=>{
    const previous=document.body.style.overflow;document.body.style.overflow='hidden';
    const receive=(event:MessageEvent)=>{
      const data=event.data;
      if(event.source!==frame.current?.contentWindow||data?.channel!=='ending-cinematic')return;
      if(data.type==='ready')frame.current.contentWindow?.postMessage({channel:'ending-cinematic',type:'start',runId:runId.current,input,reducedMotion:matchMedia('(prefers-reduced-motion:reduce)').matches},'*');
      if(data.type==='complete'&&data.runId===runId.current)setFinished(true);
      if(data.type==='enter-lab'&&data.runId===runId.current&&!navigating.current){
        navigating.current=true;audioDirector.unlock();audioDirector.cue('transition');
        if(!/^https?:$/.test(location.protocol)){setLabNote(true);navigating.current=false;return;}
        void fetch('/api/display').then(r=>{if(!r.ok)throw new Error('classroom');return r.json();}).then(()=>{setLeaving(true);audioDirector.setScene('lab',.35);navigationTimer.current=window.setTimeout(()=>location.assign('/'),550);}).catch(()=>{setLabNote(true);navigating.current=false;});
      }
    };
    addEventListener('message',receive);
    return()=>{removeEventListener('message',receive);document.body.style.overflow=previous;};
  },[input]);
  return createPortal(<section className="ending-cinematic" data-testid="ending-cinematic" data-scene-id="level3.compare" data-finished={finished} aria-label="Ending animation"><iframe ref={frame} title="Ending animation" srcDoc={film} allow="autoplay; fullscreen" allowFullScreen />{leaving&&<div className="ending-lab-fade"/>}{labNote&&<div className="ending-lab-note" role="dialog" aria-modal="true" aria-label="Open Design Lab"><h2>Continue with your classroom.</h2><p>Open Start-Gaming-the-System.exe from the classroom package to play the game and join Design Lab together.</p><button type="button" onClick={()=>setLabNote(false)}>Back</button></div>}</section>,document.body);
}
