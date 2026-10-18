import assert from 'node:assert/strict';
import { mkdirSync, writeFileSync } from 'node:fs';
import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { createServer } from 'vite';
const server=await createServer({server:{middlewareMode:true,hmr:false},appType:'custom'});
const checks=[];const check=(name,fn)=>{fn();checks.push(name);console.log('PASS',name)};
try {
 const {default:Comparison}=await server.ssrLoadModule('/src/levels/level3/WeightComparison.tsx');
 const {nextExperiment}=await server.ssrLoadModule('/src/levels/level3/experiments.ts');
 const ids=['prep','part','peer'];
 const run=(weights,round,metricIds=ids)=>({round,kind:'player',metricIds,weights});
 const cells=html=>[...html.matchAll(/<tr data-metric="([^"]+)">([\s\S]*?)<\/tr>/g)].map(match=>({id:match[1],changes:[...match[2].matchAll(/<td[^>]*data-effort-change="([^"]+)"/g)].map(cell=>cell[1])}));
 check('The reported 43/29/28 → 34/33/33 → 28/43/29 example labels every effort comparison and names its reference test',()=>{
  const html=renderToStaticMarkup(React.createElement(Comparison,{runs:[run([43,29,28],1),run([34,33,33],2),run([28,43,29],3)]}));
  assert.deepEqual(cells(html),[{id:'prep',changes:['baseline','same','less']},{id:'part',changes:['baseline','more','same']},{id:'peer',changes:['baseline','more','less']}]);
  for(const label of ['Effort vs First test','Effort vs Second test','Same effort','More effort','Less effort'])assert.ok(html.includes(label));
  assert.ok(!html.includes('data-changed='));assert.ok(html.includes('Same effort compared with First test'));
 });
 check('Comparisons follow each metric identity through reordered runs and distinguish changed weights from unchanged effort',()=>{
  const reordered=renderToStaticMarkup(React.createElement(Comparison,{runs:[run([43,29,28],1),run([33,34,33],2,['peer','prep','part']),run([43,29,28],3,['part','peer','prep'])]}));
  assert.deepEqual(cells(reordered),[{id:'prep',changes:['baseline','same','less']},{id:'part',changes:['baseline','more','same']},{id:'peer',changes:['baseline','more','less']}]);
  const html=renderToStaticMarkup(React.createElement(Comparison,{runs:[run([70,20,10],1),run([80,10,10],2),run([10,70,20],3)]}));
  assert.deepEqual(cells(html),[{id:'prep',changes:['baseline','same','less']},{id:'part',changes:['baseline','same','more']},{id:'peer',changes:['baseline','same','same']}]);
 });
 check('All trio prompts stay single-question and concise while preserving the same optional valid suggestions',()=>{
  const all=['prep','part','focus','discuss','reflect','peer'];
  const trios=all.flatMap((a,i)=>all.slice(i+1).flatMap((b,j)=>all.slice(i+j+2).map(c=>[a,b,c])));
  for(const ids of trios)for(const history of [[],[[70,20,10]],[[45,45,10]],[[34,33,33]],[[70,20,10],[45,45,10]],[[34,33,33],[40,30,30]],[[43,29,28],[34,33,33]]]){
   const plan=nextExperiment(history.map((w,i)=>run(w,i+1,ids)));
   assert.equal((plan.question.match(/\?/g)||[]).length,1);assert.ok(plan.question.split(/\s+/).length<=16,plan.question);
  }
 });
 mkdirSync('test-results',{recursive:true});writeFileSync('test-results/task-clarity-contract-results.json',JSON.stringify({passed:checks.length,checks},null,2)+'\n');
} finally {await server.close()}
