"""The real game cinematic host must play the approved 100-metric edit and return once.
Requires the normal Vite server; no ZIP rebuild or full-game path replay.
"""
import json,os
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'test-results';OUT.mkdir(exist_ok=True)
base=os.environ.get('GAME_TEST_URL','http://127.0.0.1:5173')
(OUT/'metric100-game-host.html').write_text('''<!doctype html><html><head><style>body{margin:0;background:#f8f4ea}</style></head><body><div id="root"></div><script type="module">
import React from 'react';import {createRoot} from 'react-dom/client';import LevelTwoCinematic from '/src/cinematics/level2/LevelTwoCinematic.tsx';
window.finishedCount=0;
function Host(){const [done,setDone]=React.useState(false);return done?React.createElement('p',{id:'returned'},'Returned to the game'):React.createElement(LevelTwoCinematic,{request:{sceneId:'level2.checklist',kind:'checklist',branch:'mixed',playerName:'Riley & 李',selectedMetricIds:['prep','part','focus'],metricCount:100},onComplete:()=>{window.finishedCount++;window.review=structuredClone(document.querySelector('iframe').contentWindow.gameAudit);setDone(true);}});}
createRoot(document.getElementById('root')).render(React.createElement(Host));
</script></body></html>''')
errors=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1440,'height':900});page.on('pageerror',lambda e:errors.append(str(e)))
 page.add_init_script('''(()=>{
 window.gameAudit={shots:[],lines:[],entered:null,captionAt:null,start:null,paper:false,errors:[],final:false};
 const seen=new Set();const visible=e=>!!e&&e.getClientRects().length>0&&getComputedStyle(e).visibility!=='hidden';
 const timer=setInterval(()=>{
  const f=document.querySelector('.l2-film');if(!f)return;const a=gameAudit;
  if(!a.shots.includes(f.dataset.shot))a.shots.push(f.dataset.shot);
  if(a.start===null)a.start={shot:f.dataset.shot,mode:f.querySelector('.l2-checking')?.dataset.checkingShot,criterion:f.querySelector('.l2-checking-pen-anchor')?.closest('[data-criterion]')?.dataset.criterion,name:f.dataset.playerName};
  if(f.dataset.shot==='reflection'&&a.entered===null)a.entered=performance.now();
  if(f.dataset.shot==='hundred'&&f.querySelector('.l2-scene')?.dataset.performance==='world'){
   const lists=f.querySelectorAll('.l2-checklist');
   for(const list of lists){
    const nodes=['.l2-checklist-header','.l2-checklist-tally','.l2-checklist-evidence-strip','.l2-checklist-footer'];
    if(list.querySelectorAll('.l2-checklist-row-label').length===100&&list.querySelectorAll('.l2-checklist-evidence-ref').length===100&&nodes.every(s=>visible(list.querySelector(s))))a.paper=true;
   }
  }
  if([...f.querySelectorAll('.l2-chapter,.l2-stage-caption,.l2-reference-credit,.l2-dialogue,.l2-priority,.l2-priority-question')].some(visible))a.errors.push('Extra visible overlay');
  const caption=f.querySelector('.l2-spoken'),text=caption?.querySelector('[role=status]'),label=caption?.querySelector('.l2-speaker');
  if(text){
   if(a.captionAt===null)a.captionAt=performance.now();
   if(!a.lines.includes(text.textContent))a.lines.push(text.textContent);
   const l=label.getBoundingClientRect(),c=text.getBoundingClientRect();
   if(label.textContent!=='You'||getComputedStyle(text).color!=='rgb(255, 226, 163)'||getComputedStyle(label).color!=='rgb(255, 226, 163)'||getComputedStyle(text).backgroundColor!=='rgba(0, 0, 0, 0)'||l.bottom>c.top+.1||Math.abs(l.x+l.width/2-c.x-c.width/2)>1)a.errors.push('Caption standard mismatch');
   if(Number(getComputedStyle(f.querySelector('.l2-film-cover')).opacity)>0)a.errors.push('Final caption covered before it ends');
  }
  if(f.dataset.finished==='true'){a.final={time:Number(f.dataset.elapsed),duration:Number(f.dataset.duration),text:text?.textContent,cover:Number(getComputedStyle(f.querySelector('.l2-film-cover')).opacity)};clearInterval(timer);}
 },10);
})();''')
 page.goto(base+'/test-results/metric100-game-host.html',wait_until='networkidle',timeout=60000)
 expect(page.locator('#returned')).to_be_visible(timeout=25000)
 page.wait_for_timeout(300);assert page.evaluate('finishedCount')==1
 audit=page.evaluate('review')
 assert audit['start']=={'shot':'hundred','mode':'insert','criterion':'66','name':'Riley & 李'},audit
 assert audit['shots']==['hundred','reflection'] and audit['paper'] and not audit['errors'],audit
 assert audit['lines']==['Maybe adding more metrics isn’t the answer...','What if some metrics mattered more than others?'],audit
 delay=(audit['captionAt']-audit['entered'])/1000;assert .75<delay<1.3,audit
 assert audit['final'] and abs(audit['final']['time']-audit['final']['duration'])<.002 and audit['final']['cover']==0,audit
 assert audit['final']['text']==audit['lines'][-1],audit
 browser.close()
assert not errors,errors
report={'passed':4,'checks':['Game host begins on the Criterion 66 insert and preserves the complete Coverage map','Conversation begins captions about one second after entry with the approved You/caption styling','Only hundred/reflection shots play; final dialogue remains uncovered until completion','Real LevelTwoCinematic callback fires once and returns control to the game'], 'realSecondsBeforeFirstSubtitle':delay,'audit':audit,'runtimeErrors':errors,'zipArchivesUpdated':False}
(OUT/'metric100-game-integration-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
for check in report['checks']:print('PASS',check,flush=True)
