import { metricDefinition, type MetricId } from '../../shared/data/metrics';
import { joinNames, type TrialIntent, type WeightRun } from './data';
import { effortAt, isNearEven, validWeights, type Weights } from './weights';

export const TRIAL_INTENTS: { id: TrialIntent; label: string; shortLabel: string }[] = [
  { id: 'attention', label: 'Give all three attention', shortLabel: 'Share attention' },
  { id: 'priority', label: 'Shift Alex’s priority', shortLabel: 'Shift priority' },
  { id: 'exploration', label: 'Keep Alex exploring', shortLabel: 'Encourage exploration' },
];
export const intentLabel = (intent?: TrialIntent) => TRIAL_INTENTS.find(item => item.id === intent)?.shortLabel;
export type Experiment = { purpose: 'explore' | 'adjust' | 'verify'; label: string; question: string; focus: MetricId[]; hint: string; suggestion?: Weights };
const names = (ids: MetricId[]) => joinNames(ids.map(id => metricDefinition(id).shortName));
const wasTested = (weights: Weights, runs: WeightRun[]) => runs.some(run => run.weights.every((value, i) => value === weights[i]));

/** Suggestions are opt-in examples, never an answer or a condition for progression. */
export function nextExperiment(runs: WeightRun[], intent?: TrialIntent): Experiment {
  const previous = runs.at(-1);
  const purpose = !runs.length ? 'explore' : runs.length === 1 ? 'adjust' : 'verify';
  const plan: Experiment = { purpose, label: purpose === 'explore' ? 'Explore' : purpose === 'adjust' ? 'Adjust' : 'Verify',
    question: !runs.length ? 'What do you want to change?' : runs.length === 1 ? 'What will you try next?' : 'What will you check again?',
    focus: [], hint: 'Choose what you want this test to investigate.' };
  if (!intent) return plan;
  if (intent === 'priority') {
    const target = previous ? previous.weights.indexOf(Math.min(...previous.weights)) : 0;
    const candidates = [70, 75, 80].map(value => {
      const weights: [number, number, number] = [10, 10, 10];
      weights[target] = value;
      weights[(target + 1) % 3] = 90 - value;
      return weights;
    });
    return { ...plan, hint: 'Move the biggest reward to another task. Watch where Alex puts his effort.', suggestion: candidates.find(weights => !wasTested(weights, runs)) };
  }
  const candidates: Weights[] = [[34,33,33], [36,32,32], [30,40,30], [31,35,34]];
  return { ...plan,
    hint: intent === 'attention' ? 'Try giving the overlooked tasks a larger share. Watch all three.' : 'Try a different split. Watch what Alex does after meeting the requirements.',
    suggestion: candidates.find(weights => !wasTested(weights, runs)),
  };
}

/** Any new positive allocation can test an idea, including unchanged effort bands. */
export function meetsExperiment(weights: Weights, runs: WeightRun[], _experiment?: Experiment) {
  return validWeights(weights) && !wasTested(weights, runs);
}
export function experimentHint() { return 'This split was already tested. Reset weights to try another.'; }

/** These are observations about effort, not a score for learning or the player's choice. */
export function trialFinding(run: WeightRun, previous?: WeightRun) {
  if (run.intent === 'attention') {
    const low = run.metricIds.filter((_, i) => effortAt(run.weights, i) === 'low');
    return low.length ? `${names(low)} still got minimum effort.` : 'All three received attention. What made Alex stop?';
  }
  if (run.intent === 'priority') {
    if (!previous) return 'A starting point. Compare his priority after your next change.';
    const rank = { low: 0, medium: 1, high: 2 };
    const leaders = (record: WeightRun) => {
      const levels = record.metricIds.map((_, i) => rank[effortAt(record.weights, i)]);
      return record.metricIds.filter((_, i) => levels[i] === Math.max(...levels));
    };
    const current = leaders(run), before = leaders(previous);
    if (current.length === 3) return 'Alex gave all three the same level of effort.';
    const moved = current.some(id => !before.includes(id)) || before.some(id => !current.includes(id));
    return `${names(current)} ${moved ? 'now' : 'still'} ${current.length > 1 ? 'draw' : 'draws'} his strongest effort.`;
  }
  if (run.intent === 'exploration') return isNearEven(run.weights)
    ? 'All boxes ticked. Alex packed up.'
    : 'Effort follows the rewards. A new reason to learn is still unproven.';
  return '';
}
