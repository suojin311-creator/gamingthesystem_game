import { useEffect, useId, useRef } from 'react';
import type { LevelOneResult } from '../../levels/level1/LevelOne';
import { PerspectivePanel } from '../../levels/level1/LevelOne';
import { getMetric } from '../../levels/level1/metrics';
import Icon from '../../shared/components/Icon';
import './settlement.css';

export type SettlementProps = {
  result: LevelOneResult;
  onTryAnother: () => void;
};

export default function Settlement({ result, onTryAnother }: SettlementProps) {
  const metric = getMetric(result.metricId)!;
  const title = useRef<HTMLHeadingElement>(null);
  const id = useId();
  const prediction = result.prediction.trim();

  useEffect(() => {
    title.current?.focus({ preventScroll: true });
  }, []);

  return <section className="l1-settlement" aria-labelledby={`${id}-title`}>
    <header className="l1-settlement-heading">
      <p className="l1-settlement-eyebrow">Level 1 results</p>
      <h1 id={`${id}-title`} ref={title} tabIndex={-1}>What changed?</h1>
    </header>

    <div className="l1-settlement-metric">
      <span className="l1-settlement-metric-icon"><Icon name={metric.id} /></span>
      <div>
        <p className="l1-settlement-label">Your chosen metric</p>
        <h2>{metric.name}</h2>
      </div>
    </div>

    <PerspectivePanel metric={metric} evaluated observed highlight={null} />

    {prediction && <details className="l1-settlement-prediction">
      <summary>Your prediction</summary>
      <blockquote>{prediction}</blockquote>
    </details>}

    <footer className="action-row only-action l1-settlement-actions">
      <button className="button primary-button" type="button" onClick={onTryAnother}>Try another metric<Icon name="arrow" /></button>
    </footer>
  </section>;
}
