"""Read-only Padlet handoff from real game trials; never post or vote externally."""
import json,re,threading,subprocess,socket,time
from pathlib import Path
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'test-results';OUT.mkdir(exist_ok=True)
URL='https://padlet.com/embed/s024sqd75q7kuy5xciyy';checks=[];errors=[];requests=[]
sock=socket.socket();sock.bind(('0.0.0.0',0));port=sock.getsockname()[1];sock.close()
log=(OUT/'padlet-server.log').open('w');proc=subprocess.Popen([str(ROOT/'design-lab/build/design-lab-linux'),'--port',str(port),'--no-browser'],stdout=log,stderr=subprocess.STDOUT)
source=(ROOT/'tests/release.py').read_text();ns={'expect':expect,'re':re,'checks':[]};exec(source[source.index('def advance('):source.index("if '--integrity-only' in sys.argv:")],ns)
class Static(BaseHTTPRequestHandler):
 def do_GET(self):
  self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.end_headers();self.wfile.write((ROOT/'dist/index.html').read_bytes())
 def log_message(self,*a):pass
static=ThreadingHTTPServer(('127.0.0.1',0),Static);threading.Thread(target=static.serve_forever,daemon=True).start()
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--no-proxy-server'])
  for mode in ['static-html','lan']:
   c=browser.new_context(viewport={'width':1280,'height':800});page=c.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.on('request',lambda r:requests.append(r.url) if '/api/display' in r.url else None)
   base=f'http://172.26.91.252:{port}/game' if mode=='lan' else f'http://127.0.0.1:{static.server_port}/index.html'
   page.goto(base+'?level=3',wait_until='domcontentloaded',timeout=90000);page.clock.install()
   ns['choose_three'](page);ns['weights_three'](page,[60,30,10]);page.get_by_role('button',name='Try another split',exact=True).click();ns['weights_three'](page,[10,60,30]);page.get_by_role('button',name='Compare the results',exact=True).click();page.get_by_role('button',name='Step back and reflect',exact=True).click()
   film=page.frame_locator('iframe[title="Ending animation"]');expect(film.locator('.ending-viewport')).to_be_visible();expect(film.locator('.ending-loading')).to_have_count(0)
   ns['advance'](page,46);expect(film.get_by_role('button',name='ENTER DESIGN LAB')).to_be_visible()
   film.get_by_role('button',name='ENTER DESIGN LAB').click(force=True,no_wait_after=True);page.clock.run_for(1200)
   expect(page.locator('[data-padlet-lab]')).to_be_visible();expect(page.get_by_title('Design Lab · Padlet')).to_have_attribute('src',URL)
   expect(page.get_by_role('link',name='Open in a new tab')).to_have_attribute('href',URL)
   assert not requests,requests
   checks.append(mode+': real ending opens full-screen Padlet without a local Lab API, with an external-tab fallback')
   if mode=='lan':
    page.wait_for_timeout(6000)
    remote=[f for f in page.frames if f.url.startswith('https://padlet.com/')]
    remote_info=[{'url':f.url,'text':f.locator('body').inner_text(timeout=10000)[:700]} for f in remote]
    page.screenshot(path=str(OUT/'padlet-integration.png'))
   c.close()
  browser.close()
 assert not errors,errors
finally:static.shutdown();proc.terminate();proc.wait(timeout=10);log.close()
(OUT/'padlet-results.json').write_text(json.dumps({'checks':checks,'runtimeErrors':errors,'boardReadOnlyObservation':remote_info,'postedOrVoted':False,'boardLoadVerified':bool(remote_info),'verificationLimit':'Environment outbound proxy rejects Padlet CONNECT with 403; board permissions and anonymous posting are unverified. Direct file navigation is blocked; standalone HTML tested via static HTTP.'},indent=2)+'\n')
for check in checks:print('PASS',check,flush=True)
print('REMOTE',json.dumps(remote_info),flush=True)
