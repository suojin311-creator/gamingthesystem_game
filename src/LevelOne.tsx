import { useEffect, useRef, useState, type ReactNode } from 'react';
import { METRICS, getMetric, type Metric, type MetricId } from './metrics';
import { INITIAL_SESSION, loadSession, saveSession, type Phase } from './state';
import Icon from './components/Icon';
import CinematicPlaceholder, { type CinematicRequest } from './components/CinematicPlaceholder';

export type LevelOneResult = {
  metricId: MetricId; prediction: string;
  reportedScore: { before: number; after: number; target: number };
};
export type LevelOneProps = {
  playerName?: string;
  /** The host supplies only the selected story branch. Keep numbers and predictions in this dashboard. */
  renderCinematic?: (request: CinematicRequest, onComplete: () => void) => ReactNode;
  onComplete?: (result: LevelOneResult) => void;
  /** Give each in-memory player/session a separate mount; disable persistence for a host-owned save system. */
  persist?: boolean;
};

const steps = ['Choose a focus', 'Make a prediction', 'See the result', 'Observe & reflect'];
const phaseStep: Record<Phase, number> = { choose: 0, predict: 1, result: 2, cinematic: 3, review: 3, complete: 4 };
const TARGET = 70;

function ResultChart({ metric, ready, score }: { metric: Metric; ready: boolean; score: number }) {
  return <div className="score-paper">
    <div className="score-paper-top"><span className="eyebrow">{metric.shortName} · REPORTED SCORE</span><span className={`achievement ${ready ? 'achieved' : ''}`}><Icon name={ready ? 'check' : 'spark'} />{ready ? 'Target achieved' : 'Evaluating'}</span></div>
    <div className="score-numbers" aria-label={`Reported score: ${metric.before} before, ${metric.after} after`}><span className="before-score">{metric.before}<small>BEFORE</small></span><span className="score-arrow">⟶</span><span className="after-score">{score}<small>AFTER</small></span></div>
    <div className="score-plot" aria-hidden="true"><div className="chart-guide" /><div className="chart-guide" /><div className="plot-bar before-bar" style={{ height: `${metric.before}%` }}><span>{metric.before}</span></div><div className="plot-bar after-bar" style={{ height: `${score}%` }}><span>{score}</span></div><div className="target-line" style={{ bottom: `${TARGET}%` }}><span>Target {TARGET}</span></div></div>
    <div className="chart-axis" aria-hidden="true"><span>Before</span><span>After</span></div>
    <p className="data-note">Illustrative score · 0–100 index</p>
  </div>;
}

function PerspectivePanel({ metric, evaluated, observed }: { metric?: Metric; evaluated: boolean; observed: boolean }) {
  return <aside className="perspectives" aria-label="Two perspectives">
    <div className="perspective-intro"><span className="eyebrow">TWO PERSPECTIVES</span><span className="tiny-rule" /></div>
    <section className={`perspective university ${evaluated ? 'has-result' : ''}`} aria-labelledby="university-title">
      <div className="perspective-heading"><span className="perspective-icon"><Icon name="school" /></span><span><span className="eyebrow">UNIVERSITY VIEW</span><h3 id="university-title">The reported result</h3></span></div>
      {evaluated && metric ? <><div className="university-value"><span>{metric.after}<small>/100</small></span><span className="gain">+{metric.after - metric.before}<span className="sr-only">points</span><Icon name="arrow" /></span></div><div className="mini-bar" aria-hidden="true"><span style={{ width: `${metric.after}%` }} /></div><p className="perspective-status"><Icon name="check" />Target achieved</p><p className="perspective-description">{metric.name}</p></> : <><div className="waiting-chart" aria-hidden="true"><span /><span /><span /><span /><span /></div><p className="pending-title">Awaiting an evaluation</p><p className="perspective-description">Choose a metric to give the university a measurable result.</p></>}
    </section>
    <div className="perspective-connector" aria-hidden="true"><span /><i>&</i><span /></div>
    <section className={`perspective student ${observed ? 'has-evidence' : ''}`} aria-labelledby="student-title">
      <div className="perspective-heading"><span className="perspective-icon"><Icon name="student" /></span><span><span className="eyebrow">STUDENT VIEW</span><h3 id="student-title">The classroom response</h3></span></div>
      {observed && metric ? <><p className="student-improvement"><Icon name="check" />{metric.improvement}</p><blockquote>“{metric.studentQuote}”<cite>— Alex</cite></blockquote><p className="uncertainty"><span />{metric.uncertainty}</p></> : <><div className="waiting-quote" aria-hidden="true">“</div><p className="pending-title">Not observed yet</p><p className="perspective-description">Visit the classroom after the evaluation to hear from students.</p></>}
    </section>
    <p className="perspective-footnote">One classroom.<br />Two ways of seeing it.</p>
  </aside>;
}

