import React,{useState} from 'react';
import{createRoot}from'react-dom/client';
import ChapterTransition from '../../src/shared/components/ChapterTransition';
import Gameplay from '../../src/Gameplay';
import{useFeedback}from'../../src/shared/hooks/useFeedback';
import office from '../../src/cinematics/opening/assets/backgrounds/BG_Office_FirstPerson_v01.png';
import '../../src/shared/styles/base.css';
import './review.css';
function Review(){
 const [entering,setEntering]=useState(false),[finished,setFinished]=useState(false);
 const feedback=useFeedback();
 return <div className="handoff-review" data-entering={entering} data-finished={finished}>
 {entering&&<div className="handoff-incoming"><Gameplay playerName="fei"/></div>}
 {!finished&&<div className="handoff-outgoing" aria-hidden={entering} inert={entering} onAnimationEnd={e=>{if(e.target===e.currentTarget&&e.animationName==='handoff-out'){setFinished(true);window.handoffFinished=performance.now();}}}>
 <main className="first-chapter-shell"><ChapterTransition level={1} backdrop={office} playerName="fei" play={feedback.play} onStart={()=>{window.handoffStarted=performance.now();setEntering(true);if(matchMedia('(prefers-reduced-motion: reduce)').matches)setFinished(true);}}/></main>
 </div>}
 </div>;
}
createRoot(document.getElementById('root')!).render(<Review/>);
