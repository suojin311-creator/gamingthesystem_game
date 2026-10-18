import './styles.css';
import { useEffect, useRef, useState, type ReactNode } from 'react';
import { METRIC_CATALOG, metricDefinition, type MetricId } from '../../shared/data/metrics';
import Icon from '../../shared/components/Icon';
import ChapterTransition from '../../shared/components/ChapterTransition';
import Conversation from '../../shared/components/Conversation';
import LearningRisk from '../../shared/components/LearningRisk';
import MetricSelection from '../../shared/components/MetricSelection';
import EffortDisplay from './EffortDisplay';
import CriteriaStop from './CriteriaStop';
import WeightComparison from './WeightComparison';
import WeightGuide from './WeightGuide';
import ExperimentPrompt from './ExperimentPrompt';
import { experimentHint, meetsExperiment, nextExperiment } from './experiments';
import ManagementSatisfaction, { MANAGEMENT_PROGRESS } from '../../shared/components/ManagementSatisfaction';
import { useFeedback } from '../../shared/hooks/useFeedback';
import { useVisibleDelay } from '../../shared/hooks/useVisibleDelay';
import { resolvePlayerName } from '../../shared/utils/playerName';
import CinematicPlaceholder from './CinematicPlaceholder';
import { workbenchDialogue } from './dialogue';
import { EFFORT_LABELS, cinematicRequest, compareRuns, copyRun, type LevelThreeCinematicRequest, type LevelThreeResult, type WeightRun } from './data';
import { EVEN_WEIGHTS, MIN_WEIGHT, allocateWeight, canRun, confirmWeight, effortAt, isNearEven, maximumWeight, type Confirmed, type WeightGoal, type Weights } from './weights';

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

