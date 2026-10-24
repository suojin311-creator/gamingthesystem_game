"""Verify all shared chapter entrances, then record one real Level 2 entrance."""
import json,threading,time,subprocess,sys
from pathlib import Path
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'node_modules/.cache/chapter-review';checks=[];errors=[];timings=[]
class Handler(BaseHTTPRequestHandler):
 def do_GET(self):
  data=(OUT/'index.html').read_bytes();self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.end_headers();self.wfile.write(data)
 def log_message(self,*a):pass
server=ThreadingHTTPServer(('127.0.0.1',0),Handler);threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}'
AUDIT='''window.chapterAudit={};
const sample=()=>{const root=document.querySelector('.chapter-transition');if(root?.dataset.beat==='ready'&&!chapterAudit.ready){chapterAudit.ready=performance.now();chapterAudit.question=root.querySelector('.chapter-bridge p')?.textContent;if(getComputedStyle(root.querySelector('.chapter-entry')).animationName==='none')chapterAudit.settled=performance.now();}if(!root&&document.querySelector('.game-page')&&!chapterAudit.entered)chapterAudit.entered=performance.now();};
new MutationObserver(sample).observe(document,{subtree:true,childList:true,attributes:true,attributeFilter:['data-beat','data-phase']});
addEventListener('animationend',event=>{if(event.target.classList.contains('chapter-entry'))chapterAudit.settled=performance.now();});'''
def record(text):checks.append(text);print('PASS',text,flush=True)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 if '--record-only' not in sys.argv:
  for level,query,motion in [(1,'','no-preference'),(2,'','no-preference'),(3,'','no-preference'),(3,'&carried=1','no-preference'),(2,'','reduce')]:
   c=b.new_context(viewport={'width':1440,'height':900},reduced_motion=motion);c.add_init_script(AUDIT);page=c.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
   page.goto(base+f'/?level={level}'+query,wait_until='domcontentloaded');page.wait_for_function('!!chapterAudit.ready');assert page.locator('.chapter-actions button').count()==0
   page.wait_for_function('!!chapterAudit.entered',timeout=10000)
   audit=page.evaluate('chapterAudit');assert audit.get('settled'),audit
   delay=audit['entered']-audit['settled'];assert 1950<=delay<2600,(level,audit)
   assert 'Alex' not in audit['question'];expect(page.locator(f'.level-{[None,"one","two","three"][level]}')).to_be_visible()
   if level in [2,3]:expect(page.locator(f'.level-{[None,"one","two","three"][level]}')).to_have_attribute('data-phase','choose')
   texts=page.evaluate('__teacherReview');assert texts['teacherTexts'] and all('Alex' not in t for t in texts['teacherTexts']);assert texts['studentNames'] and all(t=='Alex' for t in texts['studentNames'])
   timings.append({'level':level,'carried':bool(query),'reducedMotion':motion=='reduce','settledToEntryMs':delay})
   record(f'Level {level}{query}: automatic entry two seconds after the final entrance animation, no button or direct name address ({motion})')
   c.close()
  c=b.new_context(viewport={'width':1440,'height':900});c.add_init_script(AUDIT);page=c.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.goto(base+'/?level=2',wait_until='domcontentloaded');page.wait_for_function('!!chapterAudit.settled');page.evaluate("Object.defineProperty(document,'hidden',{configurable:true,get:()=>true});document.dispatchEvent(new Event('visibilitychange'))")
  page.wait_for_timeout(2500);assert page.locator('.chapter-transition').count()==1
  page.evaluate("delete document.hidden;document.dispatchEvent(new Event('visibilitychange'))");page.wait_for_function('!!chapterAudit.entered',timeout=6000);c.close();record('Background tabs pause the two-second hold, then automatically enter when visible again')
  record('All six Level 1 review questions and all Level 2 teacher conversation branches omit the direct name; student speaker identities remain intact')
 else:
  previous=json.loads((OUT/'validation.json').read_text());checks.extend(c for c in previous['checks'] if not c.startswith('Recorded'));timings.extend(previous['timings'])
 c=b.new_context(viewport={'width':1600,'height':1000},record_video_dir=str(OUT/'video'),record_video_size={'width':1600,'height':1000});c.add_init_script(AUDIT)
 created=time.monotonic();page=c.new_page();video=page.video;page.on('pageerror',lambda e:errors.append(str(e)));page.goto(base+'/?level=2',wait_until='domcontentloaded');page.wait_for_function('!!chapterAudit.entered',timeout=12000);page.wait_for_timeout(2300);c.close();path=video.path();b.close()
 assert not errors,errors
 subprocess.run(['ffmpeg','-y','-i',str(path),'-an','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(ROOT/'play/Chapter-auto-entry-preview.mp4')],stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,check=True)
 record('Recorded one complete Level 2 entrance and the real six-metric selection interface, without clicking an entry button')
server.shutdown();(OUT/'validation.json').write_text(json.dumps({'checks':checks,'timings':timings,'runtimeErrors':errors},indent=2)+'\n')
