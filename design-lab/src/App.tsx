import { useEffect, useRef, useState, type ReactNode } from 'react';
import { AnimatePresence, motion, useReducedMotion } from 'framer-motion';
import useClassroom, { type View } from './useClassroom';
import type { Choice, Snapshot } from './types';
import { Arrow, Bomb, Check, Clock, Flower } from './Icons';

const PROMPT = 'How would you know Alex is really learning?';
const QUESTIONS = {
  question1: 'Did the most flowers mean the deepest thinking?',
  question2: 'Did knowing there would be a ranking change what you wrote?',
};
const phaseLabels: Record<string, string> = { lobby: 'Gathering', writing: 'Writing', review: 'Sharing', ranking: 'The ranking', question1: 'A question', question2: 'A question', ending: 'Goodhart’s Law', empty: 'Closing', closed: 'Classroom closed' };
function useTime(now: () => number) { const [time, setTime] = useState(now); useEffect(() => { const t = setInterval(() => setTime(now()), 80); return () => clearInterval(t); }, [now]); return time; }
function remaining(deadline: number, now: number) { return Math.max(0, Math.ceil((deadline - now) / 1000)); }
function formatTime(n: number) { return `${Math.floor(n / 60)}:${String(n % 60).padStart(2, '0')}`; }
function Timer({ seconds, label }: { seconds: number; label?: string }) { return <div className={`timer ${seconds <= 5 ? 'last-seconds' : ''}`}><Clock />{label && <span>{label}</span>}<strong>{formatTime(seconds)}</strong></div>; }
function Brand({ view, phase }: { view: View; phase?: string }) { return <header className="lab-header"><div className="wordmark"><span className="emblem">g<span>s</span></span><span>GAMING<br/><b>THE SYSTEM</b></span></div><div className="lab-header-title">DESIGN LAB</div><span className="phase-pill"><i/>{view === 'host' ? 'Host controls' : phaseLabels[phase || 'lobby']}</span></header>; }

function Button({ children, disabled, onClick, secondary = false }: { children: ReactNode; disabled?: boolean; onClick: () => void; secondary?: boolean }) { return <button type="button" className={secondary ? 'button secondary' : 'button primary'} disabled={disabled} onClick={onClick}>{children}<Arrow /></button>; }
function Waiting({ title, children }: { title: string; children: ReactNode }) { return <section className="waiting paper"><div className="waiting-illustration" aria-hidden="true"><span/><span/><span/></div><h1>{title}</h1><div className="waiting-copy">{children}</div></section>; }

const revealEase = [.22, 1, .36, 1] as const;
function Ranking({ state }: { state: Snapshot }) {
  return <section className="ranking paper" aria-label="Final flower ranking">
    <div className="section-top"><span className="eyebrow">THE RESULTS</span><span>{state.ranking.length} reflections</span></div>
    <h1>Flowers received.</h1>
    <div className="rank-head"><span>Rank</span><span>Reflection</span><span><Flower/><span className="sr-only">Flowers</span></span></div>
    <div className="rank-window" tabIndex={0}><div className="rank-body">
      {state.ranking.map(r => <div className="rank-row" key={r.id}><strong className="rank-number">{String(r.rank).padStart(2, '0')}</strong><div><span className="rank-label">{r.label}</span><p>{r.text}</p></div><strong className="flower-count">{r.flowers}</strong></div>)}
    </div></div>
  </section>;
}

function Closing() {
  const reduced = useReducedMotion();
  const enter = (delay: number) => ({ duration: reduced ? 0 : 1.1, delay: reduced ? 0 : delay, ease: revealEase });
  return <motion.section className="closing paper" aria-label="Goodhart’s Law" initial={{ opacity: 0, y: reduced ? 0 : 18 }} animate={{ opacity: 1, y: 0 }} transition={enter(.25)}>
    <motion.div className="portrait-panel" initial={{ opacity: reduced ? 1 : 0 }} animate={{ opacity: 1 }} transition={enter(.5)}><img src="/goodhart.png" alt="An illustrated half-length portrait of Charles Goodhart."/></motion.div>
    <div className="closing-copy">
      <motion.div initial={{ opacity: reduced ? 1 : 0, y: reduced ? 0 : 10 }} animate={{ opacity: 1, y: 0 }} transition={enter(.7)}><span className="eyebrow">ONE LAST THOUGHT</span><h1>Goodhart’s Law.</h1></motion.div>
      <motion.blockquote initial={{ opacity: reduced ? 1 : 0, y: reduced ? 0 : 8 }} animate={{ opacity: 1, y: 0 }} transition={enter(1)}><span>When a measure becomes a target,</span>{' '}<span>it ceases to be a good measure.</span></motion.blockquote>
      <motion.div initial={{ opacity: reduced ? 1 : 0 }} animate={{ opacity: 1 }} transition={enter(1.2)}><p className="attribution">Charles Goodhart</p><div className="closing-rule"/></motion.div>
    </div>
  </motion.section>;
}

