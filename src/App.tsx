import { useEffect, useState } from 'react';
import LevelOne, { type LevelOneResult } from './levels/level1/LevelOne';
import LevelTwo from './levels/level2/LevelTwo';

// The dedicated preview starts at Level 2. A fresh full game starts at Level 1.
const initialLevel = import.meta.env.MODE === 'level2' ? 2 : 1;
export default function App() {
  const [level, setLevel] = useState(initialLevel);
  const [previousResult, setPreviousResult] = useState<LevelOneResult>();
  useEffect(() => {
    const fresh = (event: PageTransitionEvent) => {
      if (event.persisted) { setLevel(initialLevel); setPreviousResult(undefined); }
    };
    window.addEventListener('pageshow', fresh);
    return () => window.removeEventListener('pageshow', fresh);
  }, []);
  return level === 1
    ? <LevelOne onComplete={setPreviousResult} onContinue={() => { setLevel(2); window.scrollTo(0, 0); }} />
    : <LevelTwo previousMetricId={previousResult?.metricId} />;
}
