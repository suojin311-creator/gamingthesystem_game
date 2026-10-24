import React,{useEffect,useLayoutEffect,useRef,useState} from 'react';
import {createRoot} from 'react-dom/client';
import {PerspectivePanel} from '../../src/levels/level1/LevelOne';
import {getMetric} from '../../src/levels/level1/metrics';
import {METRIC_CATALOG} from '../../src/shared/data/metrics';
import Icon from '../../src/shared/components/Icon';
import '../../src/shared/styles/base.css';
import '../../src/levels/level2/styles.css';
import './review.css';
const metric=getMetric('part')!;
function Review(){
 const motion=new URLSearchParams(location.search).has('motion');
 const [focused,setFocused]=useState(!motion),[checked,setChecked]=useState(!motion);
 const [reported,setReported]=useState(!motion),[enabled,setEnabled]=useState(!motion);
 const stage=useRef<HTMLDivElement>(null),slot=useRef<HTMLLIElement>(null);
 const [geometry,setGeometry]=useState<{from:{left:number,top:number,width:number,height:number},to:{left:number,top:number,width:number,height:number}}|null>(null);
 const timers=useRef<ReturnType<typeof setTimeout>[]>([]),started=useRef(0),completed=useRef(false),focusedOnce=useRef(false);
 const after=(delay:number,fn:()=>void)=>timers.current.push(setTimeout(fn,delay));
 const mark=(key:string)=>{window.iconReviewTimings[key]=performance.now()-started.current;};
 useLayoutEffect(()=>{
  const measure=()=>{if(!stage.current||!slot.current)return;
   const a=stage.current.getBoundingClientRect(),b=slot.current.getBoundingClientRect();
   const width=Math.min(400,stage.current.clientWidth-48),height=225;
   setGeometry({from:{left:b.left-a.left-stage.current.clientLeft,top:b.top-a.top-stage.current.clientTop,width:b.width,height:b.height},
    to:{left:(stage.current.clientWidth-width)/2,top:(stage.current.clientHeight-height)/2,width,height}});
  };measure();const resize=new ResizeObserver(measure);if(stage.current)resize.observe(stage.current);return()=>resize.disconnect();
 },[]);
 useEffect(()=>{
  window.iconReviewTimings={};started.current=performance.now();if(!motion)return;
  after(1100,()=>{setFocused(true);mark('focusStart');});
  return()=>timers.current.forEach(clearTimeout);
 },[motion]);
 const focusComplete=()=>{
  if(!motion||!focused||focusedOnce.current)return;focusedOnce.current=true;mark('focusComplete');
  after(180,()=>{setChecked(true);mark('targetMet');after(650,()=>{setReported(true);mark('managementUpdate');});});
 };
 useEffect(()=>{if(focused&&geometry&&matchMedia('(prefers-reduced-motion: reduce)').matches)focusComplete();},[focused,geometry]);
 const managementComplete=()=>{
  if(!motion||completed.current)return;completed.current=true;mark('managementComplete');
  after(350,()=>{setEnabled(true);mark('buttonEnabled');});
 };
 return <div className="game-page level-one icon-review" data-checked={checked} data-reported={reported} data-focused={focused} data-enabled={enabled}>
 <header className="masthead"><a className="wordmark" href="#icon-review-main"><span className="brand-emblem" aria-hidden="true">g<span>s</span><i/></span><span>GAMING<br/><b>THE SYSTEM</b></span></a><span className="review-sound"><Icon name="sound"/>Sound on</span></header>
 <main className="workbench" id="icon-review-main">
 <div className="workbench-heading"><div className="chapter-heading"><span className="chapter-number">01</span><h1>One metric.</h1></div><span className="office-location"><span/>THE OFFICE</span></div>
 <nav className="stepper" aria-label="Level steps"><ol>{['Choose','Predict','Evaluate','Observe'].map((s,i)=><li key={s} className={i<2?'done':i===2?'current':''}><span className="step-number">{i<2?<Icon name="check"/>:String(i+1).padStart(2,'0')}</span>{s}</li>)}</ol></nav>
 <div className="workbench-body"><section className="decision-area icon-assessment-main">
 <div className="section-intro"><h2>{checked?'The target is met.':'Checking the metric.'}</h2></div>
 <div className="level-two single-metric-report"><div ref={stage} className="metric-stage" aria-label="Six metrics and your chosen metric">
 <ul className="l2-evaluation-list metric-overview">{METRIC_CATALOG.map(m=><li key={m.id} ref={m.id===metric.id?slot:undefined} className={`metric-option ${m.id===metric.id?'selected-slot':''}`} data-metric={m.id} aria-hidden={m.id===metric.id||focused}>
 <span className="l2-eval-name"><Icon name={m.id}/>{m.shortName}</span>
 </li>)}</ul>
 {geometry&&<div className="selected-metric-card" data-checked={checked} style={focused?geometry.to:geometry.from} onTransitionEnd={e=>{if(e.target===e.currentTarget&&e.propertyName==='width')focusComplete();}}>
 <span className="l2-eval-name"><Icon name={metric.id}/>{metric.shortName}</span>
 <span className="l2-eval-result" aria-live="polite">{checked?<><Icon name="check"/>Target met</>:focused?<><i className="l2-checking"/>Checking</>:<span className="selection-label">Selected</span>}</span>
 </div>}
 </div></div>
 <div className="action-row"><button type="button" className="button primary-button" disabled={!enabled}><Icon name="play"/>Observe the class</button></div>
 </section><PerspectivePanel metric={metric} evaluated={reported} observed={false} highlight={null} assessmentReport managementReplay={motion?{from:12,enabled:reported,onComplete:managementComplete}:undefined}/></div>
 </main><footer className="page-footer">GAMING THE SYSTEM · LEVEL 01</footer>
 </div>;
}
createRoot(document.getElementById('root')!).render(<Review/>);
