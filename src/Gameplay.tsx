import { useEffect, useState } from 'react';
import LevelOne, { type LevelOneProps, type LevelOneResult } from './levels/level1/LevelOne';
import LevelTwo, { type LevelTwoProps } from './levels/level2/LevelTwo';
import LevelThree, { type LevelThreeProps } from './levels/level3/LevelThree';

export type GameplayProps = {
  // The opening owns name entry. Pass its confirmed playerName here once it ends.
  playerName: string;
  initialLevel?: 1 | 2 | 3;
  renderLevelOneCinematic?: LevelOneProps['renderCinematic'];
  renderLevelTwoCinematic?: LevelTwoProps['renderCinematic'];
  renderLevelThreeCinematic?: LevelThreeProps['renderCinematic'];
  onLevelOneComplete?: LevelOneProps['onComplete'];
  onLevelTwoComplete?: LevelTwoProps['onComplete'];
  onLevelThreeComplete?: LevelThreeProps['onComplete'];
  onDesignLab?: LevelThreeProps['onDesignLab'];
};

export default function Gameplay({ playerName, initialLevel = 1, renderLevelOneCinematic, renderLevelTwoCinematic, renderLevelThreeCinematic, onLevelOneComplete, onLevelTwoComplete, onLevelThreeComplete, onDesignLab }: GameplayProps) {
  const [level, setLevel] = useState(initialLevel);
  const [previousResult, setPreviousResult] = useState<LevelOneResult>();
  useEffect(() => {
    const fresh = (event: PageTransitionEvent) => {
      if (event.persisted) { setLevel(initialLevel); setPreviousResult(undefined); }
    };
    window.addEventListener('pageshow', fresh);
    return () => window.removeEventListener('pageshow', fresh);
  }, [initialLevel]);
  if (level === 1) return <LevelOne playerName={playerName} renderCinematic={renderLevelOneCinematic} onComplete={result => { setPreviousResult(result); onLevelOneComplete?.(result); }} onContinue={() => { setLevel(2); window.scrollTo(0, 0); }} />;
  if (level === 2) return <LevelTwo playerName={playerName} previousMetricId={previousResult?.metricId} renderCinematic={renderLevelTwoCinematic} onComplete={onLevelTwoComplete} onContinue={() => { setLevel(3); window.scrollTo(0, 0); }} />;
  return <LevelThree playerName={playerName} renderCinematic={renderLevelThreeCinematic} onComplete={onLevelThreeComplete} onDesignLab={onDesignLab} />;
}
