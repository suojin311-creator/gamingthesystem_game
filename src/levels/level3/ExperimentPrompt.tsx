import { useEffect, useRef, useState, type CSSProperties } from 'react';
import Icon from '../../shared/components/Icon';
import type { Experiment } from './experiments';

export default function ExperimentPrompt({ experiment, attended, applied, onApply }: {
  experiment: Experiment; attended: boolean; applied: boolean; onApply: () => void;
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
    <div className="l3-experiment-question"><span className="eyebrow">TRY THIS</span><p id="experiment-question">{experiment.question}</p></div>
    {experiment.suggestion && <div className="l3-experiment-suggestion"><button className="button secondary-button" onClick={onApply}>Apply suggested weights<Icon name="arrow" /></button><span role="status" aria-live="polite">{applied ? 'Weights set. Adjust or confirm.' : 'Sets the sliders; you confirm.'}</span></div>}
  </section>;
}
