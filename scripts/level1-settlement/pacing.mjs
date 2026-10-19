/** English reading holds at about 220 words/minute, plus a short settling margin. */
export function readingSeconds(text, minimum = 2.1) {
  return Math.max(minimum, (text.trim().match(/\S+/g)?.length ?? 0) * .27 + .4);
}
/** Map a shorter review clock onto the original unmodified composition clock. */
export function createPacing(branch) {
  const segments = [
    [0, 2.2, .65],
    [2.2, 5.3, readingSeconds(branch.boast)],
    [5.3, 5.5, .15],
    [5.5, 8.2, readingSeconds(branch.question)],
    [8.2, 8.9, .30],
    [8.9, 12.1, readingSeconds(branch.reveal)],
    [12.1, 12.6, .20],
    [12.6, 12.75, .15],
    [12.75, 16.5, readingSeconds('Professor! I figured out exactly what you were looking for!')],
    [16.5, 16.6, .10],
    [16.6, 18.0, .65],
    [18.0, 18.9, .60],
    [18.9, 19.85, .65],
    [19.85, 22.6, 1.65],
    [22.6, 23.2, .20],
    [23.2, 23.7, 2.40],
    // Keep reading holds; the presentation uses cuts instead of opacity ramps.
    [23.7, 24.25, .15],
    [24.25, 26.35, readingSeconds('The numbers look great... but something still feels wrong.') - .3],
    [26.35, 26.7, .15],
    [26.7, 26.8, .10],
    [26.8, 27.7, .10],
    [27.7, 27.8, .10],
    [27.8, 28.3, .15],
    [28.3, 29.95, readingSeconds('Maybe one metric is too narrow.') - .3],
    [29.95, 30.3, .15],
    [30.3, 30.4, .10],
    [30.4, 31.1, .15],
    [31.1, 33.4, readingSeconds('What if we measured more than one?')],
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
