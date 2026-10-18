import assert from 'node:assert/strict';
import { mkdirSync, writeFileSync } from 'node:fs';
import { createServer } from 'vite';

const server = await createServer({ server: { middlewareMode: true, hmr: false }, appType: 'custom' });
const checks = [];
const check = (name, test) => { test(); checks.push(name); console.log('PASS', name); };
try {
  const { nextExperiment } = await server.ssrLoadModule('/src/levels/level3/experiments.ts');
  const { observedStudentBehaviour, effortChanged, joinNames } = await server.ssrLoadModule('/src/levels/level3/data.ts');
  const { effortAt } = await server.ssrLoadModule('/src/levels/level3/weights.ts');
  const { metricDefinition } = await server.ssrLoadModule('/src/shared/data/metrics.ts');
  const ids = ['prep', 'part', 'focus', 'discuss', 'reflect', 'peer'];
  const trios = ids.flatMap((a, i) => ids.slice(i + 1).flatMap((b, j) => ids.slice(i + j + 2).map(c => [a, b, c])));
  const patterns = [[70, 20, 10], [45, 45, 10], [65, 24, 11], [38, 34, 28]];
  const sameBands = [[68, 21, 11], [46, 44, 10], [64, 25, 11], [34, 33, 33]];
  const permutations = [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]];
  const run = (weights, round = 1, metricIds = ids.slice(0, 3)) => ({ round, kind: 'player', metricIds, weights });
  const neglected = record => record.metricIds.filter((_, i) => effortAt(record.weights, i) === 'low');
  const lowMessage = 'Low-weight areas get less attention.';
  const coveredMessage = 'Stops when the criteria are met.';

  check('The first prompt teaches controls without supplying an allocation or implying an earlier result', () => {
    assert.deepEqual(nextExperiment([]), {
      purpose: 'explore', question: 'How would you split the 100%?',
      hint: 'Move any slider to start. Confirm your weights, then watch Alex.',
    });
  });
  check('Second-trial prompts cover all four effort families, every task position and all twenty metric trios', () => {
    for (const trio of trios) for (const weights of patterns) for (const order of permutations) {
      const record = run(order.map(i => weights[i]), 1, trio), low = neglected(record);
      const prompt = nextExperiment([record]);
      assert.equal(prompt.purpose, 'respond');
      assert.equal(observedStudentBehaviour(record.weights), low.length ? lowMessage : coveredMessage);
      if (low.length) {
        assert.equal(prompt.question, `Can you bring more attention to ${joinNames(low.map(id => metricDefinition(id).shortName))}?`);
        assert.equal(prompt.hint, 'Give a neglected task more weight. Watch what happens to the others.');
      } else {
        assert.equal(prompt.question, 'All three got attention. Has that solved the problem?');
        assert.equal(prompt.hint, 'Try a different split. Does Alex still stop once the criteria are met?');
      }
    }
  });
  check('Unchanged third-trial prompts take precedence for all four families, including non-equal steady weights', () => {
    for (const trio of trios) for (const [index, weights] of patterns.entries()) for (const order of permutations) {
      const history = [run(order.map(i => weights[i]), 1, trio), run(order.map(i => sameBands[index][i]), 2, trio)];
      assert.equal(effortChanged(...history), false);
      const prompt = nextExperiment(history);
      assert.equal(prompt.question, 'Alex’s effort stayed the same. What could you change?');
      assert.equal(prompt.hint, 'Make a bigger change to the shares. Does Alex’s effort change this time?');
      assert.equal(observedStudentBehaviour(history[1].weights), index === 3 ? coveredMessage : lowMessage);
    }
  });
  check('Changed third-trial prompts follow the latest neglected tasks, handle singular/plural, and retain score-based stopping for coverage', () => {
    for (const trio of trios) for (const weights of patterns) for (const order of permutations) {
      const current = run(order.map(i => weights[i]), 2, trio);
      const baseline = run(patterns[weights === patterns[3] ? 0 : 3], 1, trio);
      assert.ok(effortChanged(baseline, current));
      const low = neglected(current), prompt = nextExperiment([baseline, current]);
      assert.equal(prompt.purpose, 'verify');
      if (low.length) {
        assert.equal(prompt.question, `${joinNames(low.map(id => metricDefinition(id).shortName))} ${low.length === 1 ? 'gets' : 'get'} little attention. What could you change?`);
        assert.equal(prompt.hint, 'Give a neglected task more weight. Can you avoid neglecting another?');
        assert.equal(observedStudentBehaviour(current.weights), lowMessage);
      } else {
        assert.equal(prompt.question, 'The effort changed. Did the stopping point?');
        assert.equal(prompt.hint, 'Try another split. Does Alex still stop when the criteria are met?');
        assert.equal(observedStudentBehaviour(current.weights), coveredMessage);
      }
    }
  });
  check('Switching the leading task counts as changed effort even when the overall family stays one-high/two-low', () => {
    const prompt = nextExperiment([run([70, 20, 10]), run([20, 70, 10], 2)]);
    assert.equal(prompt.question, 'Preparation and Focus get little attention. What could you change?');
    assert.equal(prompt.hint, 'Give a neglected task more weight. Can you avoid neglecting another?');
  });
  check('Branch selection matches task identity rather than array order, and reading hints leaves observations untouched', () => {
    const records = [run([70, 20, 10]), run([10, 70, 20], 2, ['focus', 'prep', 'part'])];
    const before = JSON.stringify(records), prompt = nextExperiment(records);
    assert.equal(prompt.question, 'Alex’s effort stayed the same. What could you change?');
    assert.equal(JSON.stringify(records), before);
  });
  mkdirSync('test-results', { recursive: true });
  writeFileSync('test-results/level3-hint-alignment-results.json', JSON.stringify({ passed: checks.length, checks }, null, 2) + '\n');
} finally { await server.close(); }
