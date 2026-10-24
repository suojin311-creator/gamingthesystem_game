import React,{useEffect,useState} from 'react';
import {createRoot} from 'react-dom/client';
import {ResultChart,PerspectivePanel} from '../../src/levels/level1/LevelOne';
import {getMetric} from '../../src/levels/level1/metrics';
import Dialogue from '../../src/levels/level1/components/Dialogue';
import Icon from '../../src/shared/components/Icon';
import '../../src/shared/styles/base.css';
import './review.css';
const metric=getMetric('part')!;
function Review(){
 const motion=new URLSearchParams(location.search).has('motion');
 const [score,setScore]=useState(motion?metric.before:metric.after);
 const [ready,setReady]=useState(!motion),[reported,setReported]=useState(!motion);
 const [bridge,setBridge]=useState(!motion),[but,setBut]=useState(!motion);
 useEffect(()=>{
  if(!motion)return;
  const started=performance.now();
  window.assessmentTimings={};
  const mark=(key:string)=>{window.assessmentTimings[key]=performance.now()-started;};
  let raf=0;
  const timers:ReturnType<typeof setTimeout>[]=[];
  timers.push(setTimeout(()=>{
   const begin=performance.now();mark('numberStart');
   const tick=(now:number)=>{const progress=Math.min(1,(now-begin)/2000);
    setScore(Math.round(metric.before+(metric.after-metric.before)*(1-(1-progress)**3)));
    if(progress<1)raf=requestAnimationFrame(tick);else{setReady(true);mark('numberComplete');
     timers.push(setTimeout(()=>{setReported(true);mark('managementUpdate');
      timers.push(setTimeout(()=>{setBridge(true);mark('bridgeReveal');
       timers.push(setTimeout(()=>{setBut(true);mark('butAndButton');},800));
      },1300));
     },900));
    }
   };raf=requestAnimationFrame(tick);
  },650));
  return()=>{timers.forEach(clearTimeout);cancelAnimationFrame(raf);};
 },[motion]);
 return <main className="level-one assessment-review" data-motion={motion} data-ready={ready} data-reported={reported} data-bridge={bridge} data-but={but}>
 <div className="assessment-context"><span className="chapter-number">01</span><h1>One metric.</h1></div>
 <div className="assessment-layout"><section className="assessment-main">
 <div className="section-intro"><h2>Percentage of students meeting the criteria</h2></div>
 <section className="assessment-card">
 <ResultChart metric={metric} ready={ready} score={score} assessmentReport />
 <div className="assessment-bridge"><p><span className="bridge-statement" data-visible={bridge}>Learning performance looks better. Management is satisfied.</span> <strong data-visible={but}>But…</strong></p></div>
 </section>
 <div className="action-row"><button type="button" className="button primary-button" disabled={!but}><Icon name="play"/>Look behind the number</button></div>
 </section><PerspectivePanel metric={metric} evaluated={reported} observed={false} highlight={null} assessmentReport /></div>
 <Dialogue phase="result" playerName="fei" assessmentReport enabled={reported} play={()=>{}} onSettled={()=>{}} />
 </main>;
}
createRoot(document.getElementById('root')!).render(<Review/>);
