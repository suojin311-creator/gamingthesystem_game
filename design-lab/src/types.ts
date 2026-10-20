export type Phase = 'lobby' | 'writing' | 'review' | 'ranking' | 'question1' | 'question2' | 'ending' | 'empty' | 'closed';
export type Choice = 'flower' | 'bomb';
export type ReflectionCard = { id: string; label: string; text: string; vote: Choice | '' };
export type Ranked = { id: string; label: string; text: string; flowers: number; rank: number };
export type Snapshot = {
  revision: number; sessionId: string; phase: Phase; now: number; startedAt: number; deadline: number;
  joined: number; submitted: number; audienceCount: number; reflectionCount: number; finishedCount: number;
  writingMs: number; rankingMs: number; participantId?: string; hasSubmitted: boolean;
  isAudience: boolean; cursor: number; reviewTotal: number; finished: boolean; card: ReflectionCard | null;
  ranking: Ranked[]; joinUrls?: string[];
};
