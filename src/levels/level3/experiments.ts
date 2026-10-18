import { metricDefinition } from '../../shared/data/metrics';
import { effortChanged, joinNames, type WeightRun } from './data';
import { effortAt, hasLowEffort, validWeights, type Weights } from './weights';

export const MIN_TRIALS = 2;
export const MAX_TRIALS = 3;
export type Experiment = { purpose: 'explore' | 'respond' | 'verify'; label: string; question: string; hint: string };
export const canCompare = (runs: WeightRun[]) => runs.length >= MIN_TRIALS && runs.length <= MAX_TRIALS;
export const canTryAgain = (runs: WeightRun[]) => runs.length < MAX_TRIALS;

/** A question follows the observed result; no goal choice or prescribed numbers. */
export function nextExperiment(runs: WeightRun[]): Experiment {
  if (!runs.length) return {
    purpose: 'explore', label: 'Your first test',
    question: 'Can a different split improve what happens in class?',
    hint: 'Choose a split you think will help. Publish it, then observe Alex’s choices.',
  };
  const previous = runs.at(-1)!;
  const neglected = joinNames(previous.metricIds.filter((_, index) => effortAt(previous.weights, index) === 'low').map(id => metricDefinition(id).shortName));
  if (runs.length === 1) return neglected ? {
    purpose: 'respond', label: 'Follow the evidence',
    question: `What would you change for ${neglected}?`,
    hint: `${neglected} received minimum effort. You could give those tasks a larger share and watch the trade-off.`,
  } : {
    purpose: 'respond', label: 'Follow the evidence',
    question: 'All three got attention. What would a different emphasis change?',
    hint: 'You already gave each task attention. Try changing which task counts most, and watch whether Alex’s choices change.',
  };
  const unchanged = runs.slice(1).every((run, index) => !effortChanged(runs[index], run));
  if (unchanged) return {
    purpose: 'verify', label: 'An optional check',
    question: 'The routine stayed the same. What would make a useful contrast?',
    hint: 'Similar splits can produce a similar routine. Try moving the emphasis to another task to check what guides Alex’s choices.',
  };
  return hasLowEffort(previous.weights) ? {
    purpose: 'verify', label: 'An optional check',
    question: `What would you change for ${neglected} now?`,
    hint: 'Use the comparison to choose what you want to check. You decide which shares to change.',
  } : {
    purpose: 'verify', label: 'An optional check',
    question: 'Attention is broader. Would another split change when Alex stops?',
    hint: 'All three now receive attention. If you try another idea, watch both where Alex works and what makes him stop.',
  };
}

export function meetsExperiment(weights: Weights, runs: WeightRun[]) {
  return canTryAgain(runs) && validWeights(weights) && !runs.some(run => run.weights.every((value, index) => value === weights[index]));
}
export function experimentHint() { return 'That split is already in your results. Reset weights to try a different one.'; }
