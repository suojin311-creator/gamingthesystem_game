import './styles.css';
import { useEffect, useRef, useState, type ReactNode } from 'react';
import { METRIC_CATALOG, metricDefinition, type MetricId } from '../../shared/data/metrics';
import Icon from '../../shared/components/Icon';
import type { ConversationLine } from '../../shared/components/Conversation';
import { useFeedback } from '../../shared/hooks/useFeedback';
import { useVisibleDelay } from '../../shared/hooks/useVisibleDelay';
import Conversation, { findingReadingTime } from './Conversation';
import MetricChecklist from './MetricChecklist';
import CinematicPlaceholder from './CinematicPlaceholder';
import { resolvePlayerName } from '../../shared/utils/playerName';
import Perspectives from './Perspectives';
import { CHECKLISTS, FINAL_EVIDENCE, SIX_EVIDENCE, THREE_OUTCOMES, classifyTrio, nextCount, sceneRequest, type LevelTwoCinematicRequest, type LevelTwoResult, type RoundCount } from './data';

type Phase = 'intro' | 'choose' | 'evaluate' | 'scene' | 'observe' | 'gaps' | 'complete';
export type LevelTwoProps = {
  playerName?: string;
  previousMetricId?: MetricId;
  renderCinematic?: (request: LevelTwoCinematicRequest, onComplete: () => void) => ReactNode;
  onComplete?: (result: LevelTwoResult) => void;
};
const ALL_IDS = METRIC_CATALOG.map(metric => metric.id);
const STAGES = ['Choose three', 'Cover the gaps', 'Keep adding'];

