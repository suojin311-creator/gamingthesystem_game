// Scene changes wait for the live CSS cover's transitionend, then two painted
// frames before uncovering. Source-clock jumps cannot bypass the solid cover.
export const SCENE_COVER_SECONDS = .28;
export const SOURCE_TRANSITION_START = 12.25;

export function clockAtSource(pacing, source) {
  const segment = pacing.timeline.find(part => source <= part.to) ?? pacing.timeline.at(-1);
  if (segment.to === segment.from) return segment.start;
  return segment.start + (segment.end - segment.start) * (source - segment.from) / (segment.to - segment.from);
}
const ease = value => { const x = Math.max(0, Math.min(1, value)); return x * x * (3 - 2 * x); };
export function finalCoverOpacity(pacing, elapsed, reducedMotion = false) {
  // Reach full cover before the actual ended event hands off to the recap.
  const closing = reducedMotion ? .12 : .15;
  return ease((elapsed - (pacing.duration - closing)) / (closing - .10));
}
