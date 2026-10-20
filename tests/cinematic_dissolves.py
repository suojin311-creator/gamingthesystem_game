"""Check changed Level 1/2 joins directly, without replaying full game paths."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
OUT=Path('test-results');errors=[];checks=[]
films={name:Path(f'node_modules/.cache/{name}-cinematic/index.html').read_bytes() for name in ['level1','level2']}
configs=[{'channel':'level1-settlement-review','type':'start','runId':'soft','metric':'pre-class-preparation','playerName':'Riley','reducedMotion':False},
 *[{'channel':'level2-cinematic','type':'start','runId':'soft','preview':True,'reducedMotion':False,'request':{'sceneId':'level2.'+kind,'kind':kind,'branch':'mixed','selectedMetricIds':['prep','discuss','peer'],'playerName':'Riley'}} for kind in ['three','checklist']]]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 context=browser.new_context(viewport={'width':1280,'height':720});context.set_default_timeout(30000)
 active=[configs[0]];movie=['level1']
 def serve(route):
  if route.request.url.endswith('/film.html'):route.fulfill(content_type='text/html',body=films[movie[0]])
  else:
   config=json.dumps(active[0])
   route.fulfill(content_type='text/html',body=('''<!doctype html><style>html,body{margin:0;width:100%;height:100%}iframe{border:0;width:100%;height:100%}</style><script>window.done=0;addEventListener('message',e=>{if(e.source!==frames[0])return;if(e.data.type==='ready')frames[0].postMessage(CONFIG,'*');if(e.data.type==='complete')window.done++});window.send=(action,value)=>frames[0].postMessage({channel:'level2-cinematic',type:'control',runId:'soft',action,value},'*');</script><iframe name="film" src="/film.html"></iframe>'''.replace('CONFIG',config)))
 context.route('https://dissolves.test/**',serve)
 page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
 for config in configs:
  active[0]=config;movie[0]='level1' if 'metric' in config else 'level2'
  page.goto('https://dissolves.test/',wait_until='networkidle');frame=page.frame(name='film')
  cls='.l1-film' if movie[0]=='level1' else '.l2-film'
  frame.wait_for_selector(cls)
  frame.evaluate('''cls=>{window.audit={intermediate:false,black:false,captions:[]};const root=document.querySelector(cls),cover=root.querySelector('[class$="cover"]');window.timer=setInterval(()=>{const h=document.querySelector('[data-cinematic-dissolve]');if(h){const o=Number(getComputedStyle(h).opacity);if(o>0&&o<1)window.audit.intermediate=true;if(Number(getComputedStyle(cover).opacity)>.001)window.audit.black=true;}if(root.dataset.shot==='reflection'){const text=root.querySelector('[role=status]')?.textContent;if(text&&!window.audit.captions.includes(text))window.audit.captions.push(text);}},15);}''',cls)
  if movie[0]=='level1':
   frame.wait_for_function("document.querySelector('.l1-film').dataset.handoff==='done'")
   frame.locator('.l1-film').screenshot(path=str(OUT/'level1-soft-office-join.png'))
  else:
   page.evaluate("send('speed',4)")
   page.wait_for_function('window.done===1',timeout=35000)
   page.wait_for_timeout(150);assert page.evaluate('window.done')==1
  audit=frame.evaluate('()=>{clearInterval(window.timer);return window.audit;}')
  assert audit['intermediate'] and not audit['black'],audit
  if config.get('request',{}).get('kind')=='checklist':assert audit['captions']==['Maybe adding more metrics isn’t the answer...','What if some metrics mattered more than others?'],audit
  checks.append(movie[0]+': '+config.get('request',{}).get('kind','classroom → office')+' cross-dissolves without an internal black cover; reflection captions and single completion preserved')
  print('PASS',checks[-1],flush=True)
 context.close();browser.close()
assert not errors,errors
(OUT/'cinematic-dissolve-results.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'runtimeErrors':errors},indent=2)+'\n')
