import React,{useEffect,useRef,useState} from 'react';
import {createRoot} from 'react-dom/client';
import {Level2ConsequencesSequence} from '@partner/cinematics/level2/Level2ConsequencesSequence';
import {getLevel2Shots,shotAt} from '@partner/cinematics/level2/level2Timeline';
import {level2Performance} from '@partner/cinematics/level2/level2Performance';
import neutral from '@partner-assets/characters/alex-rig/production/base/ALEX-PROD-001 — Seated Alex Neutral.png';
import blink from '@partner-assets/characters/alex-rig/production/expressions/ALEX-PROD-002 — Blink.png';
import pleased from '@partner-assets/characters/alex-rig/production/expressions/ALEX-PROD-003 — Pleased.png';
import uncertain from '@partner-assets/characters/alex-rig/production/expressions/ALEX-PROD-004 — Uncertain.png';
import hand from '@partner-assets/characters/alex-rig/production/actions/checking/ALEX-HAND-CHECKING.png';
import classroom from '@partner-scenes/REF-L2-003 — Mixed : Broad Classroom.png?inline';
import {SPEAKER_COLORS,CAPTION_SHADOW} from '../../src/shared/data/cinematicPalette.js';
import {dissolveFrame} from '../cinematic-dissolve.mjs';
import {createHundredPacing,sampleAt} from './pacing.mjs';
import './style.css';
const request={requestId:'hundred-original-review',cinematicId:'level2',level:2,input:{phase:'100',selectedMetrics:['pre-class-preparation','in-class-participation','on-task-focus','in-class-discussion-quality','learning-reflection-quality','online-peer-response-quality']}};
const shots=getLevel2Shots(request),pacing=createHundredPacing(shots),ignore=()=>{};
function keyAt(t){const sample=sampleAt(pacing,t),current=shotAt(shots,sample.sourceSeconds),acting=level2Performance(current.shot.id,current.time);return `${current.shot.id}:${acting.view}:${acting.expression==='uncertain'?'uncertain':'base'}`;}
function Player(){
  const [ready,setReady]=useState(false),[failed,setFailed]=useState(false),[time,setTime]=useState(0),[playing,setPlaying]=useState(true);
  const reducedMotion=matchMedia('(prefers-reduced-motion:reduce)').matches;
  const surface=useRef(null),clock=useRef(0),key=useRef(keyAt(0)),transition=useRef(null),changing=useRef(false),lastTime=useRef(performance.now());
  useEffect(()=>{let live=true;Promise.all([neutral,blink,pleased,uncertain,hand,classroom].map(src=>{const img=new Image();img.src=src;return img.decode();})).then(()=>{if(live)setReady(true);},()=>{if(live)setFailed(true);});return()=>{live=false;transition.current?.cancel();};},[]);
  useEffect(()=>{
    const visibility=()=>{lastTime.current=performance.now();};
    document.addEventListener('visibilitychange',visibility);
    return()=>document.removeEventListener('visibilitychange',visibility);
  },[]);
  useEffect(()=>{
    if(!ready||!playing)return;let raf=0;lastTime.current=performance.now();
    const tick=now=>{
      if(!document.hidden){
        const next=Math.min(pacing.duration,clock.current+Math.max(0,now-lastTime.current)/1000),nextKey=keyAt(next);
        const commit=()=>{
          const entering=clock.current<pacing.conversationAt&&next>=pacing.conversationAt;
          // Start the one-second entrance after the outgoing snapshot has been
          // captured. Cloning its dense paper DOM must not consume the lead-in.
          const value=entering?pacing.conversationAt:next;
          clock.current=value;key.current=nextKey;setTime(value);
          if(entering)lastTime.current=performance.now();
        };
        if(nextKey!==key.current&&!changing.current){
          changing.current=true;transition.current=dissolveFrame(surface.current,commit,{duration:480,reducedMotion});transition.current.finished.then(()=>{changing.current=false;});
        }else commit();
        if(next>=pacing.duration){setPlaying(false);return;}
      }
      lastTime.current=Math.max(lastTime.current,now);raf=requestAnimationFrame(tick);
    };
    raf=requestAnimationFrame(tick);return()=>cancelAnimationFrame(raf);
  },[ready,playing,reducedMotion]);
  const seek=value=>{transition.current?.cancel();changing.current=false;clock.current=value;key.current=keyAt(value);setTime(value);setPlaying(false);};
  const sample=sampleAt(pacing,time),current=shotAt(shots,sample.sourceSeconds),line=sample.dialogue;
  const role=line?.speaker==='Alex'?'alex':'player';
  return <><div className="hundred-viewport"><main ref={surface} className="hundred-film" data-time={time.toFixed(3)} data-source={sample.sourceSeconds.toFixed(3)} data-shot={current.shot.id} data-segment={sample.id} data-finished={time>=pacing.duration} data-duration={pacing.duration}>
    {ready?<Level2ConsequencesSequence request={request} elapsed={sample.sourceSeconds} active={playing&&!document.hidden} reducedMotion={reducedMotion} onComplete={ignore}/>:<p className="hundred-loading" role="status">{failed?'Please reopen the preview.':'Preparing the animation…'}</p>}
    {ready&&line&&<div className="hundred-caption" data-role={role} style={{color:SPEAKER_COLORS[role],textShadow:CAPTION_SHADOW,fontStyle:role==='player'?'italic':'normal'}}><p className="hundred-speaker">{role==='player'?'You':'Alex'}</p><p role="status">{line.text}</p></div>}
  </main></div><details className="hundred-controls"><summary>预览控制</summary><div><button disabled={!ready} onClick={()=>{if(playing){setPlaying(false);transition.current?.pause();}else{if(time>=pacing.duration)seek(0);setPlaying(true);transition.current?.play();}}}>{playing?'Pause':'Play'}</button><button disabled={!ready} onClick={()=>{seek(0);setPlaying(true);}}>Replay</button><input aria-label="Preview time" type="range" min="0" max={pacing.duration} step=".01" value={time} onChange={event=>seek(Number(event.target.value))}/><output>{time.toFixed(1)} / {pacing.duration.toFixed(1)}s</output></div></details></>;
}
createRoot(document.getElementById('root')).render(<Player/>);
