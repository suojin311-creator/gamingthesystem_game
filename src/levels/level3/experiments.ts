import { metricDefinition, type MetricId } from '../../shared/data/metrics';
import { joinNames, type WeightRun } from './data';
import { CONTRAST_WEIGHTS, EVEN_WEIGHTS, effortAt, isNearEven, validWeights, type Weights } from './weights';

type Purpose = 'explore' | 'adjust' | 'balance' | 'contrast' | 'redirect';
export type Experiment = { purpose: Purpose; label: string; question: string; focus: MetricId[]; suggestion?: Weights; reference?: WeightRun };
const names = (ids: MetricId[]) => joinNames(ids.map(id => metricDefinition(id).shortName));

/** Three player-led tests: explore, respond to evidence, then test the explanation. */
export function nextExperiment(runs: WeightRun[]): Experiment {
  if (!runs.length) return { purpose: 'explore', label: 'Explore', question: 'Can new weights change Alex’s goal?', focus: [] };
  const previous = runs.at(-1)!;
  const low = previous.metricIds.filter((_, i) => effortAt(previous.weights, i) === 'low');
  if (runs.length === 1) return {
    purpose: 'adjust', label: 'Adjust',
    question: isNearEven(previous.weights)
      ? 'What if one task counted much more?'
      : `What if ${names(low)} counted more?`,
    focus: low, suggestion: isNearEven(previous.weights) ? [...CONTRAST_WEIGHTS] : [...EVEN_WEIGHTS],
  };
  if (runs.every(run => !isNearEven(run.weights))) return {
    purpose: 'balance', label: 'Verify', question: 'What if all three counted about the same?',
    focus: low, suggestion: [...EVEN_WEIGHTS],
  };
  if (runs.every(run => isNearEven(run.weights))) return {
    purpose: 'contrast', label: 'Verify', question: 'Will Alex follow the biggest reward?',
    focus: [previous.metricIds[0]], suggestion: [...CONTRAST_WEIGHTS],
  };
  const reference = [...runs].reverse().find(run => !isNearEven(run.weights))!;
  const [a, b, c] = reference.weights;
  const suggestion: Weights = [c, a, b];
  const focus = reference.metricIds.filter((_, i) => effortAt(reference.weights, i) === 'low' && effortAt(suggestion, i) !== 'low');
  return {
    purpose: 'redirect', label: 'Verify', question: `Will Alex follow a bigger reward for ${names(focus)}?`,
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
