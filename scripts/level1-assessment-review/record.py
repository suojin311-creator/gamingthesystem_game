"""Record real browser playback of the proposed assessment sequence."""
import threading,json,subprocess
from pathlib import Path
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'node_modules/.cache/level1-assessment-review'
class Handler(BaseHTTPRequestHandler):
 def do_GET(self):
  self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.end_headers();self.wfile.write((OUT/'index.html').read_bytes())
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),Handler);threading.Thread(target=server.serve_forever,daemon=True).start()
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 context=browser.new_context(viewport={'width':1600,'height':1000},record_video_dir=str(OUT/'video'),record_video_size={'width':1600,'height':1000})
 page=context.new_page();video=page.video;errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(f'http://127.0.0.1:{server.server_port}/?motion=1',wait_until='domcontentloaded')
 root=page.locator('.assessment-review');button=page.get_by_role('button',name='Look behind the number',exact=True)
 expect(button).to_be_disabled()
 expect(page.locator('.management-satisfaction-state')).to_have_text('Awaiting results')
 expect(root).to_have_attribute('data-ready','true',timeout=5000)
 expect(page.locator('.after-score')).to_contain_text('85%')
 expect(root).to_have_attribute('data-reported','true',timeout=2500)
 expect(page.locator('.management-satisfaction-state')).to_have_text('Satisfied')
 expect(root).to_have_attribute('data-bridge','true',timeout=2500)
 expect(button).to_be_disabled()
 expect(button).to_be_enabled(timeout=2000)
 expect(page.locator('.dialogue-strip .speaker-name')).to_have_text('fei')
 expect(page.locator('.dialogue-strip p')).to_have_text('More students met the criteria. What happened in class?')
 times=page.evaluate('window.assessmentTimings')
 assert times['numberStart']<times['numberComplete']<times['managementUpdate']<times['bridgeReveal']<times['butAndButton'],times
 assert times['managementUpdate']-times['numberComplete']>=850,times
 assert times['bridgeReveal']-times['managementUpdate']>=1250,times
 page.wait_for_timeout(3500)
 page.locator('.assessment-review').screenshot(path=str(ROOT/'play/Level1-assessment-preview.png'))
 assert not errors,errors
 context.close();source=video.path();browser.close()
server.shutdown()
output=ROOT/'play/Level1-assessment-preview.mp4'
subprocess.run(['ffmpeg','-y','-i',str(source),'-an','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(output)],stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,check=True)
(ROOT/'play/LEVEL1_ASSESSMENT_VIDEO_REVIEW.json').write_text(json.dumps({'scope':'Independent browser preview; formal game unchanged.','video':output.name,'timingsMs':times,'checks':['Animated actual ResultChart data, then updated actual ManagementSatisfaction status.','Bridge reveal follows management update; But and enabled Look behind the number follow bridge.','Original teacher dialogue retained in separate shaded bottom strip.'],'runtimeErrors':errors,'audio':False},indent=2)+'\n')
print(json.dumps(times))
