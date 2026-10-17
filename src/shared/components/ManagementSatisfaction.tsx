import type { ReactNode } from 'react';
import '../styles/management-satisfaction.css';

// Narrative checkpoints, not measured learning or a score for the player.
// Each chapter starts at the preceding chapter's final report, including
// standalone previews. Deriving this from reports prevents replay rewards.
export const MANAGEMENT_PROGRESS = {
  awaiting: 12,
  targetMet: 44,
  metrics: { 3: 60, 6: 70, 10: 77, 25: 82, 100: 86 },
  weightTests: [86, 90, 93, 95],
} as const;

export default function ManagementSatisfaction({ value, children }: { value: number; children: ReactNode }) {
  const status = value >= 93 ? 'Delighted' : value >= 70 ? 'Very satisfied' : value >= 44 ? 'Satisfied' : 'Awaiting results';
  return <div className="management-satisfaction" data-awaiting={value < 44}>
    <span className="management-satisfaction-label">Satisfaction</span>
    <strong className="management-satisfaction-state" aria-live="polite" aria-atomic="true">{status}</strong>
    <div className="management-satisfaction-track" role="progressbar" aria-label="Management satisfaction" aria-valuemin={0} aria-valuemax={100} aria-valuenow={value} aria-valuetext={status}>
      <span style={{ width: `${value}%` }} />
    </div>
    <div className="management-satisfaction-evidence">{children}</div>
  </div>;
}
