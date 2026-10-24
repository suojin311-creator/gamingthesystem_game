"""Render the five actual observation components with unchanged production CSS."""
import threading,json,hashlib
from pathlib import Path
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'node_modules/.cache/observation-copy-review'
class Handler(BaseHTTPRequestHandler):
 def do_GET(self):
  self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.end_headers();self.wfile.write((OUT/'index.html').read_bytes())
 def log_message(self,*a):pass
server=ThreadingHTTPServer(('127.0.0.1',0),Handler);threading.Thread(target=server.serve_forever,daemon=True).start();errors=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=browser.new_page(viewport={'width':1280,'height':1500},device_scale_factor=1.5);page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(f'http://127.0.0.1:{server.server_port}',wait_until='networkidle');expect(page.locator('.classroom-observation')).to_have_count(5);page.wait_for_timeout(500)
 rows=[]
 for card in page.locator('.classroom-observation').all():
  row=card.locator('.observation-copy').inner_text();assert row.count('Students')==1 and '\nBut they ' in row,row
  styles=card.locator('.observation-copy').evaluate("e=>({body:getComputedStyle(e).fontSize,bodyColor:getComputedStyle(e).color,emphasis:getComputedStyle(e.querySelector('strong')).fontSize,emphasisColor:getComputedStyle(e.querySelector('strong')).color,background:getComputedStyle(e.parentElement).backgroundColor})")
  assert styles=={'body':'18px','bodyColor':'rgb(128, 116, 89)','emphasis':'24px','emphasisColor':'rgb(131, 84, 47)','background':'rgb(242, 233, 214)'},styles
  rows.append({'copy':row,'styles':styles})
 assert not errors,errors
 output=ROOT/'play/Level2-observation-copy-preview.png';page.locator('#root>.game-page').screenshot(path=str(output));browser.close()
server.shutdown();(ROOT/'play/LEVEL2_OBSERVATION_COPY_REVIEW.json').write_text(json.dumps({'scope':'Five text substitutions only in src/levels/level2/data.ts; production observation renderer/CSS and game ZIPs unchanged.','image':output.name,'sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'rows':rows,'runtimeErrors':errors},indent=2)+'\n')
print('Five copy variants rendered with original layout, colors and 18px/24px typography.')
