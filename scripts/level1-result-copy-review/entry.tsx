import React from 'react';
import {createRoot} from 'react-dom/client';
import Settlement from '../../src/levels/level1/Settlement';
import '../../src/shared/styles/base.css';
createRoot(document.getElementById('root')!).render(<main className="game-page level-one" style={{width:'calc(100% - 80px)',maxWidth:1280,margin:'40px auto'}}><Settlement result={{metricId:'prep',prediction:'',reportedScore:{before:40,after:90,target:80}}} onContinue={()=>{}} /></main>);
