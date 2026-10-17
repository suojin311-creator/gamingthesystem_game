import Icon from '../../shared/components/Icon';
import { metricDefinition, type MetricId } from '../../shared/data/metrics';

/** A passive record of Alex's requirements, separate from the clickable cards. */
export default function Notebook({ ids, checked, choosing = false }: {
  ids: MetricId[]; checked: MetricId[]; choosing?: boolean;
}) {
  const capacity = choosing ? 3 : ids.length;
  return <section className={`l2-notebook ${choosing ? 'l2-notebook-draft' : ''} ${capacity === 6 ? 'l2-notebook-six' : ''}`} aria-label="Alex’s notebook" data-testid="level2-notebook">
    <div className="l2-notebook-heading"><span className="l2-notebook-avatar" aria-hidden="true">A</span><span className="eyebrow">ALEX’S NOTEBOOK</span><span className="l2-notebook-count">{choosing ? ids.length : checked.filter(id => ids.includes(id)).length} / {capacity} {choosing ? 'chosen' : 'complete'}</span></div>
    <ol>{Array.from({ length: capacity }, (_, index) => {
      const id = ids[index];
      const done = !!id && checked.includes(id);
      return <li key={id || `empty-${index}`} data-checked={done} aria-label={id ? `${metricDefinition(id).name}: ${done ? 'checked' : 'not checked'}` : 'Not selected'}>
        <span className="l2-notebook-box" aria-hidden="true">{done && <Icon name="check" />}</span>
        {id ? <span>{metricDefinition(id).shortName}</span> : <span className="l2-notebook-rule" aria-hidden="true" />}
      </li>;
    })}</ol>
  </section>;
}
