import { metricDefinition, type MetricId } from '../../shared/data/metrics';
import { joinNames, type WeightRun } from './data';
import { CONTRAST_WEIGHTS, EVEN_WEIGHTS, effortAt, isNearEven, validWeights, type Weights } from './weights';

type Purpose = 'explore' | 'adjust' | 'balance' | 'contrast' | 'redirect';
export type Experiment = { purpose: Purpose; label: string; question: string; focus: MetricId[]; suggestion?: Weights; reference?: WeightRun };
const names = (ids: MetricId[]) => joinNames(ids.map(id => metricDefinition(id).shortName));

/** Three player-led tests: explore, respond to evidence, then test the explanation. */
export function nextExperiment(runs: WeightRun[]): Experiment {
  if (!runs.length) return { purpose: 'explore', label: 'Explore', question: 'Can changing the weights change what Alex is aiming for?', focus: [] };
  const previous = runs.at(-1)!;
  const low = previous.metricIds.filter((_, i) => effortAt(previous.weights, i) === 'low');
  if (runs.length === 1) return {
    purpose: 'adjust', label: 'Adjust',
    question: isNearEven(previous.weights)
      ? 'Alex stopped at the checklist. What if one task counted much more?'
      : `${names(low)} got little attention. How would you change the shares?`,
    focus: low, suggestion: isNearEven(previous.weights) ? [...CONTRAST_WEIGHTS] : [...EVEN_WEIGHTS],
  };
  if (runs.every(run => !isNearEven(run.weights))) return {
    purpose: 'balance', label: 'Verify', question: 'Give all three a similar share. Does Alex go beyond the checklist?',
    focus: low, suggestion: [...EVEN_WEIGHTS],
  };
  if (runs.every(run => isNearEven(run.weights))) return {
    purpose: 'contrast', label: 'Verify', question: 'Make one task count much more. What pulls Alex towards it?',
    focus: [previous.metricIds[0]], suggestion: [...CONTRAST_WEIGHTS],
  };
  const reference = [...runs].reverse().find(run => !isNearEven(run.weights))!;
  const [a, b, c] = reference.weights;
  const suggestion: Weights = [c, a, b];
  const focus = reference.metricIds.filter((_, i) => effortAt(reference.weights, i) === 'low' && effortAt(suggestion, i) !== 'low');
  return {
    purpose: 'redirect', label: 'Verify', question: `Shift the reward towards ${names(focus)}. Does Alex follow it?`,
    focus, suggestion, reference,
  };
}

export function meetsExperiment(weights: Weights, runs: WeightRun[], experiment = nextExperiment(runs)) {
  if (!validWeights(weights) || runs.some(run => run.weights.every((value, i) => value === weights[i]))) return false;
  if (experiment.purpose === 'balance') return isNearEven(weights);
  if (experiment.purpose === 'contrast') return !isNearEven(weights);
  if (experiment.purpose === 'redirect') {
    const reference = experiment.reference!;
    return !isNearEven(weights) && experiment.focus.some(id => effortAt(weights, reference.metricIds.indexOf(id)) !== 'low');
  }
  return true;
}

export function experimentHint(experiment: Experiment) {
  if (experiment.purpose === 'balance') return 'Bring the highest and lowest weights within 10 percentage points.';
  if (experiment.purpose === 'contrast') return 'Separate the highest and lowest weights by more than 10 percentage points.';
  if (experiment.purpose === 'redirect') return `Give ${names(experiment.focus)} a larger share so the reward changes direction.`;
  return 'Change the split from your earlier tests.';
}
