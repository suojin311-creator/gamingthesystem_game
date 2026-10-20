"""Target the actual offline ending ZIP, its real-history shots and final hold."""
import base64, hashlib, json, sys, threading
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
closing_only='--closing-only' in sys.argv
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
  if closing_only:
   load(case);seek(9.4)
   assert page.locator('.end-memory-caption p').inner_text()=='The weights changed. Learning still came second.'
   assert page.locator('.ending-metric-name').count()==0
   page.locator('details').evaluate('e=>e.open=false')
   page.locator('.ending-screen').screenshot(path=str(OUT/'ending-level3.png'))
   seek(24)
   page.locator('.ending-screen').screenshot(path=str(OUT/'ending-changed-final.png'))
   checks.append('Level 3 recap uses the accepted negative consequence and still omits metric headings')
   break
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
   for name,t in [('opening',1),('level1',4.9),('level2',7.4),('level3',9.8),('question',11.5),('handoff',18.4)]:
    seek(t);page.locator('.ending-review-controls').evaluate('e=>e.open=false')
    page.locator('.ending-screen').screenshot(path=str(OUT/f'ending-{name}.png'))
   assert page.locator('.ending-design-button').count()==0
  seek(24);assert page.locator('.end-recap-memories,.end-handoff-ghost,.end-dashboard,.ending-metric-name,.end-theory').count()==0
  page.locator('.ending-review-controls').evaluate('e=>e.open=false')
  page.locator('.ending-screen').screenshot(path=str(OUT/f'ending-{case}-final.png'))
  checks.append(case+': office reflection, centred gold You captions, one moving actual Level 3 task, notebook tick from five to six; no metric headers or repeated montage')
  print('PASS',checks[-1],flush=True)
 # The final screen explains the next activity, rather than ending on a quote.
 assert page.locator('.ending-closing-rule,.end-theory-rule,.end-theory,.end-convergence').count()==0
 assert page.locator('.ending-destination').inner_text()=='NEXT · DESIGN LAB'
 assert page.locator('#ending-next-title').inner_text()=='Share what real\nlearning looks like.'
 assert page.locator('.ending-game-connection').inner_text()=='You’ve seen how numbers shaped Alex’s choices.'
 assert page.locator('.ending-next-task').inner_text()=='Now write a short reflection, then read and vote on your classmates’ ideas.'
 assert 'Goodhart' not in page.locator('.ending-screen').inner_text()
 previous=page.url
 assert page.locator('.ending-design-button').get_attribute('aria-disabled')=='true'
 page.get_by_role('button',name='ENTER DESIGN LAB').click(force=True)
 assert page.url==previous and page.locator('.ending-handoff').is_visible()
 checks.append('Destination, connection to Alex, reflection/read/vote task and single entry action are explicit; decorative rule and premature theory reveal are absent')
 # At small sizes the entry page uses the viewport rather than shrinking prose
 # into a letterboxed film. All guidance and the action must remain reachable.
 for width,height in [(1280,720),(1920,1080),(1440,900),(844,390),(640,360),(390,844),(320,568)]:
  page.set_viewport_size({'width':width,'height':height})
  fit=page.locator('.ending-handoff').evaluate("""e=>{const r=e.getBoundingClientRect(),copy=e.querySelector('.ending-handoff-copy').getBoundingClientRect(),t=e.querySelector('h1').getBoundingClientRect(),q=e.querySelector('.ending-next-task').getBoundingClientRect(),b=e.querySelector('button').getBoundingClientRect();return {width:r.width,height:r.height,copyLeft:copy.left,copyRight:copy.right,copyTop:copy.top,copyBottom:copy.bottom,clear:t.bottom<q.top&&q.bottom<b.top,font:parseFloat(getComputedStyle(e.querySelector('.ending-next-task')).fontSize),overflow:document.documentElement.scrollWidth>innerWidth};}""")
  assert abs(fit['width']-width)<1 and abs(fit['height']-height)<1 and not fit['overflow'],fit
  assert fit['copyLeft']>=0 and fit['copyRight']<=width+.1 and fit['copyTop']>=0 and fit['copyBottom']<=height-20 and fit['clear'] and fit['font']>=14,fit
  if (width,height) in [(1280,720),(390,844)]:
   page.screenshot(path=str(OUT/f'ending-handoff-{width}.png'))
 checks.append('Seven desktop/landscape/portrait sizes retain readable full-viewport guidance and a visible non-overlapping action')
 page.set_viewport_size({'width':1280,'height':720})
 if closing_only:
  seek(16.6)
  before=page.locator('.end-office-night').evaluate('e=>Number(getComputedStyle(e).opacity)')
  assert page.locator('.ending-design-button').count()==0
  seek(18.4)
  after=page.locator('.end-office-night').evaluate('e=>Number(getComputedStyle(e).opacity)')
  assert after<before and page.locator('.ending-design-button').count()==0
  seek(19.2);assert page.locator('.ending-design-button').is_visible()
  page.locator('summary').click();page.get_by_role('button',name='Replay',exact=True).click();page.get_by_role('button',name='Pause',exact=True).click()
  assert page.locator('.ending-handoff').count()==0 and page.locator('.ending-screen').get_attribute('data-layout')=='film'
  checks.append('Office lighting/content fade into the task page before its action appears; replay restores the cinematic layout')
 if not closing_only:
  # Live cross-dissolve and once-only ending hold. Accelerate only review time.
  load('changed');seek(.5)
  page.evaluate('''()=>{window.audit={dissolve:false,sections:[]};window.timer=setInterval(()=>{const e=document.querySelector('.end-stage'),h=document.querySelector('[data-cinematic-dissolve]');if(!audit.sections.includes(e.dataset.section))audit.sections.push(e.dataset.section);if(h){const opacity=Number(getComputedStyle(h).opacity);if(opacity>0&&opacity<1)audit.dissolve=true;}},20);}''')
  page.get_by_label('Speed',exact=True).select_option('4');page.get_by_role('button',name='Play',exact=True).click()
  page.wait_for_function('document.querySelector(".ending-viewport").dataset.completions==="1"',timeout=35000)
  page.wait_for_timeout(300)
  assert page.locator('.ending-viewport').get_attribute('data-completions')=='1'
  assert page.locator('.end-stage').get_attribute('data-elapsed')=='24.000'
  audit=page.evaluate('()=>{clearInterval(timer);return audit;}')
  assert audit['dissolve'] and audit['sections']==['opening','level1','level2','level3','question','threshold','closing'],audit
  checks.append('Live joins cross-dissolve; playback ends once and holds the closing/button rather than entering another scene')
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
