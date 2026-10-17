import assert from 'node:assert/strict';
import { mkdirSync, writeFileSync } from 'node:fs';
import { allocateWeight, canRun, confirmWeight, effortAt, goalMet, isNearEven, maximumWeight, spread, validWeights } from '../src/levels/level3/weights.ts';

const checks = [];
const check = (name, run) => { run(); checks.push(name); console.log('PASS', name); };
check('Every possible integer split preserves total 100, range 0–100 and deterministic effort', () => {
  for (let a = 0; a <= 100; a++) for (let b = 0; b <= 100 - a; b++) {
    const weights = [a, b, 100 - a - b];
    assert.ok(validWeights(weights));
    assert.equal(isNearEven(weights),Math.max(...weights)-Math.min(...weights)<=10);
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
check('Either remaining card confirms the pair after any first-card choice', () => {
  for (let first = 0; first < 3; first++) for (const second of [0,1,2].filter(i=>i!==first)) {
    const weights = allocateWeight([34,33,33], [false,false,false], first, 80);
    const locked = confirmWeight([false,false,false], first);
    assert.equal(locked.filter(Boolean).length,1);
    const remaining = [0,1,2].find(i=>i!==first&&i!==second);
    const next = allocateWeight(weights,locked,second,15);
    assert.equal(next[first],80);assert.equal(next[second],15);assert.equal(next[remaining],5);
    assert.ok(validWeights(next));
    const finished=confirmWeight(locked,second);
    assert.deepEqual(finished,[true,true,true]);
    assert.ok(canRun(next,finished,[34,33,33],'first'));
    for (let i=0;i<3;i++) assert.deepEqual(allocateWeight(next,finished,i,50),next);
  }
});
check('Both equal remaining sliders can move in either direction before confirmation', () => {
  const weights=[80,10,10],locked=[true,false,false];
  assert.deepEqual(allocateWeight(weights,locked,1,15),[80,15,5]);
  assert.deepEqual(allocateWeight(weights,locked,2,15),[80,5,15]);
  assert.deepEqual(allocateWeight(weights,locked,1,0),[80,0,20]);
  assert.deepEqual(allocateWeight(weights,locked,2,20),[80,0,20]);
  assert.deepEqual(weights,[80,10,10]);
});
check('Available bounds clamp safely, including zero, without changing locked weights or snapshots', () => {
  const old=[70,20,10];
  assert.deepEqual(allocateWeight(old,[true,false,false],1,80),[70,30,0]);
  assert.equal(maximumWeight(old,[true,false,false],1),30);
  assert.deepEqual(allocateWeight([34,33,33],[false,false,false],0,-100),[0,50,50]);
  assert.deepEqual(allocateWeight([34,33,33],[false,false,false],0,100),[100,0,0]);
  assert.deepEqual(old,[70,20,10]);
  assert.deepEqual(allocateWeight(old,[false,false,false],0,NaN),old);
  assert.deepEqual(allocateWeight([100,0,0],[true,false,false],1,20),[100,0,0]);
});
check('Near-even accepts gaps through 10 points inclusively, rejects 11, and produces three medium shots', () => {
  for (const weights of [[36,33,31],[37,33,30],[38,33,29],[40,30,30]]) {
    for (const order of [[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]]) {
      const permuted=order.map(index=>weights[index]);
      assert.ok(isNearEven(permuted));
      assert.deepEqual([0,1,2].map(i=>effortAt(permuted,i)),['medium','medium','medium']);
    }
  }
  assert.ok(!isNearEven([40,31,29]));
  assert.ok(!isNearEven([29,40,31]));
  assert.deepEqual([0,1,2].map(i=>effortAt([34,33,33],i)), ['medium','medium','medium']);
  for (const [weights, expected] of [[[33,57,10],'low'], [[34,56,10],'medium'], [[66,24,10],'medium'], [[67,23,10],'high']]) assert.equal(effortAt(weights,0), expected);
});
check('Run requires all three confirmed weights (including the linked pair) and a valid complete allocation', () => {
  for (const confirmed of [[false,false,false], [true,true,false], [true,false,true], [false,true,true]]) assert.ok(!canRun([34,33,33], confirmed, [34,33,33], 'first'));
  assert.ok(canRun([70,20,10], [true,true,true], [34,33,33], 'first'));
  assert.ok(canRun([100,0,0], [true,true,true], [34,33,33], 'first'));
  assert.ok(canRun([90,5,5], [true,true,true], [34,33,33], 'first'));
  for (const weights of [[30,30,30], [-1,51,50], [101,0,-1], [33.5,33.5,33]]) assert.ok(!validWeights(weights));
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
