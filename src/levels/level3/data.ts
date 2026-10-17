import { metricDefinition, type MetricId } from '../../shared/data/metrics';
import { effortAt, isNearEven, type Effort, type Weights } from './weights';

export type WeightRun = { round: number; kind: 'player' | 'balance-check'; metricIds: MetricId[]; weights: Weights };
export type LevelThreeCinematicRequest = {
  sceneId: 'level3.weights' | 'level3.compare' | 'theory.reveal';
  kind: 'weights' | 'comparison' | 'theory'; playerName: string;
  runs: WeightRun[];
  shots: { sceneId: string; metricId: MetricId; weight: number; effort: Effort }[];
};
export type LevelThreeResult = { selectedMetricIds: MetricId[]; runs: WeightRun[]; compared: { nearEven: WeightRun; uneven: WeightRun } };

export const EFFORT_LABELS: Record<Effort, string> = { low: 'Minimum effort', medium: 'Steady effort', high: 'Intense effort' };
export const BEHAVIOURS: Record<MetricId, Record<Effort, { action: string; line: string }>> = {
  prep: {
    low: { action: 'Alex skims the reading title, then closes the page.', line: 'I’ll just do the basics.' },
    medium: { action: 'Alex reads the material and completes the preparation.', line: 'Okay, preparation done!' },
    high: { action: 'Alex arrives early with a pile of notes and checks every preparation requirement.', line: 'I can’t miss a single preparation point!' },
  },
  part: {
    low: { action: 'Alex raises his hand only occasionally.', line: 'I’ll speak if I have to.' },
    medium: { action: 'Alex contributes several times during class.', line: 'I should contribute more.' },
    high: { action: 'Alex tries to answer almost every question while classmates wait.', line: 'Me again! I have something to add!' },
  },
  focus: {
    low: { action: 'Alex checks his phone between tasks.', line: 'I’ll focus when needed.' },
    medium: { action: 'Alex puts his phone away and works on the classroom task.', line: 'Stay focused. Got it.' },
    high: { action: 'Alex sits bolt upright, keeping his eyes fixed on the screen.', line: 'Maximum focus!' },
  },
  discuss: {
    low: { action: 'Alex nods along without developing the discussion.', line: 'Yeah, that makes sense.' },
    medium: { action: 'Alex asks questions and explains his view.', line: 'Can you explain your idea?' },
    high: { action: 'Alex uses his discussion prompt cards to repeat the phrases that score well.', line: 'I’d like to build on your point. Could you elaborate?' },
  },
  reflect: {
    low: { action: 'Alex writes two quick sentences and submits them.', line: 'That should be enough.' },
    medium: { action: 'Alex writes a complete reflection.', line: 'I learned something new today.' },
    high: { action: 'Alex checks every line of the reflection against the rubric.', line: 'Before, I thought... Now, I think...' },
  },
  peer: {
    low: { action: 'Alex leaves a brief comment.', line: 'Nice work!' },
    medium: { action: 'Alex reads the post and gives a specific suggestion.', line: 'Maybe you could add an example.' },
    high: { action: 'Alex opens several posts and checks each reply against the response criteria.', line: 'Specific feedback? Check. Suggestion? Check!' },
  },
};

export function copyRun(run: WeightRun): WeightRun {
  return { ...run, metricIds: [...run.metricIds], weights: [...run.weights] };
}

export function compareRuns(runs: WeightRun[]) {
  const nearEven = runs.find(run => isNearEven(run.weights));
  const uneven = runs.find(run => !isNearEven(run.weights));
  return nearEven && uneven ? { nearEven: copyRun(nearEven), uneven: copyRun(uneven) } : null;
}

export function finding(run: WeightRun) {
  if (isNearEven(run.weights)) return 'Alex spreads his effort more evenly, but still follows the scoring percentages.';
  const highest = run.weights.indexOf(Math.max(...run.weights));
  const lowest = run.weights.indexOf(Math.min(...run.weights));
  return `${metricDefinition(run.metricIds[highest]).shortName} counts for ${run.weights[highest]}%. It gets more attention; ${metricDefinition(run.metricIds[lowest]).shortName.toLowerCase()} gets less.`;
}

export function cinematicRequest(kind: LevelThreeCinematicRequest['kind'], playerName: string, runs: WeightRun[]): LevelThreeCinematicRequest {
  const run = runs[runs.length - 1];
  return { sceneId: kind === 'weights' ? 'level3.weights' : kind === 'comparison' ? 'level3.compare' : 'theory.reveal', kind, playerName,
    runs: runs.map(copyRun), shots: kind !== 'weights' ? [] : run.metricIds.map((metricId, index) => ({
      sceneId: `level3.${metricId}.${effortAt(run.weights, index)}`, metricId, weight: run.weights[index], effort: effortAt(run.weights, index),
    })),
  };
}
