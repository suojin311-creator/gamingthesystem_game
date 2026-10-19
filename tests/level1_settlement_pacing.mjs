import assert from 'node:assert/strict';
import { createPacing } from '../scripts/level1-settlement/pacing.mjs';
// Authored dialogue from the pinned partner delivery, not the game-side recap.
const samples = [
 ['prep','I finished everything on the list!','What was the main idea in the reading?','Uh... I finished the checklist.'],
 ['part','I agree! Same here!','Can you explain why?','I just wanted to participate.'],
 ['focus','Look, I stayed on task the whole time!','What did you discover?','I... kept the page open.'],
 ['discuss','Could you elaborate? I’d like to build on that.','What new idea came out of the discussion?','I followed the discussion checklist.'],
 ['reflect','Before, I thought... Now, I think...','What actually changed your mind?','That’s the format on the rubric.'],
 ['peer','Specific suggestion? Check. Follow-up question? Check!','Did you really discuss their ideas?','I met every response criterion.'],
];
function clockAt(pacing, source) {
  const segment = pacing.timeline.find(part => source <= part.to) ?? pacing.timeline.at(-1);
  return segment.start + (segment.end - segment.start) * (source - segment.from) / (segment.to - segment.from);
}
const wordCount = text => text.trim().split(/\s+/).length;
for (const [id, boast, question, reveal] of samples) {
  const pacing = createPacing({boast, question, reveal});
  assert(pacing.duration > 24 && pacing.duration < 28, id + ': useful overall reduction');
  assert.equal(pacing.sourceSeconds(0), 0);
  assert.equal(pacing.sourceSeconds(pacing.duration), 33.4);
  let prior = -1;
  for (let frame = 0; frame <= Math.ceil(pacing.duration * 30); frame++) {
    const source = pacing.sourceSeconds(frame / 30);
    assert(source >= prior && source <= 33.4, id + ': uninterrupted monotonic source clock');
    prior = source;
  }
  for (const [start, end, text] of [[2.2,5.3,boast],[5.5,8.2,question],[8.9,12.1,reveal],[12.75,16.5,'Professor! I figured out exactly what you were looking for!']]) {
    assert(clockAt(pacing,end)-clockAt(pacing,start) >= wordCount(text)*.25+.25, id+': reading time for '+text);
  }
  assert(clockAt(pacing,23.7)-clockAt(pacing,23.2) >= 2.4-1e-8, id+': fully visible target result');
  assert(clockAt(pacing,26.35)-clockAt(pacing,24.25) >= 2.4, id+': clear first thought');
  assert(clockAt(pacing,29.95)-clockAt(pacing,28.3) >= 1.7, id+': clear second thought');
  assert(clockAt(pacing,27.7)-clockAt(pacing,26.8) <= .11, id+': removed memory no longer causes a lingering empty beat');
  console.log('PASS',id,pacing.duration.toFixed(2)+'s: full source coverage, readable lines and target result');
}
