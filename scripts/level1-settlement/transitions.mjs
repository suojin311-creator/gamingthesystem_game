/** Keep photos opaque; change shots only under a short, solid-colour cover. */
export function clockAtSource(pacing, source) {
  const segment = pacing.timeline.find(part => source <= part.to) ?? pacing.timeline.at(-1);
  if (segment.to === segment.from) return segment.start;
  return segment.start + (segment.end - segment.start) * (source - segment.from) / (segment.to - segment.from);
}
const ease = value => { const x = Math.max(0, Math.min(1, value)); return x * x * (3 - 2 * x); };
export function sceneCoverOpacity(pacing, elapsed, reducedMotion = false) {
  const half = reducedMotion ? .06 : .16;
  const fullyCovered = .04;
  let opacity = 0;
  for (const source of [12.6, 16.6]) {
    const distance = Math.abs(elapsed - clockAtSource(pacing, source));
    opacity = Math.max(opacity, 1 - ease((distance - fullyCovered) / (half - fullyCovered)));
  }
  // Reach full cover before the actual ended event hands off to the recap.
  const closing = reducedMotion ? .12 : .15;
  return Math.max(opacity, ease((elapsed - (pacing.duration - closing)) / (closing - .10)));
}
