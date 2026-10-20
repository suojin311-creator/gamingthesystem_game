import { useCallback, useEffect, useRef, useState } from 'react';
import type { Snapshot } from './types';

/** Short, quiet ticks follow the same accelerated row position as the highlight. */
export default function useRankingSound(state: Snapshot | null, now: number) {
  const audio=useRef<AudioContext | null>(null),master=useRef<GainNode | null>(null);
  const voices=useRef(new Set<OscillatorNode>()),last=useRef('');
  const [muted,setMuted]=useState(false),[available,setAvailable]=useState(typeof AudioContext==='function');
  const mute=useRef(false);
  const stop=useCallback(()=>{voices.current.forEach(voice=>{try{voice.stop();}catch{/* Already ended. */}});voices.current.clear();},[]);
  const unlock=useCallback(()=>{
    if(mute.current || typeof AudioContext!=='function')return;
    try{
      if(!audio.current || audio.current.state==='closed'){
        audio.current=new AudioContext();master.current=audio.current.createGain();
        master.current.gain.value=.14;master.current.connect(audio.current.destination);
      }
      if(audio.current.state==='suspended')void audio.current.resume().catch(()=>setAvailable(false));
    }catch{setAvailable(false);}
  },[]);
  const toggle=useCallback(()=>{
    mute.current=!mute.current;setMuted(mute.current);
    if(mute.current)stop();else unlock();
  },[stop,unlock]);
  const scanning=state?.phase==='ranking' && state.ranking.length>0;
  const progress=scanning?Math.min(1,Math.max(0,(now-state.startedAt)/state.rankingMs)):0;
  const active=scanning?Math.min(state.ranking.length-1,Math.floor((state.ranking.length-1)*progress*progress)):-1;
  const scanId=scanning?`${state.sessionId}:${state.startedAt}`:'';
  useEffect(()=>{
    if(!scanning){last.current='';stop();return;}
    const key=`${scanId}:${active}`;
    if(last.current===key)return;last.current=key;
    const context=audio.current,gain=master.current;
    if(mute.current || !context || context.state!=='running' || !gain || document.hidden)return;
    const oscillator=context.createOscillator(),envelope=context.createGain(),at=context.currentTime;
    oscillator.type='sine';oscillator.frequency.setValueAtTime(440+progress*260,at);
    oscillator.frequency.exponentialRampToValueAtTime(280+progress*120,at+.045);
    envelope.gain.setValueAtTime(0,at);envelope.gain.linearRampToValueAtTime(.32,at+.004);
    envelope.gain.exponentialRampToValueAtTime(.001,at+.055);
    oscillator.connect(envelope);envelope.connect(gain);voices.current.add(oscillator);
    oscillator.onended=()=>{voices.current.delete(oscillator);oscillator.disconnect();envelope.disconnect();};
    oscillator.start(at);oscillator.stop(at+.065);
  // Progress shapes the pitch when the row changes; it must not retrigger a row.
  },[scanning,scanId,active,progress,stop]);
  useEffect(()=>{
    const visibility=()=>{if(document.hidden)stop();};
    document.addEventListener('visibilitychange',visibility);
    return()=>{document.removeEventListener('visibilitychange',visibility);stop();void audio.current?.close();};
  },[stop]);
  return {muted,available,unlock,toggle};
}
