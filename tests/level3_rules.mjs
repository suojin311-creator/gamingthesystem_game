import assert from 'node:assert/strict';
import { mkdirSync, writeFileSync } from 'node:fs';
import { allocateWeight, canRun, confirmWeight, effortAt, goalMet, isNearEven, maximumWeight, spread, validWeights, MIN_WEIGHT, MAX_WEIGHT } from '../src/levels/level3/weights.ts';

const checks = [];
const check = (name, run) => { run(); checks.push(name); console.log('PASS', name); };
check('Every possible integer split preserves total 100, range 1–98 and deterministic allocation', () => {
  for (let a = 1; a <= 98; a++) for (let b = 1; b < 100 - a; b++) {
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
check('The 24/25 and 66/67 boundaries apply independently to the same task in every card position', () => {
  for (const [weight, expected] of [[1,'low'],[24,'low'],[25,'medium'],[33,'medium'],[66,'medium'],[67,'high'],[98,'high']]) {
    for (let index = 0; index < 3; index++) {
      const weights = [1,1,1];
      weights[index] = weight;
      weights[(index+1)%3] = 99-weight;
      assert.ok(validWeights(weights));
      assert.equal(effortAt(weights,index),expected,JSON.stringify({weights,index}));
    }
  }
});
check('Across all 4,851 positive splits, increasing a task share never lowers its effort and other shares cannot change its effort', () => {
  const ranks = {low:0,medium:1,high:2};
  const effortByShare = new Map();
  let splits = 0;
  for (let a=1;a<=98;a++) for (let b=1;b<100-a;b++) {
    const weights=[a,b,100-a-b];
    splits++;
    for (let index=0;index<3;index++) {
      const current=effortAt(weights,index), share=weights[index];
      if(effortByShare.has(share)) assert.equal(current,effortByShare.get(share),JSON.stringify({weights,index,share}));
      else effortByShare.set(share,current);
      for(let donor=0;donor<3;donor++) {
        if(donor===index||weights[donor]===1)continue;
        const next=[...weights];next[index]++;next[donor]--;
        assert.ok(validWeights(next));
        assert.ok(ranks[effortAt(next,index)]>=ranks[current],JSON.stringify({weights,next,index}));
      }
    }
  }
  assert.equal(splits,4851);assert.equal(effortByShare.size,98);
  for(let share=1;share<98;share++) assert.ok(ranks[effortByShare.get(share+1)]>=ranks[effortByShare.get(share)]);
});
check('Crossing the near-even description boundary cannot reduce effort when a share rises', () => {
  assert.ok(isNearEven([40,30,30]));assert.ok(!isNearEven([40,31,29]));
  assert.deepEqual([0,1,2].map(i=>effortAt([40,30,30],i)),['medium','medium','medium']);
  assert.deepEqual([0,1,2].map(i=>effortAt([40,31,29],i)),['medium','medium','medium']);
  assert.ok(!isNearEven([50,25,25]));
  assert.deepEqual([0,1,2].map(i=>effortAt([50,25,25],i)),['medium','medium','medium']);
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
  assert.deepEqual(allocateWeight(weights,locked,1,0),[80,1,19]);
  assert.deepEqual(allocateWeight(weights,locked,2,20),[80,1,19]);
  assert.deepEqual(weights,[80,10,10]);
});
check('Available bounds clamp safely, reserving one percent, without changing locked weights or snapshots', () => {
  const old=[70,20,10];
  assert.deepEqual(allocateWeight(old,[true,false,false],1,80),[70,29,1]);
  assert.equal(maximumWeight(old,[true,false,false],1),29);
  assert.deepEqual(allocateWeight([34,33,33],[false,false,false],0,-100),[1,50,49]);
  assert.deepEqual(allocateWeight([34,33,33],[false,false,false],0,100),[98,1,1]);
  assert.deepEqual(old,[70,20,10]);
  assert.deepEqual(allocateWeight(old,[false,false,false],0,NaN),old);
  assert.deepEqual(allocateWeight([98,1,1],[true,false,false],1,20),[98,1,1]);
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
  for (const [weights, expected] of [[[24,66,10],'low'], [[25,65,10],'medium'], [[66,24,10],'medium'], [[67,23,10],'high']]) assert.equal(effortAt(weights,0), expected);
});
check('Run requires all three confirmed weights (including the linked pair) and a valid complete allocation', () => {
  for (const confirmed of [[false,false,false], [true,true,false], [true,false,true], [false,true,true]]) assert.ok(!canRun([34,33,33], confirmed, [34,33,33], 'first'));
  assert.ok(canRun([70,20,10], [true,true,true], [34,33,33], 'first'));
  assert.ok(!canRun([100,0,0], [true,true,true], [34,33,33], 'first'));
  assert.ok(!canRun([61,39,0], [true,true,true], [34,33,33], 'first'));
  assert.ok(canRun([98,1,1], [true,true,true], [34,33,33], 'first'));
  assert.equal(MIN_WEIGHT,1);assert.equal(MAX_WEIGHT,98);
  assert.deepEqual(allocateWeight([61,20,19],[true,false,false],1,39),[61,38,1]);
  assert.ok(canRun([90,5,5], [true,true,true], [34,33,33], 'first'));
  for (const weights of [[30,30,30], [-1,51,50], [101,0,-1], [33.5,33.5,33]]) assert.ok(!validWeights(weights));
});
check('The second experiment requires a changed split and never forces a direction or degree of balance', () => {
  assert.ok(!goalMet([34,33,33], [34,33,33], 'different'));
  for (const weights of [[40,30,30],[33,34,33],[70,20,10]]) assert.ok(goalMet(weights,[34,33,33],'different'));
  assert.ok(!goalMet([70,20,10], [70,20,10], 'different'));
  for (const weights of [[80,10,10],[50,30,20],[34,33,33]]) assert.ok(goalMet(weights,[70,20,10],'different'));
  assert.ok(canRun([80,10,10],[true,true,true],[70,20,10],'different'));
});
mkdirSync('test-results', {recursive:true});
writeFileSync('test-results/level3-rules-results.json', JSON.stringify({passed:checks.length, checks},null,2)+'\n');
