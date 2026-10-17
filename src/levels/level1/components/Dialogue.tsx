import type { Phase } from '../state';
import type { Cue } from '../../../shared/hooks/useFeedback';
import Conversation, { type ConversationLine } from '../../../shared/components/Conversation';

export default function Dialogue({ phase, playerName, studentReplies, enabled, paused = false, play, onSettled }: {
  phase: Phase; playerName: string; studentReplies?: readonly string[]; enabled: boolean;
  play: (cue: Cue) => void; onSettled: () => void; paused?: boolean;
}) {
  const single: Record<Phase, string> = {
    choose: 'Where should I start?', predict: 'What do I expect students to do?',
    result: 'Looking good. I’ll check the classroom.', cinematic: '',
    review: 'The score went up. What did you learn?',
  };
  const lines: ConversationLine[] = [{ speaker: 'Maya', name: playerName, text: single[phase], delivery: phase === 'review' ? 'speech' : 'thought' }];
  if (phase === 'review') lines.push(...(studentReplies || ['I finished the tasks.']).map(text => ({ speaker: 'Alex' as const, name: 'Alex', text })));
  return <Conversation lines={lines} enabled={enabled} paused={paused} play={play} onSettled={onSettled} />;
}
