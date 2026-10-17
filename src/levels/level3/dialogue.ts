import type { ConversationLine } from '../../shared/components/Conversation';
import type { WeightRun } from './data';
import { effortGroups } from './data';
import { isNearEven, type WeightGoal } from './weights';

export function workbenchDialogue(phase: string, playerName: string, goal: WeightGoal, current: WeightRun | undefined, hasComparison: boolean): ConversationLine[] {
  const thought = (text: string): ConversationLine => ({ speaker: 'Maya', name: playerName, text, delivery: 'thought' });
  const alex = (text: string): ConversationLine => ({ speaker: 'Alex', name: 'Alex', text });
  if (phase === 'weights') {
    if (goal === 'different') return [thought('Would a different split change what Alex focuses on?'), alex('New percentages again? 🙃'), alex('Hang on… which task pays off now?')];
    return [thought('I’ll test whether these weights change how Alex spends his effort.'), alex('Let me check the percentages. 🔎'), alex('I know where to spend my energy!')];
  }
  if (phase === 'publish') return [thought('I’ll see how Alex responds.'), alex('Got the new scoring sheet!'), alex('Time to plan my next move. 🔀')];
  if (phase === 'result' && current) {
    if (current.round === 1) {
      if (isNearEven(current.weights)) return [thought('Would a different split change Alex’s choices?'), alex('Each task is worth about the same.'), alex('A bit of everything, then! 🤑')];
      const groups = effortGroups(current);
      const low = groups.find(group => group.effort === 'low');
      return [thought('Would another split change what Alex works on?'), alex(`I’m putting my energy into ${groups[0].names}. 🥇`), alex(low ? `${low.names}? Just the basics.` : 'I want every point I can get!')];
    }
    if (!hasComparison) return [thought(isNearEven(current.weights) ? 'Both tests look similar. What if one task counted much more?' : 'I’ve tried two different splits. What would an equal split show?'), alex('I’ve tried both sets of rules. 🧮'), alex('I check what earns points before I start.')];
    return [thought('The weights changed. So did Alex’s priorities.'), alex('Different points, different plan. 🧩'), alex('I still want the best score!')];
  }
  if (phase === 'compare') return [thought('Different splits, but the scoring rules still guide his choices.'), alex('I plan my work around the scores. 🗺️'), alex('That’s how I know what counts!')];
  return [];
}
