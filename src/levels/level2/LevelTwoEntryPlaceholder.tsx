import './styles.css';
import Icon from '../../shared/components/Icon';

/** Reserved for the future Level 2 host. Never mounted by LevelOne. */
export default function LevelTwoEntryPlaceholder({ onReview, onRestart }: {
  onReview?: () => void;
  onRestart?: () => void;
}) {
  return <section className="level-two-entry" aria-label="Level 2 entry placeholder">
    <div className="completion-seal"><Icon name="check" /><span>LEVEL 1 COMPLETE</span></div>
    <div className="section-intro completion-intro"><h2>What if we measured<br /><em>more than one?</em></h2></div>
    <div className="next-chapter"><span className="chapter-number">02</span><div><span className="eyebrow">NEXT</span><h3>More metrics.</h3></div><span className="coming-label">Coming next</span></div>
    <p className="eyebrow">Maybe one metric is too narrow.</p>
    {(onReview || onRestart) && <div className="action-row">
      {onReview && <button className="back-button" onClick={onReview}>← Review this experiment</button>}
      {onRestart && <button className="button secondary-button" onClick={onRestart}>Try another metric<Icon name="restart" /></button>}
    </div>}
  </section>;
}
