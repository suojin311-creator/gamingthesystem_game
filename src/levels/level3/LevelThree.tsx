import './styles.css';
import { useEffect, useRef, useState, type ReactNode } from 'react';
import { METRIC_CATALOG, metricDefinition, type MetricId } from '../../shared/data/metrics';
import Icon from '../../shared/components/Icon';
import Conversation from '../../shared/components/Conversation';
import LearningRisk from '../../shared/components/LearningRisk';
import { useFeedback } from '../../shared/hooks/useFeedback';
import { useVisibleDelay } from '../../shared/hooks/useVisibleDelay';
import { resolvePlayerName } from '../../shared/utils/playerName';
import CinematicPlaceholder from './CinematicPlaceholder';
import { workbenchDialogue } from './dialogue';
import { EFFORT_LABELS, cinematicRequest, compareRuns, copyRun, referenceTest, type LevelThreeCinematicRequest, type LevelThreeResult, type WeightRun } from './data';
import { EVEN_WEIGHTS, MIN_WEIGHT, allocateWeight, canRun, confirmWeight, effortAt, goalMet, isNearEven, maximumWeight, type Confirmed, type WeightGoal, type Weights } from './weights';

type Phase = 'intro' | 'choose' | 'weights' | 'publish' | 'scene' | 'result' | 'compare' | 'comparison-scene' | 'theory' ;
export type LevelThreeProps = {
  playerName?: string;
  initialMetricIds?: readonly MetricId[];
  renderCinematic?: (request: LevelThreeCinematicRequest, onComplete: () => void) => ReactNode;
  onComplete?: (result: LevelThreeResult) => void;
  onDesignLab?: () => void;
};
const STAGES = ['Choose three', 'Set weights', 'Try another split', 'Compare'];
const EMPTY_CONFIRMATIONS: Confirmed = [false, false, false];
const dialogueTime = (text: string) => Math.min(2500, Math.max(1300, 450 + text.split(/\s+/).length * 110));

function RunRows({ run, shown = 3, compact = false }: { run: WeightRun; shown?: number; compact?: boolean }) {
  return <div className={`l3-run-table ${compact ? 'l3-compact-table' : ''}`}><div className="l3-result-legend" aria-hidden="true"><span>METRIC</span><span>WEIGHT</span><span>ALEX’S EFFORT</span></div><ol className="l3-run-rows">{run.metricIds.map((id, index) => {
    const effort = effortAt(run.weights, index);
    return <li key={id} data-metric={id} data-effort={effort} data-shown={index < shown} aria-hidden={index >= shown} aria-label={`${metricDefinition(id).name}: score weight ${run.weights[index]} percent; Alex’s effort: ${EFFORT_LABELS[effort]}`} style={{ '--row-index': index } as React.CSSProperties}>
      <span className="l3-row-metric"><Icon name={id} /><span>{metricDefinition(id).name}</span></span>
      <strong className="l3-row-weight">{run.weights[index]}<small>%</small></strong>
      <span className="l3-effort"><span className="l3-effort-bars" aria-hidden="true">{[0, 1, 2].map(i => <i key={i} data-active={i < (effort === 'low' ? 1 : effort === 'medium' ? 2 : 3)} />)}</span><strong className="l3-effort-label">{EFFORT_LABELS[effort]}</strong></span>
    </li>;
  })}</ol></div>;
}

