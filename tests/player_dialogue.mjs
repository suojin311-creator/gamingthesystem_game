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
 const ids=METRICS.map(m=>m.id),intents=['attention','priority','exploration'];
 const trios=ids.flatMap((a,i)=>ids.slice(i+1).flatMap((b,j)=>ids.slice(i+j+2).map(c=>[a,b,c])));
 const histories=[[[34,33,33],[40,30,30],[31,35,34]],[[70,20,10],[80,10,10],[90,5,5]],[[70,20,10],[10,70,20],[20,10,70]],[[45,45,10],[10,45,45],[45,10,45]],[[70,20,10],[34,33,33],[10,70,20]],[[34,33,33],[70,20,10],[40,30,30]],[[40,30,30],[40,31,29],[50,25,25]],[[24,25,51],[25,24,51],[25,50,25]]];
 const normalize=line=>`${line.speaker==='Maya'||line.speaker==='Riley'?'teacher':line.speaker}:${line.text.toLowerCase().replace(/[^\p{L}\p{N}]/gu,'')}`;
 let paths=0;
 check('Player-purpose dialogue and all three scene readings stay fresh across uniform and mixed patterns, every trio and all purpose combinations',()=>{
  for(const trio of trios)for(const history of histories)for(const a of intents)for(const b of intents)for(const c of intents){
   const runs=[],lines=[];
   for(const [index,weights] of history.entries()){
    runs.push({round:index+1,kind:'player',metricIds:trio,weights,intent:[a,b,c][index]});
    const request=cinematicRequest('weights','Riley',runs);
    lines.push(...request.shots.map((_,i)=>({speaker:'Alex',text:weightedSceneReply(request,i)})));
    const review=workbenchDialogue('result','Riley',index?'different':'first',runs);
    assert.equal(review.length,3);assert.equal(review[0].name,'Riley');
    assert.ok(review.every(line=>line.text.split(/\s+/).length<=20));
    lines.push(...review);
   }
   for(const decision of ['keep','revise']){
    const ending=comparisonDialogue('Riley',runs,decision);
    assert.match(ending[0].text,decision==='keep'?/keep this split/:/rethink this setup/);
    const final=[...lines,...ending];
    for(const metric of METRICS){
     const earlier=[...metric.scene,{speaker:'Maya',text:metric.reviewQuestion},...metric.studentReplies.map(text=>({speaker:'Alex',text}))];
     for(const count of [3,6,100])earlier.push(...classroomDialogue(sceneRequest(count,trio,'Riley')),...observationDialogue(count===100,count,trio,'Riley'));
     const texts=[...earlier,...final].map(normalize);
     assert.equal(new Set(texts).size,texts.length,JSON.stringify({trio,history,intents:[a,b,c],duplicates:texts.filter((text,i)=>texts.indexOf(text)!==i)}));
     const emojis=[...earlier,...final].flatMap(line=>[...line.text.matchAll(/\p{Extended_Pictographic}/gu)].map(m=>m[0]));
     assert.equal(new Set(emojis).size,emojis.length,JSON.stringify({trio,history,intents:[a,b,c],metric:metric.id,emojis}));
    }
   }
   paths++;
  }
  assert.equal(paths,trios.length*histories.length*intents.length**3);
 });
 mkdirSync('test-results',{recursive:true});writeFileSync('test-results/player-dialogue-results.json',JSON.stringify({passed:checks.length,checks,trialPurposePaths:paths},null,2)+'\n');
}finally{await server.close()}
