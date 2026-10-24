import React,{useEffect,useState} from 'react';
import {createRoot} from 'react-dom/client';
import {createPortal} from 'react-dom';
import {ResultChart,PerspectivePanel} from '../../src/levels/level1/LevelOne';
import {getMetric} from '../../src/levels/level1/metrics';
import Icon from '../../src/shared/components/Icon';
import '../../src/shared/styles/base.css';
import './review.css';
const metric=getMetric('part')!;
function Review(){
 const motion=new URLSearchParams(location.search).has('motion');
 const [score,setScore]=useState(motion?metric.before:metric.after);
 const [ready,setReady]=useState(!motion),[target,setTarget]=useState(!motion);
 const [reported,setReported]=useState(!motion),[managementNote,setManagementNote]=useState(!motion);
 const [question,setQuestion]=useState(!motion),[enabled,setEnabled]=useState(!motion);
 const [managementHost,setManagementHost]=useState<HTMLElement|null>(null);
 useEffect(()=>setManagementHost(document.querySelector('[data-management-panel]')),[]);
 useEffect(()=>{
  if(!motion)return;
  const started=performance.now();window.assessmentTimings={};
  const mark=(key:string)=>{window.assessmentTimings[key]=performance.now()-started;};
  let raf=0;const timers:ReturnType<typeof setTimeout>[]=[];
  const after=(delay:number,fn:()=>void)=>timers.push(setTimeout(fn,delay));
  after(650,()=>{
   const begin=performance.now();mark('numberStart');
   const tick=(now:number)=>{const progress=Math.min(1,(now-begin)/2000);
    setScore(Math.round(metric.before+(metric.after-metric.before)*(1-(1-progress)**3)));
    if(progress<1)raf=requestAnimationFrame(tick);else{
     setReady(true);mark('numberComplete');
     after(450,()=>{setTarget(true);mark('targetReveal');
      after(1500,()=>{setReported(true);mark('managementUpdate');
       after(1100,()=>{setManagementNote(true);mark('managementCaption');
        after(1000,()=>{setQuestion(true);mark('questionReveal');
         after(500,()=>{setEnabled(true);mark('buttonEnabled');});
        });
       });
      });
     });
    }
   };raf=requestAnimationFrame(tick);
  });
  return()=>{timers.forEach(clearTimeout);cancelAnimationFrame(raf);};
 },[motion]);
 return <main className="level-one assessment-review" data-motion={motion} data-ready={ready} data-target={target} data-reported={reported} data-management-note={managementNote} data-question={question} data-enabled={enabled}>
 <div className="assessment-context"><span className="chapter-number">01</span><h1>One metric.</h1></div>
 <div className="assessment-layout"><section className="assessment-main">
 <section className="assessment-card">
 <ResultChart metric={metric} ready={ready} score={score} assessmentReport />
 <div className="assessment-bridge"><p data-visible={question}><strong>But…</strong> what changed in the classroom?</p></div>
 </section>
 <div className="action-row"><button type="button" className="button primary-button" disabled={!enabled}><Icon name="play"/>Look behind the number</button></div>
 </section><PerspectivePanel metric={metric} evaluated={reported} observed={false} highlight={null} assessmentReport /></div>
 {managementHost&&createPortal(<p className="assessment-management-copy" data-visible={managementNote}>Management is satisfied.</p>,managementHost)}
 </main>;
}
createRoot(document.getElementById('root')!).render(<Review/>);
