import type { ConversationLine } from '../../shared/components/Conversation';
import { metricDefinition, type MetricId } from '../../shared/data/metrics';
import { BEHAVIOURS, joinNames, type LevelThreeCinematicRequest, type WeightRun } from './data';
import { effortAt, isNearEven, type Effort, type WeightGoal } from './weights';

export type WeightPattern = 'one-higher' | 'two-higher' | 'near-even';

export function weightPattern(run: WeightRun): WeightPattern {
  if (isNearEven(run.weights)) return 'near-even';
  return run.weights.filter(weight => weight >= 34).length === 2 ? 'two-higher' : 'one-higher';
}

const names = (ids: MetricId[]) => joinNames(ids.map(id => metricDefinition(id).shortName));
function priorities(run: WeightRun) {
  const higher = run.metricIds.filter((_, index) => run.weights[index] >= 34);
  return { higher, lead: names(higher), low: names(run.metricIds.filter(id => !higher.includes(id))) };
}

// Reactions belong to separate beats. Replaying a scene keeps its original lines.
const publishReaction = { 'one-higher': '🏆', 'two-higher': '⚖️', 'near-even': '🍰' };
const republishReaction = { 'one-higher': '🧲', 'two-higher': '🛠️', 'near-even': '🧁' };

export function workbenchDialogue(phase: string, playerName: string, goal: WeightGoal, runs: WeightRun[]): ConversationLine[] {
  const teacher = (text: string): ConversationLine => ({ speaker: 'Maya', name: playerName, text });
  const alex = (text: string): ConversationLine => ({ speaker: 'Alex', name: 'Alex', text });
  const current = runs.at(-1);
  const previous = runs.at(-2);
  if (phase === 'weights') {
    if (goal === 'different') return [teacher('Alex, I’m trying a different split. Will that change your plan?'), alex('New percentages again? 🙃'), alex('Let me see what earns the most points now.')];
    return [teacher('Alex, how will you decide which tasks to focus on?'), alex('Let me check the percentages. 🔎'), alex('The bigger rewards get more of my time!')];
  }
  if (!current) return [];
  const pattern = weightPattern(current);
  const { lead, low } = priorities(current);
  if (phase === 'publish') {
    if (!previous) {
      const reaction = publishReaction[pattern];
      if (pattern === 'one-higher') return [teacher(`${lead} counts most, Alex. Where will you start?`), alex(`${lead} first! That’s the big prize. ${reaction}`), alex(`I’ll keep ${low} to the basics.`)];
      if (pattern === 'two-higher') return [teacher(`${lead} count more, Alex. How will you split your time?`), alex(`Those two get most of my time! ${reaction}`), alex(`${low} can wait till I’ve covered them.`)];
      return [teacher('These three count about the same, Alex. What’s your plan?'), alex(`A little time for each! ${reaction}`), alex('No tiny task I can skip this time.')];
    }
    const reaction = republishReaction[pattern];
    if (pattern === 'near-even') return [teacher(isNearEven(previous.weights) ? 'The rewards are still close, Alex. Would you change your approach?' : 'The rewards are closer now, Alex. How will you tackle the tasks?'), alex(`I’ll keep all three in play. ${reaction}`), alex(isNearEven(previous.weights) ? 'Small changes, same sort of plan!' : 'Leaving one out would hurt my total.')];
    const samePriority = lead === priorities(previous).lead && !isNearEven(previous.weights);
    if (pattern === 'one-higher') return [teacher(`${lead} now counts most. Does that change where you’ll start?`), alex(`${samePriority ? 'Still' : 'I’m switching to'} ${lead}${samePriority ? ' first' : ''}! ${reaction}`), alex(samePriority ? 'The numbers moved, but that’s still the biggest reward.' : `I’ll save time on ${low} to make room.`)];
    return [teacher(`${lead} are the bigger rewards now. What’s your new plan?`), alex(`${samePriority ? 'Those two still' : 'Those two now'} get the best slots! ${reaction}`), alex(`${low} gets whatever time I have left.`)];
  }
  if (phase === 'result') {
    if (!previous) {
      if (pattern === 'one-higher') return [teacher(`You gave ${lead} most of your attention. What happened to the other two?`), alex(`${lead} got my best shot. 🥇`), alex(`${low}? Just enough to get by.`)];
      if (pattern === 'two-higher') return [teacher(`You kept up with ${lead}. Why so little time on ${low}?`), alex('The two bigger rewards kept me busy. 🛎️'), alex(`${low} wasn’t worth as much, so I rushed it.`)];
      return [teacher('You worked on all three, Alex. What kept you moving between them?'), alex('Leaving one out would cost me points. 🤑'), alex('So I made a little room for every task.')];
    }
    if (current.kind !== 'player') {
      if (pattern === 'near-even') return [teacher('With similar rewards, you kept all three going. What were you aiming for?'), alex('No easy points to leave on the table. 🧮'), alex('I spread out the work so I could collect them all.')];
      return [teacher(`When one reward grew, you put ${lead} first. Why?`), alex('That one was too tempting to ignore! 🥨'), alex('I saved the smaller jobs for whatever time was left.')];
    }
    if (pattern === 'near-even') return [teacher(isNearEven(previous.weights) ? 'The percentages changed a little. Did that change how you worked?' : 'Your time is more spread out now. What changed your approach?'), alex(isNearEven(previous.weights) ? 'Not much! Each task still paid about the same.' : 'I couldn’t leave one task behind this time.'), alex('I kept all three going for the score. 🪁')];
    // Reflect actual effort changes, including changed weights with unchanged effort bands.
    const intensity = { low: 0, medium: 1, high: 2 };
    const changed = (direction: number) => current.metricIds.filter((id, index) => {
      const oldIndex = previous.metricIds.indexOf(id);
      return oldIndex >= 0 && Math.sign(intensity[effortAt(current.weights, index)] - intensity[effortAt(previous.weights, oldIndex)]) === direction;
    });
    const up = names(changed(1)), down = names(changed(-1));
    const question = up && down ? `${up} got more effort, while ${down} got less. Why the switch?` : up ? `You stepped up your work on ${up}. What made that worth it?` : down ? `You eased off on ${down}. What changed?` : 'The weights moved, but your effort looks similar. Why?';
    return [teacher(question), alex(`I’m watching the bigger rewards in ${lead}. 🧩`), alex(up || down ? `${low} got the quick version so I could save time.` : 'A few points changed, but I could keep my old routine.')];
  }
  if (phase === 'compare') {
    if (pattern === 'near-even') return [teacher('Your effort is more balanced now. Are you choosing by learning value or by points?'), alex('I’m still following the rewards. 🗺️'), alex('A fairer split just means three jobs to score on.')];
    return [teacher(`You shifted toward ${lead}. What decided which task came first?`), alex('The reward made that decision easy. 🎲'), alex('Change the points and I’ll change my priorities.')];
  }
  return [];
}

