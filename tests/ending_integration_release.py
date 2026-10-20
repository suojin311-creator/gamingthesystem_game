"""Actual game archives: Level 3 comparison enters the approved ending offline.
Reuse release integrity checks and its player controls, without replaying Levels 1/2.
"""
from pathlib import Path
source=Path('tests/release.py').read_text().split('with sync_playwright() as playwright:')[0]
exec(compile(source,'tests/release.py (integrity and helpers)','exec'))
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
import threading
class Handler(BaseHTTPRequestHandler):
 def do_GET(self):
  self.send_response(200);self.send_header('Content-Type','text/html');self.send_header('Content-Length',str(len(artifacts['Level3.html'])));self.end_headers();self.wfile.write(artifacts['Level3.html'])
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),Handler);threading.Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}'
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 context=browser.new_context(viewport={'width':1366,'height':900},reduced_motion='reduce')
 context.route('**/*',lambda r:r.continue_() if r.request.url.startswith(base) or r.request.url.startswith('data:') else r.abort())
 context.add_init_script("""addEventListener('message',event=>{if(event.data?.channel==='ending-cinematic'&&event.data.type==='start'){window.endingStart=event.data;window.endingShots=[];const timer=setInterval(()=>{const task=document.querySelector('.ending-actual-task');if(task&&!endingShots.includes(task.dataset.sceneId))endingShots.push(task.dataset.sceneId);if(document.querySelector('.end-stage')?.dataset.elapsed==='24.000')clearInterval(timer);},20);}});""")
 page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
 page.clock.install();page.goto(base,wait_until='load',timeout=90000)
 print('Checking first actual trial',flush=True)
 choose_three(page);weights_three(page,[60,30,10])
 print('Checking second actual trial',flush=True)
 page.get_by_role('button',name='Try another split',exact=True).click();weights_three(page,[10,60,30])
 page.get_by_role('button',name='Compare the results',exact=True).click()
 page.get_by_role('button',name='Watch Alex’s response',exact=True).click()
 print('Checking integrated ending',flush=True)
 expect(page.get_by_test_id('ending-cinematic')).to_be_visible(timeout=30000)
 frame=page.frame_locator('iframe[title="Ending animation"]')
 expect(frame.locator('.ending-loading')).to_have_count(0,timeout=30000)
 expect(frame.locator('.ending-spoken')).to_be_visible(timeout=15000)
 data=frame.locator('body').evaluate('()=>window.endingStart.input')
 assert [r['runs'][0]['weights'] for r in data['history']]==[[60,30,10],[10,60,30]],data
 assert data['lastRun']['shots'][-1]['sceneId']=='level3.focus.medium'
 box=page.get_by_test_id('ending-cinematic').bounding_box();assert box=={'x':0,'y':0,'width':1366,'height':900},box
 expect(page.locator('.l3-masthead,.l3-footer,.l3-cinematic')).to_have_count(0)
 expect(frame.locator('.ending-review-controls')).to_have_count(0)
 checks.append('Actual standalone game enters full-viewport ending directly after comparison with two real non-near-even trials; no placeholder, game chrome or preview controls')
 for _ in range(28):page.clock.run_for(1000);page.wait_for_timeout(30)
 assert frame.locator('body').evaluate('()=>window.endingShots')==['level3.focus.medium']
 checks.append('Ending memory uses the last actual task and effort rather than a fabricated near-even result')
 expect(page.get_by_test_id('ending-cinematic')).to_have_attribute('data-finished','true')
 expect(frame.locator('#ending-next-title')).to_have_text('Share what reallearning looks like.')
 expect(frame.get_by_role('button',name='ENTER DESIGN LAB')).to_be_visible()
 assert 'Goodhart' not in frame.locator('body').inner_text()
 frame.get_by_role('button',name='ENTER DESIGN LAB').click(force=True)
 expect(page.get_by_test_id('ending-cinematic')).to_have_attribute('data-finished','true')
 expect(page.locator('.l3-cinematic')).to_have_count(0)
 page.screenshot(path='test-results/ending-integrated-game.png')
 checks.append('Ending completes and holds the accepted title/button page; it never falls through to the old theory or opens the separate classroom program')
 context.close();browser.close()
server.shutdown()
assert not errors,errors
checks.append('No browser runtime errors; all game archives retain valid production hashes')
Path('test-results/ending-integration-release-results.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'runtimeErrors':errors},indent=2)+'\n')
for check in checks:print('PASS',check,flush=True)
