import { useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import film from 'virtual:ending-cinematic-film';
import type { MetricId } from '../../shared/data/metrics';
import type { WeightRun } from '../../levels/level3/data';
import { endingInputFromRuns } from './input';
import './styles.css';

/** The approved film holds its final page; it never opens the old theory slot. */
export default function EndingCinematic({ levelOneMetricId, runs }: { levelOneMetricId: MetricId; runs: WeightRun[] }) {
  const frame=useRef<HTMLIFrameElement>(null),runId=useRef(crypto.randomUUID());
  const [input]=useState(()=>endingInputFromRuns(levelOneMetricId,runs));
  const [finished,setFinished]=useState(false);
  useEffect(()=>{
    const previous=document.body.style.overflow;document.body.style.overflow='hidden';
    const receive=(event:MessageEvent)=>{
      const data=event.data;
      if(event.source!==frame.current?.contentWindow||data?.channel!=='ending-cinematic')return;
      if(data.type==='ready')frame.current.contentWindow?.postMessage({channel:'ending-cinematic',type:'start',runId:runId.current,input,reducedMotion:matchMedia('(prefers-reduced-motion:reduce)').matches},'*');
      if(data.type==='complete'&&data.runId===runId.current)setFinished(true);
    };
    addEventListener('message',receive);
    return()=>{removeEventListener('message',receive);document.body.style.overflow=previous;};
  },[input]);
  return createPortal(<section className="ending-cinematic" data-testid="ending-cinematic" data-scene-id="level3.compare" data-finished={finished} aria-label="Ending animation"><iframe ref={frame} title="Ending animation" srcDoc={film} allow="autoplay; fullscreen" allowFullScreen /></section>,document.body);
}
