import assert from 'node:assert/strict';
import { mkdirSync, writeFileSync } from 'node:fs';
import { createServer } from 'vite';
const server = await createServer({server:{middlewareMode:true,hmr:false},appType:'custom'});
const checks=[];const check=(name,run)=>{run();checks.push(name);console.log('PASS',name)};
try {
 const {nextExperiment,meetsExperiment,trialFinding,TRIAL_INTENTS}=await server.ssrLoadModule('/src/levels/level3/experiments.ts');
 const {validWeights}=await server.ssrLoadModule('/src/levels/level3/weights.ts');
 const {compareRuns,copyRun,cinematicRequest}=await server.ssrLoadModule('/src/levels/level3/data.ts');
 const ids=['prep','part','focus','discuss','reflect','peer'];
 const trios=ids.flatMap((a,i)=>ids.slice(i+1).flatMap((b,j)=>ids.slice(i+j+2).map(c=>[a,b,c])));
 const run=(weights,round=1,metricIds=ids.slice(0,3),intent='attention')=>({round,kind:'player',metricIds,weights,intent});
 check('Every positive allocation is allowed in a third test regardless of earlier balance, except exact repeats',()=>{
  for(const history of [[[70,20,10],[80,10,10]],[[34,33,33],[40,30,30]],[[70,20,10],[34,33,33]]]){
   const runs=history.map((weights,i)=>run(weights,i+1)),saved=JSON.stringify(runs);
   for(let a=1;a<=98;a++)for(let b=1;b<100-a;b++){
    const weights=[a,b,100-a-b];
    assert.equal(meetsExperiment(weights,runs),!history.some(old=>old.every((v,i)=>v===weights[i])));
   }
   assert.equal(JSON.stringify(runs),saved);
   for(const invalid of [[61,39,0],[99,0,1],[20,20,20],[33.5,33.5,33]])assert.ok(!meetsExperiment(invalid,runs));
  }
 });
 check('All 20 trios have opt-in goal-specific editable examples and real recorded purposes; no strategy is selected for the player',()=>{
  const cases=[[70,20,10],[45,45,10],[34,33,33],[40,30,30],[98,1,1]];
  assert.equal(nextExperiment([]).suggestion,undefined);
  for(const metricIds of trios)for(const first of cases)for(const second of cases){
   if(first.every((v,i)=>v===second[i]))continue;
   const runs=[run(first,1,metricIds),run(second,2,metricIds)],before=JSON.stringify(runs);
   assert.equal(nextExperiment(runs).suggestion,undefined);
   for(const {id:intent} of TRIAL_INTENTS){
    const plan=nextExperiment(runs,intent);
    assert.equal(plan.purpose,'verify');assert.ok(validWeights(plan.suggestion));assert.ok(meetsExperiment(plan.suggestion,runs));
    assert.equal((plan.question.match(/\?/g)||[]).length,1);
    const third=run(plan.suggestion,3,metricIds,intent),request=cinematicRequest('comparison','Riley',[...runs,third],'keep');
    assert.equal(request.runs[2].intent,intent);assert.equal(request.decision,'keep');assert.ok(trialFinding(third,runs[1]));
    const copy=copyRun(third);copy.weights[0]=1;assert.notEqual(copy.weights[0],third.weights[0]);
   }
   assert.equal(JSON.stringify(runs),before);
  }
 });
 check('Goal feedback acknowledges shared attention, unchanged effort and shifted priorities without equating any with learning',()=>{
  assert.match(trialFinding(run([34,33,33])),/All three received attention/);
  const low=trialFinding(run([70,20,10]));assert.match(low,/Participation and Focus still got minimum effort/);
  assert.match(trialFinding(run([34,33,33],2,ids.slice(0,3),'exploration')),/packed up/);
  assert.match(trialFinding(run([70,20,10],2,ids.slice(0,3),'exploration')),/unproven/);
  assert.match(trialFinding(run([80,10,10],2,ids.slice(0,3),'priority'),run([70,20,10])),/Preparation still draws/);
  assert.match(trialFinding(run([10,70,20],2,ids.slice(0,3),'priority'),run([70,20,10])),/Participation now draws/);
  assert.equal(compareRuns([run([70,20,10]),run([80,10,10],2),run([10,70,20],3)]),null);
  assert.equal(compareRuns([run([34,33,33]),run([40,30,30],2),run([31,35,34],3)]),null);
  assert.ok(compareRuns([run([70,20,10]),run([34,33,33],2),run([10,70,20],3)]));
 });
 mkdirSync('test-results',{recursive:true});writeFileSync('test-results/experiment-rules-results.json',JSON.stringify({passed:checks.length,checks},null,2)+'\n');
} finally {await server.close()}
