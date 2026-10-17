import './styles.css';
import { useEffect, useRef, useState, type ReactNode } from 'react';
import { METRICS, getMetric, type Metric, type MetricId } from './metrics';
import { INITIAL_SESSION, type Phase } from './state';
import Icon from '../../shared/components/Icon';
import LearningRisk from '../../shared/components/LearningRisk';
import Dialogue from './components/Dialogue';
import CinematicPlaceholder, { type CinematicRequest } from './components/CinematicPlaceholder';
import { useFeedback } from '../../shared/hooks/useFeedback';
import WorkbenchGuide from './components/WorkbenchGuide';
import { useVisibleDelay } from '../../shared/hooks/useVisibleDelay';
import { readingTime } from '../../shared/utils/readingTime';
import { resolvePlayerName } from '../../shared/utils/playerName';

export type LevelOneResult = {
  metricId: MetricId; prediction: string;
  reportedScore: { before: number; after: number; target: number };
};
export type LevelOneProps = {
  playerName?: string;
  renderCinematic?: (request: CinematicRequest, onComplete: () => void) => ReactNode;
  onComplete?: (result: LevelOneResult) => void;
  onContinue?: () => void;
  showIntro?: boolean;
};

const steps = ['Choose', 'Predict', 'Evaluate', 'Observe'];
const phaseStep: Record<Phase, number> = { choose: 0, predict: 1, result: 2, cinematic: 3, review: 3 };
const TARGET = 70;

function ResultChart({ metric, ready, score }: { metric: Metric; ready: boolean; score: number }) {
  return <div className="score-paper" data-ready={ready}>
    <div className="score-paper-top"><span className="eyebrow">{metric.shortName}</span><span className="score-state">{ready ? 'Evaluation complete' : 'Evaluating…'}</span></div>
    <div className="score-numbers" aria-label={`Reported score: ${metric.before} before, ${metric.after} after`}>
      <span className="before-score">{metric.before}<small>BEFORE</small></span>
      <Icon name="arrow" className="score-arrow" />
      <span className="after-score">{score}<small>AFTER</small></span>
    </div>
    <div className="score-track" aria-hidden="true"><span className="score-track-before" style={{ width: `${metric.before}%` }} /><span className="score-track-after" style={{ width: `${score}%` }} /><i style={{ left: `${TARGET}%` }} /></div>
    <div className="score-track-labels"><span>0</span><span className="target-label" style={{ left: `${TARGET}%` }}>Target {TARGET}</span><span>100</span></div>
    <p className="data-note">Illustrative score</p>
  </div>;
}

function PerspectivePanel({ metric, evaluated, observed, highlight }: {
  metric?: Metric; evaluated: boolean; observed: boolean; highlight: 'university' | null;
}) {
  return <aside className="perspectives" aria-label="Two perspectives">
    <section className={`perspective university ${evaluated ? 'has-result' : ''} ${highlight === 'university' ? 'just-updated' : ''}`} aria-labelledby="university-title" data-updated={highlight === 'university'} tabIndex={-1}>
      <div className="perspective-heading"><Icon name="school" /><h3 id="university-title">Management’s view</h3>{highlight === 'university' && <span className="new-badge">NEW</span>}</div>
      <span className="perspective-label">Reported score</span>
      {evaluated && metric ? <><div className="university-value"><span>{metric.after}</span><span className="gain">+{metric.after - metric.before}<Icon name="arrow" /></span></div><div className="mini-bar" aria-hidden="true"><span style={{ width: `${metric.after}%` }} /></div><p className="perspective-status"><Icon name="check" />Target met</p></> : <><div className="pending-symbol" aria-hidden="true">—</div><p className="pending-title">Run an evaluation</p></>}
    </section>
    <section className={`perspective student ${observed ? 'has-evidence' : ''}`} aria-labelledby="student-title" tabIndex={-1}>
      <div className="perspective-heading"><Icon name="student" /><h3 id="student-title">Students</h3></div>
      {observed && metric ? <LearningRisk behaviour={metric.studentBehaviour} /> : <><span className="perspective-label">Classroom response</span><div className="student-signal waiting-signal"><Icon name="eye" /></div><p className="pending-title">Not observed yet</p></>}
    </section>
  </aside>;
}

