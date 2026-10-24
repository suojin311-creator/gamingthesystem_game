import React from 'react';
import {createRoot} from 'react-dom/client';
import {ResultChart} from '../../src/levels/level1/LevelOne';
import {getMetric} from '../../src/levels/level1/metrics';
import Icon from '../../src/shared/components/Icon';
import '../../src/shared/styles/base.css';
import './review.css';
createRoot(document.getElementById('root')!).render(<main className="level-one assessment-review">
 <div className="section-intro"><h2>Percentage of students meeting the criteria</h2></div>
 <section className="assessment-card">
 <ResultChart metric={getMetric('part')!} ready score={85} assessmentReport />
 <div className="assessment-bridge"><p>Learning performance looks better. Management is satisfied. <strong>But…</strong></p></div>
 </section>
 <div className="action-row"><button type="button" className="button primary-button"><Icon name="play"/>Look behind the result</button></div>
</main>);
