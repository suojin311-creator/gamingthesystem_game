import { METRIC_CATALOG, type MetricId } from '../../shared/data/metrics';

export type Branch = 'visible' | 'quality' | 'mixed';
export type RoundCount = 3 | 6 | 10 | 25 | 100;
export type SceneKind = 'three' | 'six' | 'checklist';
export type LevelTwoCinematicRequest = {
  sceneId: string; kind: SceneKind; branch: Branch;
  selectedMetricIds: MetricId[]; metricCount: 3 | 6 | 100;
};
export type LevelTwoResult = { selectedMetricIds: MetricId[]; branch: Branch; metricsTracked: 100 };

export function classifyTrio(ids: readonly MetricId[]): Branch {
  if (ids.length !== 3 || new Set(ids).size !== 3 || ids.some(id => !METRIC_CATALOG.some(metric => metric.id === id))) {
    throw new Error('Choose exactly three different metrics.');
  }
  if (ids.every(id => ['prep', 'part', 'focus'].includes(id))) return 'visible';
  if (ids.every(id => ['discuss', 'reflect', 'peer'].includes(id))) return 'quality';
  return 'mixed';
}

export const THREE_OUTCOMES: Record<Branch, { report: string; evidence: string; action: string }> = {
  visible: {
    report: 'The class looks more engaged.',
    evidence: 'Preparation, participation and visible focus improve. Some students concentrate on looking prepared, active and on-task because those are the things being checked.',
    action: 'The classroom is busy: students raise their hands, keep materials open and show that they are on task.',
  },
  quality: {
    report: 'The work looks stronger.',
    evidence: 'Discussion, reflection and peer responses improve. Some students repeat the patterns that score well across the three criteria.',
    action: 'The work looks polished: discussion phrases, reflections and peer responses closely follow the expected criteria.',
  },
  mixed: {
    report: 'The dashboard looks convincing.',
    evidence: 'Different parts of engagement improve together. Some students plan their behaviour around the three selected criteria.',
    action: 'Several parts of classroom life improve, while students keep checking which of their actions will count.',
  },
};

export const SIX_EVIDENCE = 'Students check what each criterion requires and plan their work around what still needs to be shown. The measurement system is becoming part of the task itself.';
export const FINAL_EVIDENCE = 'The system tracks 100 requirements. Students reuse evidence, close unchecked gaps and look for the minimum needed to meet the remaining criteria.';

export const CHECKLISTS: Record<10 | 25 | 100, { label: string; focus: string; questions: string[] }> = {
  10: { label: 'Completing requirements', focus: 'Requirements', questions: [
    'Which requirements have I completed?',
    'Which ones are still missing?',
    'What do I need to do next?',
  ] },
  25: { label: 'Managing criteria', focus: 'Criteria', questions: [
    'Which criteria still need evidence?',
    'Can one task cover several criteria?',
    'Which requirements can I complete most efficiently?',
  ] },
  100: { label: 'Optimizing the checklist', focus: 'Checklist', questions: [
    'Which boxes are still unchecked?',
    'Where can the same evidence count more than once?',
    'What is the minimum needed to close the remaining gaps?',
  ] },
};

export function nextCount(count: RoundCount): 10 | 25 | 100 | null {
  return count === 6 ? 10 : count === 10 ? 25 : count === 25 ? 100 : null;
}

export function sceneRequest(count: 3 | 6 | 100, selectedMetricIds: MetricId[]): LevelTwoCinematicRequest {
  const branch = classifyTrio(selectedMetricIds);
  const kind: SceneKind = count === 3 ? 'three' : count === 6 ? 'six' : 'checklist';
  return { sceneId: count === 3 ? `level2.three.${branch}` : `level2.${kind}`, kind, branch, selectedMetricIds: [...selectedMetricIds], metricCount: count };
}
