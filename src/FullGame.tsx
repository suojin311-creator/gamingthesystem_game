import { useEffect, useState } from 'react';
import Opening from './cinematics/opening/Opening';
import Gameplay from './Gameplay';
import { useFeedback } from './shared/hooks/useFeedback';
import ChapterTransition from './shared/components/ChapterTransition';
import officeBackground from './cinematics/opening/assets/backgrounds/BG_Office_FirstPerson_v01.png';

/** The opening owns identity; Gameplay stays mounted across all three levels. */
export default function FullGame() {
  const [playerName, setPlayerName] = useState<string | null>(null);
  const [chapterReady, setChapterReady] = useState(false);
  const { reset, play, unlock } = useFeedback();
  useEffect(() => {
    const fresh = (event: PageTransitionEvent) => {
      if (!event.persisted) return;
      reset();
      setPlayerName(null);
      setChapterReady(false);
    };
    window.addEventListener('pageshow', fresh);
    return () => window.removeEventListener('pageshow', fresh);
  }, [reset]);
  return playerName === null
    ? <Opening onComplete={setPlayerName} />
    : !chapterReady ? <main className="first-chapter-shell" onPointerDown={unlock} onKeyDown={unlock}><ChapterTransition level={1} backdrop={officeBackground} playerName={playerName} play={play} onStart={() => { setChapterReady(true); window.scrollTo(0, 0); }} /></main>
    : <Gameplay playerName={playerName} />;
}
