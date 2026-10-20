"""Audible output and the actual local game -> Lab connection, without cloud assets."""
import json,subprocess,socket,time,re
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'test-results';OUT.mkdir(exist_ok=True)
with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
base=f'http://127.0.0.1:{port}'
log=(OUT/'audio-classroom-server.log').open('w')
proc=subprocess.Popen([str(ROOT/'design-lab/build/design-lab-linux'),'--port',str(port),'--no-browser'],stdout=log,stderr=subprocess.STDOUT)
checks=[];errors=[];csp=[];external=[]
AUDIT='''(()=>{
 const Native=window.AudioContext;if(!Native)return;
 window.audioAudit={contexts:0,peaks:[],gains:[],analyser:null};
 window.AudioContext=class extends Native{createGain(){const g=super.createGain();audioAudit.gains.push(g);return g;}constructor(...args){super(...args);audioAudit.contexts++;const analyser=this.createAnalyser();analyser.fftSize=2048;audioAudit.analyser=analyser;const original=this.destination;const connect=AudioNode.prototype.connect;const silent=this.createGain();silent.gain.value=0;connect.call(analyser,silent);connect.call(silent,this.destination);const zero=this.createConstantSource();zero.offset.value=0;connect.call(zero,analyser);zero.start();if(!window.audioConnectPatched){window.audioConnectPatched=true;AudioNode.prototype.connect=function(target,...rest){if(target instanceof AudioDestinationNode){const result=connect.call(this,target,...rest);connect.call(this,audioAudit.analyser);return result;}return connect.call(this,target,...rest);};}}};
 setInterval(()=>{if(!audioAudit.analyser)return;const a=new Float32Array(2048);audioAudit.analyser.getFloatTimeDomainData(a);audioAudit.peaks.push(Math.sqrt(a.reduce((n,x)=>n+x*x,0)/a.length));if(audioAudit.peaks.length>100)audioAudit.peaks.shift();},20);
})();'''
def report(text):checks.append(text);print('PASS',text,flush=True)
def volume(page,label,value):
 page.get_by_label(label,exact=True).evaluate("(e,v)=>{Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(e,String(v));e.dispatchEvent(new Event('input',{bubbles:true}));e.dispatchEvent(new Event('change',{bubbles:true}));}",value)
 assert page.evaluate("key=>JSON.parse(localStorage.getItem('gts-sound'))[key]",'music' if label=='Music volume' else 'effects')==float(value)