function ResultsSequence({ state }: { state: Snapshot }) {
  const reduced = useReducedMotion(), ending = state.phase === 'ending';
  const question = state.phase === 'question1' || state.phase === 'question2' ? QUESTIONS[state.phase] : null;
  return <div className="results-stage presentation-stage" data-presentation={state.phase}>
    <motion.div className="presentation-ranking" initial={{ opacity: 0 }} animate={{ opacity: ending ? 0 : 1, filter: question || ending ? 'blur(2px)' : 'blur(0px)' }} transition={{ duration: reduced ? 0 : .85, ease: revealEase }} inert={!!question || ending}>
      <Ranking state={state}/>
    </motion.div>
    <AnimatePresence>
      {question && <motion.div className="question-overlay" key="questions" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: reduced ? 0 : .75, ease: revealEase }}>
        <AnimatePresence mode="wait">
          <motion.h1 key={state.phase} initial={{ opacity: 0, y: reduced ? 0 : 12 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: reduced ? 0 : -8 }} transition={{ duration: reduced ? 0 : .5, ease: revealEase }}>{question}</motion.h1>
        </AnimatePresence>
      </motion.div>}
    </AnimatePresence>
    {ending && <div className="presentation-ending"><Closing/></div>}
  </div>;
}

type Lab = ReturnType<typeof useClassroom>;
function Participant({ lab, time }: { lab: Lab; time: number }) {
  const { state: s, act, busy } = lab;
  const [text, setText] = useState('');
  const [reaction, setReaction] = useState<Choice | ''>('');
  const reduced = useReducedMotion();
  const card = s?.card;
  useEffect(() => { setReaction(''); }, [card?.id]);
  useEffect(() => {
    if (s?.phase !== 'review' || !card?.vote) return;
    let live = true, timer = 0;
    const advance = async () => { const result = await act('/api/next', { reflectionId: card.id }); if (!result && live) timer = window.setTimeout(advance, 1000); };
    timer = window.setTimeout(advance, 450);
    return () => { live = false; clearTimeout(timer); };
  }, [card?.id, card?.vote, s?.phase, act]);
  if (!s) return null;
  if (s.phase === 'lobby') return <section className="intro paper"><div className="intro-copy"><span className="eyebrow">AFTER THE GAME</span><h1>Design Lab.</h1><p className="intro-main">Your reflection will be shared anonymously.</p><p>Everyone will vote, and a ranking will follow.</p><div className="gathering"><span className="pulsing-dot"/><span>Waiting for the lab to begin.</span></div></div><aside className="intro-aside"><div className="giant-flower"><Flower/></div><div className="intro-number">{String(s.joined).padStart(2, '0')}<span>participants joined</span></div><span className="quiet-label">A different perspective starts here.</span></aside></section>;
  if (s.phase === 'writing') {
    if (s.hasSubmitted || s.isAudience) return <><div className="above-paper"><span className="eyebrow">WRITING</span><Timer seconds={remaining(s.deadline, time)}/></div><Waiting title={s.hasSubmitted ? 'Submitted.' : 'You’re in the audience.'}><p>Waiting for the sharing round.</p><span className="submitted-mark"><Check/></span></Waiting></>;
    return <section className="writing paper"><div className="section-top"><span className="eyebrow">YOUR REFLECTION</span><Timer seconds={remaining(s.deadline, time)}/></div><h1 id="reflection-question">{PROMPT}</h1><form onSubmit={e => { e.preventDefault(); void act('/api/submit', { text }); }}><textarea aria-labelledby="reflection-question" value={text} maxLength={240} onChange={e => setText(e.target.value)} autoFocus disabled={busy}/><div className="input-meta"><span>{text.length} / 240</span></div><div className="action-row"><button className="button primary" disabled={!text.trim() || busy} type="submit">Submit<Arrow/></button></div></form></section>;
  }
  if (s.phase === 'review') {
    if (s.finished || !card) return <Waiting title="You’ve reached the end."><p>Waiting for everyone to finish.</p><span className="waiting-count">{s.finishedCount} / {s.joined} finished</span></Waiting>;
    const vote = async (choice: Choice) => { const result = await act('/api/vote', { reflectionId: card.id, choice }); if (result?.card?.id === card.id && result.card.vote === choice) setReaction(choice); };
    return <section className="review-area">
      <div className="above-paper"><span className="eyebrow">ANONYMOUS REFLECTIONS <span className="review-count">{String(s.cursor + 1).padStart(2, '0')} / {String(s.reviewTotal).padStart(2, '0')}</span></span></div>
      <AnimatePresence mode="wait" initial={false}>
        <motion.article className="reflection paper" key={card.id} initial={{ opacity: 0, y: reduced ? 0 : 8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: reduced ? 0 : -6 }} transition={{ duration: reduced ? 0 : .25 }}>
          <div className="section-top"><span className="eyebrow">{card.label}</span></div><p className="reflection-text">{card.text}</p>
          <div className="vote-zone"><span className="choose-label">Choose one.</span><div className="vote-options">
            <button className="vote-button agree" disabled={!!card.vote || busy} aria-pressed={card.vote === 'flower'} onClick={() => void vote('flower')}><Flower/><span>Agree</span>{card.vote === 'flower' && <Check/>}</button>
            <button className="vote-button disagree" disabled={!!card.vote || busy} aria-pressed={card.vote === 'bomb'} onClick={() => void vote('bomb')}><Bomb/><span>Disagree</span>{card.vote === 'bomb' && <Check/>}</button>
          </div>{reaction && !reduced && <motion.div className={`reaction-burst ${reaction}`} aria-hidden="true" initial={{ opacity: 1, scale: .8, y: 0 }} animate={{ opacity: 0, scale: 1.25, y: -35 }} transition={{ duration: .45 }}>{reaction === 'flower' ? <Flower/> : <Bomb/>}</motion.div>}</div>
        </motion.article>
      </AnimatePresence>
    </section>;
  }
  return <SharedPresentation state={s} time={time}/>;
}

