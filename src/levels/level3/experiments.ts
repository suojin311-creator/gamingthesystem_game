import { metricDefinition } from '../../shared/data/metrics';
import { effortChanged, joinNames, type WeightRun } from './data';
import { effortAt, hasLowEffort, validWeights, type Weights } from './weights';

export const MIN_TRIALS = 2;
export const MAX_TRIALS = 3;
export type Experiment = { purpose: 'explore' | 'respond' | 'verify'; question: string; hint: string };
export const canCompare = (runs: WeightRun[]) => runs.length >= MIN_TRIALS && runs.length <= MAX_TRIALS;
export const canTryAgain = (runs: WeightRun[]) => runs.length < MAX_TRIALS;

/** A question follows the observed result; no goal choice or prescribed numbers. */
export function nextExperiment(runs: WeightRun[]): Experiment {
  if (!runs.length) return {
    purpose: 'explore',
    question: 'Can a different split improve what happens in class?',
    hint: 'Set the shares, confirm them, then watch Alex.',
  };
  const previous = runs.at(-1)!;
  const neglected = joinNames(previous.metricIds.filter((_, index) => effortAt(previous.weights, index) === 'low').map(id => metricDefinition(id).shortName));
  if (runs.length === 1) return neglected ? {
    purpose: 'respond',
    question: `What would you change for ${neglected}?`,
    hint: `Give ${neglected} more weight. Watch what Alex leaves out.`,
  } : {
    purpose: 'respond',
    question: 'Can new weights make Alex go further?',
    hint: 'Try new weights. Does Alex do more than the checklist asks?',
  };
  const unchanged = runs.slice(1).every((run, index) => !effortChanged(runs[index], run));
  if (unchanged) return {
    purpose: 'verify',
    question: 'Alex kept the same routine. What else could you try?',
    hint: 'Shift the weight to another task. Watch what changes.',
  };
  return hasLowEffort(previous.weights) ? {
    purpose: 'verify',
    question: `What would you change for ${neglected} now?`,
    hint: 'Change a share, then compare Alex’s choices.',
  } : {
    purpose: 'verify',
    question: 'Alex still stopped for the marks. What else could you try?',
    hint: 'Change the shares. Watch whether Alex keeps going after earning the marks.',
  };
}

export function meetsExperiment(weights: Weights, runs: WeightRun[]) {
  return canTryAgain(runs) && validWeights(weights) && !runs.some(run => run.weights.every((value, index) => value === weights[index]));
}
export function experimentHint() { return 'That split is already in your results. Reset weights to try a different one.'; }
