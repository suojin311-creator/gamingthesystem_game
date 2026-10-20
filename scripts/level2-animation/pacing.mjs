// The approved Level 1 English-reading rule, applied only to retained dialogue.
export const readingSeconds = text => Math.max(2.1, text.trim().split(/\s+/).length * .27 + .4);
export const COVER_SECONDS = .28;

export function createPacing(kind, shots) {
  const timeline = [];
  let duration = 0;
  const add = (from, to, hold, dialogue = null) => {
    timeline.push({ from, to, start: duration, end: duration + hold, dialogue });
    duration += hold;
  };
  const offsets = new Map();
  let source = 0;
  for (const shot of shots) { offsets.set(shot.id, source); source += shot.duration; }
  const id = kind === 'three' ? 'three-checklist' : kind === 'six' ? 'six-checklist' : kind === 'checklist' ? 'reflection' : null;
  const shot = shots.find(item => item.id === id);
  if (!shot?.dialogue?.length) throw new Error('A supported placeholder scene with authored dialogue is required.');
  if (kind === 'three' && shot.dialogue[0].text !== 'I’ve completed all three requirements!') throw new Error('Review the partner three-metric opening before trimming.');
  if (kind === 'six') add(0, shot.dialogue[0].start, .25);
  if (kind === 'checklist') add(1.6, 5.25, 1.2); // Brief satisfied reaction, after the game's 100-item growth.
  const offset = offsets.get(id);
  for (let i = 0; i < shot.dialogue.length; i++) {
    const line = shot.dialogue[i];
    add(offset + line.start, offset + line.end, readingSeconds(line.text), line);
    const next = shot.dialogue[i + 1];
    if (next) add(offset + line.end, offset + next.start, .15);
  }
  const last = shot.dialogue.at(-1);
  add(offset + last.end, offset + Math.min(shot.duration - .01, last.end + .2), .35);
  return { kind, duration, timeline };
}

export function sampleAt(pacing, elapsed) {
  const time = Math.max(0, Math.min(pacing.duration, elapsed));
  const part = pacing.timeline.find(item => time < item.end) ?? pacing.timeline.at(-1);
  const fraction = Math.max(0, Math.min(1, (time - part.start) / (part.end - part.start)));
  return { sourceSeconds: part.from + (part.to - part.from) * fraction, dialogue: part.dialogue };
}

export function finalCover(pacing, elapsed) {
  const t = Math.max(0, Math.min(1, (elapsed - (pacing.duration - .15)) / .1));
  return t * t * (3 - 2 * t);
}
