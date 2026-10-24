"""Capture the real Level 1 settlement with the proposed text and teacher bubble."""
import threading
from pathlib import Path
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[2]
class Handler(BaseHTTPRequestHandler):
 def do_GET(self):
  self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.end_headers();self.wfile.write((ROOT/'node_modules/.cache/level1-result-copy-review/index.html').read_bytes())
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),Handler);threading.Thread(target=server.serve_forever,daemon=True).start()
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1440,'height':900},device_scale_factor=1.5)
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(f'http://127.0.0.1:{server.server_port}',wait_until='networkidle')
 expect(page.locator('.student-behaviour')).to_have_text('Alex focused on only one metric.')
 expect(page.locator('.l1-settlement-teacher p')).to_have_text('What if I measured more than one metric?')
 page.wait_for_timeout(2800)
 assert not errors,errors
 page.locator('.l1-settlement').screenshot(path=str(ROOT/'play/Level1-result-copy-preview.png'))
 browser.close()
server.shutdown()
print('Actual settlement rendered; approved headline and teacher-only prompt verified.')
