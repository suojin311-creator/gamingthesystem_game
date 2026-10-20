import React from 'react';
import { OfficeReveal } from '@ending/cinematics/ending/OfficeReveal';
import '@ending/cinematics/ending/ending.css';
import { SPEAKER_COLORS, CAPTION_SHADOW } from '../../src/shared/data/cinematicPalette.js';
import { ActualTask, SoloMemory, Convergence } from './Memories';
import { BUTTON_AT, ease, lineAt, sectionAt } from './timeline.mjs';
import './film.css';

export default function Composition({ input, time, reducedMotion, surface }) {
  const section = sectionAt(time), local = time - section.start, line = lineAt(time);
  const memoryLevel = Number(section.id.slice(-1));
  return <main ref={surface} className="end-stage ending-adapted" data-section={section.id} data-elapsed={time.toFixed(3)}>
    {section.id === 'opening' && <ActualTask {...{ input, time: local, reducedMotion }} opening />}
    {['level1', 'level2', 'level3'].includes(section.id) && <SoloMemory {...{ input, reducedMotion, time: local }} level={memoryLevel} />}
    {section.id === 'convergence' && <Convergence {...{ input, reducedMotion, time: local }} />}
    {time >= 25.4 && <OfficeReveal input={input} reducedMotion={reducedMotion} seconds={time + 9.8} />}
    {line && <div className="ending-spoken" style={{ color: SPEAKER_COLORS[line.role], textShadow: CAPTION_SHADOW, opacity: ease(time, line.start, .16) }}>
      <p className="ending-speaker">{line.speaker}</p><p role="status">{line.text}</p>
    </div>}
    <div className="end-film-vignette" aria-hidden="true" />
    {time >= BUTTON_AT && <button type="button" className="ending-design-button" aria-disabled="true" style={{ opacity: ease(time, BUTTON_AT, .9), transform: `translateY(${(1 - ease(time, BUTTON_AT, .9)) * 10}px)` }}>Go to Design Lab <span aria-hidden="true">→</span></button>}
  </main>;
}
