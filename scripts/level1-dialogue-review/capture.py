"""Capture actual chapter component with only the sign -> metric preview patch."""
import threading,json,hashlib
from pathlib import Path
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[2]
class Handler(BaseHTTPRequestHandler):
 def do_GET(self):
  self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.end_headers();self.wfile.write((ROOT/'node_modules/.cache/level1-dialogue-review/index.html').read_bytes())
 def log_message(self,*a):pass
server=ThreadingHTTPServer(('127.0.0.1',0),Handler);threading.Thread(target=server.serve_forever,daemon=True).start()
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=b.new_page(viewport={'width':1600,'height':1000},device_scale_factor=1.5);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(f'http://127.0.0.1:{server.server_port}',wait_until='networkidle')
 expect(page.locator('.chapter-transition')).to_have_attribute('data-beat','ready',timeout=7000)
 expect(page.locator('.chapter-bridge p')).to_have_text('Which metric would tell me the most?')
 expect(page.locator('.chapter-bridge .speaker-name')).to_have_text('fei')
 page.wait_for_timeout(700)
 output=ROOT/'play/Level1-metric-dialogue-preview.png';page.screenshot(path=str(output),full_page=True)
 assert not errors,errors;b.close()
server.shutdown();(ROOT/'play/LEVEL1_METRIC_DIALOGUE_REVIEW.json').write_text(json.dumps({'scope':'Preview-only sign to metric substitution; original chapter styles and formal game packages unchanged.','copy':'Which metric would tell me the most?','samplePlayerName':'fei','image':output.name,'sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'runtimeErrors':errors},indent=2)+'\n')
print('Chapter copy screenshot captured with original production layout.')