export default function LevelOne({ playerName: suppliedName, renderCinematic, onComplete, onContinue, showIntro = true }: LevelOneProps) {
  const playerName = resolvePlayerName(suppliedName);
  const [session, setSession] = useState(() => ({ ...INITIAL_SESSION }));
  const [guideOpen, setGuideOpen] = useState(showIntro);
  const [runId, setRunId] = useState(0);
  const [restartOpen, setRestartOpen] = useState(false);
  const [resultReady, setResultReady] = useState(false);
  const [animatedScore, setAnimatedScore] = useState(0);
  const [dialogueSettled, setDialogueSettled] = useState(false);
  const [highlight, setHighlight] = useState<'university' | null>(null);
  const [reviewTalkReady, setReviewTalkReady] = useState(false);
  const title = useRef<HTMLHeadingElement>(null);
  const cancelRestart = useRef<HTMLButtonElement>(null);
  const restartButton = useRef<HTMLButtonElement>(null);
  const guideButton = useRef<HTMLButtonElement>(null);
  const guideWasAutomatic = useRef(guideOpen);
  const dialog = useRef<HTMLDialogElement>(null);
  const predictionField = useRef<HTMLTextAreaElement>(null);
  const completionReported = useRef(false);
  const feedback = useFeedback();
  const paused = guideOpen || restartOpen;
  const pausedRef = useRef(paused);
  pausedRef.current = paused;
  const { phase, prediction, metricId, resultReported, reviewStep } = session;
  const metric = getMetric(metricId);
  const observed = phase === 'review' && reviewStep === 1;
  const evaluated = (phase === 'result' && resultReported) || ['cinematic', 'review'].includes(phase);
  const dialogueEnabled = phase === 'result' ? resultReported : phase === 'review' ? reviewTalkReady : true;
  const currentStep = phase === 'review' && dialogueSettled ? steps.length : phaseStep[phase];

  useVisibleDelay(`report:${runId}:${phase}:${metricId}:${resultReported}`, '.score-paper', 900,
    phase === 'result' && resultReady && !resultReported && !paused, showReport);
  useVisibleDelay(`report-emphasis:${runId}:${phase}:${metricId}:${resultReported}`, '.perspective.university', 1600,
    phase === 'result' && highlight === 'university' && !paused, () => setHighlight(null));
  useVisibleDelay(`evidence:${runId}:${phase}:${metricId}:${reviewStep}`, '.prediction-recap', 1000,
    phase === 'review' && reviewStep === 0 && !paused, showObservation);
  // Bring the conversation forward by 3.5 seconds while preserving reading order.
  useVisibleDelay(`conversation:${runId}:${phase}:${metricId}:${reviewStep}`, '.observation-recap', readingTime(metric?.evidence || '', 6000, 8000) - 3500,
    phase === 'review' && reviewStep === 1 && !paused && !reviewTalkReady, () => {
      setReviewTalkReady(true);
      bringIntoView('.dialogue-strip');
    });

  useEffect(() => {
    setDialogueSettled(false);
    setHighlight(null);
    setReviewTalkReady(false);
    if (phase === 'predict') predictionField.current?.focus({ preventScroll: true });
    else if (phase !== 'cinematic') title.current?.focus({ preventScroll: true });
    const target = title.current;
    if (phase !== 'cinematic' && target && (target.getBoundingClientRect().top < 0 || target.getBoundingClientRect().top > window.innerHeight * 0.7)) target.scrollIntoView({ block: 'start', behavior: 'instant' });
  }, [phase, runId]);
  useEffect(() => {
    const onReturn = (event: PageTransitionEvent) => { if (event.persisted) restartExperiment(); };
    window.addEventListener('pageshow', onReturn);
    return () => window.removeEventListener('pageshow', onReturn);
  }, [showIntro, feedback.reset]);
  useEffect(() => {
    if (phase !== 'result' || !metric) { setResultReady(false); return; }
    if (resultReported) { setAnimatedScore(metric.after); setResultReady(true); return; }
    setResultReady(false);
    setAnimatedScore(metric.before);
    const duration = window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 0 : 1500;
    let frame = 0;
    let elapsed = 0;
    let last = performance.now();
    let lastTick = 0;
    const tick = (now: number) => {
      // Accumulate visible time so returning to a hidden tab cannot skip the result.
      if (!document.hidden && !pausedRef.current) elapsed += Math.min(now - last, 64);
      last = now;
      const progress = duration === 0 ? 1 : Math.min(elapsed / duration, 1);
      const score = Math.round(metric.before + (metric.after - metric.before) * (1 - Math.pow(1 - progress, 3)));
      setAnimatedScore(score);
      const segment = Math.floor(progress * 5);
      if (segment > lastTick && segment < 5) { feedback.play('tick'); lastTick = segment; }
      if (progress < 1) frame = requestAnimationFrame(tick);
      else setResultReady(true);
    };
    frame = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(frame);
  }, [phase, metric, resultReported, feedback.play]);
  useEffect(() => {
    if (restartOpen) { feedback.stop(); dialog.current?.showModal(); cancelRestart.current?.focus(); }
    else if (dialog.current?.open) dialog.current.close();
  }, [restartOpen, feedback.stop]);

  function go(next: Phase) {
    feedback.stop();
    setSession(value => ({ ...value, phase: next, reviewStep: next === 'review' || next === 'cinematic' ? 0 : value.reviewStep }));
  }
  function choose(id: MetricId) {
    setSession(value => ({ ...value, metricId: id, prediction: value.metricId === id ? value.prediction : '', resultReported: false, reviewStep: 0 }));
  }
  function bringIntoView(selector: string) {
    window.requestAnimationFrame(() => {
      const panel = document.querySelector<HTMLElement>(selector);
      if (!panel) return;
      if (panel.getBoundingClientRect().top < 0 || panel.getBoundingClientRect().bottom > window.innerHeight) panel.scrollIntoView({ block: 'center', behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth' });
    });
  }
  function showReport() {
    setSession(value => ({ ...value, resultReported: true }));
    feedback.play('report');
    setHighlight('university');
    bringIntoView('.perspective.university');
  }
  function showObservation() {
    setSession(value => ({ ...value, reviewStep: 1 }));
    feedback.play('evidence');
    bringIntoView('.observation-recap');
  }
  function settleDialogue() {
    setDialogueSettled(true);
    if (phase !== 'review' || !metric || completionReported.current) return;
    completionReported.current = true;
    onComplete?.({ metricId: metric.id, prediction: prediction.trim(), reportedScore: { before: metric.before, after: metric.after, target: TARGET } });
  }
  function dismissRestart() { setRestartOpen(false); restartButton.current?.focus(); }
  function restartExperiment() {
    feedback.reset();
    completionReported.current = false;
    setSession({ ...INITIAL_SESSION });
    setRunId(value => value + 1);
    setRestartOpen(false);
    guideWasAutomatic.current = showIntro;
    setGuideOpen(showIntro);
  }
  function openGuide() { feedback.stop(); guideWasAutomatic.current = false; setGuideOpen(true); }
  function closeGuide() {
    setGuideOpen(false);
    window.requestAnimationFrame(() => {
      if (guideWasAutomatic.current) {
        title.current?.scrollIntoView({ block: 'center', behavior: 'instant' });
        title.current?.focus({ preventScroll: true });
      } else guideButton.current?.focus({ preventScroll: true });
      guideWasAutomatic.current = false;
    });
  }

  const dialogue = <Dialogue key={`${runId}:${phase}`} phase={phase} playerName={playerName} studentReplies={metric?.studentReplies} enabled={dialogueEnabled} paused={paused} play={feedback.play} onSettled={settleDialogue} />;
  const request: CinematicRequest | null = phase === 'cinematic' && metric ? { sceneId: `level1.${metric.id}`, metricId: metric.id, playerName } : null;

  return <div className="game-page level-one" onPointerDownCapture={feedback.unlock} onKeyDownCapture={feedback.unlock}>
    <header className="masthead"><a className="wordmark" href="#main-content" aria-label="Gaming the System, skip to game"><span className="brand-emblem" aria-hidden="true">g<span>s</span><i /></span><span>GAMING<br /><b>THE SYSTEM</b></span></a><div className="header-controls">{phase !== 'cinematic' && <button ref={guideButton} className="guide-button" aria-label="Guide" onClick={openGuide}><Icon name="question" /><span>Guide</span></button>}<button className="sound-button" aria-pressed={!feedback.muted} disabled={!feedback.available} onClick={feedback.toggle} title={feedback.available ? 'Toggle feedback sounds' : 'Audio is unavailable in this browser'}><Icon name={feedback.muted || !feedback.available ? 'muted' : 'sound'} /><span>{!feedback.available ? 'No audio' : feedback.muted ? 'Sound off' : 'Sound on'}</span></button><button ref={restartButton} className="restart-button" onClick={() => setRestartOpen(true)}><Icon name="restart" /><span>Restart</span></button></div></header>

    <main className="workbench" id="main-content">
      <div className="workbench-heading"><div className="chapter-heading"><span className="chapter-number">01</span><h1>One metric.</h1></div><span className="office-location"><span /> THE OFFICE</span></div>
      <nav className="stepper" aria-label="Level 1 progress"><ol>{steps.map((step, index) => <li key={step} className={`${currentStep === index ? 'current' : ''} ${currentStep > index ? 'done' : ''}`} aria-current={currentStep === index ? 'step' : undefined}><span className="step-number">{currentStep > index ? <Icon name="check" /> : `0${index + 1}`}</span><span>{step}</span></li>)}</ol></nav>

      {request ? (renderCinematic ? renderCinematic(request, () => go('review')) : <CinematicPlaceholder request={request} onComplete={() => go('review')} />) : <>
        <div className={`workbench-body phase-${phase}`}>
          <section className="decision-area" aria-label="Current decision">
            {phase === 'choose' && <>
              <div className="section-intro"><h2 ref={title} tabIndex={-1}>What will you measure?</h2><p>Choose one metric.</p></div>
              <div className="metric-grid" role="group" aria-label="Choose one metric">{METRICS.map((item, index) => <button key={item.id} type="button" data-testid={`metric-${item.id}`} className={`metric-card ${metricId === item.id ? 'selected' : ''}`} aria-pressed={metricId === item.id} onClick={() => choose(item.id)}><div className="metric-card-top"><span className="metric-illustration"><Icon name={item.id} /></span><span className="selection-circle">{metricId === item.id ? <Icon name="check" /> : <span className="card-index">0{index + 1}</span>}</span></div><h3>{item.name}</h3><p>{item.description}</p></button>)}</div>
              <div className="action-row"><span className="selection-note" role="status">{metric ? <><Icon name="check" />{metric.shortName}</> : 'Choose 1 of 6'}</span><button className="button primary-button" disabled={!metric} onClick={() => go('predict')}>Make a prediction<Icon name="arrow" /></button></div>
            </>}

            {phase === 'predict' && metric && <>
              <div className="section-intro"><h2 ref={title} tabIndex={-1}>What do you expect?</h2></div>
              <div className="selected-focus"><span className="metric-illustration"><Icon name={metric.id} /></span><h3>{metric.name}</h3><button className="text-button" onClick={() => go('choose')}>Change</button></div>
              <form className="prediction-form" onSubmit={event => { event.preventDefault(); if (prediction.trim()) setSession(value => ({ ...value, prediction: value.prediction.trim(), phase: 'result', resultReported: false })); }}>
                <label htmlFor="prediction" className="sr-only">What do you expect students to do?</label>
                <div className="prediction-paper"><span className="paper-corner" aria-hidden="true" /><textarea ref={predictionField} id="prediction" maxLength={100} value={prediction} placeholder={`e.g. ${metric.example}`} aria-describedby="prediction-count" onChange={event => setSession(value => ({ ...value, prediction: event.target.value }))} /><div id="prediction-count" className="character-counter">{prediction.length}<span> / 100</span></div></div>
                <div className="action-row prediction-actions"><button type="submit" className="button primary-button" disabled={!prediction.trim()}>Run evaluation<Icon name="arrow" /></button></div>
              </form>
            </>}

            {phase === 'result' && metric && <>
              <div className="section-intro"><h2 ref={title} tabIndex={-1}>{resultReported ? 'Target achieved.' : 'Watch the score.'}</h2></div>
              <ResultChart metric={metric} ready={resultReady} score={animatedScore} />
              <div className="action-row"><span className="selection-note" role="status">{!resultReady ? 'Evaluating…' : !resultReported ? 'Updating management…' : 'Ready to visit the class'}</span><button className="button primary-button" disabled={!resultReported} onClick={() => go('cinematic')}><Icon name="play" />Observe the class</button></div>
            </>}

            {phase === 'review' && metric && <>
              <div className="section-intro"><h2 ref={title} tabIndex={-1}>Look a little closer.</h2></div>
              <div className="comparison-stack"><article className="prediction-recap"><span className="eyebrow">YOU EXPECTED</span><blockquote>“{prediction}”</blockquote></article>
                {observed ? <article className="observation-recap" key="evidence"><span className="eyebrow">IN THE CLASSROOM</span><p>{metric.evidence}</p></article> : <div className="observation-waiting"><span>Recalling the classroom…</span></div>}
              </div>
              {dialogue}
              <div className="action-row"><button className="text-button" onClick={() => go('cinematic')}>Replay scene</button>{dialogueSettled ? <button className="button primary-button level-finished" disabled={!onContinue} onClick={onContinue}>Continue to Level 2<Icon name="arrow" /></button> : <span className="next-action-space" aria-hidden="true" />}</div>
            </>}
          </section>
          <PerspectivePanel metric={metric} evaluated={evaluated} observed={observed} highlight={highlight} />
        </div>
        {phase !== 'review' && dialogue}
      </>}
    </main>
    <footer className="page-footer">GAMING THE SYSTEM · LEVEL 01</footer>
    {guideOpen && <WorkbenchGuide key={runId} onClose={closeGuide} />}
    <dialog ref={dialog} className="restart-dialog" onCancel={event => { event.preventDefault(); dismissRestart(); }} onClose={() => { if (restartOpen) dismissRestart(); }} aria-labelledby="restart-title"><h2 id="restart-title">Restart this experiment?</h2><p>Your choice and prediction will be cleared.</p><div className="dialog-actions"><button ref={cancelRestart} className="button secondary-button" onClick={dismissRestart}>Keep playing</button><button className="button primary-button" onClick={restartExperiment}>Restart level 1</button></div></dialog>
  </div>;
}
