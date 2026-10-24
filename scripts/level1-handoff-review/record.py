"""Record actual chapter-to-workbench crossfade and delayed first-use guide."""
import threading,json,subprocess,hashlib
from pathlib import Path
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'node_modules/.cache/level1-handoff-review'
class Handler(BaseHTTPRequestHandler):
 def do_GET(self):
  self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.end_headers();self.wfile.write((OUT/'index.html').read_bytes())
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),Handler);threading.Thread(target=server.serve_forever,daemon=True).start()
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);c=b.new_context(viewport={'width':1600,'height':1000},record_video_dir=str(OUT/'video'),record_video_size={'width':1600,'height':1000})
 c.add_init_script("new MutationObserver(()=>{if(document.querySelector('.workbench-guide[open]')&&!window.guideOpened)window.guideOpened=performance.now();}).observe(document,{subtree:true,childList:true,attributes:true,attributeFilter:['open']});")
 page=c.new_page();video=page.video;errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(f'http://127.0.0.1:{server.server_port}',wait_until='domcontentloaded')
 expect(page.get_by_role('region',name='Level 1 introduction')).to_be_visible()
 expect(page.locator('.handoff-review')).to_have_attribute('data-entering','true',timeout=10000)
 expect(page.locator('.handoff-incoming')).to_have_count(1);expect(page.locator('.handoff-outgoing')).to_have_count(1)
 expect(page.locator('.workbench-guide[open]')).to_have_count(0)
 expect(page.locator('.handoff-review')).to_have_attribute('data-finished','true',timeout=2000)
 expect(page.get_by_role('dialog',name='Workbench guide')).to_be_visible(timeout=2000)
 times=page.evaluate('({start:handoffStarted,finished:handoffFinished,guide:guideOpened})')
 assert 650<times['finished']-times['start']<950,times
 assert times['guide']>times['finished']+150,times
 page.wait_for_timeout(1600);page.get_by_role('button',name='Skip guide',exact=True).click()
 expect(page.locator('.choice-grid .choice-card')).to_have_count(6)
 expect(page.locator('.maya-bubble .speaker-name')).to_have_text('fei')
 expect(page.locator('.gts-audio-controls')).to_have_count(0)
 page.wait_for_timeout(2000)
 page.screenshot(path=str(ROOT/'play/Level1-handoff-preview.png'),full_page=True)
 assert not errors,errors;c.close();source=video.path();b.close()
server.shutdown();output=ROOT/'play/Level1-handoff-preview.mp4'
subprocess.run(['ffmpeg','-y','-i',str(source),'-an','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(output)],stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,check=True)
(ROOT/'play/LEVEL1_HANDOFF_REVIEW.json').write_text(json.dumps({'scope':'Independent transition preview only; formal source and packages unchanged.','video':output.name,'sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'timingsMs':times,'checks':['Actual chapter and Gameplay share a 0.7-second overlap dissolve; no abrupt DOM replacement.','Automatic guide opens only after the incoming workbench finishes fading in.','Guide still works; six real metric options and player name retained.'],'runtimeErrors':errors,'audio':False},indent=2)+'\n')
print(json.dumps(times))
