import React from 'react';
import { ConsequenceScene } from '@ending/cinematics/level1/ConsequenceScene';
import { AlexCheckingSequence } from '@ending/cinematics/level2/AlexCheckingSequence';
import { MetricAdaptationScene } from '@level3a/cinematics/level3/MetricAdaptationScene';
import { METRICS, INTENSITIES } from '../../src/cinematics/level3/mapping.mjs';
import { METRIC_CATALOG } from '../../src/shared/data/metrics';
import { actualShotAt, RECAP, ease } from './timeline.mjs';

export function ActualTask({ input, time, opening = false, reducedMotion }) {
  const shot = actualShotAt(input, time, opening);
  // Stable, already-seen task pose. Never replay the peer-only/reaction inserts.
  const sourceTime = shot.metricId === 'part' ? 2.8 : shot.metricId === 'focus' && shot.effort === 'low' ? 1.4 : 3.99;
  return <div className="ending-actual-task" data-scene-id={shot.sceneId} data-round={input.lastRun.runs[0].round}>
    <MetricAdaptationScene metric={METRICS[shot.metricId]} intensity={INTENSITIES[shot.effort]} time={sourceTime} reducedMotion={reducedMotion} hideDialogue />
    <h2 className="ending-metric-name">{shot.label}</h2>
  </div>;
}

export function LevelMemory({ level, time, input, reducedMotion }) {
  if (level === 1) return <ConsequenceScene metric={METRICS[input.levelOneMetricId]} seconds={2.5} reducedMotion={reducedMotion} />;
  // A single useful, legible notebook view; omit checking portraits/cutaways.
  if (level === 2) return <AlexCheckingSequence elapsed={2.2} count={6} labels={METRIC_CATALOG.map(m => m.name)} progress={1} insertOnly reducedMotion={reducedMotion} />;
  return <ActualTask input={input} time={time} reducedMotion={reducedMotion} />;
}

export function SoloMemory({ level, time, input, reducedMotion }) {
  return <div className="end-memory-space">
    <div className="end-solo-memory"><LevelMemory {...{ level, time, input, reducedMotion }} /></div>
    <div className="end-memory-caption"><span>LEVEL {level}</span><p>{RECAP[level - 1]}</p></div>
  </div>;
}

export function Convergence({ time, input, reducedMotion }) {
  return <div className="end-memory-space end-convergence">
    <div className="end-thread-light" style={{ opacity: .2 + ease(time, .1, 1.2) * .3 }} />
    {[1, 2, 3].map(level => <div key={level} className={`end-floating-memory end-floating-${level}`}>
      <LevelMemory {...{ level, time: 2.8, input, reducedMotion }} />
    </div>)}
  </div>;
}
