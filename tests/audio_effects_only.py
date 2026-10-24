"""Check actual built game output: no BGM, retained effects and volume/mute."""
import ast,base64,json,threading
from pathlib import Path
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[1]
# Reuse the existing output analyser without starting its historical Lab test.
tree=ast.parse((ROOT/'tests/audio_classroom.py').read_text())
AUDIT=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='AUDIT' for t in n.targets))
AUDIT=AUDIT.replace('contexts:0,','contexts:0,decodes:0,').replace('createGain(){','decodeAudioData(...args){audioAudit.decodes++;return super.decodeAudioData(...args);}createGain(){')
body=(ROOT/'dist/index.html').read_bytes()
for asset in (ROOT/'src/audio/assets').glob('*.ogg'):
 assert base64.b64encode(asset.read_bytes()) not in body,asset.name
class Handler(BaseHTTPRequestHandler):
 def do_GET(self):
  self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.end_headers();self.wfile.write(body)
 def log_message(self,*a):pass
server=ThreadingHTTPServer(('127.0.0.1',0),Handler);threading.Thread(target=server.serve_forever,daemon=True).start()
errors=[];checks=[]
def peak(page):return page.evaluate('Math.max(0,...audioAudit.peaks.slice(-10))')
def volume(page,value):
 page.get_by_label('Sound effects volume',exact=True).evaluate("(e,v)=>{Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(e,String(v));e.dispatchEvent(new Event('input',{bubbles:true}));e.dispatchEvent(new Event('change',{bubbles:true}));}",value)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);c=b.new_context(viewport={'width':1366,'height':900});c.add_init_script(AUDIT)
 c.add_init_script("localStorage.setItem('gts-sound',JSON.stringify({muted:false,music:1,effects:.65}))")
 page=c.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.goto(f'http://127.0.0.1:{server.server_port}/?soundcheck=1',wait_until='networkidle')
 page.get_by_role('button',name='Sound',exact=True).click();page.wait_for_timeout(1200)
 expect(page.get_by_label('Music volume',exact=True)).to_have_count(0)
 expect(page.get_by_role('button',name='Opening · Office',exact=True)).to_have_count(0)
 assert peak(page)<.00005
 assert page.evaluate('audioAudit.decodes')==0
 checks.append('Old saved music=1 cannot restore BGM; no music decoding, output or music UI after unlock.')
 page.evaluate('audioAudit.peaks=[]');page.get_by_role('button',name='Select / tick',exact=True).click();page.wait_for_timeout(120)
 assert peak(page)>.0001,peak(page)
 page.wait_for_timeout(1000);assert peak(page)<.00005
 checks.append('Selection effect produces audible output, then returns to silence without background music.')
 volume(page,0);page.evaluate('audioAudit.peaks=[]');page.get_by_role('button',name='Select / tick',exact=True).click();page.wait_for_timeout(120);assert peak(page)<.00005
 volume(page,.65);page.get_by_role('button',name='Mute all sound',exact=True).click();page.get_by_role('button',name='Select / tick',exact=True).click();page.wait_for_timeout(120);assert peak(page)<.00005
 page.get_by_role('button',name='Turn sound on',exact=True).click();page.wait_for_timeout(300);page.evaluate('audioAudit.peaks=[]');page.get_by_role('button',name='Select / tick',exact=True).click();page.wait_for_timeout(120);assert peak(page)>.0001
 checks.append('Effects volume, exact zero, mute and unmute still control actual audio output.')
 assert page.evaluate('audioAudit.decodes')==0
 assert not errors,errors
 b.close()
server.shutdown();checks.append('All five former music assets excluded from actual production HTML.')
(ROOT/'test-results/audio-effects-only.json').write_text(json.dumps({'checks':checks,'runtimeErrors':errors},indent=2)+'\n')
for check in checks:print('PASS',check)
