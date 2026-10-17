import assert from 'node:assert/strict';
import { mkdirSync, writeFileSync } from 'node:fs';
import { allocateWeight, canRun, effortAt, goalMet, isNearEven, maximumWeight, spread, validWeights } from '../src/levels/level3/weights.ts';

const checks = [];
const check = (name, run) => { run(); checks.push(name); console.log('PASS', name); };
check('Every possible integer split preserves total 100, minimum 10 and deterministic effort', () => {
  for (let a = 10; a <= 80; a++) for (let b = 10; b <= 90 - a; b++) {
    const weights = [a, b, 100 - a - b];
    assert.ok(validWeights(weights));
    assert.ok(!isNearEven(weights) || weights.every((_, i) => effortAt(weights, i) === 'medium'));
    for (let index = 0; index < 3; index++) for (const requested of [0, 10, 33, 34, 50, 67, 80, 100]) {
      const next = allocateWeight(weights, [false, false, false], index, requested);
      assert.ok(validWeights(next));
      const others = next.filter((_, i) => i !== index);
      assert.ok(Math.abs(others[0] - others[1]) <= 1);
      assert.deepEqual(allocateWeight(weights, [false, false, false], index, requested), next);
    }
  }
});
check('Confirmed weights stay locked in every confirmation order; only remaining weight cannot move', () => {
  for (const order of [[0,1,2], [0,2,1], [1,0,2], [1,2,0], [2,0,1], [2,1,0]]) {
    let weights = [34,33,33], locked = [false,false,false];
    for (const [position,index] of order.entries()) {
      const next = allocateWeight(weights, locked, index, 70 - position * 20);
      assert.ok(validWeights(next));
      for (let i = 0; i < 3; i++) if (locked[i] || position === 2) assert.equal(next[i], weights[i]);
      weights = next; locked[index] = true;
      assert.deepEqual(allocateWeight(weights, locked, index, 10), weights);
    }
    assert.ok(canRun(weights, locked, [34,33,33], 'first'));
  }
});
check('Minimum and maximum clamp safely without changing the input snapshot', () => {
  const old = [70,20,10];
  assert.deepEqual(allocateWeight(old, [true,false,false], 1, 80), [70,20,10]);
  assert.equal(maximumWeight(old, [true,false,false], 1), 20);
  assert.deepEqual(allocateWeight([34,33,33], [false,false,false], 0, -100), [10,45,45]);
  assert.deepEqual(allocateWeight([34,33,33], [false,false,false], 0, 100), [80,10,10]);
  assert.deepEqual(old, [70,20,10]);
  assert.deepEqual(allocateWeight(old, [false,false,false], 0, NaN), old);
});
check('Near-even boundary is inclusive; 34/33/33 and equal-looking thresholds produce three medium shots', () => {
  assert.ok(isNearEven([36,33,31]));
  assert.ok(!isNearEven([37,33,30]));
  assert.deepEqual([0,1,2].map(i=>effortAt([34,33,33],i)), ['medium','medium','medium']);
  for (const [weights, expected] of [[[33,57,10],'low'], [[34,56,10],'medium'], [[66,24,10],'medium'], [[67,23,10],'high']]) assert.equal(effortAt(weights,0), expected);
});
check('Run requires three individual confirmations and a valid complete allocation', () => {
  for (const confirmed of [[false,false,false], [true,true,false], [true,false,true], [false,true,true]]) assert.ok(!canRun([34,33,33], confirmed, [34,33,33], 'first'));
  assert.ok(canRun([70,20,10], [true,true,true], [34,33,33], 'first'));
  for (const weights of [[30,30,30], [90,5,5], [33.5,33.5,33]]) assert.ok(!validWeights(weights));
});
check('An already balanced first run must create a clear contrast of at least 20 points', () => {
  assert.ok(!goalMet([34,33,33], [34,33,33], 'contrast'));
  assert.ok(!goalMet([45,29,26], [34,33,33], 'contrast'));
  assert.ok(goalMet([46,28,26], [34,33,33], 'contrast'));
});
check('Rebalance must improve the spread; a partial improvement still permits the later balance check', () => {
  assert.ok(!goalMet([70,20,10], [70,20,10], 'rebalance'));
  assert.ok(!goalMet([80,10,10], [70,20,10], 'rebalance'));
  assert.ok(goalMet([50,30,20], [70,20,10], 'rebalance'));
  assert.ok(!isNearEven([50,30,20]));
  assert.ok(goalMet([34,33,33], [70,20,10], 'rebalance'));
  assert.equal(spread([34,33,33]),1);
});
mkdirSync('test-results', {recursive:true});
writeFileSync('test-results/level3-rules-results.json', JSON.stringify({passed:checks.length, checks},null,2)+'\n');
