import { useEffect, useRef, useState, type CSSProperties } from 'react';
import Icon from '../../shared/components/Icon';
import { TRIAL_INTENTS, type Experiment } from './experiments';
import type { TrialIntent } from './data';

export default function ExperimentPrompt({ experiment, intent, attended, applied, onIntent, onApply }: {
  experiment: Experiment; intent: TrialIntent | null; attended: boolean; applied: boolean; onIntent: (intent: TrialIntent) => void; onApply: () => void;
}) {
  const root = useRef<HTMLElement>(null);
  const [attention, setAttention] = useState(true);
  const [visible, setVisible] = useState(false);
  const [pageVisible, setPageVisible] = useState(!document.hidden);
  useEffect(() => {
    const observer = new IntersectionObserver(entries => setVisible(entries[0].intersectionRatio >= .15), { threshold: .15 });
    if (root.current) observer.observe(root.current);
    const visibility = () => setPageVisible(!document.hidden);
    document.addEventListener('visibilitychange', visibility);
    return () => { observer.disconnect(); document.removeEventListener('visibilitychange', visibility); };
  }, []);
  return <section ref={root} className="l3-experiment" data-purpose={experiment.purpose} data-attention={attention && !attended} aria-labelledby="experiment-question" style={{ '--prompt-play-state': visible && pageVisible ? 'running' : 'paused' } as CSSProperties} onAnimationEnd={event => { if (event.target === event.currentTarget) setAttention(false); }}>
    <fieldset className="l3-experiment-choice"><legend id="experiment-question">{experiment.question}</legend><div className="l3-intent-options">{TRIAL_INTENTS.map(item => <label key={item.id} data-selected={intent === item.id}><input type="radio" name="trial-intent" value={item.id} checked={intent === item.id} onChange={() => onIntent(item.id)} /><span>{item.label}</span></label>)}</div></fieldset>
    <details className="l3-strategy-hint" key={intent || 'unselected'}><summary>Need a hint?</summary><p>{experiment.hint}</p>{experiment.suggestion && <div className="l3-experiment-suggestion"><button className="button secondary-button" onClick={onApply}>Apply suggested weights<Icon name="arrow" /></button><span role="status" aria-live="polite">{applied ? 'Weights set. Adjust or confirm.' : 'Sets the sliders; you confirm.'}</span></div>}</details>
  </section>;
}
