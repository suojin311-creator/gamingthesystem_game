"""Only the newly requested 100-metric review, from the actual standalone ZIP."""
import hashlib,json,threading
from pathlib import Path
from zipfile import ZipFile
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'test-results';OUT.mkdir(exist_ok=True)
meta=json.loads((ROOT/'play/LEVEL2_100METRICS_PREVIEW.json').read_text());archive=ROOT/'play'/meta['archive']
assert hashlib.sha256(archive.read_bytes()).hexdigest()==meta['zipSha256']
with ZipFile(archive) as z:
 assert z.testzip() is None;files={n:z.read(n) for n in z.namelist()}
for name,digest in meta['fileSha256'].items():assert hashlib.sha256(files[name]).hexdigest()==digest
class Handler(BaseHTTPRequestHandler):
 def do_GET(self):
  data=files.get(self.path.split('?')[0].lstrip('/'))
  if data is None:self.send_error(404);return
  self.send_response(200);self.send_header('Content-Type','text/html');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),Handler);threading.Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}';errors=[];external=[];checks=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 context=browser.new_context(viewport={'width':1440,'height':900})
 context.route('**/*',lambda r:r.continue_() if r.request.url.startswith(base) or r.request.url.startswith('data:') else (external.append(r.request.url),r.abort()))
 page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(base+'/START-HERE.html',wait_until='networkidle');page.wait_for_function('!document.querySelector(".hundred-loading")')
 page.locator('summary').click();page.get_by_role('button',name='Pause',exact=True).click()
 def seek(t):
  page.get_by_label('Preview time').evaluate("(e,t)=>{Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(e,t);e.dispatchEvent(new Event('input',{bubbles:true}));e.dispatchEvent(new Event('change',{bubbles:true}));}",t)
  page.wait_for_function('t=>Math.abs(Number(document.querySelector(".hundred-film").dataset.time)-t)<.006',arg=t)
 def no_overlays():assert page.locator('.l2-chapter,.l2-stage-caption,.l2-reference-credit,.l2-dialogue,.l2-priority,.l2-priority-question').count()==0
 seek(0);no_overlays()
 assert page.locator('.l2-checking').get_attribute('data-checking-shot')=='insert'
 assert page.locator('.l2-checking [data-criterion="66"]').get_attribute('class').endswith('is-next')
 assert page.locator('.l2-checking-hand').count()==1 and page.locator('.hundred-caption').count()==0
 page.locator('details').evaluate('e=>e.open=false');page.screenshot(path=str(OUT/'metric100-first-frame.png'))
 checks.append('Starts on the original Criterion 66 checking insert; no establishing frame or title overlays')
 seek(2.5);no_overlays()
 expect(page.locator('.l2-checklist-header h3')).to_have_text('Coverage map')
 for selector,count in [('.l2-checklist-row-label',100),('.l2-checklist-evidence-ref',100),('.l2-checklist-evidence-slip',3)]:expect(page.locator(selector)).to_have_count(count)
 for selector in ['.l2-checklist-header','.l2-checklist-tally','.l2-checklist-margin-note','.l2-checklist-footer']:
  assert page.locator(selector).is_visible(),selector
 page.screenshot(path=str(OUT/'metric100-complete-map.png'))
 checks.append('Original full Coverage map, tally, evidence slips/references, criterion labels and footer remain intact')
 # Read exact edit boundaries from the same authored timeline (no guessed delay).
 import subprocess
 timing=json.loads(subprocess.check_output(['node','--input-type=module','-e',"import {createHundredPacing} from './scripts/metric100-preview/pacing.mjs';const shots=[{id:'hundred',duration:5.9},{id:'perfect',duration:5.3},{id:'reflection',duration:5.1,dialogue:[{start:.1,end:2.35,speaker:'You',text:'Maybe adding more metrics isn’t the answer...'},{start:2.7,end:5.05,speaker:'You',text:'What if some metrics mattered more than others?'}]},{id:'priority',duration:2.9}];console.log(JSON.stringify(createHundredPacing(shots)));"],cwd=ROOT,text=True))
 enter=timing['conversationAt'];first=timing['firstSubtitleAt'];duration=timing['duration']
 seek(enter+.99);assert page.locator('.hundred-caption').count()==0
 seek(first+.02);no_overlays()
 expect(page.locator('.hundred-caption [role=status]')).to_have_text('Maybe adding more metrics isn’t the answer...')
 audit=page.locator('.hundred-caption').evaluate("""e=>{const s=e.querySelector('.hundred-speaker'),c=e.querySelector('[role=status]'),a=s.getBoundingClientRect(),b=c.getBoundingClientRect();return {speaker:s.textContent,color:getComputedStyle(c).color,labelColor:getComputedStyle(s).color,above:a.bottom<=b.top+.1,centered:Math.abs(a.x+a.width/2-b.x-b.width/2)<1,background:getComputedStyle(c).backgroundColor,style:getComputedStyle(c).fontStyle};}""")
 assert audit=={'speaker':'You','color':'rgb(255, 226, 163)','labelColor':'rgb(255, 226, 163)','above':True,'centered':True,'background':'rgba(0, 0, 0, 0)','style':'italic'},audit
 page.screenshot(path=str(OUT/'metric100-dialogue.png'))
 checks.append('First subtitle begins exactly one playhead second after entering the conversation; You is gold and centred above transparent italic dialogue')
 # Observe a live entrance: the dissolve must not add a hidden pause to that second.
 seek(enter-.1)
 page.evaluate("""()=>{window.audit={enter:null,caption:null,shots:[],dissolve:false};window.timer=setInterval(()=>{const f=document.querySelector('.hundred-film'),d=document.querySelector('[data-cinematic-dissolve]');if(!audit.shots.includes(f.dataset.shot))audit.shots.push(f.dataset.shot);if(d){const o=Number(getComputedStyle(d).opacity);if(o>0&&o<1)audit.dissolve=true;}if(f.dataset.shot==='reflection'&&audit.enter===null)audit.enter=performance.now();if(document.querySelector('.hundred-caption')&&audit.caption===null)audit.caption=performance.now();},10);}""")
 page.locator('details').evaluate('e=>e.open=true');page.get_by_role('button',name='Play',exact=True).click()
 page.wait_for_function('document.querySelector(".hundred-film").dataset.finished==="true"',timeout=18000)
 observed=page.evaluate('()=>{clearInterval(timer);return audit;}')
 assert observed['dissolve'] and .75<(observed['caption']-observed['enter'])/1000<1.25,observed
 assert observed['shots']==['hundred','reflection'],observed
 expect(page.locator('.hundred-caption [role=status]')).to_have_text('What if some metrics mattered more than others?')
 no_overlays();assert abs(float(page.locator('.hundred-film').get_attribute('data-time'))-duration)<.006
 end=page.locator('.hundred-film').get_attribute('data-source');page.wait_for_timeout(600)
 assert page.locator('.hundred-film').get_attribute('data-source')==end and float(end)<16.3
 checks.append('Live dissolve adds no extra wait: first caption follows entrance by about one real second; stops after the original last line with no priority or extra scene')
 page.get_by_role('button',name='Replay',exact=True).click();page.get_by_role('button',name='Pause',exact=True).click();seek(0)
 assert page.locator('.hundred-film').get_attribute('data-finished')=='false'
 checks.append('Replay returns to the checking insert; ZIP hashes pass and all resources are embedded')
 browser.close()
server.shutdown();assert not errors,errors;assert not external,external
report={'passed':len(checks),'checks':checks,'runtimeErrors':errors,'externalRequests':external,'realSecondsBeforeFirstSubtitle':(observed['caption']-observed['enter'])/1000,'zipSha256':meta['zipSha256']}
(OUT/'metric100-preview-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
for check in checks:print('PASS',check,flush=True)
