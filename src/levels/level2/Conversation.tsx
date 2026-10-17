import Conversation, { type ConversationLine } from '../../shared/components/Conversation';
import type { Cue } from '../../shared/hooks/useFeedback';

const words = (text: string) => text.trim().split(/\s+/).filter(Boolean).length;
const dialogueReadingTime = (text: string) => Math.min(2200, Math.max(1100, 400 + words(text) * 110));
export const findingReadingTime = (text: string) => Math.min(2800, Math.max(1600, 500 + words(text) * 70));

/** Level 2 stays brisk; Level 1 retains the shared component's original pace. */
export default function LevelTwoConversation(props: {
  lines: ConversationLine[]; enabled?: boolean; paused?: boolean;
  play: (cue: Cue) => void; onSettled: () => void; onLastMessage?: () => void;
}) {
  return <Conversation {...props} typingDelay={300} readDelay={dialogueReadingTime} />;
}
