"""Target the actual offline ending ZIP, its real-history shots and final hold."""
import base64, hashlib, json, threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from zipfile import ZipFile
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'test-results';OUT.mkdir(exist_ok=True)
meta=json.loads((ROOT/'play/ENDING_ANIMATION_PREVIEW.json').read_text())
with ZipFile(ROOT/'play'/meta['archive']) as z:
 assert z.testzip() is None
 files={name:z.read(name) for name in z.namelist()}
for name,sha in meta['fileSha256'].items():assert hashlib.sha256(files[name]).hexdigest()==sha
html=files['Ending-animation.html']
for claim in [b'Balancing the weights helped.',b'Alex is spreading his effort more evenly now.',b'Near-equal weights']:
 assert claim not in html,claim
rejected=Path('/tmp/gts-level3a-source/docs/visual-style/references/level3-metric-adaptations/REF-L3A-S10 — High On-Task Focus.png')
if rejected.exists():assert base64.b64encode(rejected.read_bytes()) not in html

class Handler(BaseHTTPRequestHandler):
 def do_GET(self):
  name=self.path.split('?')[0].lstrip('/') or 'START-HERE.html'
  if name not in files:self.send_error(404);return
  self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.end_headers();self.wfile.write(files[name])
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
threading.Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}'
errors=[];external=[];checks=[]
cases={
 'changed':['level3.prep.low','level3.discuss.high','level3.peer.medium'],
 'unchanged':['level3.part.high','level3.focus.medium','level3.reflect.low'],
 'three':['level3.peer.medium','level3.reflect.medium','level3.discuss.medium'],
}
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 context=browser.new_context(viewport={'width':1280,'height':720})
 context.set_default_timeout(30000)
 context.route('**/*',lambda route:route.continue_() if route.request.url.startswith(base) or route.request.url.startswith('data:') else (external.append(route.request.url),route.abort()))
 page=context.new_page();page.on('pageerror',lambda e:(errors.append(str(e)),print('RUNTIME',str(e),flush=True)))
 def seek(time):
  page.locator('input[aria-label="Preview time"]').evaluate("(e,value)=>{const setter=Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set;setter.call(e,String(value));e.dispatchEvent(new Event('input',{bubbles:true}));e.dispatchEvent(new Event('change',{bubbles:true}));}",time)
  page.wait_for_function('t=>Math.abs(Number(document.querySelector(".end-stage").dataset.elapsed)-t)<.006',arg=time)
 def load(case):
  page.goto(base+'/Ending-animation.html?case='+case,wait_until='networkidle')
  page.wait_for_function('!document.querySelector(".ending-loading")')
  page.locator('summary').click();page.get_by_role('button',name='Pause',exact=True).click()
 for case,expected in cases.items():
  load(case);seek(1)
  assert page.locator('.end-office').count()==1 and page.locator('.ending-actual-task,.ending-metric-name').count()==0
  assert page.locator('[role=status]').inner_text()=='Maybe it’s not just about finding the perfect weights…'
  for t in [1,11]:
   seek(t)
   audit=page.locator('.ending-spoken').evaluate("""e=>{const s=e.querySelector('.ending-speaker'),c=e.querySelector('[role=status]'),sr=s.getBoundingClientRect(),cr=c.getBoundingClientRect();return {name:s.textContent,color:getComputedStyle(c).color,labelColor:getComputedStyle(s).color,background:getComputedStyle(c).backgroundColor,above:sr.bottom<=cr.top+.1,centered:Math.abs(sr.x+sr.width/2-cr.x-cr.width/2)<1,text:c.textContent};}""")
   assert audit['name']=='You' and audit['color']==audit['labelColor']=='rgb(255, 226, 163)',audit
   assert audit['above'] and audit['centered'] and audit['background']=='rgba(0, 0, 0, 0)',audit
  source_times=[]
  for time in [8.1,9.7]:
   seek(time)
   assert page.locator('.ending-actual-task').get_attribute('data-scene-id')==expected[-1]
   source_times.append(float(page.locator('.ending-actual-task').get_attribute('data-source-time')))
   assert page.locator('.ending-metric-name').count()==0
   assert page.locator('.l3a-scene').get_attribute('data-beat') not in ['listen-to-peer','reaction','early-classroom','notes-insert']
  assert source_times[1]>source_times[0],source_times
  seek(6.0);assert page.locator('.l2-checklist').get_attribute('data-completed')=='5'
  seek(7.5);assert page.locator('.l2-checklist').get_attribute('data-completed')=='6'
  assert page.locator('.l2-checklist-row-label').count()==6
  assert page.locator('.end-comparison-pair,.l3b-snapshot,.end-convergence').count()==0
  if case=='changed':
   for name,t in [('opening',1),('level1',4.9),('level2',7.4),('level3',9.8),('question',11.5),('quote',21.5)]:
    seek(t);page.locator('.ending-review-controls').evaluate('e=>e.open=false')
    page.locator('.ending-screen').screenshot(path=str(OUT/f'ending-{name}.png'))
   assert page.locator('.ending-design-button').count()==0
  seek(24);assert page.locator('.end-recap-memories,.end-handoff-ghost,.end-dashboard,.ending-metric-name').count()==0
  page.locator('.ending-review-controls').evaluate('e=>e.open=false')
  page.locator('.ending-screen').screenshot(path=str(OUT/f'ending-{case}-final.png'))
  checks.append(case+': office reflection, centred gold You captions, one moving actual Level 3 task, notebook tick from five to six; no metric headers or repeated montage')
  print('PASS',checks[-1],flush=True)
 # Final composition, line layout and the deliberately unconnected button.
 final=page.locator('.ending-screen').evaluate('''e=>{const b=e.querySelector('.ending-design-button'),quote=e.querySelector('.end-theory p'),lines=[...quote.children].map(n=>{const r=n.getBoundingClientRect();return {text:n.textContent,x:r.x,y:r.y,width:r.width,height:r.height};}),r=e.getBoundingClientRect(),br=b.getBoundingClientRect();return {lines,font:parseFloat(getComputedStyle(quote).fontSize),height:r.height,width:r.width,buttonTop:br.top,buttonBottom:br.bottom,quoteBottom:quote.getBoundingClientRect().bottom,disabled:b.getAttribute('aria-disabled'),title:e.querySelector('.end-theory h1').getBoundingClientRect().bottom};}''')
 assert len(final['lines'])==2 and final['lines'][0]['text'].endswith(',') and final['lines'][1]['y']>final['lines'][0]['y'],final
 assert final['font']>40 and final['buttonTop']>final['quoteBottom'] and final['title']<final['lines'][0]['y'],final
 assert final['disabled']=='true'
 previous=page.url
 page.get_by_role('button',name='Go to Design Lab').click(force=True)
 assert page.url==previous and page.locator('.end-theory h1').inner_text()=='Goodhart’s Law'
 checks.append('Theory quote uses two explicit lines split at the comma, larger than 40px at 1280px; distinct button sits below and does not navigate')
 # Mobile landscape and portrait: the entire 16:9 composition is visible.
 for width,height in [(1920,1080),(844,390),(390,844),(320,568)]:
  page.set_viewport_size({'width':width,'height':height})
  fit=page.locator('.ending-screen').evaluate('''e=>{const r=e.getBoundingClientRect(),q=e.querySelector('.end-theory p').getBoundingClientRect(),b=e.querySelector('button').getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height,q:q.bottom,b:b.top,overflow:document.documentElement.scrollWidth>innerWidth};}''')
  assert fit['x']>=-.1 and fit['y']>=-.1 and fit['w']<=width+.1 and fit['h']<=height+.1 and not fit['overflow'] and fit['q']<fit['b'],fit
 checks.append('Full-viewport presentation retains the entire composition and separated quote/button at desktop, mobile landscape and portrait sizes')
 page.set_viewport_size({'width':1280,'height':720})
 # Live cross-dissolve and once-only ending hold. Accelerate only review time.
 load('changed');seek(.5)
 page.evaluate('''()=>{window.audit={dissolve:false,sections:[]};window.timer=setInterval(()=>{const e=document.querySelector('.end-stage'),h=document.querySelector('[data-cinematic-dissolve]');if(!audit.sections.includes(e.dataset.section))audit.sections.push(e.dataset.section);if(h){const opacity=Number(getComputedStyle(h).opacity);if(opacity>0&&opacity<1)audit.dissolve=true;}},20);}''')
 page.get_by_label('Speed',exact=True).select_option('4');page.get_by_role('button',name='Play',exact=True).click()
 page.wait_for_function('document.querySelector(".ending-viewport").dataset.completions==="1"',timeout=35000)
 page.wait_for_timeout(300)
 assert page.locator('.ending-viewport').get_attribute('data-completions')=='1'
 assert page.locator('.end-stage').get_attribute('data-elapsed')=='24.000'
 audit=page.evaluate('()=>{clearInterval(timer);return audit;}')
 assert audit['dissolve'] and audit['sections']==['opening','level1','level2','level3','question','threshold','theory'],audit
 checks.append('Live joins cross-dissolve; playback ends once and holds the theory/button rather than entering another scene')
 page.get_by_role('button',name='Replay',exact=True).click();page.get_by_role('button',name='Pause',exact=True).click()
 assert page.locator('.end-stage').get_attribute('data-section')=='opening'
 seek(1);page.evaluate("()=>{Object.defineProperty(document,'hidden',{configurable:true,value:true});document.dispatchEvent(new Event('visibilitychange'));}")
 page.get_by_role('button',name='Play',exact=True).click();before=page.locator('.end-stage').get_attribute('data-elapsed');page.wait_for_timeout(250)
 assert page.locator('.end-stage').get_attribute('data-elapsed')==before
 checks.append('Replay resets the opening and hidden tabs hold the reading clock')
 context.close();browser.close()
server.shutdown()
assert not errors,errors
assert not external,external
checks.append('ZIP integrity/hashes pass; no runtime errors or external asset requests')
(OUT/'ending-preview-results.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'runtimeErrors':errors,'externalRequests':external,'zipSha256':meta['zipSha256']},ensure_ascii=False,indent=2)+'\n')
print('PASS',len(checks),'ending preview checks',flush=True)
