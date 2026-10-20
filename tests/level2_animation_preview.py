"""Validate the exact trimmed, styled film shared by the game and review ZIP."""
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright, expect

OUT=Path('test-results');OUT.mkdir(exist_ok=True)
m=json.loads(Path('play/LEVEL2_ANIMATION_PREVIEW.json').read_text())
a=Path('play')/m['archive']
assert hashlib.sha256(a.read_bytes()).hexdigest()==m['zipSha256']
with ZipFile(a) as z:
    assert z.testzip() is None
    files={name:z.read(name) for name in z.namelist()}
for name,data in files.items(): assert hashlib.sha256(data).hexdigest()==m['fileSha256'][name]
checks=[];errors=[];external=[]
def record(text): checks.append(text);print('PASS',text,flush=True)
record('Actual adapted review ZIP passes CRC and all recorded SHA-256 checks')
origin='https://level2-review.test/'
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    c=b.new_context(viewport={'width':1366,'height':900})
    c.set_default_navigation_timeout(120000);c.set_default_timeout(30000);c.set_offline(True)
    def serve(r):
        u=urlsplit(r.request.url);data=files.get(u.path.lstrip('/')) if u.netloc=='level2-review.test' else None
        if data is None:external.append(r.request.url);r.abort()
        else:r.fulfill(status=200,content_type='text/html',body=data)
    c.route('**/*',serve)
    page=c.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto(origin+'START-HERE.html',wait_until='networkidle')
    expect(page.locator('nav a')).to_have_count(6)
    assert not page.locator('a[href*="state=10&"],a[href*="state=25"],a[href*="state=checking"]').count()
    for w in [1366,390,320]:
        page.set_viewport_size({'width':w,'height':900})
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    page.set_viewport_size({'width':1366,'height':900})
    record('Launcher contains only the five existing placeholder variants and their short continuous review')
    for state,kind in [('visible-heavy','three'),('quality-heavy','three'),('mixed-broad','three'),('six','six'),('100','checklist')]:
        page.goto(origin+'Level2-animation.html?state='+state,wait_until='networkidle')
        f=page.frame_locator('iframe');film=f.locator('.l2-film')
        expect(film).to_be_visible()
        page.get_by_role('button',name='Pause',exact=True).click()
        slider=page.get_by_label('Preview time',exact=True);slider.press('Home')
        expect(film).to_have_attribute('data-kind',kind)
        if kind=='three':expect(f.locator('.l2-spoken [role=status]')).to_have_text('I’ve completed all three requirements!')
        # Audit every displayed caption and each scene swap, not just a final screenshot.
        film.evaluate("""root=>{
          window.filmAudit={errors:[],speakers:[],shots:[],swaps:[],checklists:[],cutCaptions:[]};let closingText=null,cutPhase='';
          const sample=()=>{
            const a=window.filmAudit,shot=root.dataset.shot;
            if(!a.shots.includes(shot))a.shots.push(shot);
            if(['entry','pattern','expand','ten','twenty-five','priority','checking'].includes(shot))a.errors.push('Extra shot '+shot);
            const scene=root.querySelector('.l2-scene');
            const visible=e=>getComputedStyle(e).visibility==='visible'&&e.getClientRects().length>0;
            const walker=document.createTreeWalker(scene,NodeFilter.SHOW_TEXT);
            while(walker.nextNode()){
              const node=walker.currentNode,el=node.parentElement;
              if(node.textContent.trim()&&visible(el)&&!el.closest('.l2-checklist-row-label, .l2-checklist-group h4'))a.errors.push('Unexpected overlay text: '+node.textContent);
            }
            for(const list of scene.querySelectorAll('.l2-checklist')){
              const labels=[...list.querySelectorAll('.l2-checklist-row-label')];
              if(!labels.length||!visible(labels[0]))continue;
              const count=Number(list.dataset.count);
              if(labels.length!==count||labels.some(e=>!visible(e)||!e.textContent.trim()))a.errors.push('Missing checklist text');
              if(count===100){
                if(labels.some((e,i)=>e.textContent!=='Criterion '+String(i+1).padStart(2,'0')))a.errors.push('Incorrect 100-metric text');
                const groups=[...list.querySelectorAll('h4')];
                if(groups.length!==5||groups.some(e=>!visible(e)))a.errors.push('Missing checklist group headings');
              }
              if(!a.checklists.includes(count))a.checklists.push(count);
            }
            const spoken=root.querySelector('.l2-spoken');
            if(spoken){
              const label=spoken.querySelector('.l2-speaker'),text=spoken.querySelector('[role=status]');
              const name=label.textContent,color=name==='You'?'rgb(255, 226, 163)':'rgb(204, 238, 255)';
              if(!['You','Alex'].includes(name))a.errors.push('Unexpected speaker '+name);
              if(getComputedStyle(label).color!==color||getComputedStyle(text).color!==color)a.errors.push('Incorrect caption colour');
              if(getComputedStyle(text).backgroundColor!=='rgba(0, 0, 0, 0)'||getComputedStyle(spoken).backgroundColor!=='rgba(0, 0, 0, 0)')a.errors.push('Caption background');
              if(!a.speakers.includes(name))a.speakers.push(name);
            }
            const phase=root.dataset.handoff;
            const caption=spoken?.querySelector('[role=status]')?.textContent??null;
            if(root.dataset.kind==='checklist'&&shot==='reflection'){
              if(phase==='closing')closingText=caption;
              if(phase==='covered'&&cutPhase!=='covered'){
                a.cutCaptions.push(caption);
                if(!caption||caption===closingText)a.errors.push('Final reflection reopened with a stale or missing caption');
              }
              cutPhase=phase;
            }
            if(phase==='covered'){
              const opacity=Number(getComputedStyle(root.querySelector('.l2-film-cover')).opacity);
              a.swaps.push(opacity);if(opacity<.999)a.errors.push('Uncovered scene swap');
            }
          };
          new MutationObserver(sample).observe(root,{subtree:true,childList:true,attributes:true});sample();
        }""")
        still=film.get_attribute('data-elapsed');page.wait_for_timeout(250)
        assert abs(float(film.get_attribute('data-elapsed'))-float(still))<.08
        page.screenshot(path=str(OUT/f'level2-adapted-{state}.png'),full_page=True)
        page.get_by_label('Speed',exact=True).select_option('4')
        page.get_by_role('button',name='Play',exact=True).click()
        if kind=='checklist':
            expect(f.locator('.l2-spoken [role=status]')).to_have_text('What if some metrics mattered more than others?',timeout=40000)
            expect(film).to_have_attribute('data-handoff','idle')
            page.screenshot(path=str(OUT/'level2-100-final-caption-after-cut.png'),full_page=True)
        expect(page.locator('footer')).to_have_attribute('data-completion-count','1',timeout=40000)
        audit=film.evaluate('window.filmAudit')
        assert not audit['errors'],audit
        if kind!='three':assert (6 if kind=='six' else 100) in audit['checklists'],audit
        if kind=='checklist':
            assert audit['shots']==['hundred','perfect','reflection'],audit
            assert audit['cutCaptions']==['Maybe adding more metrics isn’t the answer...', 'What if some metrics mattered more than others?'],audit
        assert set(audit['speakers'])==({'You','Alex'} if kind!='checklist' else {'You'}),audit
        assert audit['swaps'] and min(audit['swaps'])>=.999,audit
        expect(film).to_have_attribute('data-finished','true')
        assert float(f.locator('.l2-film-cover').evaluate('e=>getComputedStyle(e).opacity'))==1
        page.wait_for_timeout(200);expect(page.locator('footer')).to_have_attribute('data-completion-count','1')
        page.get_by_role('button',name='Replay',exact=True).click()
        expect(page.locator('footer')).to_have_attribute('data-completion-count','0')
        expect(f.locator('.l2-film')).to_be_visible()
        page.get_by_role('button',name='Pause',exact=True).click()
        record(state+': authored checklist text restored, correct trim, You/Alex colours, opaque swaps, completion and fresh replay')
    # Visible-time hold and reduced-motion coverage use the same shipped film.
    page.goto(origin+'Level2-animation.html?state=six&reduced=1',wait_until='networkidle')
    f=page.frame_locator('iframe');expect(f.locator('.l2-film')).to_be_visible()
    f.locator('.l2-film').evaluate("""()=>{Object.defineProperty(document,'hidden',{configurable:true,value:true});document.dispatchEvent(new Event('visibilitychange'));}""")
    before=float(f.locator('.l2-film').get_attribute('data-elapsed'));page.wait_for_timeout(600)
    assert abs(float(f.locator('.l2-film').get_attribute('data-elapsed'))-before)<.08
    f.locator('.l2-film').evaluate("""()=>{Object.defineProperty(document,'hidden',{configurable:true,value:false});document.dispatchEvent(new Event('visibilitychange'));}""")
    page.get_by_label('Speed',exact=True).select_option('4')
    expect(page.locator('footer')).to_have_attribute('data-completion-count','1',timeout=40000)
    record('Hidden-page reading time holds and reduced-motion scenes resume to a real completion')
    for w in [390,320]:
        page.set_viewport_size({'width':w,'height':900});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    page.set_viewport_size({'width':1366,'height':900})
    page.goto(origin+'Level2-animation.html?state=full',wait_until='networkidle')
    expect(page.get_by_label('Speed',exact=True)).to_have_value('1')
    expect(page.locator('footer')).to_have_attribute('data-completion-count','3',timeout=90000)
    record('All three placeholder scenes play once each at normal speed; the 100-metric prelude is retained and no separate 10/25 or priority page is inserted')
    c.close();b.close()
assert not errors,errors
assert not external,external
record('Adapted offline preview has no browser runtime errors or external asset requests')
(OUT/'level2-animation-preview-results.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'runtimeErrors':errors,'externalRequests':external},indent=2)+'\n')
