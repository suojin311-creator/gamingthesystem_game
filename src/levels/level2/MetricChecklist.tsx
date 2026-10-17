import Icon from '../../shared/components/Icon';
import { metricDefinition, type MetricId } from '../../shared/data/metrics';

/** The checklist records choices; the six metric cards remain the controls. */
export default function MetricChecklist({ selected }: { selected: MetricId[] }) {
  return <aside className="l2-observation l2-checklist l2-choice-checklist" aria-label="Alex’s Checklist" data-testid="level2-choice-checklist">
    <span className="eyebrow">ALEX’S CHECKLIST</span>
    <h3>Selected metrics</h3>
    <p className="l2-checklist-count" role="status">{selected.length} / 3 selected</p>
    <ol>{Array.from({ length: 3 }, (_, index) => {
      const id = selected[index];
      return <li key={id || `empty-${index}`} data-empty={!id} aria-label={id ? `Selected: ${metricDefinition(id).name}` : `Metric ${index + 1}: not selected`}>
        <span className="l2-check-box" data-checked={!!id} aria-hidden="true"><Icon name="check" /></span>
        <span>{id ? metricDefinition(id).shortName : `Metric ${index + 1}`}</span>
      </li>;
    })}</ol>
  </aside>;
}
