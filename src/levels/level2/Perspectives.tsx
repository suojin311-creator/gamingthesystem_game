import Icon from '../../shared/components/Icon';
import LearningRisk from '../../shared/components/LearningRisk';
import { METRIC_CATALOG, type MetricId } from '../../shared/data/metrics';
import { STUDENT_OBSERVATIONS, type RoundCount } from './data';

export default function Perspectives({ count, reportedCount, observedCount, selected, evaluating }: {
  count: RoundCount; reportedCount: number; observedCount: RoundCount | null;
  selected: MetricId[]; evaluating: boolean;
}) {
  const reported = reportedCount === count;
  const observed = observedCount === count;
  return <aside className="l2-perspectives" aria-label="Two perspectives">
    <section className={`l2-perspective l2-management ${reported ? 'l2-has-report' : ''}`} data-round={count}>
      <div className="l2-perspective-heading"><Icon name="school" /><h3>Management’s view</h3></div>
      <span className="l2-perspective-label">Metrics tracked</span>
      <strong className="l2-reported-count">{reported ? count : '—'}</strong>
      {reported ? <>
        <div className="l2-coverage" aria-label={`${count >= 6 ? 6 : 3} of 6 core areas covered`}>
          {METRIC_CATALOG.map(metric => <span key={metric.id} data-active={count >= 6 || selected.includes(metric.id)} title={metric.name}><Icon name={metric.id} /></span>)}
        </div>
        <p className="l2-small-note">{count >= 6 ? '6 / 6' : '3 / 6'} core areas covered</p>
      </> : <p className="l2-small-note">{evaluating ? 'Evaluating…' : 'Run an evaluation'}</p>}
    </section>
    <section className={`l2-perspective l2-students ${observed ? 'l2-has-observation' : ''}`} data-round={count} data-observed={observed}>
      <div className="l2-perspective-heading"><Icon name="student" /><h3>Students</h3></div>
      {observed ? <LearningRisk behaviour={STUDENT_OBSERVATIONS[count]} /> : <>
        <div className="l2-pending-eye"><Icon name="eye" /></div>
        <p className="l2-awaiting-observation">Awaiting observation</p>
      </>}
    </section>
  </aside>;
}
