"""Record the icon-based Level 1 result preview with real management animation."""
import threading,json,subprocess,hashlib
from pathlib import Path
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'node_modules/.cache/level1-icon-review'
class Handler(BaseHTTPRequestHandler):
 def do_GET(self):
  self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.end_headers();self.wfile.write((OUT/'index.html').read_bytes())
 def log_message(self,*a):pass
server=ThreadingHTTPServer(('127.0.0.1',0),Handler);threading.Thread(target=server.serve_forever,daemon=True).start()
errors=[];checks=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 c=b.new_context(viewport={'width':1600,'height':1000},record_video_dir=str(OUT/'video'),record_video_size={'width':1600,'height':1000})
 page=c.new_page();video=page.video;page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(f'http://127.0.0.1:{server.server_port}/?motion=1',wait_until='domcontentloaded')
 root=page.locator('.icon-review');button=page.get_by_role('button',name='Observe the class',exact=True)
 expect(button).to_be_disabled()
 expect(root).to_have_attribute('data-checked','true',timeout=4000)
 expect(page.locator('.l2-eval-result')).to_have_text('Target met')
 expect(root).to_have_attribute('data-reported','true',timeout=2000)
 expect(page.locator('.management-satisfaction-state')).to_have_text('Satisfied')
 expect(page.locator('.management-satisfaction')).to_have_attribute('data-replay-state','complete',timeout=3000)
 expect(root).to_have_attribute('data-question','true',timeout=2000)
 expect(button).to_be_enabled(timeout=1500)
 expect(page.get_by_role('progressbar')).to_have_count(1)
 expect(page.locator('.score-track,.score-numbers,.dialogue-strip')).to_have_count(0)
 assert '%' not in page.locator('.icon-assessment-main').inner_text()
 expect(page.locator('.icon-review-question p')).to_have_text('But… what changed in the classroom?')
 times=page.evaluate('window.iconReviewTimings');order=['targetMet','managementUpdate','managementComplete','questionReveal','buttonEnabled']
 assert all(times[a]<times[b] for a,b in zip(order,order[1:])),times
 checks.append('One metric icon changes from Checking to Target met; no student scores, percentages or progress bar.')
 checks.append('Actual management fill completes before the classroom question and enabled Observe the class button.')
 page.wait_for_timeout(3500)
 image=ROOT/'play/Level1-icon-results-preview.png';page.screenshot(path=str(image),full_page=True)
 c.close();source=video.path()
 c=b.new_context(viewport={'width':390,'height':844},reduced_motion='reduce');page=c.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.goto(f'http://127.0.0.1:{server.server_port}/',wait_until='networkidle')
 assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
 expect(page.get_by_role('progressbar')).to_have_count(1)
 checks.append('390px layout fits; reduced-motion static state retains one management progress indicator.')
 c.close();assert not errors,errors;b.close()
server.shutdown()
video=ROOT/'play/Level1-icon-results-preview.mp4'
subprocess.run(['ffmpeg','-y','-i',str(source),'-an','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,check=True)
(ROOT/'play/LEVEL1_ICON_RESULTS_REVIEW.json').write_text(json.dumps({'scope':'Independent visual preview only; formal source and game packages unchanged.','video':video.name,'videoSha256':hashlib.sha256(video.read_bytes()).hexdigest(),'image':image.name,'timingsMs':times,'checks':checks,'runtimeErrors':errors,'audio':False},indent=2)+'\n')
print(json.dumps({'checks':checks,'timingsMs':times}))
