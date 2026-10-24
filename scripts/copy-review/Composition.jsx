import React from 'react';
import { OfficeReveal } from '@ending/cinematics/ending/OfficeReveal';
import '@ending/cinematics/ending/ending.css';
import '../../src/cinematics/opening/styles.css';
import { SPEAKER_COLORS, CAPTION_SHADOW } from '../../src/shared/data/cinematicPalette.js';
import { SoloMemory } from './Memories';
import { HANDOFF_COPY, ease, lineAt, officeSeconds, sectionAt } from './timeline.mjs';
import './film.css';

export default function Composition({ input, time, reducedMotion, surface, onEnterLab }) {
  const section = sectionAt(time), local = time - section.start, line = lineAt(time);
  const memoryLevel = Number(section.id.slice(-1));
  const reflection = line?.id === 'reflection';
  return <main ref={surface} className="end-stage ending-adapted" data-section={section.id} data-elapsed={time.toFixed(3)} style={{'--handoff-night':.94-.39*ease(time,29.7,.85),'--thought-night':.94-.26*ease(time,16.5,.9)}}>
    {['level1', 'level2', 'level3'].includes(section.id) && <SoloMemory {...{ input, reducedMotion, time: local }} level={memoryLevel} />}
    {(section.id === 'opening' || time >= 10.1) && <OfficeReveal input={input} reducedMotion={reducedMotion} seconds={officeSeconds(time)} />}
    {time < .45 && <div className="ending-entry-shade" style={{opacity:1-ease(time,0,.45)}} aria-hidden="true" />}
    {reflection && <div className="ending-reflection-shade" aria-hidden="true" style={{opacity:ease(time,10.1,.6)*(1-ease(time,14.5,2))}} />}
    {line && <div className={`ending-spoken${reflection ? ' ending-reflection' : ''}`} style={{ color: reflection ? '#fff5e3' : SPEAKER_COLORS[line.role], textShadow: CAPTION_SHADOW, opacity: ease(time, line.start, reflection ? .6 : .16) * (reflection ? 1-ease(time,14.5,2) : 1) }}>
      {!reflection && <p className="ending-speaker">{line.speaker}</p>}<p role="status">{reflection ? <><span className="ending-question-line">Am I improving <strong className="ending-learning">learning</strong>,</span><span className="ending-question-line">or just improving the <strong className="ending-numbers">numbers</strong>?</span></> : line.text}</p>
    </div>}
    {['principle','assessment'].includes(section.id) && <section className={`ending-thought ending-thought-${section.id}`} aria-label={section.title} style={{opacity:ease(time,section.start,.75)*(1-ease(time,section.end-.65,.65))}}>
      <p>{section.id === 'principle' ? <><span>When a number <strong className="thought-becomes">becomes</strong> a measure,</span><span>it <strong className="thought-ceases">ceases</strong> to be a good measure.</span></> : <><span className="thought-assessment-opening">Your assessment doesn’t just measure learning,</span><span className="thought-conclusion">it shapes how students learn.</span></>}</p>
    </section>}
    {section.id === 'closing' && <section className="ending-handoff" aria-labelledby="ending-next-title" style={{opacity:ease(time,29.7,.85)}}>
      <div className="ending-handoff-copy">
        <p className="ending-destination">{HANDOFF_COPY.destination}</p>
        <h1 id="ending-next-title">{HANDOFF_COPY.title.map(text=><span key={text}>{text}</span>)}</h1>
        <div className="ending-handoff-action opening-scene"><button type="button" className="opening-action ending-design-button" aria-disabled={!onEnterLab} onClick={onEnterLab}>ENTER DESIGN LAB <span aria-hidden="true">→</span></button></div>
      </div>
    </section>}
    <div className="end-film-vignette" aria-hidden="true" />
  </main>;
}
