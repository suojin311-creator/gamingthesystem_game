"""Check all real Level 1 choices reach the matching result card and film."""
import threading,json
from pathlib import Path
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[1]
class Handler(BaseHTTPRequestHandler):
 def do_GET(self):
  self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.end_headers();self.wfile.write((ROOT/'dist/index.html').read_bytes())
 def log_message(self,*a):pass
server=ThreadingHTTPServer(('127.0.0.1',0),Handler);threading.Thread(target=server.serve_forever,daemon=True).start();checks=[];errors=[]
cases=[('prep','Preparation','pre-class-preparation'),('part','Participation','in-class-participation'),('focus','Focus','on-task-focus'),('discuss','Discussion','in-class-discussion-quality'),('reflect','Reflection','learning-reflection-quality'),('peer','Peer response','online-peer-response-quality')]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for i,(id,label,film_id) in enumerate(cases):
  c=b.new_context(reduced_motion='no-preference' if i==1 else 'reduce',viewport={'width':1366,'height':900});page=c.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(f'http://127.0.0.1:{server.server_port}/?level=1',wait_until='domcontentloaded');page.get_by_role('button',name='Skip guide').click(timeout=15000)
  page.get_by_test_id('metric-'+id).click();page.get_by_role('button',name='Make a prediction',exact=True).click();page.get_by_label('How will students respond when this counts towards their marks?').fill('My prediction stays with this choice.')
  page.get_by_role('button',name='View assessment results',exact=True).click()
  expect(page.locator('.metric-result .selected-metric-card h3')).to_have_text(label)
  expect(page.locator('.metric-result .metric-option')).to_have_count(6)
  button=page.get_by_role('button',name='Observe the class',exact=True);expect(button).to_be_enabled(timeout=12000)
  expect(page.get_by_role('progressbar')).to_have_count(1);expect(page.locator('.score-numbers,.score-track,.metric-result .dialogue-strip')).to_have_count(0)
  button.click();film=page.frame_locator('iframe');expect(film.locator('.l1-film')).to_have_attribute('data-metric',film_id,timeout=20000)
  checks.append(f'{id}: selected {label} card and matching {film_id} cinematic verified');c.close()
 assert not errors,errors;b.close()
server.shutdown();(ROOT/'test-results/metric-result-choices.json').write_text(json.dumps({'checks':checks,'runtimeErrors':errors},indent=2)+'\n')
for check in checks:print('PASS',check,flush=True)
