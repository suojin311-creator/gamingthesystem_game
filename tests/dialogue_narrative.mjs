import assert from 'node:assert/strict';
import { mkdirSync, writeFileSync } from 'node:fs';
import { createServer } from 'vite';

const server = await createServer({ server: { middlewareMode: true, hmr: false }, appType: 'custom' });
const checks = [];
const check = (name, run) => { run(); checks.push(name); console.log('PASS', name); };
try {
  const { workbenchDialogue: talk, weightPattern, weightedSceneReply, comparisonDialogue } = await server.ssrLoadModule('/src/levels/level3/dialogue.ts');
  const { cinematicRequest, referenceTest, compareRuns } = await server.ssrLoadModule('/src/levels/level3/data.ts');
  const { observationDialogue, classroomDialogue } = await server.ssrLoadModule('/src/levels/level2/dialogue.ts');
  const { sceneRequest } = await server.ssrLoadModule('/src/levels/level2/data.ts');
  const { METRICS } = await server.ssrLoadModule('/src/levels/level1/metrics.ts');
  const { effortAt, isNearEven } = await server.ssrLoadModule('/src/levels/level3/weights.ts');
  const ids = METRICS.map(m => m.id);
  const trios = ids.flatMap((a, i) => ids.slice(i + 1).flatMap((b, j) => ids.slice(i + j + 2).map(c => [a, b, c])));
  assert.equal(trios.length, 20);
  const makeRun = (metricIds, weights, round = 1, kind = 'player') => ({ round, kind, metricIds, weights });
  const splitCases = [[80,10,10],[70,20,10],[20,70,10],[45,45,10],[45,10,45],[46,43,11],[34,33,33],[40,30,30],[31,35,34]];
  check('Every valid integer split uses the 10-point near-even boundary and the correct one/two higher-reward family', () => {
    for (let a = 0; a <= 100; a++) for (let b = 0; b <= 100-a; b++) {
      const w = [a,b,100-a-b];
      const expected = isNearEven(w) ? 'near-even' : [...w].sort((a,b)=>a-b)[1] >= 34 ? 'two-higher' : 'one-higher';
      assert.equal(weightPattern(makeRun(ids.slice(0,3), w)), expected);
    }
  });
  check('All 20 trios publish distinct plans and teacher reviews for one high, two high and near-even weights', () => {
    const publications = new Set(), reviews = new Set();
    for (const trio of trios) {
      const families = [[70,20,10],[45,45,10],[34,33,33]].map(weights => {
        const run = makeRun(trio, weights);
        const published = talk('publish','Riley','first',[run]);
        const review = talk('result','Riley','first',[run]);
        for (const lines of [published, review]) {
          assert.equal(lines.length, 3); assert.equal(lines[0].name, 'Riley');
          assert.equal(lines.filter(line => line.speaker === 'Alex').length, 2);
          assert.ok(lines.every(line => line.text.length && !line.text.includes('undefined')));
        }
        if (weightPattern(run) !== 'near-even') {
          const lower = trio.filter((_,i) => weights[i]<34).map(id=>METRICS.find(m=>m.id===id).shortName);
          lower.forEach(name=>assert.ok(published.some(line=>line.text.includes(name))));
          lower.forEach(name=>assert.ok(review.some(line=>line.text.includes(name))));
        }
        publications.add(JSON.stringify(published)); reviews.add(JSON.stringify(review));
        return { published, review };
      });
      assert.equal(new Set(families.map(f=>f.published[0].text)).size,3);
      assert.equal(new Set(families.map(f=>f.review[0].text)).size,3);
    }
    // Near-even deliberately describes all three together; metric-specific table rows carry the names.
    assert.ok(publications.size >= 41 && reviews.size >= 41);
  });
  check('Second-result questions describe actual increases, decreases and unchanged effort bands', () => {
    const trio=ids.slice(0,3);
    const question=(a,b)=>talk('result','Riley','different',[makeRun(trio,a),makeRun(trio,b,2)])[0].text;
    assert.match(question([70,20,10],[20,70,10]),/Participation got more effort, while Preparation got less/);
    assert.match(question([70,20,10],[80,10,10]),/effort looks similar/);
    assert.match(question([34,33,33],[40,30,30]),/Did that change how you worked/);
    assert.match(question([70,20,10],[34,33,33]),/more spread out/);
    assert.match(question([45,45,10],[70,20,10]),/Preparation got more effort, while Participation got less/);
  });
  check('Both comparison orders and both system references describe the latest actual pattern without assuming an improvement', () => {
    for (const sequence of [[[70,20,10],[34,33,33]],[[34,33,33],[70,20,10]],[[70,20,10],[80,10,10]],[[34,33,33],[40,30,30]]]) {
      const runs=sequence.map((weights,i)=>makeRun(ids.slice(0,3),weights,i+1));
      const reference=referenceTest(runs);
      if(reference) runs.push(makeRun(ids.slice(0,3),reference.weights,3,reference.kind));
      assert.ok(compareRuns(runs));
      const text=comparisonDialogue('Riley',runs)[0].text;
      assert.match(text,isNearEven(runs.at(-1).weights)?/Spreading the rewards/:/Making Preparation worth more/);
      assert.ok(!JSON.stringify(comparisonDialogue('Riley',runs)).includes('Balancing the weights helped'));
    }
  });
  let paths=0;
  check('No dialogue or emoji repeats within 8,640 complete trial paths, including repeated patterns and unchanged scene intensity', () => {
    for (const trio of trios) for (const first of splitCases) for (const second of splitCases) {
      if(JSON.stringify(first)===JSON.stringify(second))continue;
      const runs=[]; const story=[];
      const append=lines=>story.push(...lines.map(line=>({speaker:line.speaker==='Maya'||line.speaker==='Riley'?'teacher':line.speaker,text:line.text})));
      append(talk('weights','Riley','first',runs));
      for(const weights of [first,second]) {
        if(runs.length)append(talk('weights','Riley','different',runs));
        runs.push(makeRun(trio,weights,runs.length+1));
        append(talk('publish','Riley',runs.length===1?'first':'different',runs));
        const request=cinematicRequest('weights','Riley',runs);
        append(request.shots.map((_,i)=>({speaker:'Alex',text:weightedSceneReply(request,i)})));
        append(talk('result','Riley',runs.length===1?'first':'different',runs));
      }
      const reference=referenceTest(runs);
      if(reference){
        runs.push(makeRun(trio,reference.weights,3,reference.kind));
        append(talk('publish','Riley','different',runs));
        const request=cinematicRequest('weights','Riley',runs);
        append(request.shots.map((_,i)=>({speaker:'Alex',text:weightedSceneReply(request,i)})));
        append(talk('result','Riley','different',runs));
      }
      append(talk('compare','Riley','different',runs));append(comparisonDialogue('Riley',runs));
      for(const metric of METRICS){
        const earlier=[...metric.scene.map(line=>({speaker:line.speaker==='Maya'?'teacher':line.speaker,text:line.text})),{speaker:'teacher',text:metric.reviewQuestion},...metric.studentReplies.map(text=>({speaker:'Alex',text}))];
        for(const count of [3,6,100]) earlier.push(...classroomDialogue(sceneRequest(count,trio,'Riley')).map(line=>({speaker:line.speaker==='Riley'?'teacher':line.speaker,text:line.text})));
        for(const count of [3,6,100])earlier.push(...observationDialogue(count===100,count,trio,'Riley').map(line=>({speaker:line.speaker==='Maya'?'teacher':line.speaker,text:line.text})));
        const full=[...earlier,...story];
        const normalized=full.map(line=>`${line.speaker}:${line.text.toLowerCase().replace(/[^\p{L}\p{N}]/gu,'')}`);
        assert.equal(new Set(normalized).size,normalized.length,JSON.stringify({trio,first,second,duplicates:normalized.filter((text,i)=>normalized.indexOf(text)!==i)}));
        const emojis=full.flatMap(line=>[...line.text.matchAll(/\p{Extended_Pictographic}/gu)].map(match=>match[0]));
        assert.equal(new Set(emojis).size,emojis.length);
        paths++;
      }
      // Changing a reply never changes the scene IDs, effort rules or replayed request.
      const request=cinematicRequest('weights','Riley',runs);
      const snapshot=JSON.stringify(request);
      request.shots.forEach((shot,i)=>{
        assert.equal(shot.effort,effortAt(runs.at(-1).weights,i));
        assert.equal(weightedSceneReply(request,i),weightedSceneReply(request,i));
      });
      assert.equal(JSON.stringify(request),snapshot);
    }
    assert.equal(paths,8640);
  });
  check('Six Level 1 review questions and all 20 Level 2 trio exchanges differ; player names remain supplied text', () => {
    assert.equal(new Set(METRICS.map(m=>m.reviewQuestion)).size,6);
    const seen=new Set();
    for(const trio of trios){
      const lines=observationDialogue(false,3,trio,'Alex');
      assert.equal(lines[0].speaker,'Maya');assert.equal(lines[0].name,'Alex');
      seen.add(JSON.stringify(lines));
    }
    assert.equal(seen.size,20);
  });
  mkdirSync('test-results',{recursive:true});
  writeFileSync('test-results/dialogue-narrative-results.json',JSON.stringify({passed:checks.length,checks,completeTrialPaths:paths},null,2)+'\n');
} finally { await server.close(); }
