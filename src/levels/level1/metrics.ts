export type MetricId = 'prep' | 'part' | 'focus' | 'discuss' | 'reflect' | 'peer';
export type SceneLine = { speaker: 'Alex' | 'Maya'; text: string };
export type Metric = {
  id: MetricId;
  name: string;
  shortName: string;
  description: string;
  example: string;
  before: number;
  after: number;
  improvement: string;
  uncertainty: string;
  evidence: string;
  studentQuote: string;
  learningLabel: string;
  takeaway: string;
  scene: SceneLine[];
};

// Illustrative scores, not measurements of real students. Stable across replays.
export const METRICS: Metric[] = [
  {
    id: 'prep', name: 'Pre-class Preparation', shortName: 'Preparation',
    description: 'Finish the preparation.',
    example: 'Students will arrive ready to discuss the reading.', before: 34, after: 88,
    improvement: 'More preparation tasks completed', uncertainty: 'Understanding still unclear',
    evidence: 'Students complete the preparation, but some skim just enough to meet the requirement.',
    studentQuote: 'Uh... I finished the checklist.',
    learningLabel: 'Understanding', takeaway: 'The checklist is complete. The ideas are unclear.',
    scene: [
      { speaker: 'Alex', text: 'I finished everything on the list!' },
      { speaker: 'Maya', text: 'What was the main idea in the reading?' },
      { speaker: 'Alex', text: 'Uh... I finished the checklist.' },
    ],
  },
  {
    id: 'part', name: 'In-class Participation', shortName: 'Participation',
    description: 'Speak up in class.',
    example: 'Students will contribute more thoughtful ideas.', before: 29, after: 85,
    improvement: 'More visible contributions', uncertainty: 'Depth still unclear',
    evidence: 'Students speak more often, but some contributions are brief or repetitive.',
    studentQuote: 'I just wanted to participate.',
    learningLabel: 'Depth', takeaway: 'More contributions. Little explanation.',
    scene: [
      { speaker: 'Alex', text: 'I agree! Same here!' },
      { speaker: 'Maya', text: 'Can you explain why?' },
      { speaker: 'Alex', text: 'I just wanted to participate.' },
    ],
  },
  {
    id: 'focus', name: 'On-task Focus', shortName: 'Focus',
    description: 'Stay on the task.',
    example: 'Students will think more deeply about the task.', before: 41, after: 91,
    improvement: 'More visible time on task', uncertainty: 'Thinking still unclear',
    evidence: 'Students stay visibly on task, but some focus on looking busy rather than thinking deeply.',
    studentQuote: 'I... kept the page open.',
    learningLabel: 'Thinking', takeaway: 'The page stayed open. The thinking is unclear.',
    scene: [
      { speaker: 'Alex', text: 'Look, I stayed on task the whole time!' },
      { speaker: 'Maya', text: 'What did you discover?' },
      { speaker: 'Alex', text: 'I... kept the page open.' },
    ],
  },
  {
    id: 'discuss', name: 'In-class Discussion Quality', shortName: 'Discussion',
    description: 'Develop ideas together.',
    example: 'Students will explore and develop ideas together.', before: 32, after: 84,
    improvement: 'More discussion criteria met', uncertainty: 'New ideas still unclear',
    evidence: 'Students use the discussion behaviours that earn credit, but some contributions become formulaic.',
    studentQuote: 'I followed the discussion checklist.',
    learningLabel: 'New ideas', takeaway: 'The right phrases. Few new ideas.',
    scene: [
      { speaker: 'Alex', text: "Could you elaborate? I’d like to build on that." },
      { speaker: 'Maya', text: 'What new idea came out of the discussion?' },
      { speaker: 'Alex', text: 'I followed the discussion checklist.' },
    ],
  },
  {
    id: 'reflect', name: 'Learning Reflection Quality', shortName: 'Reflection',
    description: 'Reflect on learning.',
    example: 'Students will reflect on what changed their thinking.', before: 38, after: 89,
    improvement: 'More structured reflections', uncertainty: 'Changed thinking still unclear',
    evidence: 'Reflections match the expected structure, but some students repeat the same safe patterns.',
    studentQuote: "That’s the format on the rubric.",
    learningLabel: 'Changed thinking', takeaway: 'A polished reflection. Changed thinking is unclear.',
    scene: [
      { speaker: 'Alex', text: 'Before, I thought... Now, I think...' },
      { speaker: 'Maya', text: 'What actually changed your mind?' },
      { speaker: 'Alex', text: "That’s the format on the rubric." },
    ],
  },
  {
    id: 'peer', name: 'Online Peer Response Quality', shortName: 'Peer response',
    description: 'Respond to classmates.',
    example: 'Students will engage with their classmates’ ideas.', before: 27, after: 86,
    improvement: 'More response criteria met', uncertainty: 'Exchange of ideas still unclear',
    evidence: 'Online replies become more specific, but some students learn a repeatable response formula.',
    studentQuote: 'I met every response criterion.',
    learningLabel: 'Real exchange', takeaway: 'The criteria are met. The exchange is unclear.',
    scene: [
      { speaker: 'Alex', text: 'Specific suggestion? Check. Follow-up question? Check!' },
      { speaker: 'Maya', text: 'Did you really discuss their ideas?' },
      { speaker: 'Alex', text: 'I met every response criterion.' },
    ],
  },
];

export function getMetric(id: MetricId | null) {
  return METRICS.find(metric => metric.id === id);
}
