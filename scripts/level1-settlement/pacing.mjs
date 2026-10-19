import { FIRST_THOUGHT, BRIDGE_LINE } from './content.mjs';

/** English reading holds at about 220 words/minute, plus a short settling margin. */
export function readingSeconds(text, minimum = 2.1) {
  return Math.max(minimum, (text.trim().match(/\S+/g)?.length ?? 0) * .27 + .4);
}
/** Keep source timings for retained shots; skip the common ending and office approach. */
export function createPacing(branch) {
  const segments = [
    [0, 2.2, .65],
    [2.2, 5.3, readingSeconds(branch.boast)],
    [5.3, 5.5, .15],
    [5.5, 8.2, readingSeconds(branch.question)],
    [8.2, 8.9, .30],
    [8.9, 12.1, readingSeconds(branch.reveal)],
    [12.1, 12.6, .45],
    // The complete email is present on the first office frame, under the cover.
    [18.9, 23.7, 4.10],
    // Keep reading holds; the presentation uses cuts instead of opacity ramps.
    [23.7, 24.25, .15],
    [24.25, 26.35, readingSeconds(FIRST_THOUGHT) - .3],
    [26.35, 26.7, .15],
    [26.7, 26.8, .10],
    [26.8, 27.7, .10],
    [27.7, 27.8, .10],
    [27.8, 28.3, .15],
    [28.3, 29.95, readingSeconds('Maybe one metric is too narrow.') - .3],
    [29.95, 30.3, .15],
    [30.3, 30.4, .10],
    [30.4, 31.1, .15],
    [31.1, 33.4, readingSeconds(BRIDGE_LINE)],
    [33.4, 33.4, .35], // Hold the final thought, then cover for the recap handoff.
  ];
  let duration = 0;
  const timeline = segments.map(([from, to, hold]) => {
    const start = duration;
    duration += hold;
    return { from, to, start, end: duration };
  });
  return {
    duration,
    timeline,
    sourceSeconds(seconds) {
      const segment = timeline.find(part => seconds <= part.end) ?? timeline[timeline.length - 1];
      const fraction = Math.max(0, Math.min(1, (seconds - segment.start) / (segment.end - segment.start)));
      return segment.from + (segment.to - segment.from) * fraction;
    },
  };
}
