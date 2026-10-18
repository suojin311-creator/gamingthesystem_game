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

/** Only observation results need a workbench exchange; operations stay visual. */
export function workbenchDialogue(phase: string, playerName: string, _goal: WeightGoal, runs: WeightRun[]): ConversationLine[] {
  if (phase !== 'result') return [];
  const teacher = (text: string): ConversationLine => ({ speaker: 'Maya', name: playerName, text });
  const alex = (text: string): ConversationLine => ({ speaker: 'Alex', name: 'Alex', text });
  const current = runs.at(-1);
  const previous = runs.at(-2);
  if (!current) return [];
  const pattern = weightPattern(current);
  const { lead, low } = priorities(current);
  if (!previous) {
    if (pattern === 'one-higher') return [teacher('Why leave the other two behind, Alex?'), alex(`${lead} was worth the most. 🥇`), alex(`I rushed ${low}.`)];
    if (pattern === 'two-higher') return [teacher(`What happened to ${low}?`), alex(`${lead} kept me busy. 🛎️`), alex(`I gave ${low} the quick version.`)];
    return [teacher('What would you like to explore next?'), alex('Does that earn extra points?'), alex('If not, I’m done. 😏')];
  }
  if (current.round === 3) {
    if (pattern === 'near-even') return [teacher('Everyone got a share. Did your reason for working change?'), alex('I covered all three requirements.'), alex('The checklist still tells me when to stop.')];
    if (runs.slice(0, 2).every(run => isNearEven(run.weights))) return [teacher(`Why did ${lead} pull you back?`), alex('That’s where the marks went.'), alex('I’m still checking what pays off.')];
    return [teacher('What made you change which task came first?'), alex(`${lead} pays more now.`), alex('Same plan: collect the marks, then stop.')];
  }
  if (current.kind !== 'player') {
    if (pattern === 'near-even') return [teacher('All three got time. What about going further?'), alex('I’d need a reason to keep going. 🧮'), alex('Is there another mark for that?')];
    return [teacher(`What pulled you toward ${lead}?`), alex('That bigger reward! 🥨'), alex('The smaller tasks could wait.')];
  }
  if (pattern === 'near-even') {
    const stillEven = isNearEven(previous.weights);
    return [teacher(stillEven ? 'Did the new split change your goal?' : 'You shared your time. What made you stop?'), alex(stillEven ? 'Not really. I still ticked all three boxes.' : 'Every requirement had its tick.'), alex(`${stillEven ? 'Then I packed up.' : 'That’s my cue to close the book.'} 🪁`)];
  }
  const intensity = { low: 0, medium: 1, high: 2 };
  const changed = (direction: number) => current.metricIds.filter((id, index) => {
    const oldIndex = previous.metricIds.indexOf(id);
    return oldIndex >= 0 && Math.sign(intensity[effortAt(current.weights, index)] - intensity[effortAt(previous.weights, oldIndex)]) === direction;
  });
  const up = names(changed(1)), down = names(changed(-1));
  const question = up && down ? `Why switch effort from ${down} to ${up}?` : up ? `Why spend more time on ${up}?` : down ? `Why ease off on ${down}?` : 'New weights, same routine?';
  return [teacher(question), alex(`I’m following the rewards in ${lead}. 🧩`), alex(up || down ? `${low} got the quick version.` : 'I could keep my old shortcuts.')];
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

const nearEvenTasks: Record<MetricId, { action: string; lines: readonly [string, string] }> = {
  prep: { action: 'Alex checks the preparation requirements, completes the reading task and closes the material as soon as every box is ticked.', lines: ['Preparation boxes ticked. Next task!', 'Reading requirement met. Closing that one.'] },
  part: { action: 'Alex makes the required contributions, marks participation complete and stops looking for another idea to share.', lines: ['Contribution made. That covers my mark.', 'I’ve spoken enough for the participation points.'] },
  focus: { action: 'Alex stays on task for the required activity, checks the focus criterion and packs away the task when it is met.', lines: ['Stayed on task. That should count.', 'Focus requirement covered. I can wrap this up.'] },
  discuss: { action: 'Alex follows the discussion criteria, ticks off the required behaviours and puts the prompt cards away.', lines: ['Used the prompts. Discussion box ticked.', 'That’s every discussion behaviour on the list.'] },
  reflect: { action: 'Alex fills the required reflection sections, checks the rubric and closes the notebook without exploring another question.', lines: ['Every required section is filled in.', 'Reflection format checked. Ready to submit.'] },
  peer: { action: 'Alex reads a post and writes the required suggestion, then closes the post once the response criteria are satisfied.', lines: ['Suggestion written. Reply requirement met.', 'My response ticks the boxes. On to the next job.'] },
};

export function weightedSceneAction(request: LevelThreeCinematicRequest, index: number) {
  const shot = request.shots[index];
  return isNearEven(request.runs.at(-1)!.weights) ? nearEvenTasks[shot.metricId].action : BEHAVIOURS[shot.metricId][shot.effort].action;
}

/** Replaying a request is deterministic; later observations have fresh lines. */
export function weightedSceneReply(request: LevelThreeCinematicRequest, index: number) {
  const shot = request.shots[index];
  if (isNearEven(request.runs.at(-1)!.weights)) {
    const seen = request.runs.slice(0, -1).filter(run => isNearEven(run.weights)).length;
    return nearEvenTasks[shot.metricId].lines[Math.min(seen, 1)];
  }
  const seen = request.runs.slice(0, -1).filter(run => {
    const priorIndex = run.metricIds.indexOf(shot.metricId);
    return priorIndex >= 0 && effortAt(run.weights, priorIndex) === shot.effort;
  }).length;
  return seen ? repeatedAction[shot.metricId][shot.effort][Math.min(seen - 1, 1)] : BEHAVIOURS[shot.metricId][shot.effort].line;
}

export function comparisonDialogue(playerName: string, runs: WeightRun[]) {
  const current = runs.at(-1)!;
  return [
    { speaker: playerName, text: isNearEven(current.weights) ? 'Your time is shared now. What are you aiming for?' : 'You moved your effort. What are you aiming for?' },
    { speaker: 'Alex', text: 'The best score I can get.' },
    { speaker: 'Alex', text: 'I work out what earns marks, then stop when I’ve got them.' },
  ];
}
