"""Target the eighteen Level 3A states, trimmed footage and real cross-dissolves."""
import base64,hashlib,json
from pathlib import Path
from zipfile import ZipFile
from playwright.sync_api import sync_playwright

OUT=Path('test-results');OUT.mkdir(exist_ok=True)
meta=json.loads(Path('play/LEVEL3A_ANIMATION_PREVIEW.json').read_text())
with ZipFile(Path('play')/meta['archive']) as z:
    assert hashlib.sha256(z.read(meta['html'])).hexdigest()==meta['htmlSha256']
film=Path('node_modules/.cache/level3-cinematic/index.html').read_bytes()
assert hashlib.sha256(film).hexdigest()==meta['film']['htmlSha256']
source=Path('/tmp/gts-level3a-source')
for rejected in [source/'docs/visual-style/references/level3-metric-adaptations/REF-L3A-S10 — High On-Task Focus.png',source/'assets/props/PROP-L1-001 — Checklist : Reading Sheet.png']:
    assert base64.b64encode(rejected.read_bytes()) not in film,rejected
fixtures=json.loads((OUT/'level3a-fixtures.json').read_text())
checks=[];seen={};errors=[];external=[]
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    context=browser.new_context(viewport={'width':1280,'height':720});context.set_default_timeout(30000)
    current=[fixtures[0]]
    def serve(route):
        path=route.request.url.split('?')[0]
        if path=='https://level3a.test/film.html':route.fulfill(content_type='text/html',body=film)
        elif path=='https://level3a.test/':
            config=json.dumps({'channel':'level3a-cinematic','type':'start','runId':'test','request':current[0]['request'],'preview':True,'reducedMotion':False})
            body='''<!doctype html><style>html,body{margin:0;width:100%;height:100%;background:#111710}iframe{border:0;width:100%;height:100%;display:block}</style><script>window.completed=0;window.send=(action,value)=>frames[0].postMessage({channel:'level3a-cinematic',type:'control',runId:'test',action,value},'*');addEventListener('message',e=>{if(e.source!==frames[0])return;if(e.data.type==='ready')frames[0].postMessage(CONFIG,'*');if(e.data.type==='complete')window.completed++;});</script><iframe name="film" src="/film.html"></iframe>'''.replace('CONFIG',config)
            route.fulfill(content_type='text/html',body=body)
        else:external.append(route.request.url);route.abort()
    context.route('**/*',serve)
    page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
    for fixture_index,fixture in enumerate(fixtures):
        current[0]=fixture
        page.goto('https://level3a.test/',wait_until='networkidle')
        frame=page.frame(name='film');frame.wait_for_selector('.l3-film')
        page.evaluate("send('pause')")
        for clip in fixture['pacing']['timeline']:
            name=clip['metric']+'-'+clip['intensity'].lower()
            for position in [.02,.5,.95]:
                target=clip['start']+(clip['end']-clip['start'])*position
                page.evaluate("v=>send('seek',v)",target)
                frame.wait_for_function('v=>Math.abs(Number(document.querySelector(".l3-film").dataset.elapsed)-v)<.005',arg=target)
                audit=frame.evaluate('''()=>{
                  const root=document.querySelector('.l3-film'),s=root.querySelector('.l3a-scene'),label=root.querySelector('.l3-speaker'),caption=root.querySelector('[role=status]'),title=root.querySelector('.l3-metric-name');
                  return {metric:root.dataset.metric,intensity:root.dataset.intensity,scene:root.dataset.shotId,beat:s.dataset.beat,text:root.innerText,title:title.textContent,label:label.textContent,caption:caption.textContent,color:getComputedStyle(caption).color,labelColor:getComputedStyle(label).color,background:getComputedStyle(caption).backgroundColor,extra:root.querySelectorAll('.l3a-priority-sheet,.l3a-result-anchor').length};
                }''')
                assert audit['metric']==clip['metric'] and audit['intensity']==clip['intensity'],audit
                assert audit['scene']==clip['sceneId'] and audit['caption']==clip['caption'],audit
                assert audit['label']=='Alex' and audit['color']==audit['labelColor']=='rgb(204, 238, 255)',audit
                assert audit['background']=='rgba(0, 0, 0, 0)',audit
                assert not any(c.isdigit() for c in audit['text']),audit
                assert audit['extra']==0 and audit['beat'] not in ['listen-to-peer','reaction','early-classroom','notes-insert'],audit
                if position==.5:frame.locator('.l3-film').screenshot(path=str(OUT/f'level3a-{name}.png'))
            seen[name]=audit
        print('PASS rendered fixture',fixture_index+1,flush=True)
    assert len(seen)==18
    checks.append('All 18 metric/effort states at start, middle and end retain the correct game-supplied scene/caption/title, Alex blue, transparent captions, no numeric pages or rejected cutaways')
    # A live run checks the transition itself, including the two actual clip joins.
    current[0]=fixtures[0];page.goto('https://level3a.test/',wait_until='networkidle');frame=page.frame(name='film');frame.wait_for_selector('.l3-film')
    frame.evaluate('''()=>{window.audit={shots:[],intermediate:false,black:false};new MutationObserver(()=>{const r=document.querySelector('.l3-film');if(!window.audit.shots.includes(r.dataset.shotId))window.audit.shots.push(r.dataset.shotId);}).observe(document.querySelector('.l3-film'),{subtree:true,attributes:true});window.timer=setInterval(()=>{const h=document.querySelector('[data-cinematic-dissolve]');if(h){const o=Number(getComputedStyle(h).opacity);if(o>0&&o<1)window.audit.intermediate=true;if(Number(getComputedStyle(document.querySelector('.l3-end-cover')).opacity)>0)window.audit.black=true;}},20);}''')
    page.evaluate("send('speed',4)")
    page.wait_for_function('window.completed===1',timeout=35000)
    audit=frame.evaluate('()=>{clearInterval(window.timer);return window.audit;}')
    assert audit['shots']==[s['sceneId'] for s in fixtures[0]['request']['shots']],audit
    assert audit['intermediate'] and not audit['black'],audit
    page.wait_for_timeout(150);assert page.evaluate('window.completed')==1
    checks.append('A complete live montage cross-dissolves through the three actual shots without a black internal cut and completes exactly once')
    current[0]=fixtures[1];page.goto('https://level3a.test/',wait_until='networkidle');frame=page.frame(name='film');frame.wait_for_selector('.l3-film')
    frame.evaluate("()=>{Object.defineProperty(document,'hidden',{configurable:true,value:true});document.dispatchEvent(new Event('visibilitychange'));}")
    before=frame.locator('.l3-film').get_attribute('data-elapsed');page.wait_for_timeout(250)
    assert frame.locator('.l3-film').get_attribute('data-elapsed')==before
    checks.append('A hidden film holds the reading clock')
    for width in [390,320]:
        page.set_viewport_size({'width':width,'height':int(width*9/16)})
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    checks.append('The film fits narrow screens without horizontal overflow')
    context.close();browser.close()
assert not errors,errors
assert not external,external
checks.append('No runtime errors or external requests; the rejected single portrait and numbered reading-sheet bytes are absent')
(OUT/'level3a-preview-results.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'states':list(seen),'runtimeErrors':errors,'externalRequests':external},indent=2)+'\n')
print('PASS',len(checks),'targeted browser checks; eighteen states.',flush=True)
