import React,{useEffect,useMemo,useRef,useState} from 'react';
import {createRoot} from 'react-dom/client';
import film from 'virtual:level3-cinematic-film';
import {cinematicRequest} from '../src/levels/level3/data';
import {weightedSceneReply} from '../src/levels/level3/dialogue';
import {metricDefinition} from '../src/shared/data/metrics';
import './level2-review.css';
const groups={first:['prep','discuss','peer'],second:['part','focus','reflect']};
const patterns={shared:[34,33,33],one:[49,26,25],two:[45,45,10],graded:[60,30,10]};
function Review(){
  const query=new URLSearchParams(location.search),group=query.get('group')==='second'?'second':'first';
  const pattern=patterns[query.get('pattern')]?query.get('pattern'):'shared';
  const lead=[0,1,2].includes(Number(query.get('lead')))?Number(query.get('lead')):0;
  const[run,setRun]=useState(0),[playing,setPlaying]=useState(true),[elapsed,setElapsed]=useState(0),[duration,setDuration]=useState(0),[speed,setSpeed]=useState(1),[done,setDone]=useState(false),[count,setCount]=useState(0);
  const frame=useRef(null),token=useMemo(()=>crypto.randomUUID(),[run]);
  const request=useMemo(()=>{
    const weights=patterns[pattern].map((_,i)=>patterns[pattern][(i-lead+3)%3]);
    const r=cinematicRequest('weights','Review',[{round:1,kind:'player',metricIds:groups[group],weights}]);
    return{...r,shots:r.shots.map((s,i)=>({...s,caption:weightedSceneReply(r,i)}))};
  },[group,pattern,lead]);
  const control=(action,value)=>frame.current?.contentWindow?.postMessage({channel:'level3a-cinematic',type:'control',runId:token,action,value},'*');
  useEffect(()=>{
    const receive=event=>{const d=event.data;if(event.source!==frame.current?.contentWindow||d?.channel!=='level3a-cinematic')return;
      if(d.type==='ready')frame.current.contentWindow.postMessage({channel:'level3a-cinematic',type:'start',runId:token,request,preview:true,reducedMotion:query.get('reduced')==='1'||matchMedia('(prefers-reduced-motion:reduce)').matches},'*');
      if(d.runId!==token)return;
      if(d.type==='progress'){setElapsed(d.elapsed);setDuration(d.duration);}
      if(d.type==='complete'){setDone(true);setPlaying(false);setCount(n=>n+1);}
    };window.addEventListener('message',receive);return()=>window.removeEventListener('message',receive);
  },[token,request]);
  return <main className="level2-review"><header><h1>Level 3A animation preview</h1><a href="START-HERE.html">All previews</a></header>
    <nav aria-label="Metric groups"><a href={`?group=first&pattern=${pattern}&lead=${lead}`} aria-current={group==='first'?'page':undefined}>Preparation · Discussion · Peer response</a><a href={`?group=second&pattern=${pattern}&lead=${lead}`} aria-current={group==='second'?'page':undefined}>Participation · Focus · Reflection</a></nav>
    <nav aria-label="Effort patterns">{Object.entries({shared:'Shared attention',one:'One priority',two:'Two priorities',graded:'Graduated priorities'}).map(([key,label])=><a key={key} href={`?group=${group}&pattern=${key}&lead=${lead}`} aria-current={pattern===key?'page':undefined}>{label}</a>)}</nav>
    <nav aria-label="Emphasize a metric">{groups[group].map((id,index)=><a key={id} href={`?group=${group}&pattern=${pattern}&lead=${index}`} aria-current={lead===index?'page':undefined}>{metricDefinition(id).shortName}</a>)}</nav>
    <div className="review-controls"><button disabled={!duration||done} onClick={()=>{control(playing?'pause':'play');setPlaying(!playing);}}>{playing?'Pause':'Play'}</button><button onClick={()=>{setRun(run+1);setDone(false);setCount(0);setPlaying(true);setElapsed(0);setDuration(0);setSpeed(1);}}>Replay</button>
      <label>Speed <select aria-label="Speed" value={speed} onChange={e=>{const v=Number(e.target.value);setSpeed(v);control('speed',v);}}>{[1,2,4].map(n=><option key={n} value={n}>{n}×</option>)}</select></label>
      <label className="review-scrub">Preview time <input aria-label="Preview time" type="range" min={0} max={duration||1} step={.05} value={elapsed} disabled={!duration||done} onChange={e=>{const v=Number(e.target.value);control('seek',v);setElapsed(v);setPlaying(false);}}/></label><output>{elapsed.toFixed(1)} / {duration.toFixed(1)}s</output></div>
    <div className="review-stage"><iframe key={token} ref={frame} title="Level 3A classroom animation" srcDoc={film}/></div><footer data-completion-count={count} data-complete={done}>{done?'Clip complete':playing?'Playing':'Paused'} · Level 3A only</footer>
  </main>;
}
createRoot(document.getElementById('root')).render(<Review/>);
