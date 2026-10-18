import assert from 'node:assert/strict';
import { mkdirSync, writeFileSync } from 'node:fs';
import { createServer } from 'vite';
const server = await createServer({server:{middlewareMode:true,hmr:false},appType:'custom'});
const checks=[];const check=(name,run)=>{run();checks.push(name);console.log('PASS',name)};
try {
 const {nextExperiment,meetsExperiment}=await server.ssrLoadModule('/src/levels/level3/experiments.ts');
 const {validWeights,isNearEven,effortAt}=await server.ssrLoadModule('/src/levels/level3/weights.ts');
 const {compareRuns}=await server.ssrLoadModule('/src/levels/level3/data.ts');
 const ids=['prep','part','focus','discuss','reflect','peer'];
 const trios=ids.flatMap((a,i)=>ids.slice(i+1).flatMap((b,j)=>ids.slice(i+j+2).map(c=>[a,b,c])));
 const run=(weights,round=1,metricIds=ids.slice(0,3))=>({round,kind:'player',metricIds,weights});
 check('Every positive first split has a relevant second-test prompt and a valid optional starting point, without changing the first record',()=>{
  assert.equal(nextExperiment([]).purpose,'explore');assert.ok(meetsExperiment([34,33,33],[]));
  for(let a=1;a<=98;a++)for(let b=1;b<100-a;b++){
   const first=run([a,b,100-a-b]);const saved=JSON.stringify(first),plan=nextExperiment([first]);
   assert.equal(plan.purpose,'adjust');assert.ok(validWeights(plan.suggestion));assert.ok(meetsExperiment(plan.suggestion,[first]));
   assert.notEqual(isNearEven(first.weights),isNearEven(plan.suggestion));
   assert.ok(!meetsExperiment(first.weights,[first]));assert.equal(JSON.stringify(first),saved);
  }
 });
 check('All three adaptive verification routes produce a third distinct player test and a near-even/uneven comparison',()=>{
  const cases=[[70,20,10],[20,70,10],[10,20,70],[45,45,10],[45,10,45],[10,45,45],[34,33,33],[40,30,30],[31,35,34],[98,1,1],[61,38,1]];
  for(const metricIds of trios)for(const first of cases)for(const second of cases){
   if(first.every((v,i)=>v===second[i]))continue;
   const runs=[run(first,1,metricIds),run(second,2,metricIds)],before=JSON.stringify(runs),plan=nextExperiment(runs);
   assert.ok(meetsExperiment(plan.suggestion,runs),JSON.stringify({runs,plan}));
   assert.equal(plan.purpose,runs.every(r=>isNearEven(r.weights))?'contrast':runs.every(r=>!isNearEven(r.weights))?'balance':'redirect');
   assert.ok(!meetsExperiment(first,runs));assert.ok(!meetsExperiment(second,runs));
   if(plan.purpose==='redirect')for(const id of plan.focus){
    const i=metricIds.indexOf(id);assert.equal(effortAt(plan.reference.weights,i),'low');assert.notEqual(effortAt(plan.suggestion,i),'low');
   }
   assert.ok(compareRuns([...runs,run(plan.suggestion,3,metricIds)]));assert.equal(JSON.stringify(runs),before);
  }
 });
 check('Verification accepts player-chosen valid alternatives, rejects irrelevant repeats and zero, and supplies independently copied suggestions',()=>{
  const uneven=[run([70,20,10]),run([45,45,10],2)],balanced=[run([34,33,33]),run([40,30,30],2)],mixed=[run([70,20,10]),run([34,33,33],2)];
  assert.ok(meetsExperiment([31,35,34],uneven));assert.ok(!meetsExperiment([80,10,10],uneven));
  assert.ok(meetsExperiment([10,20,70],balanced));assert.ok(!meetsExperiment([31,35,34],balanced));
  assert.ok(meetsExperiment([20,60,20],mixed));assert.ok(!meetsExperiment([80,10,10],mixed));
  for(const history of [[],uneven,balanced,mixed])assert.ok(!meetsExperiment([61,39,0],history));
  const plan=nextExperiment(uneven);plan.suggestion[0]=98;assert.deepEqual(nextExperiment(uneven).suggestion,[34,33,33]);
 });
 mkdirSync('test-results',{recursive:true});writeFileSync('test-results/experiment-rules-results.json',JSON.stringify({passed:checks.length,checks},null,2)+'\n');
} finally {await server.close()}
