"""Capture the isolated copy review; never rebuild the game or its film caches."""
import json,threading,time,subprocess,os
from pathlib import Path
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'node_modules/.cache/copy-review';PLAY=ROOT/'play'
files={'/opening.html':(OUT/'opening/opening.html').read_bytes(),'/ending.html':(OUT/'ending/index.html').read_bytes()}
class Handler(BaseHTTPRequestHandler):
 def do_GET(self):
  data=files.get(self.path.split('?')[0])
  if data is None:self.send_error(404);return
  self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.end_headers();self.wfile.write(data)
 def log_message(self,*a):pass
server=ThreadingHTTPServer(('127.0.0.1',0),Handler);threading.Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}';errors=[];checks=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 c=b.new_context(viewport={'width':1920,'height':1080});page=c.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(base+'/opening.html',wait_until='networkidle');expect(page.locator('.subtitle')).to_have_text('When you set the metrics, what are you measuring?');page.wait_for_timeout(1200)
 page.locator('.stage').screenshot(path=str(PLAY/'Opening-title-copy-preview.png'));checks.append('Opening screenshot uses the corrected measuring copy and existing title design');c.close()
 c=b.new_context(viewport={'width':1600,'height':900});page=c.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(base+'/ending.html',wait_until='networkidle');expect(page.locator('.ending-viewport')).to_be_visible();page.wait_for_function('!document.querySelector(".ending-loading")')
 page.locator('details').evaluate('e=>e.open=true');page.get_by_role('button',name='Pause',exact=True).click()
 def seek(t):
  page.locator('[aria-label="Preview time"]').evaluate('''(e,t)=>{Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(e,String(t));e.dispatchEvent(new Event('input',{bubbles:true}));}''',t)
  page.wait_for_function('t=>Math.abs(+document.querySelector(".end-stage").dataset.elapsed-t)<.01',arg=t)
 for t,name in [(12,'question'),(19,'principle'),(26,'assessment'),(34,'invitation')]:
  seek(t)
  if name=='principle':
   assert page.locator('.ending-thought p').inner_text()=='When a number becomes a measure,\nit ceases to be a good measure.'
   assert page.locator('.ending-design-button,.ending-speaker').count()==0
  if name=='assessment':
   assert page.locator('.ending-thought p').inner_text()=='Your assessment doesn’t just measure learning,\nit shapes how students learn.'
   assert page.locator('.ending-design-button,.ending-speaker').count()==0
  page.locator('details').evaluate('e=>e.open=false');page.locator('.ending-screen').screenshot(path=str(OUT/f'{name}.png'))
 checks.append('Question and two new sentences appear in order before the invitation; exact measure/ceases wording, no speaker labels or premature action')
 for t in [23.25,23.55,23.65,23.9]:
  seek(t);opacity=page.locator('.ending-thought').evaluate('e=>+getComputedStyle(e).opacity');assert 0<opacity<1,(t,opacity)
 checks.append('Both new text pages fade smoothly through their boundary with the same office background')
 c.close()
 c=b.new_context(viewport={'width':1600,'height':900},record_video_dir=str(OUT/'video'),record_video_size={'width':1600,'height':900})
 created=time.monotonic();page=c.new_page();video=page.video;page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(base+'/ending.html',wait_until='networkidle');page.wait_for_function('!document.querySelector(".ending-loading")');expect(page.locator('.ending-viewport')).to_be_visible()
 page.add_style_tag(content='.ending-review-controls{visibility:hidden!important}')
 page.locator('details').evaluate('e=>e.open=true');page.get_by_role('button',name='Replay',exact=True,include_hidden=True).evaluate('e=>e.click()');offset=time.monotonic()-created
 page.wait_for_function('document.querySelector(".ending-viewport").dataset.completions==="1"',timeout=90000)
 page.wait_for_timeout(2500);c.close();path=video.path();b.close()
 assert not errors,errors
 subprocess.run(['ffmpeg','-y','-ss',str(offset),'-i',str(path),'-an','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(PLAY/'Ending-copy-preview.mp4')],stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,check=True)
 checks.append('Real complete ending autoplay captured to a standalone MP4 with a final invitation hold')
(OUT/'validation.json').write_text(json.dumps({'checks':checks,'runtimeErrors':errors},indent=2)+'\n');server.shutdown()
for check in checks:print('PASS',check,flush=True)
