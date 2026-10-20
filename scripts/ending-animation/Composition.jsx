import React from 'react';
import { OfficeReveal } from '@ending/cinematics/ending/OfficeReveal';
import '@ending/cinematics/ending/ending.css';
import '../../src/cinematics/opening/styles.css';
import { SPEAKER_COLORS, CAPTION_SHADOW } from '../../src/shared/data/cinematicPalette.js';
import { SoloMemory } from './Memories';
import { BUTTON_AT, CLOSING_LINES, ease, lineAt, officeSeconds, sectionAt } from './timeline.mjs';
import './film.css';

export default function Composition({ input, time, reducedMotion, surface }) {
  const section = sectionAt(time), local = time - section.start, line = lineAt(time);
  const memoryLevel = Number(section.id.slice(-1));
  return <main ref={surface} className="end-stage ending-adapted" data-section={section.id} data-elapsed={time.toFixed(3)}>
    {['level1', 'level2', 'level3'].includes(section.id) && <SoloMemory {...{ input, reducedMotion, time: local }} level={memoryLevel} />}
    {(section.id === 'opening' || time >= 10.1) && <OfficeReveal input={input} reducedMotion={reducedMotion} seconds={officeSeconds(time)} />}
    {time < .45 && <div className="ending-entry-shade" style={{opacity:1-ease(time,0,.45)}} aria-hidden="true" />}
    {line && <div className="ending-spoken" style={{ color: SPEAKER_COLORS[line.role], textShadow: CAPTION_SHADOW, opacity: ease(time, line.start, .16) }}>
      <p className="ending-speaker">{line.speaker}</p><p role="status">{line.text}</p>
    </div>}
    {section.id === 'closing' && <section className="ending-closing" aria-label="Closing reflection" style={{opacity:ease(time,16.75,1.1)}}>
      <span className="ending-closing-rule" aria-hidden="true" />
      <p>{CLOSING_LINES.map(text=><span className="ending-closing-line" key={text}>{text}</span>)}</p>
    </section>}
    <div className="end-film-vignette" aria-hidden="true" />
    {time >= BUTTON_AT && <div className="ending-action-frame opening-scene" style={{ opacity: ease(time, BUTTON_AT, .9), transform: `translateY(${(1 - ease(time, BUTTON_AT, .9)) * 10}px)` }}><button type="button" className="opening-action ending-design-button" aria-disabled="true">ENTER DESIGN LAB <span aria-hidden="true">→</span></button></div>}
  </main>;
}
