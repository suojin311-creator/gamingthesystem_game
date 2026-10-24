import React from 'react';
import{createRoot}from'react-dom/client';
import ChapterTransition from '../../src/shared/components/ChapterTransition';
import office from '../../src/cinematics/opening/assets/backgrounds/BG_Office_FirstPerson_v01.png';
import '../../src/shared/styles/base.css';
createRoot(document.getElementById('root')!).render(<main className="first-chapter-shell"><ChapterTransition level={1} backdrop={office} playerName="fei" play={()=>{}} onStart={()=>{}}/></main>);
