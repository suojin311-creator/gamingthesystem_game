export type Weights = readonly [number, number, number];
export type Confirmed = readonly [boolean, boolean, boolean];
export type WeightGoal = 'first' | 'different';
export type Effort = 'low' | 'medium' | 'high';
export const EVEN_WEIGHTS: Weights = [34, 33, 33];
export const CONTRAST_WEIGHTS: Weights = [70, 20, 10];
export const MIN_WEIGHT = 1;
export const MAX_WEIGHT = 100 - MIN_WEIGHT * 2;
export const NEAR_EVEN_SPREAD = 10;

export const spread = (weights: Weights) => Math.max(...weights) - Math.min(...weights);
export const isNearEven = (weights: Weights) => spread(weights) <= NEAR_EVEN_SPREAD;
export const validWeights = (weights: Weights) => weights.length === 3 && weights.every(value => Number.isInteger(value) && value >= MIN_WEIGHT && value <= MAX_WEIGHT) && weights.reduce((sum, value) => sum + value, 0) === 100;

/** Integer percentages keep the total exact; a one-point remainder goes in card order. */
export function allocateWeight(weights: Weights, confirmed: Confirmed, index: number, requested: number): Weights {
  if (!Number.isInteger(index) || index < 0 || index > 2 || confirmed[index] || !Number.isFinite(requested)) return weights;
  const others = [0, 1, 2].filter(i => i !== index && !confirmed[i]);
  if (!others.length) return weights;
  const lockedTotal = weights.reduce((sum, value, i) => sum + (confirmed[i] ? value : 0), 0);
  const value = Math.max(MIN_WEIGHT, Math.min(100 - lockedTotal - MIN_WEIGHT * others.length, Math.round(requested)));
  const next: [number, number, number] = [...weights];
  next[index] = value;
  const remaining = 100 - lockedTotal - value;
  others.forEach((i, position) => { next[i] = Math.floor(remaining / others.length) + (position < remaining % others.length ? 1 : 0); });
  return next;
}

export function maximumWeight(weights: Weights, confirmed: Confirmed, index: number) {
  if (confirmed[index]) return weights[index];
  return 100 - weights.reduce((sum, value, i) => sum + (confirmed[i] ? value : 0), 0)
    - MIN_WEIGHT * confirmed.filter((locked, i) => !locked && i !== index).length;
}

/** Either of the final two cards confirms their complete remaining split. */
export function confirmWeight(confirmed: Confirmed, index: number): Confirmed {
  if (!Number.isInteger(index) || index < 0 || index > 2 || confirmed[index]) return confirmed;
  const unlocked = confirmed.filter(locked => !locked).length;
  if (unlocked <= 2) return [true, true, true];
  const next: [boolean, boolean, boolean] = [...confirmed];
  next[index] = true;
  return next;
}

export function goalMet(weights: Weights, baseline: Weights, goal: WeightGoal) {
  return goal === 'first' || weights.some((weight, index) => weight !== baseline[index]);
}

export function canRun(weights: Weights, confirmed: Confirmed, baseline: Weights, goal: WeightGoal) {
  return validWeights(weights) && confirmed.length === 3 && confirmed.every(Boolean) && goalMet(weights, baseline, goal);
}

export function effortAt(weights: Weights, index: number): Effort {
  // Narrative V2: near-even overrides the absolute thresholds for all three shots.
  return isNearEven(weights) ? 'medium' : weights[index] < 34 ? 'low' : weights[index] < 67 ? 'medium' : 'high';
}
