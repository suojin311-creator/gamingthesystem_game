import React from 'react';
import { AbsoluteFill, Img } from 'remotion';
import { ConsequenceScene } from '@partner/cinematics/level1/ConsequenceScene';
import { DialogueLayer } from '@partner/cinematics/shared/engine/DialogueLayer/DialogueLayer';
import { branches, COMMON_LINE, FIRST_THOUGHT, SECOND_THOUGHT, BRIDGE_LINE, LEVEL1 } from '@partner/cinematics/level1/level1Content';
import officeBackground from '@partner-assets/backgrounds/BG_Office_FirstPerson_v01.png';
import '@partner/styles.css';
import '@partner/cinematics/level1/level1.css';
import '@partner/cinematics/level1/office.css';

export function filmImages(metric) {
  return [...new Set([branches[metric].plate, branches['in-class-participation'].plate, officeBackground])];
}

// The partner's artwork, prop animation and script stay shared. This adapter owns
// player-facing shot assembly: one opaque scene at a time, with fixed framing.
function SpokenLine({ text, player = false }) {
  return <div className="l1-spoken" data-speaker={player ? 'player' : 'alex'}>
    <div className="l1-dialogue-shade" aria-hidden="true" />
    <p className="l1-speaker">{player ? 'You' : 'Alex'}</p>
    <DialogueLayer style={{ bottom: '7%', left: '10%', right: '10%', fontSize: '2.15cqw', lineHeight: 1.5, fontStyle: player ? 'italic' : 'normal' }}>{text}</DialogueLayer>
  </div>;
}

function OfficeEnding({ metric, seconds, playerName }) {
  const name = playerName?.trim();
  const thought = seconds >= 7.1 && seconds < 10.1 ? FIRST_THOUGHT
    : seconds >= 11.2 && seconds < 13.7 ? SECOND_THOUGHT
    : seconds >= 13.8 ? BRIDGE_LINE : null;
  return <div className="l1-office" aria-label="Your sunlit office">
    <div className="office-camera" style={{ scale: 2.65, translate: '62.275% -1.325%' }}>
      <Img className="office-background" src={officeBackground} alt="Your desk, laptop, plants and office door in warm afternoon light." />
      <div className="laptop-screen">
        {seconds >= 1.4 && seconds < 2.3 && <div className="notification" role="status">
          <span className="envelope" aria-hidden="true">✉</span>
          <span><strong>University Management</strong><span className="notification-detail">New message <i aria-hidden="true" /></span><b>Great work!</b></span>
        </div>}
        {seconds >= 2.3 && <article className="email" aria-label="Email from University Management">
          <header className="mail-bar"><span aria-hidden="true">✉</span> University <span className="inbox-label">INBOX / 1</span></header>
          <div className="mail-content">
            <div className="sender"><span className="sender-seal" aria-hidden="true">U</span><div><small>From</small><strong>University Management</strong></div><time>Just now</time></div>
            <h2>{name ? `Great work, ${name}!` : 'Great work!'}</h2>
            <p>Student engagement has improved significantly!</p>
            <p className="l1-office-signature">University Management</p>
            {seconds >= 6 && <div className="l1-office-result" role="status">
              <small>Selected metric</small><strong>{branches[metric].label}</strong>
              <span><span aria-hidden="true">✓</span> TARGET ACHIEVED</span>
            </div>}
          </div>
        </article>}
      </div>
    </div>
    <div className="vignette" aria-hidden="true" />
    <div className="l1-office-thought-shade" aria-hidden="true" style={{ opacity: .65 }} />
    {thought && <DialogueLayer style={{ fontSize: '2.05cqw', lineHeight: 1.6, fontStyle: 'italic', bottom: '8.2%', left: '10%', right: '10%' }}>{thought}</DialogueLayer>}
  </div>;
}

export function LevelOneFilm({ selectedMetric, playerName, seconds, reducedMotion }) {
  const branch = branches[selectedMetric];
  const officeStart = LEVEL1.branch + LEVEL1.common;
  const phase = seconds < LEVEL1.branch ? 'branch' : seconds < officeStart ? 'common' : 'office';
  const text = seconds >= 2.2 && seconds < 5.3 ? branch.boast
    : seconds >= 5.5 && seconds < 8.2 ? branch.question
    : seconds >= 8.9 && seconds < 12.1 ? branch.reveal : null;
  return <AbsoluteFill className="l1-film" data-metric={selectedMetric} data-phase={phase} data-source-seconds={seconds.toFixed(3)}>
    <div className="l1-scene" key={phase} data-shot={phase}>
      {phase === 'branch' ? <>
        <ConsequenceScene metric={selectedMetric} seconds={seconds} reducedMotion={reducedMotion} />
        {text && <SpokenLine text={text} player={seconds >= 5.5 && seconds < 8.2} />}
      </> : phase === 'common' ? <>
        <Img className="l1-common-plate" src={branches['in-class-participation'].plate} alt="Alex, looking eagerly toward you in the classroom." />
        {seconds >= LEVEL1.branch + .15 && seconds < officeStart - .1 && <SpokenLine text={COMMON_LINE} />}
      </> : <OfficeEnding metric={selectedMetric} seconds={seconds - officeStart} playerName={playerName} />}
    </div>
  </AbsoluteFill>;
}