function Dialogue({ phase, playerName }: { phase: Phase; playerName: string }) {
  const maya: Record<Phase, string> = {
    choose: 'I need a way to track engagement. Which metric should I start with?',
    predict: 'Before I try it, what do I expect students to do?',
    result: 'That looks promising. Let’s see what changed in class.',
    cinematic: '',
    review: 'The numbers look great... but something still feels wrong.',
    complete: 'Maybe one metric is too narrow.',
  };
  return <section className={`dialogue-strip ${phase === 'review' ? 'two-voices' : ''}`} aria-label="Character dialogue">
    <div className="dialogue-character"><span className="avatar maya-avatar" aria-hidden="true">{playerName.charAt(0).toUpperCase()}</span><div className="speech-bubble maya-bubble"><span className="speaker-name">{playerName}</span><p>{maya[phase]}</p></div></div>
    {phase === 'review' ? <div className="dialogue-character alex-character"><div className="speech-bubble alex-bubble"><span className="speaker-name">Alex</span><p>Professor! I figured out exactly what you were looking for!</p></div><span className="avatar alex-avatar" aria-hidden="true">A</span></div> : <span className="dialogue-mark" aria-hidden="true">a classroom experiment</span>}
  </section>;
}

export default function LevelOne({ playerName = 'Maya', renderCinematic, onComplete, persist = true }: LevelOneProps) {
  const [session, setSession] = useState(() => persist ? loadSession() : { ...INITIAL_SESSION });
  const [storageAvailable, setStorageAvailable] = useState(true);
  const [restartOpen, setRestartOpen] = useState(false);
  const [resultReady, setResultReady] = useState(false);
  const [animatedScore, setAnimatedScore] = useState(0);
  const title = useRef<HTMLHeadingElement>(null);
  const cancelRestart = useRef<HTMLButtonElement>(null);
  const restartButton = useRef<HTMLButtonElement>(null);
  const dialog = useRef<HTMLDialogElement>(null);
  const predictionField = useRef<HTMLTextAreaElement>(null);
  const { phase, prediction, metricId } = session;
  const metric = getMetric(metricId);
  const observed = phase === 'review' || phase === 'complete';
  const evaluated = observed || phase === 'cinematic' || (phase === 'result' && resultReady);

  useEffect(() => { if (persist) setStorageAvailable(saveSession(session)); }, [session, persist]);
  useEffect(() => {
    if (phase === 'predict') predictionField.current?.focus({ preventScroll: true });
    else if (phase !== 'cinematic') title.current?.focus({ preventScroll: true });
    const target = title.current;
    if (phase !== 'cinematic' && target && (target.getBoundingClientRect().top < 0 || target.getBoundingClientRect().top > window.innerHeight * 0.7)) {
      target.scrollIntoView({ block: 'start', behavior: 'instant' });
    }
  }, [phase]);
  useEffect(() => {
    if (phase !== 'result' || !metric) { setResultReady(false); return; }
    setResultReady(false);
    setAnimatedScore(metric.before);
    const duration = window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 0 : 1400;
    let frame = 0;
    const start = performance.now();
    const tick = (now: number) => {
      const progress = duration === 0 ? 1 : Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      setAnimatedScore(Math.round(metric.before + (metric.after - metric.before) * eased));
      if (progress < 1) frame = requestAnimationFrame(tick);
      else setResultReady(true);
    };
    frame = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(frame);
  }, [phase, metric]);
  useEffect(() => {
    if (restartOpen) { dialog.current?.showModal(); cancelRestart.current?.focus(); }
    else if (dialog.current?.open) dialog.current.close();
  }, [restartOpen]);

  function go(next: Phase) { setSession(value => ({ ...value, phase: next })); }
  function choose(id: MetricId) {
    setSession(value => ({ ...value, metricId: id, prediction: value.metricId === id ? value.prediction : '' }));
  }
  function finish() {
    if (!metric) return;
    go('complete');
    onComplete?.({ metricId: metric.id, prediction: prediction.trim(), reportedScore: { before: metric.before, after: metric.after, target: TARGET } });
  }
  function dismissRestart() { setRestartOpen(false); restartButton.current?.focus(); }

  return <div className="game-page">
    <header className="masthead"><a className="wordmark" href="#main-content" aria-label="Gaming the System, skip to game"><span className="brand-emblem" aria-hidden="true">g<span>s</span><i /></span><span>GAMING<br /><b>THE SYSTEM</b></span></a><div className="masthead-caption"><span className="mini-cross" aria-hidden="true"><Icon name="spark" /></span> What gets measured<br /><em>changes what we do.</em></div><button ref={restartButton} className="restart-button" onClick={() => setRestartOpen(true)}><Icon name="restart" /><span>Restart</span></button></header>

    <main className="workbench" id="main-content">
      <div className="workbench-heading"><div className="chapter-heading"><span className="chapter-number">01</span><div><p className="eyebrow">YOUR FIRST EXPERIMENT</p><h1>One metric.</h1></div></div><span className="office-location"><span /> THE OFFICE<span className="location-separator">/</span>MONDAY</span></div>
      <nav className="stepper" aria-label="Level 1 progress"><ol>{steps.map((step, index) => <li key={step} className={`${phaseStep[phase] === index ? 'current' : ''} ${phaseStep[phase] > index ? 'done' : ''}`} aria-current={phaseStep[phase] === index ? 'step' : undefined}><span className="step-number">{phaseStep[phase] > index ? <Icon name="check" /> : `0${index + 1}`}</span><span>{step}</span></li>)}</ol></nav>

      {phase === 'cinematic' && metric ? (renderCinematic ? renderCinematic({ sceneId: `level1.${metric.id}`, metricId: metric.id }, () => go('review')) : <CinematicPlaceholder request={{ sceneId: `level1.${metric.id}`, metricId: metric.id }} playerName={playerName} onComplete={() => go('review')} />) : <>
        <div className={`workbench-body phase-${phase}`}>
          <section className="decision-area" aria-label="Current decision">
            {phase === 'choose' && <>
              <div className="section-intro"><p className="eyebrow">START WITH ONE THING</p><h2 ref={title} tabIndex={-1}>What will you measure?</h2><p>Choose one indicator to track student engagement.</p></div>
              <div className="metric-grid" role="group" aria-label="Choose one metric">{METRICS.map((item, index) => <button key={item.id} type="button" data-testid={`metric-${item.id}`} className={`metric-card ${metricId === item.id ? 'selected' : ''}`} aria-pressed={metricId === item.id} onClick={() => choose(item.id)}><div className="metric-card-top"><span className="metric-illustration"><Icon name={item.id} /></span><span className="selection-circle">{metricId === item.id ? <Icon name="check" /> : <span className="card-index">0{index + 1}</span>}</span></div><h3>{item.name}</h3><p>{item.description}</p></button>)}</div>
              <div className="action-row"><span className="selection-note" role="status">{metric ? <><span className="status-dot" />One metric selected</> : 'Select one of the six indicators.'}</span><button className="button primary-button" disabled={!metric} onClick={() => go('predict')}>Make a prediction<Icon name="arrow" /></button></div>
            </>}

            {phase === 'predict' && metric && <>
              <div className="section-intro"><p className="eyebrow">BEFORE YOU TRY IT</p><h2 ref={title} tabIndex={-1}>What do you expect?</h2><p>Imagine this metric becomes the main target for students.</p></div>
              <div className="selected-focus"><span className="metric-illustration"><Icon name={metric.id} /></span><div><span className="eyebrow">YOUR CHOSEN METRIC</span><h3>{metric.name}</h3></div><button className="text-button" onClick={() => go('choose')}>Change</button></div>
              <form className="prediction-form" onSubmit={event => { event.preventDefault(); if (prediction.trim()) { setSession(value => ({ ...value, prediction: value.prediction.trim(), phase: 'result' })); } }}>
                <label htmlFor="prediction">What do you expect students to do?</label><p id="prediction-help" className="field-help">Write one short sentence. You’ll return to it after observing the class.</p>
                <div className="prediction-paper"><span className="paper-corner" aria-hidden="true" /><textarea ref={predictionField} id="prediction" maxLength={100} value={prediction} placeholder={`e.g. ${metric.example}`} aria-describedby="prediction-help prediction-count" onChange={event => setSession(value => ({ ...value, prediction: event.target.value }))} /><div id="prediction-count" className="character-counter">{prediction.length}<span> / 100</span></div></div>
                <div className="action-row"><button type="button" className="back-button" onClick={() => go('choose')}>← Back to metrics</button><button type="submit" className="button primary-button" disabled={!prediction.trim()}>Run evaluation<Icon name="arrow" /></button></div>
              </form>
            </>}

            {phase === 'result' && metric && <>
              <div className="section-intro"><p className="eyebrow">AFTER USING THIS METRIC</p><h2 ref={title} tabIndex={-1}>The number went up.</h2><p>{metric.name}</p></div>
              <ResultChart metric={metric} ready={resultReady} score={animatedScore} />
              <p className="result-prompt">A promising result. What changed in the classroom?</p>
              <div className="action-row"><span className="selection-note" aria-live="polite">{resultReady ? 'The evaluation is complete.' : 'Evaluating the selected metric…'}</span><button className="button primary-button" disabled={!resultReady} onClick={() => go('cinematic')}><Icon name="play" />Observe the class</button></div>
            </>}

            {phase === 'review' && metric && <>
              <div className="section-intro"><p className="eyebrow">BACK AT YOUR DESK</p><h2 ref={title} tabIndex={-1}>Look a little closer.</h2><p>The same experiment, seen from two perspectives.</p></div>
              <div className="review-metric"><Icon name={metric.id} /><span>{metric.name}</span><span className="review-score">{metric.before} → {metric.after}</span></div>
              <div className="comparison-stack"><article className="prediction-recap"><span className="eyebrow">YOUR PREDICTION</span><blockquote>“{prediction}”</blockquote><span className="handwritten-note">Before the evaluation</span></article><article className="observation-recap"><span className="eyebrow">WHAT YOU OBSERVED</span><p>{metric.evidence}</p><span className="evidence-stamp">Classroom observation</span></article></div>
              <p className="reflection-question">Did the result capture the engagement you hoped for?</p>
              <div className="action-row"><button className="text-button" onClick={() => go('cinematic')}>Revisit the classroom</button><button className="button primary-button" onClick={finish}>Try more metrics<Icon name="arrow" /></button></div>
            </>}

            {phase === 'complete' && metric && <>
              <div className="completion-seal"><Icon name="check" /><span>EXPERIMENT 01 COMPLETE</span></div>
              <div className="section-intro completion-intro"><p className="eyebrow">A NEW QUESTION</p><h2 ref={title} tabIndex={-1}>What if we measured<br /><em>more than one?</em></h2><p>You have a result. You have a classroom response.<br />Now you’re ready to broaden the picture.</p></div>
              <div className="next-chapter"><span className="chapter-number">02</span><div><span className="eyebrow">NEXT CHAPTER</span><h3>More metrics.</h3><p>The next level will continue from here.</p></div><span className="coming-label">Coming next</span></div>
              <div className="action-row completion-actions"><button className="back-button" onClick={() => go('review')}>← Review this experiment</button><button className="button secondary-button" onClick={() => setRestartOpen(true)}>Try another metric<Icon name="restart" /></button></div>
            </>}
          </section>
          <PerspectivePanel metric={metric} evaluated={evaluated} observed={observed} />
        </div>
        <Dialogue phase={phase} playerName={playerName} />
      </>}
    </main>
    <footer className="page-footer"><span>GAMING THE SYSTEM<span className="footer-dot">·</span>LEVEL 01</span><span>A small experiment. A bigger question.</span></footer>
    {!storageAvailable && <p className="storage-notice" role="status">Progress can’t be saved in this browser. Keep this tab open to continue your experiment.</p>}
    <dialog ref={dialog} className="restart-dialog" onCancel={event => { event.preventDefault(); dismissRestart(); }} onClose={() => { if (restartOpen) dismissRestart(); }} aria-labelledby="restart-title"><span className="eyebrow">A FRESH START</span><h2 id="restart-title">Restart this experiment?</h2><p>Your current choice and prediction will be cleared.</p><div className="dialog-actions"><button ref={cancelRestart} className="button secondary-button" onClick={dismissRestart}>Keep playing</button><button className="button primary-button" onClick={() => { setSession({ ...INITIAL_SESSION }); dismissRestart(); }}>Restart level 1</button></div></dialog>
  </div>;
}