function RunRows({ run, shown = 3 }: { run: WeightRun; shown?: number }) {
  return <div className="l3-run-table"><div className="l3-result-legend" aria-hidden="true"><span>METRIC</span><span>WEIGHT</span><span>ALEX’S EFFORT</span></div><ol className="l3-run-rows">{run.metricIds.map((id, index) => {
    const effort = effortAt(run.weights, index);
    return <li key={id} data-metric={id} data-effort={effort} data-shown={index < shown} aria-hidden={index >= shown} aria-label={`${metricDefinition(id).name}: score weight ${run.weights[index]} percent; Alex’s effort: ${EFFORT_LABELS[effort]}`} style={{ '--row-index': index } as React.CSSProperties}>
      <span className="l3-row-metric"><Icon name={id} /><span>{metricDefinition(id).shortName}</span></span>
      <strong className="l3-row-weight">{run.weights[index]}<small>%</small></strong>
      <EffortDisplay metricId={id} effort={effort} />
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
  const [guideOpen, setGuideOpen] = useState(false);
  const [promptAttended, setPromptAttended] = useState(false);
  const [suggestionApplied, setSuggestionApplied] = useState(false);
  const [guideSeen, setGuideSeen] = useState(false);
  const [adjustedIndex, setAdjustedIndex] = useState<number | null>(null);
  const [published, setPublished] = useState(0);
  const [reportReady, setReportReady] = useState(false);
  const [resultRows, setResultRows] = useState(0);
  const [resultTalkReady, setResultTalkReady] = useState(false);
  const [routineReady, setRoutineReady] = useState(false);
  const [dialogueReady, setDialogueReady] = useState(false);
  const [runId, setRunId] = useState(0);
  const [hint, setHint] = useState('');
  const title = useRef<HTMLHeadingElement>(null);
  const completionReported = useRef(false);
  const lastTick = useRef(0);
  const feedback = useFeedback();
  const current = runs.at(-1);
  const baseline = runs.at(-1)?.weights || EVEN_WEIGHTS;
  const experiment = nextExperiment(runs);
  const readyToRun = runs.length < 3 && canRun(weights, confirmed, baseline, goal) && meetsExperiment(weights, runs, experiment);
  const guideStep = confirmed.filter(Boolean).length === 3 ? 3 : confirmed.some(Boolean) ? 2 : adjustedIndex === null ? 0 : 1;
  const compared = compareRuns(runs);
  const key = `${runId}:${phase}:${runs.length}`;
  const confirmedCount = confirmed.filter(Boolean).length;
  const showPerspectives = phase === 'publish' || phase === 'result' || phase === 'compare';
  const hasReport = phase !== 'publish' || reportReady;
  const completedReports = runs.length - (hasReport ? 0 : 1);
  const satisfaction = MANAGEMENT_PROGRESS.weightTests[Math.min(completedReports, 3)];
  const hasObservation = phase === 'compare' || phase === 'result' && resultRows === 3;
  const stage = phase === 'intro' || phase === 'choose' ? 0 : ['compare', 'comparison-scene', 'theory'].includes(phase) ? 3 : runs.length > (phase === 'weights' ? 0 : 1) ? 2 : 1;
  const sceneKind = phase === 'scene' ? 'weights' : phase === 'comparison-scene' ? 'comparison' : phase === 'theory' ? 'theory' : null;
  const request = sceneKind ? cinematicRequest(sceneKind, playerName, runs) : null;
  const lines = workbenchDialogue(phase, playerName, goal, runs);

  function move(next: Phase) { feedback.stop(); setHint(''); setResultTalkReady(false); setRoutineReady(false); setDialogueReady(false); setPhase(next); }
  function choose(id: MetricId) {
    if (selected.includes(id)) setSelected(selected.filter(value => value !== id));
    else if (selected.length < 3) setSelected(METRIC_CATALOG.map(metric => metric.id).filter(value => value === id || selected.includes(value)));
    else { setHint('Three selected. Deselect one to swap it.'); return; }
    setHint(''); feedback.play('tick');
  }
  function startEditor(next: WeightGoal) {
    setGoal(next); setWeights([...baseline]); setAdjustedIndex(null); setPromptAttended(false); setSuggestionApplied(false);
    if (!guideSeen) { setGuideOpen(true); setGuideSeen(true); }
    setConfirmed(EMPTY_CONFIRMATIONS); setAutoConfirmedIndex(null); move('weights');
  }
  function adjust(index: number, value: number) {
    setPromptAttended(true); setSuggestionApplied(false);
    const next = allocateWeight(weights, confirmed, index, value);
    setWeights(next);
    if (next.some((weight, i) => weight !== weights[i])) setAdjustedIndex(index);
    if (performance.now() - lastTick.current > 130) { feedback.play('tick'); lastTick.current = performance.now(); }
  }
  function confirm(index: number) {
    if (confirmed[index]) return;
    setPromptAttended(true);
    const automatic = confirmedCount === 1 ? confirmed.findIndex((locked, i) => !locked && i !== index) : -1;
    setAutoConfirmedIndex(automatic >= 0 ? automatic : null);
    setConfirmed(confirmWeight(confirmed, index)); feedback.play('tick');
  }
  function resetWeights() {
    setPromptAttended(true); setSuggestionApplied(false);
    setWeights([...baseline]); setAdjustedIndex(null); setConfirmed(EMPTY_CONFIRMATIONS); setAutoConfirmedIndex(null); feedback.play('tick');
  }
  function publish(next = weights, kind: WeightRun['kind'] = 'player') {
    if (runs.length >= 3 || !canRun(next, confirmed, baseline, goal) || !meetsExperiment(next, runs, experiment)) return;
    setGuideOpen(false);
    const record: WeightRun = { round: runs.length + 1, kind, metricIds: [...selected], weights: [...next] };
    setRuns([...runs, record]); setPublished(0); setReportReady(false); setResultRows(0); move('publish');
  }
  function completeLevel() {
    if (runs.length !== 3 || !compared || completionReported.current) return;
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
    setRuns([]); setGoal('first'); setGuideOpen(false); setGuideSeen(false); setAdjustedIndex(null); setPublished(0); setReportReady(false); setResultRows(0); setAutoConfirmedIndex(null);
    setRunId(value => value + 1); feedback.reset(); move('intro');
  }

  useVisibleDelay(`${key}:${published}`, '.l3-publish', 550, phase === 'publish' && published < 3, () => {
    setPublished(value => value + 1); feedback.play('tick');
  });
  useVisibleDelay(key, '.l3-publish', 650, phase === 'publish' && published === 3 && !reportReady, () => { setReportReady(true); feedback.play('report'); });
  useVisibleDelay(`${key}:${resultRows}`, '.l3-results', 700, phase === 'result' && resultRows < 3, () => {
    setResultRows(value => value + 1); feedback.play('evidence');
  });
  useVisibleDelay(`${key}:dialogue`, '.l3-results', 450, phase === 'result' && resultRows === 3 && (!current || !isNearEven(current.weights) || routineReady) && !resultTalkReady, () => {
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

  const action = current && (runs.length < 3
    ? <button className="button primary-button" onClick={() => startEditor('different')}>{runs.length === 1 ? 'Adjust the weights' : 'Test your explanation'}<Icon name="arrow" /></button>
    : compared && <button className="button primary-button" onClick={() => move('compare')}>Compare the patterns<Icon name="arrow" /></button>);

  function useSuggestion() {
    if (!experiment.suggestion) return;
    setPromptAttended(true); setSuggestionApplied(true);
    setWeights([...experiment.suggestion]); setAdjustedIndex(null); setConfirmed(EMPTY_CONFIRMATIONS); setAutoConfirmedIndex(null); feedback.play('tick');
  }

  return <div className="game-page level-three" data-phase={phase} data-round={runs.length} onPointerDown={feedback.unlock} onKeyDown={event => { feedback.unlock(); if (event.key === 'Escape') setGuideOpen(false); }}>
    <header className="l3-masthead"><a className="l3-wordmark" href="#level-three-main" aria-label="Gaming the System, skip to game"><span className="l3-emblem" aria-hidden="true">g<span>s</span><i /></span><span>GAMING<br /><b>THE SYSTEM</b></span></a><div className="l3-header-controls">{phase === 'weights' && <button onClick={() => setGuideOpen(true)}><Icon name="question" /><span>Guide</span></button>}<button aria-pressed={!feedback.muted} disabled={!feedback.available} onClick={feedback.toggle}><Icon name={feedback.muted || !feedback.available ? 'muted' : 'sound'} /><span>{!feedback.available ? 'No audio' : feedback.muted ? 'Sound off' : 'Sound on'}</span></button></div></header>
    <main className="l3-workbench" id="level-three-main">
      {phase !== 'intro' && <><div className="l3-heading"><div><span className="chapter-number">03</span><h1>The weighting trap.</h1></div><span className="l3-location"><i />THE OFFICE</span></div>
      <nav className="l3-stepper" aria-label="Level 3 progress"><ol>{STAGES.map((label, index) => <li key={label} className={stage === index ? 'current' : stage > index ? 'done' : ''} aria-current={stage === index ? 'step' : undefined}><span>{stage > index ? <Icon name="check" /> : `0${index + 1}`}</span>{label}</li>)}</ol></nav></>}
      {request ? (renderCinematic ? renderCinematic(request, finishScene) : <CinematicPlaceholder key={`${key}:${request.sceneId}`} request={request} onComplete={finishScene} />)
        : phase === 'intro' ? <ChapterTransition key={`intro:${runId}`} level={3} playerName={playerName} initialMetricIds={initialSelection} play={feedback.play} onStart={() => move('choose')} />
        : <div className={`l3-body ${showPerspectives ? 'l3-with-perspectives' : ''}`}><section className="l3-decision">
          <div className="section-intro"><span className="eyebrow l3-round-label">{phase === 'weights' ? `TEST ${runs.length + 1} OF 3 · ${experiment.label.toUpperCase()}` : current && phase !== 'choose' ? `TEST ${current.round} OF 3` : 'CHOOSE EXACTLY THREE'}</span><h2 ref={title} tabIndex={-1}>{phase === 'choose' ? 'Which three would I prioritize?' : phase === 'weights' ? runs.length === 0 ? 'Set your first split.' : runs.length === 1 ? 'Make an adjustment.' : 'Test your explanation.' : phase === 'publish' ? reportReady ? 'Weights published.' : 'Sharing the new weights…' : phase === 'result' ? 'Where did Alex’s effort go?' : 'What changed across the tests?'}</h2></div>
          {phase === 'choose' && <><MetricSelection level={3} capacity={3} selected={selected} onToggle={choose} hint={hint} /><div className="action-row l3-only-action"><button className="button primary-button" disabled={selected.length !== 3} onClick={() => startEditor('first')}>Set the weights<Icon name="arrow" /></button></div></>}
          {phase === 'weights' && <><ExperimentPrompt experiment={experiment} attended={promptAttended} applied={suggestionApplied} onApply={useSuggestion} />{guideOpen && <WeightGuide step={guideStep} onClose={() => setGuideOpen(false)} />}{confirmedCount === 3 && !readyToRun && <p className="l3-edit-error" role="alert">{experimentHint(experiment)} Reset weights to adjust.</p>}{goal !== 'first' && <div className="l3-previous"><span>Last run</span>{selected.map((id, index) => <span key={id}>{metricDefinition(id).shortName} <b>{baseline[index]}%</b></span>)}</div>}<div className="l3-weight-grid">{selected.map((id, index) => {
            const locked = confirmed[index];
            const automatic = autoConfirmedIndex === index;
            return <article className="l3-weight-card" data-testid={`weight-card-${id}`} data-confirmed={locked} data-auto-confirmed={automatic} data-focus={experiment.focus.includes(id)} data-guide={guideOpen ? guideStep === 0 ? 'slider' : guideStep === 1 && adjustedIndex === index ? 'confirm' : guideStep === 2 && !locked ? 'remaining' : undefined : undefined} key={id} style={{ '--card-index': index } as React.CSSProperties}>
              <div className="l3-weight-card-top"><Icon name={id} /><span>{locked ? <><Icon name="check" />{automatic ? 'Auto-confirmed' : 'Locked'}</> : confirmedCount ? `Up to ${maximumWeight(weights, confirmed, index)}%` : ''}</span></div><h3><label htmlFor={`weight-${id}`}>{metricDefinition(id).name}</label></h3><output htmlFor={`weight-${id}`} className="l3-weight-value">{weights[index]}<span>%</span></output>
              <input id={`weight-${id}`} type="range" min={MIN_WEIGHT} max={locked ? weights[index] : maximumWeight(weights, confirmed, index)} aria-valuemin={MIN_WEIGHT} aria-valuemax={locked ? weights[index] : maximumWeight(weights, confirmed, index)} step={1} value={weights[index]} disabled={locked} aria-label={`${metricDefinition(id).name} weight`} aria-describedby={guideOpen ? 'weight-guide-instruction' : undefined} aria-valuetext={`${weights[index]} percent${locked ? automatic ? ', confirmed automatically' : ', confirmed' : ''}`} onChange={event => adjust(index, Number(event.target.value))} />
              <button className={`button ${locked ? 'secondary-button' : 'primary-button'}`} disabled={locked} data-testid={`confirm-${id}`} aria-describedby={guideOpen ? 'weight-guide-instruction' : undefined} onClick={() => confirm(index)}>{locked ? <><Icon name="check" />{automatic ? 'Auto-confirmed' : 'Confirmed'}</> : 'Confirm weight'}</button>
            </article>;
          })}</div><div className="l3-allocation" aria-label="100 percent allocated"><div className="l3-allocation-bar" aria-hidden="true">{weights.map((value, index) => <i key={index} style={{ width: `${value}%` }} />)}</div><span>100% allocated</span></div><div className="l3-editor-tools"><button className="text-button" onClick={resetWeights}><Icon name="restart" />Reset weights</button></div><div className="action-row l3-only-action l3-run-action" data-guide={guideOpen && guideStep === 3 ? 'run' : undefined}><button className="button primary-button" disabled={!readyToRun} aria-describedby={guideOpen ? 'weight-guide-instruction' : undefined} onClick={() => publish()}>Run evaluation<Icon name="arrow" /></button></div></>}
          {phase === 'publish' && current && <><div className="l3-publish" role="status"><ol>{selected.map((id, index) => <li key={id} data-published={index < published}><Icon name={id} /><span>{metricDefinition(id).shortName}</span><strong>{current.weights[index]}%</strong><span>{index < published ? <Icon name="check" /> : <i className="l3-pending-dot" />}</span></li>)}</ol></div><div className="action-row l3-only-action"><button className="button primary-button" disabled={!reportReady} onClick={() => move('scene')}><Icon name="play" />Observe the class</button></div></>}
          {phase === 'result' && current && <><div className="l3-results"><RunRows run={current} shown={resultRows} />{resultRows === 3 && isNearEven(current.weights) && <CriteriaStop key={key} runKey={key} onComplete={() => setRoutineReady(true)} />}{resultRows < 3 && <p className="l3-watching" role="status">Watching Alex adapt…</p>}</div><div className="action-row"><button className="text-button" onClick={() => move('scene')}>Replay scene</button>{resultRows === 3 && dialogueReady ? action : <span className="l3-action-space" aria-hidden="true" />}</div></>}
          {phase === 'compare' && compared && <><WeightComparison runs={runs} /><div className="action-row l3-only-action"><button className="button primary-button" onClick={() => { completeLevel(); move('comparison-scene'); }}>Watch Alex’s response<Icon name="play" /></button></div></>}

        </section>{showPerspectives && current && <aside className="l3-perspectives"><section className="l3-perspective l3-management" data-management-panel data-reported={hasReport}><h3><Icon name="school" />Management’s view</h3><ManagementSatisfaction value={satisfaction}>{hasReport ? '3 priorities · 100% allocated' : 'Publishing weights…'}</ManagementSatisfaction></section><section className={`l3-perspective student ${hasObservation ? 'l3-observed' : ''}`}><h3><Icon name="student" />Students</h3>{hasObservation ? <LearningRisk behaviour={phase === 'compare' ? 'Scores still set the stopping point.' : isNearEven(current.weights) ? 'Stops when the criteria are met.' : 'Low-weight areas get less attention.'} /> : <><Icon name="eye" /><p className="l3-awaiting">Awaiting observation</p></>}</section></aside>}</div>}
      {lines.length > 0 && <div className="l3-bottom-dialogue" aria-label="Player dialogue"><Conversation key={`workbench:${key}:${goal}`} lines={lines} enabled={resultTalkReady} typingDelay={300} readDelay={dialogueTime} play={feedback.play} onLastMessage={() => setDialogueReady(true)} onSettled={() => {}} /></div>}
    </main><footer className="l3-footer"><span>GAMING THE SYSTEM</span><span>LEVEL 03</span></footer>

  </div>;
}
