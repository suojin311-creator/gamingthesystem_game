import type { CSSProperties } from 'react';
import Icon from '../../shared/components/Icon';
import { metricDefinition } from '../../shared/data/metrics';
import { EFFORT_LABELS, type WeightRun } from './data';
import { effortAt, isNearEven } from './weights';
import EffortDisplay from './EffortDisplay';

export default function WeightComparison({ runs }: { runs: WeightRun[] }) {
  return <div className="l3-comparison" data-testid="weight-comparison">
    <table className="l3-compare-table" aria-label="Alex’s effort across all tested weights" style={{ '--trial-count': runs.length } as CSSProperties}>
      <thead><tr><th scope="col" className="l3-compare-metric-heading">Metric</th>{runs.map(run => <th scope="col" key={run.round} data-run={run.round} data-kind={run.kind} className={isNearEven(run.weights) ? 'near-even' : 'uneven'}><span className="eyebrow">{run.kind !== 'player' ? 'Reference' : run.round === 1 ? 'First test' : run.round === 2 ? 'Second test' : 'Third test'}</span><small>{isNearEven(run.weights) ? 'Near-even weights' : 'Uneven weights'}</small></th>)}</tr></thead>
      <tbody>{runs[0].metricIds.map(id => <tr key={id} data-metric={id}>
        <th scope="row"><Icon name={id} /><span>{metricDefinition(id).shortName}</span></th>
        {runs.map((run, runIndex) => {
          const index = run.metricIds.indexOf(id);
          const effort = effortAt(run.weights, index);
          const previous = runs[runIndex - 1];
          const changed = !!previous && effortAt(previous.weights, previous.metricIds.indexOf(id)) !== effort;
          return <td key={run.round} data-run={run.round} data-effort={effort} data-changed={changed} className={isNearEven(run.weights) ? 'near-even' : 'uneven'} aria-label={`${metricDefinition(id).name}, ${run.kind !== 'player' ? 'reference' : `test ${run.round}`}: score weight ${run.weights[index]} percent; Alex’s effort: ${EFFORT_LABELS[effort]}`}>
            <span className="l3-compare-weight"><span className="sr-only">Score weight: </span><strong className="l3-row-weight">{run.weights[index]}<small>%</small></strong></span>
            <EffortDisplay metricId={id} effort={effort} />
          </td>;
        })}
      </tr>)}</tbody>
    </table>
  </div>;
}
