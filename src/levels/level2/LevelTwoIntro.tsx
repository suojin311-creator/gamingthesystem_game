import Icon from '../../shared/components/Icon';
import Conversation from '../../shared/components/Conversation';
import type { Cue } from '../../shared/hooks/useFeedback';

export default function LevelTwoIntro({ playerName, previousMetricName, onStart, paused, play }: {
  playerName: string; previousMetricName?: string; onStart: () => void;
  paused: boolean; play: (cue: Cue) => void;
}) {
  return <section className="l2-intro" aria-labelledby="l2-intro-title">
    <span className="eyebrow">A WIDER VIEW</span>
    <h2 id="l2-intro-title" tabIndex={-1}>What if we measured<br /><em>more than one?</em></h2>
    {previousMetricName && <p className="l2-previous">Previously tracked: {previousMetricName}</p>}
    <div className="l2-empty-slots" aria-label="Three metrics to choose">{[1, 2, 3].map(number => <div key={number}><span className="eyebrow">METRIC {number}</span><Icon name="spark" /><span>Your choice</span></div>)}</div>
    <Conversation lines={[{ speaker: 'Maya', name: playerName, text: 'One metric wasn’t enough. What if we tracked three?' }]} paused={paused} play={play} onSettled={() => {}} />
    <div className="action-row"><span className="l2-small-note">Choose three from the same six metrics.</span><button className="button primary-button" onClick={onStart}>Choose three metrics<Icon name="arrow" /></button></div>
  </section>;
}