def peak(page):return page.evaluate('Math.max(0,...audioAudit.peaks.slice(-10))')
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  context=browser.new_context(viewport={'width':1366,'height':900});context.add_init_script(AUDIT)
  page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('console',lambda m:csp.append(m.text) if m.type=='error' and ('Content Security Policy' in m.text or 'Refused to' in m.text) else None)
  page.on('request',lambda r:external.append(r.url) if not r.url.startswith(base) and not r.url.startswith('data:') and r.url!='about:srcdoc' else None)
  for n in range(50):
   try:page.goto(base+'/host',wait_until='networkidle');break
   except Exception:
    if n==49:raise
    time.sleep(.1)
  assert page.get_by_label('Share this link with the class.').input_value().endswith('/game')
  if '--ending-only' not in __import__('sys').argv:
   page.goto(base+'/game?soundcheck=1',wait_until='networkidle',timeout=90000)
   page.get_by_role('button',name='Opening · Office',exact=True).click()
   page.wait_for_function('()=>document.querySelector("[data-audio-playing]")?.dataset.audioPlaying==="true"',timeout=20000);page.wait_for_timeout(1200)
   assert peak(page)>.0001,peak(page)
   assert page.evaluate('audioAudit.contexts')==1
   report('Packaged original score decodes and produces measurable audio through one context under the real classroom CSP')
   for title in ['Levels 1–3 · Shared theme','Ending · Reflection','Design Lab · Quiet focus','Goodhart’s Law · Reveal']:
    page.get_by_role('button',name=title,exact=True).click();page.wait_for_timeout(1300);assert peak(page)>.0001,(title,peak(page))
   report('All five original score cues produce output; changes retain one shared audio context')
   page.get_by_role('button',name='Pause music',exact=True).click();page.wait_for_timeout(500);assert peak(page)<.00005,peak(page)
   page.get_by_role('button',name='Resume music',exact=True).click();page.wait_for_timeout(1200);assert peak(page)>.0001
   report('Pause silences music and resume restores it')
   page.get_by_role('button',name='Sound',exact=True).click();page.get_by_role('button',name='Mute all sound',exact=True).click();page.wait_for_timeout(500);assert peak(page)<.00005
   page.get_by_role('button',name='Select / tick',exact=True).click();page.wait_for_timeout(200);assert peak(page)<.00005
   page.get_by_role('button',name='Turn sound on',exact=True).click();page.wait_for_timeout(1200);assert peak(page)>.0001
   report('Master mute silences both buses and unmutes correctly')
   volume(page,'Music volume',0);page.wait_for_timeout(800);assert peak(page)<.00005
   page.evaluate('audioAudit.peaks=[]');page.get_by_role('button',name='Select / tick',exact=True).click();page.wait_for_timeout(200);assert peak(page)>.0001,peak(page)
   volume(page,'Sound effects volume',0);page.wait_for_timeout(1000);page.evaluate('audioAudit.peaks=[]');page.get_by_role('button',name='Select / tick',exact=True).click();page.wait_for_timeout(200);assert peak(page)<.00005,peak(page)
   volume(page,'Music volume',.58);volume(page,'Sound effects volume',.65);page.wait_for_timeout(1200)
   report('Music/effects sliders independently control actual output, including zero-volume silence')
   page.get_by_role('button',name='Opening · Office',exact=True).click();page.wait_for_timeout(1200)
   page.evaluate("Object.defineProperty(document,'hidden',{configurable:true,get:()=>true});document.dispatchEvent(new Event('visibilitychange'))");page.wait_for_timeout(500);assert peak(page)<.00005
   page.evaluate("Object.defineProperty(document,'hidden',{configurable:true,get:()=>false});document.dispatchEvent(new Event('visibilitychange'))");page.wait_for_timeout(1200);assert peak(page)>.0001
   report('Browser visibility events silence the hidden page and restore playback on return')
   (OUT/'audio-output-results.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'runtimeErrors':errors,'cspErrors':csp},indent=2)+'\n')
   page.screenshot(path=str(OUT/'sound-preview.png'))
  # Validate the approved invitation using the actual shared game component,
  # real ending film handshake and real classroom endpoint (no fake completion).
  page.goto(base+'/game?level=3',wait_until='networkidle',timeout=90000)
  page.clock.install()
  helpers=(ROOT/'tests/release.py').read_text();helpers=helpers[helpers.index('def advance('):helpers.index("if '--integrity-only' in sys.argv:")]
  ns={'expect':expect,'checks':[],'re':re};exec(helpers,ns)
  ns['choose_three'](page);ns['weights_three'](page,[60,30,10])
  page.get_by_role('button',name='Try another split',exact=True).click();ns['weights_three'](page,[10,60,30])
  page.get_by_role('button',name='Compare the results',exact=True).click();page.get_by_role('button',name='Step back and reflect',exact=True).click()
  film=page.frame_locator('iframe[title="Ending animation"]');expect(film.locator('.ending-loading')).to_have_count(0,timeout=30000)
  for n in range(30):page.clock.run_for(1000);page.wait_for_timeout(25)
  expect(film.locator('.ending-question-line')).to_have_count(0)
  expect(film.get_by_role('button',name='ENTER DESIGN LAB')).to_be_visible()
  film.get_by_role('button',name='ENTER DESIGN LAB').click(force=True,no_wait_after=True);page.wait_for_timeout(500);page.clock.run_for(1000)
  page.wait_for_url(base+'/',timeout=30000);expect(page.locator('.intro')).to_be_visible(timeout=20000)
  assert page.locator('.error-note').count()==0
  page.wait_for_timeout(1800)
  assert page.evaluate('audioAudit.contexts')==1
  assert peak(page)>.0001,('Lab did not continue sound',peak(page))
  report('Two real Level 3 trials enter the approved fullscreen ending and its button connects to this classroom Lab')
  assert not errors,errors
  assert not csp,csp
  assert not external,external
  report('No runtime errors, CSP violations or external service requests')
  browser.close()
finally:proc.terminate();proc.wait(timeout=10);log.close()
(OUT/'audio-classroom-results.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'runtimeErrors':errors,'cspErrors':csp,'externalRequests':external},indent=2)+'\n')
