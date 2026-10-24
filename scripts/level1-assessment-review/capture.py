"""Capture the isolated assessment review, using the actual production chart."""
import threading,json,hashlib
from pathlib import Path
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[2]
class Handler(BaseHTTPRequestHandler):
 def do_GET(self):
  self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.end_headers();self.wfile.write((ROOT/'node_modules/.cache/level1-assessment-review/index.html').read_bytes())
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),Handler);threading.Thread(target=server.serve_forever,daemon=True).start()
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1160,'height':850},device_scale_factor=1.5)
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(f'http://127.0.0.1:{server.server_port}',wait_until='networkidle')
 expect(page.get_by_role('heading')).to_have_text('Percentage of students meeting the criteria')
 expect(page.locator('.score-paper-top .eyebrow,.assessment-report-label')).to_have_count(0)
 expect(page.locator('.before-score')).to_contain_text('29%')
 expect(page.locator('.after-score')).to_contain_text('85%')
 expect(page.get_by_role('button')).to_have_text('Look behind the result')
 assert page.locator('.assessment-bridge').bounding_box()['y']<page.get_by_role('button').bounding_box()['y']
 output=ROOT/'play/Level1-assessment-preview.png';page.locator('.assessment-review').screenshot(path=str(output))
 page.set_viewport_size({'width':390,'height':850})
 assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
 assert not errors,errors
 browser.close()
server.shutdown()
(ROOT/'play/LEVEL1_ASSESSMENT_REVIEW.json').write_text(json.dumps({'scope':'Isolated preview only; production sources and formal game packages unchanged.','image':output.name,'sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'checks':['Actual production chart uses 29% to 85% unchanged.','Metric name and duplicate heading removed.','Bridge above original Look behind the result button.','Desktop render and 390px layout fit.'],'runtimeErrors':errors},indent=2)+'\n')
print('Assessment preview captured; desktop and mobile layout checks passed.')
