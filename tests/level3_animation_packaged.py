"""Exercise the new default Level 3A host and changed complete-ZIP launchers only."""
import hashlib,json
import tempfile
import functools,threading
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlsplit
from zipfile import ZipFile
from playwright.sync_api import sync_playwright,expect
OUT=Path('test-results');manifest=json.loads(Path('play/LATEST.json').read_text())
expect.set_options(timeout=30000)
entry=next(e for e in manifest['entries'] if e['archive']=='Level3-play.zip')
with ZipFile(Path('play')/entry['archive']) as z:level3=z.read(entry['html'])
assert hashlib.sha256(level3).hexdigest()==entry['htmlSha256']
with ZipFile(Path('play')/manifest['completeBundle']['archive']) as z:complete={n:z.read(n) for n in z.namelist()}
errors=[];external=[];checks=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 context=browser.new_context(viewport={'width':1366,'height':900});context.set_default_timeout(30000);context.set_default_navigation_timeout(120000)
 def serve(route):
  u=urlsplit(route.request.url)
  data=level3 if u.netloc=='level3-game.test' else complete.get(u.path.lstrip('/')) if u.netloc=='complete-game.test' else None
  if data is None:external.append(route.request.url);route.abort()
  else:route.fulfill(content_type='text/html',body=data)
 context.route('**/*',serve)
 page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto('https://level3-game.test/',wait_until='networkidle')
 page.get_by_role('button',name='Choose priorities',exact=True).click()
 for metric in ['prep','discuss','peer']:page.get_by_test_id('level3-metric-'+metric).click()
 page.get_by_role('button',name='Set the weights',exact=True).click()
 page.get_by_role('button',name='Skip guide',exact=True).click()
 for metric,value in [('prep',60),('discuss',30)]:
  slider=page.get_by_test_id('weight-card-'+metric).locator('input')
  slider.evaluate('(e,v)=>{Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,"value").set.call(e,String(v));e.dispatchEvent(new Event("input",{bubbles:true}));}',value)
  page.get_by_test_id('confirm-'+metric).click()
 page.get_by_role('button',name='Run evaluation',exact=True).click()
 page.get_by_role('button',name='Observe the class',exact=True).click()
 frame=page.frame_locator('iframe[title="Level 3A classroom animation"]');expect(frame.locator('.l3-film')).to_be_visible()
 frame.locator('.l3-film').evaluate('''root=>{window.shots=[];const record=()=>{const s=root.dataset.shotId;if(!window.shots.includes(s))window.shots.push(s);parent.postMessage({type:'level3-host-audit',shots:window.shots},'*');};new MutationObserver(record).observe(root,{attributes:true});record();}''')
 page.evaluate("addEventListener('message',e=>{if(e.data?.type==='level3-host-audit')window.hostShots=e.data.shots;})")
 expect(page.locator('.level-three')).to_have_attribute('data-phase','result',timeout=40000)
 assert page.evaluate('window.hostShots')==['level3.prep.high','level3.discuss.medium','level3.peer.low']
 assert page.locator('.l3-run-rows li').evaluate_all("nodes=>nodes.map(n=>n.dataset.effort)")==['high','medium','low']
 checks.append('Actual Level3-play.zip uses the default real film for a 60/30/10 trial, plays prep high → discussion medium → peer low and returns to matching results')
 print('PASS',checks[-1],flush=True)
 page.get_by_role('button',name='Replay scene',exact=True).click()
 expect(frame.locator('.l3-film')).to_have_attribute('data-shot-id','level3.prep.high')
 checks.append('Replay mounts a fresh movie at the first actual shot')
 print('PASS',checks[-1],flush=True)
 # Only entry points are exercised here, not full opening/Level 1/2 paths.
 # Read the extracted files directly: avoid transferring the large inline movie
 # strings through DevTools' route.fulfill for every launcher navigation.
 extracted=Path(tempfile.mkdtemp(prefix='gts-level3a-complete-'))
 for name,data in complete.items():
  path=extracted/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
 context.unroute('**/*',serve)
 # Managed Chromium disallows file://. Serve the extracted bytes on loopback
 # instead; there are no network assets or rewritten application files.
 class Handler(SimpleHTTPRequestHandler):
  def log_message(self,*args):pass
 server=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(extracted)))
 thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
 origin=f'http://127.0.0.1:{server.server_port}/'
 for level in [None,1,2,3]:
  page.goto(origin+'START-HERE.html',wait_until='domcontentloaded')
  name='Full-game/Gaming-the-System.html' if level is None else f'Level{level}/Level{level}.html'
  page.locator(f'a[href="{name}"]').click(no_wait_after=True)
  if level is None:expect(page.locator('.opening-scene .stage')).to_have_attribute('data-beat','title')
  elif level==1:expect(page.get_by_role('heading',name='One metric.',exact=True)).to_be_visible()
  elif level==2:expect(page.locator('.level-two')).to_have_attribute('data-phase','intro')
  else:expect(page.locator('.level-three')).to_have_attribute('data-phase','intro')
  target=manifest['completeBundle'].get('sharedGameLaunchers',{}).get(name,name)
  expect(page).to_have_url(origin+target)
  print('PASS extracted complete-ZIP entry',name,flush=True)
 checks.append('All four complete-ZIP entry points open the intended opening or standalone level through the shared offline game HTML')
 server.shutdown();server.server_close()
 context.close();browser.close()
assert not errors,errors
assert not external,external
(OUT/'level3a-packaged-results.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'runtimeErrors':errors,'externalRequests':external},indent=2)+'\n')
for text in checks:print('PASS',text,flush=True)
