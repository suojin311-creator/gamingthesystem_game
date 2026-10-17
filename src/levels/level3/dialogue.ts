import type { ConversationLine } from '../../shared/components/Conversation';
import type { WeightRun } from './data';
import { effortGroups } from './data';
import { isNearEven, type WeightGoal } from './weights';

export function workbenchDialogue(phase: string, playerName: string, goal: WeightGoal, current: WeightRun | undefined, hasComparison: boolean): ConversationLine[] {
  const teacher = (text: string): ConversationLine => ({ speaker: 'Maya', name: playerName, text });
  const alex = (text: string): ConversationLine => ({ speaker: 'Alex', name: 'Alex', text });
  if (phase === 'weights') {
    if (goal === 'different') return [teacher('Alex, I’m trying a different split. Will that change your plan?'), alex('New percentages again? 🙃'), alex('Let me see what earns the most points now.')];
    return [teacher('Alex, how will you decide which tasks to focus on?'), alex('Let me check the percentages. 🔎'), alex('The bigger rewards get more of my time!')];
  }
  if (phase === 'publish') return [teacher('Here are the new weights, Alex. What’s your plan?'), alex('Got the new scoring sheet!'), alex('I’ll start with whatever earns the most points. 🔀')];
  if (phase === 'result' && current) {
    if (current.round === 1) {
      if (isNearEven(current.weights)) return [teacher('Alex, how did you divide your effort this time?'), alex('The tasks were worth about the same.'), alex('So I gave each one some time! 🤑')];
      const groups = effortGroups(current);
      const low = groups.find(group => group.effort === 'low');
      return [teacher('Alex, why did you focus on some tasks more than others?'), alex(`${groups[0].names} ${groups[0].metricIds.length === 1 ? 'is' : 'are'} worth more points. 🥇`), alex(low ? `${low.names}? I only did the basics.` : 'I want every point I can get!')];
    }
    if (!hasComparison) {
      const alreadyEven = isNearEven(current.weights);
      return [teacher(alreadyEven ? 'Alex, what if one task counted much more?' : 'Alex, what if all three counted equally?'), alex(`${alreadyEven ? 'I’d check that one first.' : 'Then each task would matter for my score.'} 🧮`), alex(alreadyEven ? 'That’s where more of my effort would go.' : 'I’d have a reason to spend time on all three.')];
    }
    return [teacher('Alex, what made you change your plan?'), alex('Different points, different plan. 🧩'), alex('I still want the best score!')];
  }
  if (phase === 'compare') return [teacher('Alex, are you choosing what helps you learn, or what earns points?'), alex('I plan my work around the scores. 🗺️'), alex('That’s how I know what counts!')];
  return [];
}