function SharedPresentation({ state: s, time }: { state: Snapshot; time: number }) {
  if (['ranking', 'question1', 'question2', 'ending'].includes(s.phase)) return <ResultsSequence state={s}/>;
  if (s.phase === 'empty') return <Waiting title="No reflections this time."><p>Waiting for the closing thought.</p></Waiting>;
  if (s.phase === 'closed') return <Waiting title="Thank you for taking part."><p>The classroom is now closed.</p></Waiting>;
  if (s.phase === 'lobby') return <Waiting title="Design Lab."><p>{s.joined} participants have joined.</p></Waiting>;
  if (s.phase === 'writing') return <section className="display-writing paper"><div className="section-top"><span className="eyebrow">YOUR REFLECTION</span><Timer seconds={remaining(s.deadline, time)}/></div><h1>{PROMPT}</h1></section>;
  return <Waiting title="Different ideas. One classroom."><p>Everyone is exploring the reflections at their own pace.</p><span className="waiting-count">{s.finishedCount} / {s.joined} finished</span></Waiting>;
}

function Host({ lab, time }: { lab: Lab; time: number }) {
  const s = lab.state!;
  const [copied, setCopied] = useState(false);
  const [confirmClose, setConfirmClose] = useState(false);
  const share = s.joinUrls?.[0] || window.location.origin;
  const input = useRef<HTMLInputElement>(null);
  const copy = async () => { try { await navigator.clipboard.writeText(share); setCopied(true); } catch { input.current?.select(); document.execCommand('copy'); setCopied(true); } };
  const steps = ['Gathering', 'Writing', 'Sharing', 'Reflection'];
  const step = s.phase === 'lobby' ? 0 : s.phase === 'writing' ? 1 : s.phase === 'review' ? 2 : 3;
  return <div className="host-layout"><section className="host-main paper"><span className="eyebrow">CLASSROOM CONTROLS</span><h1>{s.phase === 'lobby' ? 'Ready when everyone is.' : s.phase === 'writing' ? 'Give the ideas a moment.' : s.phase === 'review' ? 'Let every perspective be seen.' : 'Leave space to think.'}</h1><ol className="host-steps">{steps.map((label, i) => <li key={label} data-current={i === step} data-done={i < step}><span>{i < step ? <Check/> : `0${i + 1}`}</span>{label}</li>)}</ol><div className="host-stats"><div><strong>{String(s.joined).padStart(2, '0')}</strong><span>participants joined</span></div><div><strong>{String(s.submitted).padStart(2, '0')}</strong><span>reflections submitted</span></div>{s.phase === 'review' ? <div><strong>{String(s.finishedCount).padStart(2, '0')}</strong><span>finished sharing</span></div> : <div><strong>{Math.round(s.writingMs / 1000)}<small>s</small></strong><span>writing time</span></div>}</div>{s.phase === 'writing' && <div className="host-deadline"><Timer seconds={remaining(s.deadline, time)} label="Writing closes in"/></div>}<div className="host-primary">{s.phase === 'lobby' ? <Button disabled={!s.joined || lab.busy} onClick={() => void lab.act('/api/host/start')}>Start writing</Button> : s.phase === 'empty' ? <Button disabled={lab.busy} onClick={() => void lab.act('/api/host/ending')}>Show Goodhart’s Law</Button> : <span className="host-status"><span className="pulsing-dot"/>{s.phase === 'closed' ? 'Classroom closed' : s.phase === 'ending' ? 'The closing thought is on screen.' : s.phase === 'question1' || s.phase === 'question2' ? 'The closing questions advance automatically.' : s.phase === 'ranking' ? 'The ranking is on screen.' : 'The activity is running.'}</span>}</div></section><aside className="host-share paper"><span className="eyebrow">INVITE THE CLASS</span><h2>One link.<br/>Everyone’s ideas.</h2><label htmlFor="share-link">Share this link with the class.</label><div className="share-input"><input ref={input} id="share-link" readOnly value={share} onFocus={e => e.currentTarget.select()}/><button type="button" onClick={() => void copy()}>{copied ? 'Copied' : 'Copy'}</button></div>{s.joinUrls && s.joinUrls.length > 1 && <details><summary>Other local addresses</summary>{s.joinUrls.slice(1).map(url => <p className="alternate-url" key={url}>{url}</p>)}</details>}<a className="host-link" href="/" target="_blank" rel="noreferrer">Join as a participant<Arrow/></a><a className="host-link" href="/display" target="_blank" rel="noreferrer">Open classroom display<Arrow/></a><p className="host-note">Join the activity in a separate tab if you’re taking part too. Start writing when everyone has arrived.</p></aside>{step === 3 && s.phase !== 'closed' && <section className="host-preview"><SharedPresentation state={s} time={time}/></section>}<footer className="host-footer"><span>Design Lab · Gaming the System</span>{s.phase !== 'closed' && <button className="text-button" onClick={() => setConfirmClose(true)}>Close classroom</button>}</footer>{confirmClose && <div className="dialog-backdrop"><section role="dialog" aria-modal="true" aria-labelledby="close-title" className="close-dialog paper"><h2 id="close-title">Close the classroom?</h2><p>Everyone will be disconnected and this session will be cleared.</p><div className="action-row"><button className="text-button" onClick={() => setConfirmClose(false)}>Keep open</button><Button onClick={() => { setConfirmClose(false); void lab.act('/api/host/close'); }}>Close classroom</Button></div></section></div>}</div>;
}

export default function App() {
  const view: View = location.pathname === '/host' ? 'host' : location.pathname === '/display' ? 'display' : 'participant';
  const lab = useClassroom(view);
  const time = useTime(lab.now);
  useEffect(() => { const image = new Image(); image.src = '/goodhart.png'; void image.decode().catch(() => undefined); }, []);
  return <div className={`lab-shell view-${view}`}><Brand view={view} phase={lab.state?.phase}/><main className="lab-main">{!lab.connected && lab.state?.phase !== 'closed' && <div className="connection-note" role="status">{lab.state ? 'Reconnecting to the classroom…' : 'Connecting to the classroom…'}</div>}{lab.error && <div className="error-note" role="alert">{lab.error}</div>}{!lab.state ? <Waiting title="Design Lab."><p>Connecting to the classroom…</p></Waiting> : view === 'host' ? <Host lab={lab} time={time}/> : view === 'display' ? <SharedPresentation state={lab.state} time={time}/> : <Participant lab={lab} time={time}/>}</main><div className="page-footer" aria-hidden="true"><span>GAMING THE SYSTEM</span><span>A little distance from the numbers.</span></div></div>;
}
