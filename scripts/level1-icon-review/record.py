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
 expect(page.locator('.metric-option')).to_have_count(6)
 before=page.locator('.selected-metric-card').bounding_box()
 page.screenshot(path=str(ROOT/'play/Level1-icon-results-overview.png'),full_page=True)
 expect(root).to_have_attribute('data-checked','true',timeout=4000)
 expect(page.locator('.l2-eval-result')).to_have_text('Target met')
 expect(root).to_have_attribute('data-reported','true',timeout=2000)
 expect(page.locator('.management-satisfaction-state')).to_have_text('Satisfied')
 expect(page.locator('.management-satisfaction')).to_have_attribute('data-replay-state','complete',timeout=3000)
 expect(button).to_be_enabled(timeout=1500)
 expect(page.get_by_role('progressbar')).to_have_count(1)
 expect(page.locator('.score-track,.score-numbers,.dialogue-strip')).to_have_count(0)
 assert '%' not in page.locator('.icon-assessment-main').inner_text()
 expect(page.locator('.icon-review-question')).to_have_count(0)
 assert 'But' not in page.locator('.icon-assessment-main').inner_text()
 card=page.locator('.selected-metric-card').bounding_box();stage=page.locator('.metric-stage').bounding_box()
 assert abs(card['x']+card['width']/2-stage['x']-stage['width']/2)<2
 assert abs(card['y']+card['height']/2-stage['y']-stage['height']/2)<2
 assert card['width']>before['width']
 times=page.evaluate('window.iconReviewTimings');order=['focusStart','focusComplete','targetMet','managementUpdate','managementComplete','buttonEnabled']
 assert all(times[a]<times[b] for a,b in zip(order,order[1:])),times
 checks.append('All six metrics appear; the chosen Participation card moves from its grid slot into the center and enlarges, then shows Target met.')
 checks.append('Actual management fill completes before Observe the class enables; no But sentence, student percentages or extra progress bar.')
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
