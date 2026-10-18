const STEPS = [
  { title: 'Move a slider', text: 'Adjust any weight. The other two share what remains.' },
  { title: 'Confirm your choice', text: 'Click Confirm weight to lock the value you just chose.' },
  { title: 'Set the remaining pair', text: 'Adjust either remaining slider. Confirming one locks both.' },
  { title: 'Try your weights', text: 'All three are confirmed. Run the evaluation to observe Alex.' },
];

export default function WeightGuide({ step, onClose }: { step: number; onClose: () => void }) {
  return <aside className="l3-weight-guide" aria-label="Weight guide" data-step={step}>
    <div className="l3-guide-top"><span className="eyebrow">QUICK GUIDE · {step + 1} / 4</span><button className="text-button" onClick={onClose}>Skip guide</button></div>
    <div id="weight-guide-instruction" role="status" aria-live="polite" aria-atomic="true"><strong>{STEPS[step].title}</strong><p>{STEPS[step].text}</p></div>
    <div className="l3-guide-dots" aria-hidden="true">{STEPS.map((_, index) => <i key={index} data-current={index === step} data-done={index < step} />)}</div>
  </aside>;
}