export default function LevelThree({ playerName: suppliedName, initialMetricIds, renderCinematic, onComplete }: LevelThreeProps) {
  const playerName = resolvePlayerName(suppliedName);
  const carried = METRIC_CATALOG.filter(metric => initialMetricIds?.includes(metric.id)).map(metric => metric.id);
  const initialSelection = carried.length === 3 ? carried : [];
  const [phase, setPhase] = useState<Phase>('intro');
  const [selected, setSelected] = useState<MetricId[]>(initialSelection);
  const [weights, setWeights] = useState<Weights>(EVEN_WEIGHTS);
  const [confirmed, setConfirmed] = useState<Confirmed>(EMPTY_CONFIRMATIONS);
  const [autoConfirmedIndex, setAutoConfirmedIndex] = useState<number | null>(null);
  const [runs, setRuns] = useState<WeightRun[]>([]);
  const [goal, setGoal] = useState<WeightGoal>('first');
  const [introReady, setIntroReady] = useState(false);
  const [published, setPublished] = useState(0);
  const [reportReady, setReportReady] = useState(false);
  const [resultRows, setResultRows] = useState(0);
  const [resultTalkReady, setResultTalkReady] = useState(false);
  const [dialogueReady, setDialogueReady] = useState(false);
  const [runId, setRunId] = useState(0);
  const [hint, setHint] = useState('');
  const title = useRef<HTMLHeadingElement>(null);
  const completionReported = useRef(false);
  const lastTick = useRef(0);
  const feedback = useFeedback();
  const current = runs.at(-1);
  const baseline = goal === 'first' ? EVEN_WEIGHTS : runs[0].weights;
  const compared = compareRuns(runs);
  const key = `${runId}:${phase}:${runs.length}`;
  const confirmedCount = confirmed.filter(Boolean).length;
  const showPerspectives = phase === 'publish' || phase === 'result' || phase === 'compare';
  const hasReport = phase !== 'publish' || reportReady;
  const hasObservation = phase === 'compare' || phase === 'result' && resultRows === 3;
  const reference = referenceTest(runs);
  const stage = phase === 'intro' || phase === 'choose' ? 0 : ['compare', 'comparison-scene', 'theory'].includes(phase) ? 3 : runs.length > (phase === 'weights' ? 0 : 1) ? 2 : 1;
  const sceneKind = phase === 'scene' ? 'weights' : phase === 'comparison-scene' ? 'comparison' : phase === 'theory' ? 'theory' : null;
  const request = sceneKind ? cinematicRequest(sceneKind, playerName, runs) : null;
  const lines = workbenchDialogue(phase, playerName, goal, current, !!compared);

  function move(next: Phase) { feedback.stop(); setHint(''); setResultTalkReady(false); setDialogueReady(false); setPhase(next); }
  function choose(id: MetricId) {
    if (selected.includes(id)) setSelected(selected.filter(value => value !== id));
    else if (selected.length < 3) setSelected(METRIC_CATALOG.map(metric => metric.id).filter(value => value === id || selected.includes(value)));
    else { setHint('Three selected. Deselect one to swap it.'); return; }
    setHint(''); feedback.play('tick');
  }
  function startEditor(next: WeightGoal) {
    setGoal(next); setWeights(next === 'first' ? EVEN_WEIGHTS : [...runs[0].weights]);
    setConfirmed(EMPTY_CONFIRMATIONS); setAutoConfirmedIndex(null); move('weights');
  }
  function adjust(index: number, value: number) {
    setWeights(allocateWeight(weights, confirmed, index, value));
    if (performance.now() - lastTick.current > 130) { feedback.play('tick'); lastTick.current = performance.now(); }
  }
  function confirm(index: number) {
    if (confirmed[index]) return;
    const automatic = confirmedCount === 1 ? confirmed.findIndex((locked, i) => !locked && i !== index) : -1;
    setAutoConfirmedIndex(automatic >= 0 ? automatic : null);
    setConfirmed(confirmWeight(confirmed, index)); feedback.play('tick');
  }
  function resetWeights() {
    setWeights([...baseline]); setConfirmed(EMPTY_CONFIRMATIONS); setAutoConfirmedIndex(null); feedback.play('tick');
  }
  function publish(next = weights, kind: WeightRun['kind'] = 'player') {
    if (kind === 'player' && !canRun(next, confirmed, baseline, goal)) return;
    const record: WeightRun = { round: runs.length + 1, kind, metricIds: [...selected], weights: [...next] };
    setRuns([...runs, record]); setPublished(0); setReportReady(false); setResultRows(0); move('publish');
  }
  function completeLevel() {
    if (!compared || completionReported.current) return;
    completionReported.current = true;
    onComplete?.({ selectedMetricIds: [...selected], runs: runs.map(copyRun), compared });
  }
  function finishScene() {
    if (phase === 'scene') { setResultRows(0); move('result'); }
    else if (phase === 'comparison-scene') move('theory');
    // The final theory placeholder is the end of this preview.
  }
  function resetForNewVisit() {
    completionReported.current = false; setSelected(initialSelection); setWeights(EVEN_WEIGHTS); setConfirmed(EMPTY_CONFIRMATIONS);
    setRuns([]); setGoal('first'); setIntroReady(false); setPublished(0); setReportReady(false); setResultRows(0); setAutoConfirmedIndex(null);
    setRunId(value => value + 1); feedback.reset(); move('intro');
  }

  useVisibleDelay(`${key}:${published}`, '.l3-publish', 550, phase === 'publish' && published < 3, () => {
    setPublished(value => value + 1); feedback.play('tick');
  });
  useVisibleDelay(key, '.l3-publish', 650, phase === 'publish' && published === 3 && !reportReady, () => { setReportReady(true); feedback.play('report'); });
  useVisibleDelay(`${key}:${resultRows}`, '.l3-results', 700, phase === 'result' && resultRows < 3, () => {
    setResultRows(value => value + 1); feedback.play('evidence');
  });
  useVisibleDelay(`${key}:dialogue`, '.l3-results', 900, phase === 'result' && resultRows === 3 && !resultTalkReady, () => {
    setResultTalkReady(true);
    requestAnimationFrame(() => document.querySelector('.level-three .l3-bottom-dialogue')?.scrollIntoView({ block: 'nearest', behavior: 'smooth' }));
  });
  useVisibleDelay(key, '.l3-comparison', 1600, phase === 'compare' && !completionReported.current, completeLevel);
  useEffect(() => {
    if (request) return;
    title.current?.focus({ preventScroll: true });
    const rect = title.current?.getBoundingClientRect();
    if (rect && (rect.top < 0 || rect.bottom > innerHeight)) title.current?.scrollIntoView({ block: 'start' });
  }, [phase, runId, runs.length]);
  useEffect(() => {
    const fresh = (event: PageTransitionEvent) => { if (event.persisted) resetForNewVisit(); };
    window.addEventListener('pageshow', fresh);
    return () => window.removeEventListener('pageshow', fresh);
  });

  const goalHint = 'Change at least one weight to try another split.';
  const action = current && (runs.length === 1
    ? <button className="button primary-button" onClick={() => startEditor('different')}>Try another split<Icon name="arrow" /></button>
    : compared ? <button className="button primary-button" onClick={() => move('compare')}>Compare the patterns<Icon name="arrow" /></button>
    : reference && <button className="button primary-button" onClick={() => publish(reference.weights, reference.kind)}>{reference.kind === 'balance-check' ? 'What if they counted equally?' : 'What if one counted more?'}<Icon name="arrow" /></button>);

  return <div className="game-page level-three" data-phase={phase} data-round={runs.length} onPointerDown={feedback.unlock} onKeyDown={feedback.unlock}>
    <header className="l3-masthead"><a className="l3-wordmark" href="#level-three-main" aria-label="Gaming the System, skip to game"><span className="l3-emblem" aria-hidden="true">g<span>s</span><i /></span><span>GAMING<br /><b>THE SYSTEM</b></span></a><div className="l3-header-controls"><button aria-pressed={!feedback.muted} disabled={!feedback.available} onClick={feedback.toggle}><Icon name={feedback.muted || !feedback.available ? 'muted' : 'sound'} /><span>{!feedback.available ? 'No audio' : feedback.muted ? 'Sound off' : 'Sound on'}</span></button></div></header>
    <main className="l3-workbench" id="level-three-main">
      <div className="l3-heading"><div><span className="chapter-number">03</span><h1>The weighting trap.</h1></div><span className="l3-location"><i />THE OFFICE</span></div>
      <nav className="l3-stepper" aria-label="Level 3 progress"><ol>{STAGES.map((label, index) => <li key={label} className={stage === index ? 'current' : stage > index ? 'done' : ''} aria-current={stage === index ? 'step' : undefined}><span>{stage > index ? <Icon name="check" /> : `0${index + 1}`}</span>{label}</li>)}</ol></nav>
      {request ? (renderCinematic ? renderCinematic(request, finishScene) : <CinematicPlaceholder key={`${key}:${request.sceneId}`} request={request} onComplete={finishScene} />)
        : phase === 'intro' ? <section className="l3-intro" aria-label="Level 3 introduction"><h2 className="eyebrow" ref={title} tabIndex={-1}>LEVEL 3</h2><Conversation key={`intro:${runId}`} lines={[
          { speaker: 'Maya', name: playerName, text: initialSelection.length === 3 ? 'Alex, I’m changing how these three priorities count.' : 'Alex, I’m choosing three priorities and deciding how much each counts.' },
          { speaker: 'Alex', name: 'Alex', text: 'New rules? I’m listening! 🫡' },
          { speaker: 'Alex', name: 'Alex', text: initialSelection.length === 3 ? 'Okay—show me the percentages!' : 'Which three are you picking?' },
        ]} typingDelay={300} readDelay={dialogueTime} play={feedback.play} onLastMessage={() => setIntroReady(true)} onSettled={() => {}} /><div className="l3-intro-actions">{introReady && <button className="button primary-button" onClick={() => move('choose')}>{initialSelection.length === 3 ? 'Review priorities' : 'Choose priorities'}<Icon name="arrow" /></button>}</div></section>
        : <div className={`l3-body ${showPerspectives ? 'l3-with-perspectives' : ''}`}><section className="l3-decision">
          <div className="section-intro"><span className="eyebrow l3-round-label">{phase === 'weights' ? goal === 'first' ? 'ROUND 1 · YOUR PRIORITIES' : 'ROUND 2 · ANOTHER SPLIT' : current && phase !== 'choose' ? current.kind !== 'player' ? 'REFERENCE TEST' : `ROUND ${current.round}` : 'CHOOSE EXACTLY THREE'}</span><h2 ref={title} tabIndex={-1}>{phase === 'choose' ? 'Which three would I prioritize?' : phase === 'weights' ? goal === 'first' ? 'How much should each one count?' : 'Try a different split.' : phase === 'publish' ? reportReady ? 'Weights published.' : 'Sharing the new weights…' : phase === 'result' ? 'Where did Alex’s effort go?' : 'What changed across the tests?'}</h2></div>
          {phase === 'choose' && <><div className="l3-choice-layout"><div className="l3-metric-grid">{METRIC_CATALOG.map((metric, index) => <button className={`l3-metric-card ${selected.includes(metric.id) ? 'selected' : ''}`} data-testid={`level3-metric-${metric.id}`} key={metric.id} aria-pressed={selected.includes(metric.id)} aria-disabled={selected.length === 3 && !selected.includes(metric.id)} onClick={() => choose(metric.id)}><span className="l3-card-top"><Icon name={metric.id} /><span>{selected.includes(metric.id) ? <Icon name="check" /> : `0${index + 1}`}</span></span><h3>{metric.name}</h3><p>{metric.description}</p></button>)}</div><aside className="l3-priorities" aria-label="Your three priorities"><span className="eyebrow">YOUR PRIORITIES</span><ol>{[0, 1, 2].map(index => <li key={index} data-filled={!!selected[index]}>{selected[index] ? <><Icon name={selected[index]} /><span>{metricDefinition(selected[index]).shortName}</span></> : <><span className="l3-empty-slot">{index + 1}</span><span>Your choice</span></>}</li>)}</ol><span role="status">{selected.length} / 3 chosen</span>{hint && <p className="l3-choice-hint" role="status">{hint}</p>}</aside></div><div className="action-row l3-only-action"><button className="button primary-button" disabled={selected.length !== 3} onClick={() => startEditor('first')}>Set the weights<Icon name="arrow" /></button></div></>}
          {phase === 'weights' && <>{goal !== 'first' && confirmedCount === 3 && !goalMet(weights, baseline, goal) && <p className="l3-edit-error" role="alert">{goalHint}</p>}{goal !== 'first' && <div className="l3-previous"><span>Last run</span>{selected.map((id, index) => <span key={id}>{metricDefinition(id).shortName} <b>{baseline[index]}%</b></span>)}</div>}<div className="l3-weight-grid">{selected.map((id, index) => {
            const locked = confirmed[index];
            const automatic = autoConfirmedIndex === index;
            return <article className="l3-weight-card" data-testid={`weight-card-${id}`} data-confirmed={locked} data-auto-confirmed={automatic} key={id} style={{ '--card-index': index } as React.CSSProperties}>
              <div className="l3-weight-card-top"><Icon name={id} /><span>{locked ? <><Icon name="check" />{automatic ? 'Auto-confirmed' : 'Locked'}</> : confirmedCount ? `Up to ${maximumWeight(weights, confirmed, index)}%` : ''}</span></div><h3><label htmlFor={`weight-${id}`}>{metricDefinition(id).name}</label></h3><output htmlFor={`weight-${id}`} className="l3-weight-value">{weights[index]}<span>%</span></output>
              <input id={`weight-${id}`} type="range" min={0} max={100} aria-valuemin={MIN_WEIGHT} aria-valuemax={locked ? weights[index] : maximumWeight(weights, confirmed, index)} step={1} value={weights[index]} disabled={locked} aria-label={`${metricDefinition(id).name} weight`} aria-valuetext={`${weights[index]} percent${locked ? automatic ? ', confirmed automatically' : ', confirmed' : ''}`} onChange={event => adjust(index, Number(event.target.value))} />
              <button className={`button ${locked ? 'secondary-button' : 'primary-button'}`} disabled={locked} data-testid={`confirm-${id}`} onClick={() => confirm(index)}>{locked ? <><Icon name="check" />{automatic ? 'Auto-confirmed' : 'Confirmed'}</> : 'Confirm weight'}</button>
            </article>;
          })}</div><div className="l3-allocation" aria-label="100 percent allocated"><div className="l3-allocation-bar" aria-hidden="true">{weights.map((value, index) => <i key={index} style={{ width: `${value}%` }} />)}</div><span>100% allocated</span></div><div className="l3-editor-tools"><button className="text-button" onClick={resetWeights}><Icon name="restart" />Reset weights</button></div><div className="action-row l3-only-action"><button className="button primary-button" disabled={!canRun(weights, confirmed, baseline, goal)} onClick={() => publish()}>Run evaluation<Icon name="arrow" /></button></div></>}
          {phase === 'publish' && current && <><div className="l3-publish" role="status"><ol>{selected.map((id, index) => <li key={id} data-published={index < published}><Icon name={id} /><span>{metricDefinition(id).name}</span><strong>{current.weights[index]}%</strong><span>{index < published ? <Icon name="check" /> : <i className="l3-pending-dot" />}</span></li>)}</ol><p>{reportReady ? 'Alex can see the new percentages.' : 'Publishing the score weights…'}</p></div><div className="action-row l3-only-action"><button className="button primary-button" disabled={!reportReady} onClick={() => move('scene')}><Icon name="play" />Observe the class</button></div></>}
          {phase === 'result' && current && <><div className="l3-results"><RunRows run={current} shown={resultRows} />{resultRows < 3 && <p className="l3-watching" role="status">Watching Alex adapt…</p>}</div><div className="action-row"><button className="text-button" onClick={() => move('scene')}>Replay scene</button>{resultRows === 3 && dialogueReady ? action : <span className="l3-action-space" aria-hidden="true" />}</div></>}
          {phase === 'compare' && compared && <><div className={`l3-comparison ${runs.length === 3 ? 'l3-three-runs' : ''}`}>{runs.map(run => <article className={`l3-comparison-card ${isNearEven(run.weights) ? 'near-even' : 'uneven'}`} data-run={run.round} data-kind={run.kind} key={run.round}><span className="eyebrow">{run.kind !== 'player' ? 'SYSTEM REFERENCE' : run.round === 1 ? 'YOUR FIRST TEST' : 'YOUR SECOND TEST'}</span><h3>{isNearEven(run.weights) ? 'Near-even weights' : 'Uneven weights'}</h3><RunRows run={run} compact /></article>)}</div><div className="action-row l3-only-action"><button className="button primary-button" onClick={() => { completeLevel(); move('comparison-scene'); }}>Watch Alex’s response<Icon name="play" /></button></div></>}

        </section>{showPerspectives && current && <aside className="l3-perspectives"><section className="l3-perspective l3-management" data-reported={hasReport}><h3><Icon name="school" />Management’s view</h3><span className="l3-perspective-label">Score weights</span><strong className="l3-total">{hasReport ? <>100<small>%</small></> : '—'}</strong><div className="l3-allocation-bar" aria-hidden="true">{(phase === 'compare' ? compared!.nearEven.weights : current.weights).map((weight, index) => <i key={index} style={{ width: `${hasReport ? weight : 0}%` }} />)}</div><p>{hasReport ? 'Three priorities · total allocated' : 'Publishing weights…'}</p></section><section className={`l3-perspective student ${hasObservation ? 'l3-observed' : ''}`}><h3><Icon name="student" />Students</h3>{hasObservation ? <LearningRisk behaviour={phase === 'compare' || isNearEven(current.weights) ? 'Points still guide Alex’s choices.' : 'Low-weight areas get less attention.'} /> : <><Icon name="eye" /><p className="l3-awaiting">Awaiting observation</p></>}</section></aside>}</div>}
      {lines.length > 0 && <div className="l3-bottom-dialogue" aria-label="Player dialogue"><Conversation key={`workbench:${key}:${goal}`} lines={lines} enabled={(phase !== 'result' || resultTalkReady) && (phase !== 'publish' || reportReady)} typingDelay={300} readDelay={dialogueTime} play={feedback.play} onLastMessage={() => setDialogueReady(true)} onSettled={() => {}} /></div>}
    </main><footer className="l3-footer"><span>GAMING THE SYSTEM</span><span>LEVEL 03</span></footer>

  </div>;
}
