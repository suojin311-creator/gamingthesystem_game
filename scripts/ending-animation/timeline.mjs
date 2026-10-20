export const DURATION = 40.2;
export const BUTTON_AT = 37.8;
export const SECTIONS = [
  { id: 'opening', start: 0, end: 11.4, title: 'Opening' },
  { id: 'level1', start: 11.4, end: 14.6, title: 'Level 1 memory' },
  { id: 'level2', start: 14.6, end: 18.2, title: 'Level 2 memory' },
  { id: 'level3', start: 18.2, end: 21.8, title: 'Level 3 memory' },
  { id: 'convergence', start: 21.8, end: 25.4, title: 'Three memories' },
  { id: 'office', start: 25.4, end: 25.7, title: 'Office' },
  { id: 'question', start: 25.7, end: 30.4, title: 'The question' },
  { id: 'threshold', start: 30.4, end: 33.2, title: 'Theory reveal' },
  { id: 'theory', start: 33.2, end: DURATION, title: 'Goodhart’s Law' },
];
export const RECAP = ['One metric became the target.', 'More metrics became a checklist.', 'Scoring still guided the work.'];
export const LINES = [
  { start: .2, end: 4.4, speaker: 'You', role: 'player', text: 'Did changing the weights change why you were working?' },
  { start: 4.4, end: 7.7, speaker: 'Alex', role: 'alex', text: 'I was still working out what earns marks.' },
  { start: 7.7, end: 11.4, speaker: 'You', role: 'player', text: 'Maybe it’s not just about finding the perfect weights…' },
  { start: 25.7, end: 30.4, speaker: 'You', role: 'player', text: 'Am I improving learning, or just improving the numbers?' },
];
export const sectionAt = time => SECTIONS.find(s => time < s.end) ?? SECTIONS.at(-1);
export const lineAt = time => LINES.find(line => time >= line.start && time < line.end);
export const ease = (time, start, duration) => { const t = Math.max(0, Math.min(1, (time - start) / duration)); return t * t * (3 - 2 * t); };

// Reuse only the last real trial. No result is constructed by the film.
export function actualShotAt(input, time, opening = false) {
  const shots = input.lastRun.shots;
  // Hold the final task throughout the short conversation: no filler cuts.
  if (opening) return shots.at(-1);
  return shots[Math.min(shots.length - 1, Math.floor(Math.max(0, time) / 1.2))];
}
