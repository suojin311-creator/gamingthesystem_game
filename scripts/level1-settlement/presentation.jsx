import { teacherSpeech } from '../../src/shared/utils/teacherSpeech.js';
import React, { useEffect, useRef, useState } from 'react';
import { finalCoverOpacity, SCENE_COVER_SECONDS, SOURCE_TRANSITION_START } from '@preview-transitions';
import { AbsoluteFill, Img } from 'remotion';
import { ConsequenceScene } from '@partner/cinematics/level1/ConsequenceScene';
import { DialogueLayer } from '@partner/cinematics/shared/engine/DialogueLayer/DialogueLayer';
import { branches, SECOND_THOUGHT, LEVEL1 } from '@partner/cinematics/level1/level1Content';
import { FIRST_THOUGHT, BRIDGE_LINE, EMAIL_THOUGHT_DELAY, SPEAKER_COLORS, CAPTION_SHADOW } from './content.mjs';
import { dissolveFrame } from '../cinematic-dissolve.mjs';
import officeBackground from '@partner-assets/backgrounds/BG_Office_FirstPerson_v01.png';
import '@partner/styles.css';
import '@partner/cinematics/level1/level1.css';
import '@partner/cinematics/level1/office.css';

export function filmImages(metric) {
  return [...new Set([branches[metric].plate, officeBackground])];
}

// The partner's artwork, prop animation and script stay shared. This adapter owns
// player-facing shot assembly: one opaque scene at a time, with fixed framing.
function SpokenLine({ text, player = false, playerName }) {
  const color = SPEAKER_COLORS[player ? 'player' : 'alex'];
  return <div className="l1-spoken" data-speaker={player ? 'player' : 'alex'}>
    <p className="l1-speaker" style={{ color, textShadow: CAPTION_SHADOW }}>{player ? playerName?.trim() || 'You' : 'Alex'}</p>
    <DialogueLayer style={{ bottom: '7%', left: '10%', right: '10%', fontSize: '2.15cqw', lineHeight: 1.5, fontStyle: player ? 'italic' : 'normal', color, WebkitTextStroke: '.035em #172019', paintOrder: 'stroke fill', textShadow: CAPTION_SHADOW }}>{player ? teacherSpeech(text) : text}</DialogueLayer>
  </div>;
}

function OfficeEnding({ seconds, playerName, thoughtReady }) {
  const name = playerName?.trim();
  const thought = thoughtReady && seconds < 10.1 ? FIRST_THOUGHT
    : seconds >= 11.2 && seconds < 13.7 ? SECOND_THOUGHT
    : seconds >= 13.8 ? BRIDGE_LINE : null;
  return <div className="l1-office" aria-label="Your sunlit office">
    <div className="office-camera" style={{ scale: 2.65, translate: '62.275% -1.325%' }}>
      <Img className="office-background" src={officeBackground} alt="Your desk, laptop, plants and office door in warm afternoon light." />
      <div className="laptop-screen">
        <article className="email" aria-label="Email from University Management">
          <header className="mail-bar"><span aria-hidden="true">✉</span> University <span className="inbox-label">INBOX / 1</span></header>
          <div className="mail-content">
            <div className="sender"><span className="sender-seal" aria-hidden="true">U</span><div><small>From</small><strong>University Management</strong></div><time>Just now</time></div>
            <h2>{name ? `Great work, ${name}!` : 'Great work!'}</h2>
            <p>Student engagement has improved significantly!</p>
            <p className="l1-office-signature">University Management</p>
          </div>
        </article>
      </div>
    </div>
    {thought && <DialogueLayer style={{ fontSize: '2.05cqw', lineHeight: 1.6, fontStyle: 'italic', bottom: '8.2%', left: '10%', right: '10%', color: SPEAKER_COLORS.player, WebkitTextStroke: '.035em #172019', paintOrder: 'stroke fill', textShadow: CAPTION_SHADOW }}>{thought}</DialogueLayer>}
  </div>;
}

export function LevelOneFilm({ selectedMetric, playerName, seconds, reducedMotion, elapsed, pacing, finished }) {
  const branch = branches[selectedMetric];
  const officeStart = LEVEL1.branch + LEVEL1.common;
  const [phase, setPhase] = useState('branch');
  const [handoff, setHandoff] = useState('idle');
  const [emailReadyAt, setEmailReadyAt] = useState(null);
  const currentElapsed = useRef(elapsed);
  currentElapsed.current = elapsed;
  const surface = useRef(null);
  const transition = useRef(null);
  const started = useRef(false);
  useEffect(() => {
    if (seconds < SOURCE_TRANSITION_START || started.current) return;
    started.current = true;
    setHandoff('dissolving');
    transition.current = dissolveFrame(surface.current, () => setPhase('office'), { duration: SCENE_COVER_SECONDS * 1000, reducedMotion });
    transition.current.finished.then(() => { setEmailReadyAt(currentElapsed.current); setHandoff('done'); });
  }, [seconds, reducedMotion]);
  useEffect(() => () => transition.current?.cancel(), []);
  const text = seconds >= 2.2 && seconds < 5.3 ? branch.boast
    : seconds >= 5.5 && seconds < 8.2 ? branch.question
    : seconds >= 8.9 && seconds < 12.1 ? branch.reveal : null;
  return <AbsoluteFill ref={surface} className="l1-film" data-metric={selectedMetric} data-phase={phase} data-handoff={handoff} data-source-seconds={seconds.toFixed(3)}>
    <div className="l1-scene" key={phase} data-shot={phase}>
      {phase === 'branch' ? <>
        <ConsequenceScene metric={selectedMetric} seconds={Math.min(seconds, LEVEL1.branch)} reducedMotion={reducedMotion} />
        {text && <SpokenLine text={text} player={seconds >= 5.5 && seconds < 8.2} playerName={playerName} />}
      </> : <OfficeEnding seconds={seconds - officeStart} playerName={playerName} thoughtReady={emailReadyAt !== null && elapsed - emailReadyAt >= EMAIL_THOUGHT_DELAY} />}
    </div>
    <div className="l1-scene-cover" aria-hidden="true" style={{ position: 'absolute', inset: 0, background: '#111710', opacity: finished ? 1 : finalCoverOpacity(pacing, elapsed, reducedMotion), pointerEvents: 'none' }} />
  </AbsoluteFill>;
}
