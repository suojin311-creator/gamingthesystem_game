import assert from 'node:assert/strict';
import { mkdirSync, writeFileSync } from 'node:fs';
import { createServer } from 'vite';
const server=await createServer({server:{middlewareMode:true,hmr:false},appType:'custom'});
const checks=[];const check=(name,run)=>{run();checks.push(name);console.log('PASS',name)};
try{
 const {mostEffortIds,copyRun,cinematicRequest,compareRuns}=await server.ssrLoadModule('/src/levels/level3/data.ts');
 const {sceneRequest}=await server.ssrLoadModule('/src/levels/level2/data.ts');
 const ids=['prep','part','focus','discuss','reflect','peer'];
 const trios=ids.flatMap((a,i)=>ids.slice(i+1).flatMap((b,j)=>ids.slice(i+j+2).map(c=>[a,b,c])));
 const cases=[[[98,1,1],[0]],[[61,38,1],[0,1]],[[45,45,10],[0,1]],[[40,30,30],[0,1,2]],[[34,33,33],[0,1,2]],[[1,1,98],[2]]];
 check('All 20 trios retain single, tied and near-even highest observed effort independently of all seven forecast subsets',()=>{
  for(const metricIds of trios)for(const [weights,most] of cases)for(let mask=1;mask<8;mask++){
   const predictedMetricIds=metricIds.filter((_,i)=>mask&(1<<i));
   const run={round:1,kind:'player',metricIds,weights,predictedMetricIds};
   assert.deepEqual(mostEffortIds(run),most.map(i=>metricIds[i]));assert.deepEqual(run.predictedMetricIds,predictedMetricIds);
  }
 });
 check('Copied runs, partner requests and compared snapshots independently copy predictions as well as weights and metrics',()=>{
  const run={round:1,kind:'player',metricIds:['prep','part','focus'],weights:[70,20,10],predictedMetricIds:['focus']};
  const baseline=JSON.stringify(run);const copy=copyRun(run);copy.predictedMetricIds.push('part');copy.weights[0]=12;
  const second={...run,round:2,weights:[34,33,33],predictedMetricIds:['prep','part','focus']};
  const request=cinematicRequest('weights','Jordan',[run,second]);request.runs[0].predictedMetricIds.length=0;
  const compared=compareRuns([run,second]);compared.uneven.predictedMetricIds.push('prep');
  assert.equal(JSON.stringify(run),baseline);assert.deepEqual(second.predictedMetricIds,['prep','part','focus']);
 });
 check('Every six-metric branch supplies three peer-action beats with an unresolved content question; other scenes keep their existing contracts',()=>{
  for(const trio of trios){
   const request=sceneRequest(6,trio,'Jordan');assert.equal(request.peerInteraction.length,3);
   assert.deepEqual(request.peerInteraction.map(b=>b.speaker),['Alex','Classmate','Alex']);
   assert.match(request.peerInteraction[1].text,/why is the idea true/);assert.match(request.peerInteraction[2].action,/question remains open/);
   assert.ok(request.peerInteraction.every(b=>b.action.length&&b.text.length));
   request.peerInteraction[0].text='changed';assert.notEqual(sceneRequest(6,trio,'Jordan').peerInteraction[0].text,'changed');
   for(const count of [3,100])assert.equal(sceneRequest(count,trio,'Jordan').peerInteraction,undefined);
  }
 });
 mkdirSync('test-results',{recursive:true});writeFileSync('test-results/learning-contract-results.json',JSON.stringify({passed:checks.length,checks},null,2)+'\n');
}finally{await server.close()}
