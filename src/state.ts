import { getMetric, type MetricId } from './metrics';

export type Phase = 'choose' | 'predict' | 'result' | 'cinematic' | 'review' | 'complete';
export type Session = {
  phase: Phase; metricId: MetricId | null; prediction: string;
  resultReported: boolean; reviewStep: 0 | 1 | 2;
};
export const INITIAL_SESSION: Session = { phase: 'choose', metricId: null, prediction: '', resultReported: false, reviewStep: 0 };
const STORAGE_KEY = 'gaming-the-system:level-one:v1';

export function loadSession(): Session {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || 'null');
    if (!saved || saved.version !== 1 || typeof saved.prediction !== 'string' || saved.prediction.length > 100) return INITIAL_SESSION;
    const phases: Phase[] = ['choose', 'predict', 'result', 'cinematic', 'review', 'complete'];
    if (!phases.includes(saved.phase) || (saved.metricId !== null && !getMetric(saved.metricId))) return INITIAL_SESSION;
    if (saved.phase !== 'choose' && !getMetric(saved.metricId)) return INITIAL_SESSION;
    if (['result', 'cinematic', 'review', 'complete'].includes(saved.phase) && !saved.prediction.trim()) return INITIAL_SESSION;
    // A restored interlude restarts its placeholder from the beginning.
    return {
      phase: saved.phase, metricId: saved.metricId, prediction: saved.prediction,
      resultReported: saved.resultReported === true,
      reviewStep: saved.reviewStep === 1 || saved.reviewStep === 2 ? saved.reviewStep : 0,
    };
  } catch { return INITIAL_SESSION; }
}

export function saveSession(session: Session): boolean {
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify({ version: 1, ...session })); return true; }
  catch { return false; }
}