export default function LevelTwo({ playerName: suppliedName, previousMetricId, renderCinematic, onComplete }: LevelTwoProps) {
  const playerName = resolvePlayerName(suppliedName);
  const [phase, setPhase] = useState<Phase>('intro');
  const [selected, setSelected] = useState<MetricId[]>([]);
  const [count, setCount] = useState<RoundCount>(3);
  const [reportedCount, setReportedCount] = useState(0);
  const [observedCount, setObservedCount] = useState<RoundCount | null>(null);
  const [checked, setChecked] = useState<MetricId[]>([]);
  const [evaluationReady, setEvaluationReady] = useState(false);
  const [fromCount, setFromCount] = useState(0);
  const [shownCount, setShownCount] = useState(0);
  const [counterDone, setCounterDone] = useState(false);
  const [evidenceVisible, setEvidenceVisible] = useState(false);
  const [checklistRows, setChecklistRows] = useState(0);
  const [talkReady, setTalkReady] = useState(false);
  const [roundReady, setRoundReady] = useState(false);
  const [hint, setHint] = useState('');
  const [restartOpen, setRestartOpen] = useState(false);
  const [runId, setRunId] = useState(0);
  const title = useRef<HTMLHeadingElement>(null);
  const restart = useRef<HTMLDialogElement>(null);
  const restartButton = useRef<HTMLButtonElement>(null);
  const completionReported = useRef(false);
  const feedback = useFeedback();
  const paused = restartOpen;
  const pausedRef = useRef(paused);
  pausedRef.current = paused;
  const branch = selected.length === 3 ? classifyTrio(selected) : null;
  const growth = count >= 10;
  const growthCount = count as 10 | 25 | 100;
  const growthObservation = phase === 'observe' && growth;
  const currentIds = count === 3 ? selected : ALL_IDS;
  const pendingId = currentIds.find(id => !checked.includes(id));
  const evaluationFinished = growth ? counterDone : !pendingId;
  const evidence = phase === 'complete' ? FINAL_EVIDENCE : count === 3 && branch ? THREE_OUTCOMES[branch].evidence : SIX_EVIDENCE;
  const followingCount = nextCount(count);
  const stage = phase === 'complete' && roundReady ? 3 : phase === 'gaps' ? 1 : count === 3 ? 0 : count === 6 ? 1 : 2;
  const beatKey = `${runId}:${phase}:${count}`;

  function bringIntoView(selector: string) {
    requestAnimationFrame(() => {
      const target = document.querySelector(`.level-two ${selector}`);
      const rect = target?.getBoundingClientRect();
      if (rect && (rect.bottom > innerHeight || rect.top < 0)) target?.scrollIntoView({ block: 'center', behavior: 'smooth' });
    });
  }
  function movePhase(next: Phase) {
    feedback.stop();
    setEvidenceVisible(false); setChecklistRows(0); setTalkReady(false); setRoundReady(false); setHint('');
    setPhase(next);
  }
  function chooseMetric(id: MetricId) {
    if (selected.includes(id)) { setSelected(selected.filter(value => value !== id)); setHint(''); }
    else if (selected.length < 3) { setSelected(ALL_IDS.filter(value => value === id || selected.includes(value))); setHint(''); }
    else { setHint('Three selected. Deselect one to make a swap.'); return; }
    feedback.play('tick');
  }
  function beginRound(next: RoundCount) {
    setFromCount(reportedCount); setShownCount(reportedCount); setCounterDone(false);
    setChecked(next === 6 ? [...selected] : []); setEvaluationReady(false); setCount(next); setObservedCount(null);
    movePhase('evaluate');
  }
  function finishScene() { movePhase(count === 100 ? 'complete' : 'observe'); }
  function settleRound() {
    setRoundReady(true);
    if (phase === 'complete' && branch && !completionReported.current) {
      completionReported.current = true;
      onComplete?.({ selectedMetricIds: [...selected], branch, metricsTracked: 100 });
    }
  }
  function restartLevel() {
    completionReported.current = false;
    setSelected([]); setCount(3); setReportedCount(0); setObservedCount(null); setChecked([]);
    setShownCount(0); setFromCount(0); setCounterDone(false); setEvaluationReady(false);
    setRunId(value => value + 1); setRestartOpen(false); feedback.reset(); movePhase('intro');
  }
  function closeRestart() { setRestartOpen(false); requestAnimationFrame(() => restartButton.current?.focus()); }

  useVisibleDelay(`${beatKey}:${checked.length}`, '.l2-evaluation', 480, phase === 'evaluate' && !growth && !!pendingId && !paused, () => {
    if (pendingId) setChecked(value => [...value, pendingId]);
    feedback.play('tick');
  });
  useVisibleDelay(beatKey, '.l2-evaluation', 650, phase === 'evaluate' && evaluationFinished && !evaluationReady && !paused, () => {
    setReportedCount(count); setEvaluationReady(true); feedback.play('report');
  });
  useVisibleDelay(beatKey, '.l2-evaluation', 1000, phase === 'evaluate' && growth && evaluationReady && !paused, () => movePhase('observe'));
  useVisibleDelay(beatKey, '.l2-observation-slot', 900, (phase === 'observe' || phase === 'complete') && !evidenceVisible && !paused, () => {
    setEvidenceVisible(true); setObservedCount(count); setChecklistRows(growthObservation ? 1 : 0);
    feedback.play('evidence'); bringIntoView('.l2-observation');
  });
  useVisibleDelay(`${beatKey}:${checklistRows}`, '.l2-checklist', 550, growthObservation && evidenceVisible && checklistRows < 3 && !paused, () => setChecklistRows(value => value + 1));
  useVisibleDelay(beatKey, '.l2-checklist', 1000, growthObservation && checklistRows === 3 && !roundReady && !paused, () => setRoundReady(true));
  useVisibleDelay(beatKey, '.l2-observation', findingReadingTime(evidence), (phase === 'observe' || phase === 'complete') && !growthObservation && evidenceVisible && !talkReady && !paused, () => {
    setTalkReady(true); bringIntoView('.conversation');
  });

  useEffect(() => {
    if (phase === 'scene') return;
    const target = title.current;
    target?.focus({ preventScroll: true });
    const rect = target?.getBoundingClientRect();
    if (rect && (rect.top < 0 || rect.bottom > innerHeight)) target?.scrollIntoView({ block: 'start' });
  }, [phase, count, runId]);
  useEffect(() => {
    const restore = (event: PageTransitionEvent) => { if (event.persisted) restartLevel(); };
    window.addEventListener('pageshow', restore);
    return () => window.removeEventListener('pageshow', restore);
  });
  useEffect(() => {
    if (phase !== 'evaluate' || !growth) return;
    let frame = 0, elapsed = 0, last = performance.now(), lastTick = 0;
    const duration = matchMedia('(prefers-reduced-motion: reduce)').matches ? 0 : 1600;
    const advance = (now: number) => {
      const rect = document.querySelector('.l2-counter')?.getBoundingClientRect();
      const visible = rect && rect.bottom > 0 && rect.top < innerHeight;
      const canAdvance = !document.hidden && !pausedRef.current && visible;
      // Browsers suspend animation frames in background tabs. Do not count
      // that suspended interval as time the player has watched the counter.
      if (canAdvance) elapsed += Math.min(now - last, 64);
      last = now;
      if (!canAdvance) { frame = requestAnimationFrame(advance); return; }
      const progress = duration ? Math.min(1, elapsed / duration) : 1;
      setShownCount(Math.round(fromCount + (count - fromCount) * (1 - (1 - progress) ** 2)));
      const tick = Math.floor(progress * 4);
      if (tick > lastTick) { lastTick = tick; feedback.play('tick'); }
      if (progress < 1) frame = requestAnimationFrame(advance);
      else setCounterDone(true);
    };
    frame = requestAnimationFrame(advance);
    return () => cancelAnimationFrame(frame);
  }, [phase, count, growth, fromCount, runId, feedback.play]);
  useEffect(() => { if (restartOpen) { feedback.stop(); restart.current?.showModal(); } else restart.current?.close(); }, [restartOpen, feedback.stop]);

  const lines: ConversationLine[] = phase === 'complete'
    ? [{ speaker: 'Maya', name: playerName, text: 'What if some metrics mattered more than others?' }]
    : count === 3
      ? [{ speaker: 'Maya', name: playerName, text: 'Maybe I’m still missing something…' }, { speaker: 'Alex', name: 'Alex', text: 'Other parts? Are those being graded too?' }]
      : [{ speaker: 'Maya', name: playerName, text: 'What if I added even more metrics?' }, { speaker: 'Alex', name: 'Alex', text: 'I learned exactly how to meet the criteria!' }];
  const request = phase === 'scene' ? sceneRequest(count as 3 | 6 | 100, selected, playerName) : null;
  const counter = <div className="l2-counter" aria-label={`${shownCount} metrics tracked`}><div className="l2-counter-value"><span className="eyebrow">METRICS TRACKED</span><strong>{shownCount}</strong><span className="l2-count-change">{fromCount}<Icon name="arrow" />{count}</span></div><div className="l2-matrix" aria-hidden="true">{Array.from({ length: 100 }, (_, index) => <i key={index} data-active={index < shownCount} />)}</div></div>;

  return <div className="game-page level-two" data-phase={phase} data-round={count} data-branch={branch || ''} onPointerDown={feedback.unlock} onKeyDown={feedback.unlock}>
    <header className="l2-masthead"><a className="l2-wordmark" href="#level-two-main" aria-label="Gaming the System, skip to game"><span className="l2-emblem" aria-hidden="true">g<span>s</span><i /></span><span>GAMING<br /><b>THE SYSTEM</b></span></a><div className="l2-header-controls"><button aria-pressed={!feedback.muted} disabled={!feedback.available} onClick={feedback.toggle}><Icon name={feedback.muted || !feedback.available ? 'muted' : 'sound'} /><span>{!feedback.available ? 'No audio' : feedback.muted ? 'Sound off' : 'Sound on'}</span></button><button ref={restartButton} onClick={() => setRestartOpen(true)}><Icon name="restart" /><span>Restart</span></button></div></header>
    <main id="level-two-main" className="l2-workbench">
      <div className="l2-heading"><div><span className="chapter-number">02</span><h1>More metrics.</h1></div><span className="l2-location"><i />THE OFFICE</span></div>
      <nav className="l2-stepper" aria-label="Level 2 progress"><ol>{STAGES.map((label, index) => <li key={label} className={stage === index ? 'current' : stage > index ? 'done' : ''} aria-current={stage === index ? 'step' : undefined}><span>{stage > index ? <Icon name="check" /> : `0${index + 1}`}</span>{label}</li>)}</ol></nav>
      {request ? (renderCinematic ? renderCinematic(request, finishScene) : <CinematicPlaceholder key={`${runId}:${request.sceneId}`} request={request} onComplete={finishScene} />)
        : phase === 'intro' ? <section className="l2-intro" aria-label="Level 2 introduction">
          <h2 ref={title} tabIndex={-1} className="eyebrow">LEVEL 2</h2>
          <Conversation key={`intro:${runId}`} lines={[
            { speaker: 'Maya', name: playerName, text: 'One metric wasn’t enough. What if I tracked three? Which ones should I choose?' },
            { speaker: 'Alex', name: 'Alex', text: 'Three metrics now? Okay, I can handle that!' },
          ]} paused={paused} play={feedback.play} onSettled={() => movePhase('choose')} />
          <p className="l2-intro-next">Next: choose three metrics.</p>
        </section>
        : <div className={`l2-body ${phase === 'choose' ? 'l2-choosing' : ''}`}><section className="l2-decision">
          <div className="section-intro"><h2 ref={title} tabIndex={-1}>{phase === 'choose' ? 'Which three will you track?' : phase === 'gaps' ? 'What am I still missing?' : phase === 'evaluate' ? evaluationReady ? count === 3 && branch ? THREE_OUTCOMES[branch].report : count === 6 ? 'Six metrics. Six green ticks.' : 'More of the picture?' : growth ? 'Expanding the system…' : 'Watch the metrics.' : phase === 'complete' ? 'More measurement. What changed?' : growth ? `${count} metrics. What counts now?` : 'Look a little closer.'}</h2>{phase === 'choose' && <><p>Choose exactly three. Click a selected card to swap it.</p>{previousMetricId && <p className="l2-previous">Previously tracked: {metricDefinition(previousMetricId).shortName}</p>}</>}</div>
          {phase === 'choose' && <>
            <div className="l2-choice-layout"><div className="l2-metric-grid">{METRIC_CATALOG.map((metric, index) => <button key={metric.id} data-testid={`level2-metric-${metric.id}`} className={`l2-metric-card ${selected.includes(metric.id) ? 'selected' : ''}`} aria-pressed={selected.includes(metric.id)} aria-disabled={selected.length === 3 && !selected.includes(metric.id)} onClick={() => chooseMetric(metric.id)}><span className="l2-card-top"><span className="l2-metric-icon"><Icon name={metric.id} /></span><span className="l2-selection">{selected.includes(metric.id) ? <Icon name="check" /> : `0${index + 1}`}</span></span><h3>{metric.name}</h3><p>{metric.description}</p></button>)}</div><MetricChecklist selected={selected} /></div>
            <div className="action-row l2-choice-actions"><span className="l2-choice-summary" role="status">{hint}</span><button className="button primary-button" disabled={selected.length !== 3} onClick={() => beginRound(3)}>Run evaluation<Icon name="arrow" /></button></div>
          </>}
          {phase === 'evaluate' && <><section className="l2-evaluation" aria-label="Metric evaluation">{growth ? counter : <ul className="l2-evaluation-list">{currentIds.map(id => <li key={id} data-checked={checked.includes(id)}><span className="l2-eval-name"><Icon name={id} />{metricDefinition(id).name}</span><span className="l2-eval-result">{checked.includes(id) ? <><Icon name="check" />Improved</> : <><i className="l2-checking" />Checking</>}</span></li>)}</ul>}<p className="l2-data-note">{growth ? 'Requirements tracked, not a learning score.' : 'Illustrative outcomes'}</p></section><div className="action-row"><span className="l2-small-note" role="status">{evaluationReady ? `${count} metrics tracked` : 'Evaluation in progress…'}</span>{!growth && <button className="button primary-button" disabled={!evaluationReady} onClick={() => movePhase('scene')}><Icon name="play" />Observe the class</button>}</div></>}
          {phase === 'gaps' && <><div className="l2-gap-grid">{[true, false].map(tracked => <section className={tracked ? 'l2-covered' : 'l2-missing'} key={String(tracked)}><>{tracked ? <span className="eyebrow">TRACKED</span> : <h3 className="l2-gap-warning"><Icon name="warning" /><span>3 areas untracked</span></h3>}</><ul>{METRIC_CATALOG.filter(metric => selected.includes(metric.id) === tracked).map(metric => <li key={metric.id}><Icon name={tracked ? 'check' : metric.id} />{metric.name}</li>)}</ul></section>)}</div><p className="l2-gap-note">Three are improving. Three are still outside the frame.</p><div className="action-row"><span className="l2-small-note">Cover all six areas.</span><button className="button primary-button" onClick={() => beginRound(6)}>Add remaining metrics<Icon name="arrow" /></button></div></>}
          {(phase === 'observe' || phase === 'complete') && <>{growthObservation && counter}<div className="l2-observation-slot">{evidenceVisible ? <article className={`l2-observation ${growthObservation ? 'l2-checklist' : ''}`} key={beatKey}><span className="eyebrow">{growthObservation ? 'ALEX’S CHECKLIST' : 'IN THE CLASSROOM'}</span>{growthObservation ? <><h3>{CHECKLISTS[growthCount].label}</h3><ol>{CHECKLISTS[growthCount].actions.map((action, index) => <li key={action} data-shown={index < checklistRows} aria-hidden={index >= checklistRows} aria-label={`Completed: ${action}`}><span className="l2-check-box" data-checked={index < checklistRows} aria-hidden="true"><Icon name="check" /></span>{action}</li>)}</ol></> : <p>{evidence}</p>}</article> : <div className="l2-waiting" role="status"><Icon name="eye" /><span>Looking closer…</span></div>}</div>{!growthObservation && <Conversation key={beatKey} lines={lines} enabled={talkReady} paused={paused} play={feedback.play} onLastMessage={() => setRoundReady(true)} onSettled={settleRound} />}<div className="action-row"><span>{(!growth || phase === 'complete') && <button className="text-button" onClick={() => movePhase('scene')}>Replay scene</button>}</span>{roundReady ? phase === 'complete' ? <button className="button secondary-button" disabled>Continue to Level 3<Icon name="arrow" /></button> : count === 3 ? <button className="button primary-button" onClick={() => movePhase('gaps')}>Cover the gaps<Icon name="arrow" /></button> : followingCount ? <button className="button primary-button" onClick={() => beginRound(followingCount)}>Add more metrics<Icon name="arrow" /></button> : <button className="button primary-button" onClick={() => movePhase('scene')}><Icon name="play" />Observe the class</button> : <span className="l2-next-space" aria-hidden="true" />}</div></>}
        </section>{phase !== 'choose' && <Perspectives count={count} reportedCount={reportedCount} observedCount={observedCount} selected={selected} evaluating={phase === 'evaluate'} />}</div>}
    </main>
    <footer className="l2-footer"><span>GAMING THE SYSTEM</span><span>LEVEL 02</span></footer>
    <dialog ref={restart} className="l2-dialog" aria-labelledby="l2-restart-title" onCancel={event => { event.preventDefault(); closeRestart(); }}><span className="eyebrow">START FRESH</span><h2 id="l2-restart-title">Restart Level 2?</h2><p>Your choices in this level will be cleared.</p><div className="l2-dialog-actions"><button className="button secondary-button" autoFocus onClick={closeRestart}>Keep playing</button><button className="button primary-button" onClick={restartLevel}>Restart Level 2</button></div></dialog>
  </div>;
}
