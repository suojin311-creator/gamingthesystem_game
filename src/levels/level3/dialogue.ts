import type { ConversationLine } from '../../shared/components/Conversation';
import { metricDefinition } from '../../shared/data/metrics';
import type { WeightRun } from './data';
import { isNearEven, type WeightGoal } from './weights';

export function workbenchDialogue(phase: string, playerName: string, goal: WeightGoal, current: WeightRun | undefined, hasComparison: boolean): ConversationLine[] {
  const player = (text: string): ConversationLine => ({ speaker: 'Maya', name: playerName, text });
  const alex = (text: string): ConversationLine => ({ speaker: 'Alex', name: 'Alex', text });
  if (phase === 'weights') {
    if (goal === 'contrast') return [player('I’ll make one priority worth more.'), alex('I’ll check the new split. 🔀')];
    if (goal === 'rebalance') return [player('I’ll spread the weight more evenly.'), alex('New priorities again? 🙃')];
    return [player('I’ll test whether these weights change how Alex spends his effort.'), alex('I’m checking the percentages! 🔎')];
  }
  if (phase === 'publish') return [player('I’ll see how Alex responds.'), alex('Those are the new points? Got it.')];
  if (phase === 'result' && current) {
    if (current.round === 1) {
      if (isNearEven(current.weights)) return [player('Alex’s effort looks balanced. What if I made one priority worth much more?'), alex('I’d chase the bigger points! 🤑')];
      const highest = current.weights.indexOf(Math.max(...current.weights));
      return [player(`${metricDefinition(current.metricIds[highest]).shortName} gets ${current.weights[highest]}%. Is that why it gets so much attention?`), alex('Of course! More points, more effort. 🥇')];
    }
    if (!hasComparison) return [player('It’s still uneven. I’ll test a nearly equal split.'), alex('About a third each? Okay! 🧮')];
    return [player('The effort changed when I changed the weights.'), alex('I follow the percentages. Easy! 🧩')];
  }
  if (phase === 'compare') return [player('Balancing helps. But the points still tell Alex what matters.'), alex('Yep. I plan my work around the scores. 🗺️')];
  return [];
}
