import { StrictMode, useState } from 'react';
import { createRoot } from 'react-dom/client';
import '../../shared/styles/base.css';
import LevelOne from '../../levels/level1/LevelOne';
import Settlement from './Settlement';
import Cinematic from './Cinematic';
import './preview.css';

function Preview() {
  const [run, setRun] = useState(0);
  const name = new URLSearchParams(window.location.search).get('name')?.trim() || 'Maya';
  return <div className="l1-settlement-preview"><LevelOne key={run} playerName={name} showIntro={run === 0}
    renderCinematic={(request, complete) => <Cinematic request={request} onComplete={complete} />}
    renderSettlement={({ result, onReplay }) => <Settlement result={result} onReplay={onReplay} onTryAnother={() => setRun(value => value + 1)} />} />
  </div>;
}
createRoot(document.getElementById('root')!).render(<StrictMode><Preview /></StrictMode>);
