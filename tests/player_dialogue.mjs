import assert from 'node:assert/strict';
import { mkdirSync, writeFileSync } from 'node:fs';
import { createServer } from 'vite';
const server=await createServer({server:{middlewareMode:true,hmr:false},appType:'custom'});
const checks=[];const check=(name,fn)=>{fn();checks.push(name);console.log('PASS',name)};
try {
 const {workbenchDialogue,weightedSceneReply,comparisonDialogue}=await server.ssrLoadModule('/src/levels/level3/dialogue.ts');
 const {cinematicRequest}=await server.ssrLoadModule('/src/levels/level3/data.ts');
 const {METRICS}=await server.ssrLoadModule('/src/levels/level1/metrics.ts');
 const {observationDialogue,classroomDialogue}=await server.ssrLoadModule('/src/levels/level2/dialogue.ts');
 const {sceneRequest}=await server.ssrLoadModule('/src/levels/level2/data.ts');
 const ids=METRICS.map(m=>m.id);
 const trios=ids.flatMap((a,i)=>ids.slice(i+1).flatMap((b,j)=>ids.slice(i+j+2).map(c=>[a,b,c])));
 const histories=[[[34,33,33],[40,30,30],[31,35,34]],[[70,20,10],[80,10,10],[90,5,5]],[[70,20,10],[10,70,20],[20,10,70]],[[45,45,10],[10,45,45],[45,10,45]],[[70,20,10],[34,33,33],[10,70,20]],[[34,33,33],[70,20,10],[40,30,30]],[[40,30,30],[40,31,29],[50,25,25]],[[24,25,51],[25,24,51],[25,50,25]]];
 const normalize=line=>`${line.speaker==='Maya'||line.speaker==='Riley'?'teacher':line.speaker}:${line.text.toLowerCase().replace(/[^\p{L}\p{N}]/gu,'')}`;
 let paths=0;
 check('Two-trial endings and optional-third endings keep short, fresh dialogue across every trio and observed pattern',()=>{
  for(const trio of trios)for(const history of histories)for(const length of [2,3]){
   const runs=[],lines=[];
   for(const [index,weights] of history.slice(0,length).entries()){
    runs.push({round:index+1,kind:'player',metricIds:trio,weights});
    const request=cinematicRequest('weights','Riley',runs);
    lines.push(...request.shots.map((_,i)=>({speaker:'Alex',text:weightedSceneReply(request,i)})));
    const review=workbenchDialogue('result','Riley',index?'different':'first',runs);
    assert.equal(review.length,3);assert.equal(review[0].name,'Riley');
    assert.ok(review.every(line=>line.text.split(/\s+/).length<=20));
    lines.push(...review);
   }
   const ending=comparisonDialogue('Riley',runs);
   assert.equal(ending.length,3);
   assert.doesNotMatch(JSON.stringify(ending),/keep this split|rethink this setup/i);
   const final=[...lines,...ending];
   for(const metric of METRICS){
    const earlier=[...metric.scene,{speaker:'Maya',text:metric.reviewQuestion},...metric.studentReplies.map(text=>({speaker:'Alex',text}))];
    for(const count of [3,6,100])earlier.push(...classroomDialogue(sceneRequest(count,trio,'Riley')),...observationDialogue(count===100,count,trio,'Riley'));
    const texts=[...earlier,...final].map(normalize);
    assert.equal(new Set(texts).size,texts.length,JSON.stringify({trio,history,length,metric:metric.id,duplicates:texts.filter((text,i)=>texts.indexOf(text)!==i)}));
    const emojis=[...earlier,...final].flatMap(line=>[...line.text.matchAll(/\p{Extended_Pictographic}/gu)].map(m=>m[0]));
    assert.equal(new Set(emojis).size,emojis.length,JSON.stringify({trio,history,length,metric:metric.id,emojis}));
   }
   paths++;
  }
  assert.equal(paths,trios.length*histories.length*2);
 });
 check('Legacy intent fields cannot change the actual-observation dialogue or create a new required choice',()=>{
  for(const trio of trios)for(const history of histories){
   const runs=history.map((weights,index)=>({round:index+1,kind:'player',metricIds:trio,weights}));
   for(const length of [1,2,3]){
    const actual=runs.slice(0,length),reference=workbenchDialogue('result','Riley',length===1?'first':'different',actual);
    for(const intent of ['attention','priority','exploration']){
     const legacy=actual.map(run=>({...run,intent}));
     assert.deepEqual(workbenchDialogue('result','Riley',length===1?'first':'different',legacy),reference);
    }
   }
  }
 });
 mkdirSync('test-results',{recursive:true});writeFileSync('test-results/player-dialogue-results.json',JSON.stringify({passed:checks.length,checks,trialPaths:paths},null,2)+'\n');
}finally{await server.close()}
