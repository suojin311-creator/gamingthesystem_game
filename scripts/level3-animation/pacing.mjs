// Source windows are editorial decisions only; no effort/weight rules live here.
export function windowsFor(metric, intensity) {
  if (metric === 'in-class-discussion-quality') return [[.8, 3.99]]; // No peer-only opening.
  if (metric === 'in-class-participation') {
    if (intensity === 'High') return [[.45, 1.999], [2.45, 3.99]]; // No classmate reaction.
    if (intensity === 'Medium') return [[.75, 2.349], [3.05, 3.99]];
    return [[0, .45], [2.65, 3.99]]; // Brief inaction, then the occasional contribution.
  }
  if (metric === 'on-task-focus') return intensity === 'Low' ? [[.75, 2.3]] : [[.65, 3.99]];
  return [[.65, 3.99]]; // Begin on the task, rather than an establishing insert.
}
export function createPacing(clips) {
  let time = 0;
  const timeline = clips.map((clip, index) => {
    const duration = Math.max(4.2, (clip.caption?.trim().split(/\s+/).length ?? 0) * .27 + .8);
    const item = { ...clip, index, start: time, end: time + duration, windows: windowsFor(clip.metric, clip.intensity) };
    time += duration;
    return item;
  });
  return { timeline, duration: time + .45 };
}
export function sampleAt(pacing, elapsed) {
  const clip = pacing.timeline.find(item => elapsed < item.end) ?? pacing.timeline.at(-1);
  const fraction = Math.max(0, Math.min(1, (elapsed - clip.start) / (clip.end - clip.start)));
  const total = clip.windows.reduce((sum, [from, to]) => sum + to - from, 0);
  let offset = fraction * total;
  for (const [from, to] of clip.windows) {
    if (offset <= to - from) return { ...clip, sourceTime: from + offset };
    offset -= to - from;
  }
  return { ...clip, sourceTime: clip.windows.at(-1)[1] };
}
export function poseKey(sample, participationBeat) {
  const { metric, intensity, sourceTime: time } = sample;
  const pose = metric === 'in-class-participation' ? intensity === 'Low' && participationBeat(intensity, time) === 'listen' ? 'listen' : 'contribute'
    : metric === 'on-task-focus' && intensity === 'Low' ? time < 1.85 ? 'phone' : 'task' : 'task';
  return `${sample.index}:${metric}:${intensity}:${pose}`;
}
