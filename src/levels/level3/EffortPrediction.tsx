import Icon from '../../shared/components/Icon';
import CharacterPortrait from '../../shared/components/CharacterPortrait';
import { metricDefinition, type MetricId } from '../../shared/data/metrics';
import type { Weights } from './weights';

export default function EffortPrediction({ metricIds, weights, selected, onToggle }: {
  metricIds: readonly MetricId[]; weights: Weights; selected: readonly MetricId[]; onToggle: (id: MetricId) => void;
}) {
  return <fieldset className="l3-prediction" aria-label="Predict Alex’s highest effort">
    <legend>Pick one or more.</legend>
    <div className="l3-prediction-cards">{metricIds.map((id, index) => <button key={id} type="button" className="l3-prediction-card" data-testid={`predict-${id}`} aria-pressed={selected.includes(id)} onClick={() => onToggle(id)}>
      <span className="l3-prediction-card-top"><Icon name={id} /><small>{weights[index]}%</small></span>
      <strong>{metricDefinition(id).shortName}</strong>
      <span className="l3-prediction-portrait" aria-hidden="true"><CharacterPortrait role="student" /><span>?</span></span>
      <span className="l3-prediction-dot" data-selected={selected.includes(id)} aria-hidden="true" />
    </button>)}</div>
  </fieldset>;
}
