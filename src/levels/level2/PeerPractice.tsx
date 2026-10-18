import CharacterPortrait from '../../shared/components/CharacterPortrait';

export default function PeerPractice({ beat }: { beat: number }) {
  return <figure className="l2-peer-practice" data-beat={beat} aria-label={beat === 0 ? 'Alex shares a phrase card that earns a discussion tick.' : beat === 1 ? 'A classmate copies the phrase, then asks about the idea.' : 'Both students follow the scoring sheet; their question about the idea remains unanswered.'}>
    <div className="l2-peer-person"><span className="l2-peer-portrait"><CharacterPortrait role="student" /></span><span>Alex</span></div>
    <div className="l2-peer-desk">
      <div className="l2-phrase-card"><span>DISCUSSION</span><strong>“I agree<br />because…”</strong><i>{beat === 0 ? '→' : '✓'}</i></div>
      <div className="l2-content-question" data-active={beat > 0}>Why?</div>
      {beat > 0 && <div className="l2-phrase-copy" aria-hidden="true">“I agree<br />because…”{beat === 2 && <b>✓</b>}</div>}
      {beat === 2 && <div className="l2-shared-tick" aria-hidden="true">✓</div>}
    </div>
    <div className="l2-peer-person"><span className="l2-peer-portrait classmate"><CharacterPortrait role="student" /></span><span>Classmate</span></div>
  </figure>;
}
