export const DURATION = 24;
export const BUTTON_AT = 18.5;
export const SECTIONS = [
  { id: 'opening', start: 0, end: 3.8, title: 'Office reflection' },
  { id: 'level1', start: 3.8, end: 5.9, title: 'Level 1 memory' },
  { id: 'level2', start: 5.9, end: 8, title: 'Level 2 memory' },
  { id: 'level3', start: 8, end: 10.1, title: 'Level 3 memory' },
  { id: 'question', start: 10.1, end: 14.5, title: 'The question' },
  { id: 'threshold', start: 14.5, end: 16.5, title: 'Closing transition' },
  { id: 'closing', start: 16.5, end: DURATION, title: 'Your next step · Design Lab' },
];
export const RECAP = ['One metric became the target.', 'More metrics became a checklist.', 'The weights changed. Learning still came second.'];
export const HANDOFF_COPY = {
  destination: 'NEXT · DESIGN LAB',
  title: ['Share what real', 'learning looks like.'],
  context: 'You’ve seen how numbers shaped Alex’s choices.',
  task: 'Now write a short reflection, then read and vote on your classmates’ ideas.',
};
export const LINES = [
  { start: .15, end: 3.8, speaker: 'You', role: 'player', text: 'Maybe it’s not just about finding the perfect weights…' },
  { start: 10.1, end: 14.5, speaker: 'You', role: 'player', text: 'Am I improving learning, or just improving the numbers?' },
];
export const sectionAt = time => SECTIONS.find(s => time < s.end) ?? SECTIONS.at(-1);
export const lineAt = time => LINES.find(line => time >= line.start && time < line.end);
export const ease = (time, start, duration) => { const t = Math.max(0, Math.min(1, (time - start) / duration)); return t * t * (3 - 2 * t); };

// One short action from the player's last trial, never a fabricated comparison.
export const actualShotAt = input => input.lastRun.shots.at(-1);
export function officeSeconds(time) {
  if (time < 3.8) return 31 + time;
  if (time < 14.5) return 35.2 + time - 10.1;
  if (time < 16.5) return 40.2 + (time - 14.5) * 1.4;
  return 43 + time - 16.5;
}
