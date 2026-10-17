import type { Phase } from '../state';
import type { Cue } from '../../../shared/hooks/useFeedback';
import Conversation, { type ConversationLine } from '../../../shared/components/Conversation';

export default function Dialogue({ phase, playerName, studentQuote, enabled, paused = false, play, onSettled }: {
  phase: Phase; playerName: string; studentQuote?: string; enabled: boolean;
  play: (cue: Cue) => void; onSettled: () => void; paused?: boolean;
}) {
  const single: Record<Phase, string> = {
    choose: 'Where should I start?', predict: 'What do I expect students to do?',
    result: 'Looking good. Let’s check the classroom.', cinematic: '',
    review: 'The score is up. What about learning?',
  };
  const lines: ConversationLine[] = [{ speaker: 'Maya', name: playerName, text: single[phase] }];
  if (phase === 'review') lines.push({ speaker: 'Alex', name: 'Alex', text: studentQuote || 'I met the criteria.' });
  return <Conversation lines={lines} enabled={enabled} paused={paused} play={play} onSettled={onSettled} />;
}
