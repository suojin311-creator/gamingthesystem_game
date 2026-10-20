import { useEffect, useState } from 'react';
import AudioControls from './AudioControls';
import { audioDirector, type Scene, type Cue } from './director';
const tracks:[Scene,string][]=[['office','Opening · Office'],['metrics','Levels 1–3 · Shared theme'],['reflection','Ending · Reflection'],['lab','Design Lab · Quiet focus'],['reveal','Goodhart’s Law · Reveal']];
const effects:[Cue,string][]=[['tick','Select / tick'],['paper','Open / turn paper'],['notification','Email arrives'],['report','Result ready'],['warning','Learning at risk'],['transition','Change chapter'],['submit','Submit reflection'],['vote','Agree / Disagree']];
export default function SoundReview(){
 const [current,setCurrent]=useState<Scene>('silent'),[paused,setPaused]=useState(false),[state,setState]=useState(audioDirector.state);
 useEffect(()=>{const timer=setInterval(()=>setState(audioDirector.state),150);return()=>{clearInterval(timer);audioDirector.setScene('silent');};},[]);
 const choose=(scene:Scene)=>{audioDirector.unlock();audioDirector.setScene(scene,.8);setCurrent(scene);setPaused(false);};
 return <main style={{minHeight:'100vh',boxSizing:'border-box',padding:'8vh max(24px,8vw)',background:'#f8f4ea',color:'#34382e',font:'17px/1.6 Georgia,serif'}} data-audio-scene={state.scene} data-audio-playing={state.playing} data-audio-voices={state.voices}>
  <p style={{color:'#ad5840',font:'12px Arial',letterSpacing:'.15em'}}>GAMING THE SYSTEM · SOUND PREVIEW</p><h1 style={{fontWeight:400,fontSize:'clamp(36px,5vw,64px)',margin:'16px 0'}}>Listen, then play.</h1><p>Choose a music cue or try an interaction sound. The same score continues across the three levels.</p>
  <h2 style={{fontWeight:400,marginTop:28}}>Music</h2><div style={{display:'flex',gap:12,flexWrap:'wrap'}}>{tracks.map(([scene,label])=><button key={scene} onClick={()=>choose(scene)} aria-pressed={current===scene} style={{padding:'12px 18px',border:'1px solid #bdaa89',borderRadius:4,background:current===scene?'#ad5840':'#fffcf4',color:current===scene?'#fff5e3':'#34382e',cursor:'pointer'}}>{label}</button>)}</div>
  <button style={{marginTop:16,padding:'9px 18px'}} onClick={()=>{audioDirector.setScene(current,.8,!paused);setPaused(!paused);}}>{paused?'Resume music':'Pause music'}</button>
  <h2 style={{fontWeight:400,marginTop:28}}>Sound effects</h2><div style={{display:'flex',gap:12,flexWrap:'wrap'}}>{effects.map(([cue,label])=><button style={{padding:'10px 16px'}} key={cue} onClick={()=>{audioDirector.unlock();audioDirector.cue(cue);}}>{label}</button>)}</div>
  <nav style={{display:'flex',gap:24,marginTop:38,flexWrap:'wrap'}}><a href="/game">Play from the opening →</a>{[1,2,3].map(n=><a key={n} href={`/game?level=${n}`}>Level {n} →</a>)}<a href="/">Design Lab →</a></nav><AudioControls/>
 </main>;
}
