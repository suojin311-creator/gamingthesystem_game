import{METRICS}from'../../src/levels/level1/metrics';
import{observationDialogue}from'../../src/levels/level2/dialogue';
import React,{useState} from 'react';
import{createRoot}from'react-dom/client';
import ChapterTransition from '../../src/shared/components/ChapterTransition';
import Gameplay from '../../src/Gameplay';
import LevelTwo from '../../src/levels/level2/LevelTwo';
import LevelThree from '../../src/levels/level3/LevelThree';
import office from '../../src/cinematics/opening/assets/backgrounds/BG_Office_FirstPerson_v01.png';
import '../../src/shared/styles/base.css';
import{useFeedback}from'../../src/shared/hooks/useFeedback';
const params=new URLSearchParams(location.search);
function Review(){
 const [entered,setEntered]=useState(false);const feedback=useFeedback();
 const level=Number(params.get('level')||2);
 if(level===1)return entered?<Gameplay playerName="You"/>:<main className="first-chapter-shell"><ChapterTransition level={1} backdrop={office} playerName="You" play={feedback.play} onStart={()=>setEntered(true)}/></main>;
 if(level===3)return <LevelThree playerName="You" initialMetricIds={params.has('carried')?['prep','part','focus']:undefined}/>;
 return <LevelTwo playerName="You" previousMetricId="prep" previousObservation="Skimming just to finish."/>;
}
createRoot(document.getElementById('root')!).render(<Review/>);

const teacherTexts=METRICS.flatMap(m=>[m.reviewQuestion,...m.scene.filter(l=>l.speaker==='Maya').map(l=>l.text)]);
for(const selection of [['prep','part','focus'],['discuss','reflect','peer'],['prep','reflect','peer']] as const)for(const count of [3,6,100])teacherTexts.push(...observationDialogue(count===100,count,[...selection],'You').filter(l=>l.speaker==='Maya').map(l=>l.text));
(window as any).__teacherReview={teacherTexts,studentNames:METRICS.flatMap(m=>m.scene.filter(l=>l.speaker==='Alex').map(l=>l.speaker))};
