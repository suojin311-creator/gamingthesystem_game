import { useEffect, useRef, useState } from 'react';
import type { LevelOneResult } from '../../levels/level1/LevelOne';
import { PerspectivePanel } from '../../levels/level1/LevelOne';
import { getMetric } from '../../levels/level1/metrics';
import Icon from '../../shared/components/Icon';
import CharacterPortrait from '../../shared/components/CharacterPortrait';
import { useVisibleDelay } from '../../shared/hooks/useVisibleDelay';
import './settlement.css';

export type SettlementProps = {
  result: LevelOneResult;
  onTryAnother: () => void;
};

export default function Settlement({ result, onTryAnother }: SettlementProps) {
  const metric = getMetric(result.metricId)!;
  const recap = useRef<HTMLElement>(null);
  const prediction = result.prediction.trim();
  const handoff = useRef<HTMLDivElement>(null);
  const [uncovered, setUncovered] = useState(false);
  const [observed, setObserved] = useState(false);
  useVisibleDelay('settlement-student-reveal', '.l1-settlement [data-management-panel]', 250, uncovered, () => setObserved(true));

  useEffect(() => {
    recap.current?.focus({ preventScroll: true });
  }, []);
  useEffect(() => {
    if (uncovered || !handoff.current) return;
    const style = getComputedStyle(handoff.current);
    // The shared reduced-motion rule disables animations, so no end event fires.
    if (style.animationName === 'none' || style.animationDuration.split(',').every(part => parseFloat(part) === 0)) setUncovered(true);
  }, [uncovered]);
  useEffect(() => {
    if (!observed) return;
    const student = document.querySelector('.l1-settlement .student');
    if (student && student.getBoundingClientRect().top > innerHeight * .85) student.scrollIntoView({ block: 'center', behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth' });
  }, [observed]);

  return <section ref={recap} className="l1-settlement" aria-label="Level 1 results" tabIndex={-1} data-stage={observed ? 'observed' : 'waiting'}>
    {!uncovered && <div ref={handoff} className="l1-settlement-handoff" aria-hidden="true" onAnimationEnd={event => {
      if (event.target === event.currentTarget) setUncovered(true);
    }} />}
    <div className="l1-settlement-metric">
      <span className="l1-settlement-metric-icon"><Icon name={metric.id} /></span>
      <div>
        <p className="l1-settlement-label">Your chosen metric</p>
        <h2>{metric.name}</h2>
      </div>
    </div>

    <PerspectivePanel metric={metric} evaluated observed={observed} highlight={null} assessmentReport
      studentIllustration={<div className="settlement-student-visual" data-metric={metric.id} aria-hidden="true">
        <span className="settlement-student-portrait"><CharacterPortrait role="student" /></span>
        <div className="settlement-student-notebook"><i className="settlement-notebook-binding" />
          <span className="settlement-notebook-task"><Icon name={metric.id} /><Icon name="check" /></span>
          <i className="settlement-notebook-line" /><i className="settlement-notebook-line" />
        </div>
      </div>} />

    {prediction && <details className="l1-settlement-prediction">
      <summary>Your prediction</summary>
      <blockquote>{prediction}</blockquote>
    </details>}

    <footer className="action-row only-action l1-settlement-actions">
      <button className="button primary-button" type="button" onClick={onTryAnother}>Try another metric<Icon name="arrow" /></button>
    </footer>
  </section>;
}
