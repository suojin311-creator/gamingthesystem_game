import { useEffect, useId, useRef } from 'react';
import type { LevelOneResult } from '../../levels/level1/LevelOne';
import { getMetric } from '../../levels/level1/metrics';
import Icon from '../../shared/components/Icon';
import './settlement.css';

export type SettlementProps = {
  result: LevelOneResult;
  onReplay: () => void;
  onTryAnother: () => void;
};

export default function Settlement({ result, onReplay, onTryAnother }: SettlementProps) {
  const metric = getMetric(result.metricId)!;
  const { before, after, target } = result.reportedScore;
  const targetMet = after >= target;
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

    <div className="l1-settlement-comparison">
      <section className="l1-settlement-card l1-settlement-measured" aria-labelledby={`${id}-measured`}>
        <div className="l1-settlement-card-heading">
          <Icon name="school" />
          <h2 id={`${id}-measured`}>Measured result</h2>
        </div>
        <div className="l1-settlement-scores" aria-label={`Illustrative score: ${before} before, ${after} after`}>
          <div><span className="l1-settlement-score l1-settlement-before">{before}</span><span className="l1-settlement-label">Before</span></div>
          <Icon name="arrow" />
          <div><span className="l1-settlement-score">{after}</span><span className="l1-settlement-label">After</span></div>
        </div>
        <div className="l1-settlement-measure-notes">
          <span className="l1-settlement-target"><Icon name={targetMet ? 'check' : 'warning'} />Target {target} {targetMet ? 'met' : 'not met'}</span>
          <span className="l1-settlement-score-note">Illustrative score</span>
        </div>
        <p className="l1-settlement-card-footer">{metric.improvement}</p>
      </section>

      <section className="l1-settlement-card l1-settlement-classroom" aria-labelledby={`${id}-classroom`}>
        <div className="l1-settlement-card-heading">
          <Icon name="student" />
          <h2 id={`${id}-classroom`}>Classroom result</h2>
        </div>
        <p className="l1-settlement-behaviour">{metric.studentBehaviour}</p>
        <p className="l1-settlement-uncertainty">{metric.uncertainty}</p>
        <div className="l1-settlement-card-footer"><span className="l1-settlement-risk"><Icon name="warning" />Learning at risk</span></div>
      </section>
    </div>

    {prediction && <details className="l1-settlement-prediction">
      <summary>Your prediction</summary>
      <blockquote>{prediction}</blockquote>
    </details>}

    <footer className="l1-settlement-actions">
      <button className="l1-settlement-replay" type="button" onClick={onReplay}><Icon name="restart" />Replay animation</button>
      <button className="l1-settlement-primary" type="button" onClick={onTryAnother}>Try another metric<Icon name="arrow" /></button>
    </footer>
  </section>;
}
