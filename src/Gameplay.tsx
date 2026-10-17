import { useEffect, useState } from 'react';
import LevelOne, { type LevelOneProps, type LevelOneResult } from './levels/level1/LevelOne';
import LevelTwo, { type LevelTwoProps } from './levels/level2/LevelTwo';

export type GameplayProps = {
  // The opening owns name entry. Pass its confirmed playerName here once it ends.
  playerName: string;
  initialLevel?: 1 | 2;
  renderLevelOneCinematic?: LevelOneProps['renderCinematic'];
  renderLevelTwoCinematic?: LevelTwoProps['renderCinematic'];
  onLevelOneComplete?: LevelOneProps['onComplete'];
  onLevelTwoComplete?: LevelTwoProps['onComplete'];
};

export default function Gameplay({ playerName, initialLevel = 1, renderLevelOneCinematic, renderLevelTwoCinematic, onLevelOneComplete, onLevelTwoComplete }: GameplayProps) {
  const [level, setLevel] = useState(initialLevel);
  const [previousResult, setPreviousResult] = useState<LevelOneResult>();
  useEffect(() => {
    const fresh = (event: PageTransitionEvent) => {
      if (event.persisted) { setLevel(initialLevel); setPreviousResult(undefined); }
    };
    window.addEventListener('pageshow', fresh);
    return () => window.removeEventListener('pageshow', fresh);
  }, [initialLevel]);
  return level === 1
    ? <LevelOne playerName={playerName} renderCinematic={renderLevelOneCinematic} onComplete={result => { setPreviousResult(result); onLevelOneComplete?.(result); }} onContinue={() => { setLevel(2); window.scrollTo(0, 0); }} />
    : <LevelTwo playerName={playerName} previousMetricId={previousResult?.metricId} renderCinematic={renderLevelTwoCinematic} onComplete={onLevelTwoComplete} />;
}