const repeatedAction: Record<MetricId, Record<Effort, readonly [string, string]>> = {
  prep: {
    low: ['Another quick skim. That’ll do.', 'Just the reading essentials this time.'],
    medium: ['Reading done. Time for the next task.', 'Preparation is staying on my schedule.'],
    high: ['Back to my notes—every preparation point matters!', 'One more check of my preparation before class.'],
  },
  part: {
    low: ['I’ll let someone else answer this one.', 'I can get by with a brief contribution.'],
    medium: ['I’ve got a thought to share here.', 'I’m keeping a few contributions ready.'],
    high: ['Another question? My hand is already up!', 'I’m not letting an answer opportunity pass!'],
  },
  focus: {
    low: ['A quick phone check won’t hurt my score much.', 'I’ll get back to the task in a minute.'],
    medium: ['Phone away. Back to the task.', 'Keeping my attention on this job.'],
    high: ['Eyes on the screen. Make that focus visible!', 'Still looking completely on task!'],
  },
  discuss: {
    low: ['I’ll nod and let them carry on.', 'A little agreement should cover my part.'],
    medium: ['Here’s how I see the problem.', 'I’ll ask about that part of the idea.'],
    high: ['Which discussion phrase earns the next point?', 'My prompt cards are getting another workout!'],
  },
  reflect: {
    low: ['Two lines and I can move on.', 'A short reflection is enough for now.'],
    medium: ['I’ll finish this reflection before switching tasks.', 'Making time to write my reflection too.'],
    high: ['Checking my reflection against every requirement.', 'One more polish of that reflection format!'],
  },
  peer: {
    low: ['A short reply will have to do.', 'Just a quick comment on this post.'],
    medium: ['I’ll read their post before suggesting a change.', 'There’s time for a useful reply here.'],
    high: ['Another post, another full set of response points!', 'Checking every reply against my scoring list.'],
  },
};

/** Scene replies remember earlier shots; replaying the same request is deterministic. */
export function weightedSceneReply(request: LevelThreeCinematicRequest, index: number) {
  const shot = request.shots[index];
  const seen = request.runs.slice(0, -1).filter(run => {
    const priorIndex = run.metricIds.indexOf(shot.metricId);
    return priorIndex >= 0 && effortAt(run.weights, priorIndex) === shot.effort;
  }).length;
  return seen ? repeatedAction[shot.metricId][shot.effort][Math.min(seen - 1, 1)] : BEHAVIOURS[shot.metricId][shot.effort].line;
}

export function comparisonDialogue(playerName: string, runs: WeightRun[]) {
  const current = runs.at(-1)!;
  const lead = priorities(current).lead;
  return [
    { speaker: playerName, text: isNearEven(current.weights) ? 'Spreading the rewards changed where your time went. Did it change what you were aiming for?' : `Making ${lead} worth more pulled your attention there. Did your goal change too?` },
    { speaker: 'Alex', text: 'My goal? Get the best score I can.' },
    { speaker: playerName, text: 'So a different split changed your strategy, but the score still set the goal.' },
    { speaker: 'Alex', text: 'Well, you gave me a score to chase!' },
    { speaker: playerName, text: 'Then I need to look beyond the percentages.' },
  ];
}
