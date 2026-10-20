import { useEffect, useRef } from 'react';
import AudioControls from '../../src/audio/AudioControls';
import { audioDirector } from '../../src/audio/director';
import type { Snapshot } from './types';
export default function LabAudio({state,view}:{state:Snapshot|null;view:string}){
 const previous=useRef(''),submission=useRef(false),vote=useRef('');
 useEffect(()=>{
  if(view==='host')return;
  const unlock=()=>audioDirector.unlock();
  try{const from=new URL(document.referrer);if(from.origin===location.origin&&from.pathname==='/game')unlock();}catch{/* Direct classroom join waits for the first gesture. */}
  document.addEventListener('pointerdown',unlock);document.addEventListener('keydown',unlock);
  return()=>{document.removeEventListener('pointerdown',unlock);document.removeEventListener('keydown',unlock);audioDirector.setScene('silent');};
 },[view]);
 useEffect(()=>{
  if(!state||view==='host')return;
  const phase=state.phase;
  audioDirector.setScene(phase==='ending'?'reveal':phase==='question1'||phase==='question2'||phase==='closed'?'silent':'lab',phase==='writing'?.32:phase==='review'?.28:phase==='ending'?.85:.45);
  if(previous.current&&previous.current!==phase&&phase==='ranking')audioDirector.cue('report');
  if(state.hasSubmitted&&!submission.current)audioDirector.cue('submit');
  submission.current=!!state.hasSubmitted;
  const key=state.card?.vote?state.card.id:'';
  if(key&&vote.current!==key)audioDirector.cue('vote');vote.current=key;
  previous.current=phase;
 },[state,view]);
 return view==='host'?null:<AudioControls/>;
}
