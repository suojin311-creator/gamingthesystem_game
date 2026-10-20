import { cinematicRequest, type WeightRun } from '../../levels/level3/data';
import { weightedSceneReply } from '../../levels/level3/dialogue';
import { metricDefinition, type MetricId } from '../../shared/data/metrics';

/** History is supplied by gameplay. No fabricated balanced comparison is added. */
export function endingInputFromRuns(levelOneMetricId: MetricId, runs: WeightRun[]) {
  if (runs.length < 2 || runs.length > 3) throw new Error('The ending requires the actual two or three completed trials.');
  const history = runs.map(run => {
    const request = cinematicRequest('weights', 'You', [run]);
    return { ...request, shots: request.shots.map((shot, index) => ({ ...shot, caption: weightedSceneReply(request, index), label: metricDefinition(shot.metricId).name })) };
  });
  return { levelOneMetricId, history, lastRun: history[history.length - 1] };
}
