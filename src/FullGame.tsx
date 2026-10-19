import { useEffect, useState } from 'react';
import Opening from './cinematics/opening/Opening';
import Gameplay from './Gameplay';
import { useFeedback } from './shared/hooks/useFeedback';

/** The opening owns identity; Gameplay stays mounted across all three levels. */
export default function FullGame() {
  const [playerName, setPlayerName] = useState<string | null>(null);
  const { reset } = useFeedback();
  useEffect(() => {
    const fresh = (event: PageTransitionEvent) => {
      if (!event.persisted) return;
      reset();
      setPlayerName(null);
    };
    window.addEventListener('pageshow', fresh);
    return () => window.removeEventListener('pageshow', fresh);
  }, [reset]);
  return playerName === null
    ? <Opening onComplete={setPlayerName} />
    : <Gameplay playerName={playerName} />;
}
