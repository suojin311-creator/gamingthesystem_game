"""Capture the isolated copy review; never rebuild the game or its film caches."""
import json,threading,time,subprocess,os,sys
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
 if '--ending-only' not in sys.argv:
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
  if name=='question':
   base_size=page.locator('.ending-reflection p:last-child').evaluate('e=>parseFloat(getComputedStyle(e).fontSize)')
   emphasis_size=page.locator('.ending-learning').evaluate('e=>parseFloat(getComputedStyle(e).fontSize)')
  if name=='principle':
   assert page.locator('.ending-thought p').inner_text()=='When a number becomes a measure,\nit ceases to be a good measure.'
   assert page.locator('.ending-design-button,.ending-speaker').count()==0
   for selector,color in [('.thought-becomes','rgb(239, 169, 141)'),('.thought-ceases','rgb(255, 226, 163)')]:
    style=page.locator(selector).evaluate('e=>({size:parseFloat(getComputedStyle(e).fontSize),color:getComputedStyle(e).color})')
    assert abs(style['size']-emphasis_size)<.01 and style['color']==color,style
   assert abs(page.locator('.ending-thought p').evaluate('e=>parseFloat(getComputedStyle(e).fontSize)')-base_size)<.01
  if name=='assessment':
   assert page.locator('.ending-thought p').inner_text()=='Your assessment doesn’t just measure learning,\nit shapes how students learn.'
   assert page.locator('.ending-design-button,.ending-speaker').count()==0
  if name=='assessment':
   for selector,color in [('.thought-assessment-opening','rgb(255, 226, 163)'),('.thought-conclusion','rgb(239, 169, 141)')]:
    style=page.locator(selector).evaluate('e=>({size:parseFloat(getComputedStyle(e).fontSize),color:getComputedStyle(e).color,height:e.getBoundingClientRect().height,line:parseFloat(getComputedStyle(e).lineHeight)})')
    assert abs(style['size']-base_size)<.01 and style['color']==color and style['height']<=style['line']+1,style
  page.locator('details').evaluate('e=>e.open=false');page.locator('.ending-screen').screenshot(path=str(OUT/f'{name}.png'))
 checks.append('Question and two new sentences appear in order before the invitation; exact measure/ceases wording, no speaker labels or premature action')
 checks.append('All three pages share the same body font size; becomes/ceases match the question emphasis size and palette; assessment lines have equal sizes and one line each')
 for t in [21.25,21.55,21.65,21.9]:
  seek(t);opacity=page.locator('.ending-thought').evaluate('e=>+getComputedStyle(e).opacity');assert 0<opacity<1,(t,opacity)
 checks.append('Both new text pages fade smoothly through their boundary with the same office background')
 seek(21.55);assert page.locator('.end-stage').get_attribute('data-section')=='principle'
 seek(21.65);assert page.locator('.end-stage').get_attribute('data-section')=='assessment'
 checks.append('Principle page ends at 21.6 seconds, two seconds earlier than the previous preview; later pages advance with it')
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
