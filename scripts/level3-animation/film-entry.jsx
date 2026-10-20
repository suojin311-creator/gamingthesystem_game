import React, { useEffect, useMemo, useRef, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { MetricAdaptationScene, preloadAdaptationArt } from '@partner/cinematics/level3/MetricAdaptationScene';
import { metricLabel, participationBeat } from '@partner/cinematics/level3/adaptationTimeline';
import { adaptationClips } from '../../src/cinematics/level3/mapping.mjs';
import { SPEAKER_COLORS, CAPTION_SHADOW } from '../../src/shared/data/cinematicPalette.js';
import { dissolveFrame, smoothstep } from '../cinematic-dissolve.mjs';
import { createPacing, sampleAt, poseKey } from './pacing.mjs';
import './film.css';
const CHANNEL = 'level3a-cinematic';

function Film({ config }) {
  const pacing = useMemo(() => createPacing(adaptationClips(config.request)), [config]);
  const [elapsed,setElapsed] = useState(0), [playing,setPlaying] = useState(true), [finished,setFinished] = useState(false);
  const surface=useRef(null), clock=useRef(0), changing=useRef(false), transition=useRef(null), speed=useRef(1), complete=useRef(false);
  const key=useRef(poseKey(sampleAt(pacing,0),participationBeat));
  useEffect(()=>{window.parent.postMessage({channel:'gts-audio',playing:playing&&!finished,time:elapsed},'*');},[playing,finished,Math.floor(elapsed*4)]);
  const advance = next => {
    const nextKey=poseKey(sampleAt(pacing,next),participationBeat);
    const commit=()=>{clock.current=next;key.current=nextKey;setElapsed(next);};
    if(nextKey===key.current) return commit();
    changing.current=true;
    const differentClip=nextKey.split(':')[0]!==key.current.split(':')[0];
    transition.current=dissolveFrame(surface.current,commit,{duration:differentClip?520:300,reducedMotion:config.reducedMotion});
    transition.current.finished.then(()=>{changing.current=false;});
  };
  useEffect(()=>()=>transition.current?.cancel(),[]);
  useEffect(()=>{
    const receive=event=>{
      const d=event.data;
      if(event.source!==window.parent||d?.channel!==CHANNEL||d.runId!==config.runId||d.type!=='control')return;
      if(d.action==='pause'){setPlaying(false);transition.current?.pause();}
      if(d.action==='play'){setPlaying(true);transition.current?.play();}
      if(d.action==='speed'&&[1,2,4].includes(d.value))speed.current=d.value;
      if(d.action==='seek'&&Number.isFinite(d.value)&&!complete.current){transition.current?.cancel();changing.current=false;const time=Math.max(0,Math.min(pacing.duration-.001,d.value));clock.current=time;key.current=poseKey(sampleAt(pacing,time),participationBeat);setElapsed(time);setPlaying(false);}
    };
    if(config.preview)window.addEventListener('message',receive);
    return()=>window.removeEventListener('message',receive);
  },[config,pacing]);
  useEffect(()=>{
    if(!playing||finished)return;
    let frame=0,last=performance.now(),progressAt=0;
    const tick=now=>{
      if(!document.hidden&&!changing.current)advance(Math.min(pacing.duration,clock.current+Math.min(100,now-last)/1000*speed.current));
      last=now;
      if(config.preview&&now-progressAt>150){window.parent.postMessage({channel:CHANNEL,type:'progress',runId:config.runId,elapsed:clock.current,duration:pacing.duration},'*');progressAt=now;}
      if(clock.current>=pacing.duration){complete.current=true;setFinished(true);}else frame=requestAnimationFrame(tick);
    };
    frame=requestAnimationFrame(tick);return()=>cancelAnimationFrame(frame);
  },[playing,finished,config,pacing]);
  useEffect(()=>{
    if(!finished)return;
    let second=0;const first=requestAnimationFrame(()=>{second=requestAnimationFrame(()=>window.parent.postMessage({channel:CHANNEL,type:'complete',runId:config.runId},'*'));});
    return()=>{cancelAnimationFrame(first);cancelAnimationFrame(second);};
  },[finished,config.runId]);
  const current=sampleAt(pacing,elapsed);
  const color=SPEAKER_COLORS.alex;
  return <main ref={surface} className="l3-film" data-scene-id={config.request.sceneId} data-shot-id={current.sceneId} data-metric={current.metric} data-intensity={current.intensity} data-source-time={current.sourceTime.toFixed(3)} data-elapsed={elapsed.toFixed(3)} data-duration={pacing.duration.toFixed(3)} data-finished={finished}>
    <MetricAdaptationScene metric={current.metric} intensity={current.intensity} time={current.sourceTime} reducedMotion={config.reducedMotion} hideDialogue />
    <h2 className="l3-metric-name">{metricLabel(current.metric)}</h2>
    <div className="l3-spoken" style={{color,textShadow:CAPTION_SHADOW,WebkitTextStroke:'.035em #172019',paintOrder:'stroke fill'}}><p className="l3-speaker">Alex</p><p role="status">{current.caption}</p></div>
    <div className="l3-end-cover" aria-hidden="true" style={{opacity:finished?1:smoothstep((elapsed-(pacing.duration-.45))/.4)}} />
  </main>;
}
function Entry(){
  const[config,setConfig]=useState(null),[failed,setFailed]=useState(false);const started=useRef(false);
  useEffect(()=>{
    const receive=event=>{
      const d=event.data;if(event.source!==window.parent||d?.channel!==CHANNEL||d.type!=='start'||started.current||typeof d.runId!=='string')return;
      try{const clips=adaptationClips(d.request);if(clips.some(c=>typeof c.caption!=='string'||!c.caption.trim()))return;}catch{return;}
      started.current=true;
      preloadAdaptationArt().then(()=>setConfig(d),()=>setFailed(true));
    };
    window.addEventListener('message',receive);window.parent.postMessage({channel:CHANNEL,type:'ready'},'*');return()=>window.removeEventListener('message',receive);
  },[]);
  return config?<Film config={config}/>:<p className="l3-loading" role="status">{failed?'The classroom could not load. Please reopen the game.':'Preparing the classroom…'}</p>;
}
createRoot(document.getElementById('root')).render(<Entry/>);
