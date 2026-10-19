"""Read-only author preview: exercise the actual offline review archive, not game code."""
import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit
from zipfile import ZipFile
from playwright.sync_api import sync_playwright, expect

root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'play/LEVEL1_ANIMATION_PREVIEW.json').read_text())
archive=root/'play'/manifest['archive']
assert hashlib.sha256(archive.read_bytes()).hexdigest()==manifest['zipSha256']
with ZipFile(archive) as z:
    assert z.testzip() is None
    files={name:z.read(name) for name in z.namelist()}
assert hashlib.sha256(files[manifest['html']]).hexdigest()==manifest['htmlSha256']
checks,errors,external=[],[],[]
out=root/'test-results';out.mkdir(exist_ok=True)
def record(message):
    checks.append(message);print('PASS',message,flush=True)
def seek(page,seconds):
    page.get_by_label('Preview time in seconds',exact=True).fill(str(seconds))
    page.get_by_role('button',name='Seek',exact=True).click()

def open_branch(page,id):
    page.goto('https://level1-animation.test/START-HERE.html',wait_until='networkidle')
    label=next(x['label'] for x in manifest['metrics'] if x['id']==id)
    page.get_by_role('link',name=label,exact=True).click()
    expect(page.locator('.l1-film')).to_have_attribute('data-metric',id,timeout=10000)
    expect(page.get_by_label('Preview branch',exact=True)).to_have_value(id)

expected=[
 ('pre-class-preparation','I finished everything on the list!','What was the main idea in the reading?','Uh... I finished the checklist.'),
 ('in-class-participation','I agree! Same here!','Can you explain why?','I just wanted to participate.'),
 ('on-task-focus','Look, I stayed on task the whole time!','What did you discover?','I... kept the page open.'),
 ('in-class-discussion-quality','Could you elaborate? I’d like to build on that.','What new idea came out of the discussion?','I followed the discussion checklist.'),
 ('learning-reflection-quality','Before, I thought... Now, I think...','What actually changed your mind?','That’s the format on the rubric.'),
 ('online-peer-response-quality','Specific suggestion? Check. Follow-up question? Check!','Did you really discuss their ideas?','I met every response criterion.'),
]
record('The independent review ZIP is intact and its embedded animation matches the recorded build hash')
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    context=browser.new_context(viewport={'width':1366,'height':1000})
    context.set_offline(True)
    def serve(route):
        url=urlsplit(route.request.url)
        name=url.path.lstrip('/')
        if url.netloc=='level1-animation.test' and name in files:
            route.fulfill(status=200,content_type='text/html' if name.endswith('.html') else 'text/plain',body=files[name])
        else:
            external.append(route.request.url);route.abort()
    context.route('**/*',serve)
    page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
    for id,boast,question,reveal in expected:
        open_branch(page,id)
        seek(page,3.2);expect(page.locator('.l1-film')).to_contain_text(boast)
        assert page.locator('.l1-film img').evaluate_all('es=>es.length>0 && es.every(e=>e.complete && e.naturalWidth>0)')
        seek(page,6.3);expect(page.locator('.l1-film')).to_contain_text(question)
        seek(page,10);expect(page.locator('.l1-film')).to_contain_text(reveal)
        page.screenshot(path=str(out/('level1-animation-'+id+'.png')))
        seek(page,14);expect(page.locator('.l1-film')).to_have_attribute('data-phase','common')
        expect(page.locator('.l1-film')).to_contain_text('Professor! I figured out exactly what you were looking for!')
        seek(page,24.5);expect(page.locator('.l1-film')).to_have_attribute('data-phase','office')
        expect(page.locator('.l1-film')).to_contain_text('Great work, Taylor!')
        expect(page.locator('.l1-office-result')).to_contain_text(next(x['label'] for x in manifest['metrics'] if x['id']==id))
        expect(page.locator('.l1-film')).to_contain_text('The numbers look great... but something still feels wrong.')
        expect(page.get_by_test_id('completion-status')).to_contain_text('completion events: 0')
        record(id+': authored branch dialogue, loaded art, common ending and matching office result are available offline')
    # One complete real-time run establishes playback and single completion.
    page.get_by_role('button',name='New preview run',exact=True).click()
    expect(page.locator('.l1-film')).to_have_attribute('data-phase','branch')
    page.get_by_role('button',name='Play video',exact=True).click()
    expect(page.get_by_test_id('completion-status')).to_have_text('Sequence complete · animationComplete sent 1 time',timeout=42000)
    page.get_by_role('button',name='New preview run',exact=True).click()
    expect(page.get_by_test_id('completion-status')).to_contain_text('completion events: 0')
    page.get_by_label('Preview player name',exact=True).fill('Riley')
    page.get_by_label('Preview branch',exact=True).select_option('on-task-focus')
    expect(page.locator('.l1-film')).to_have_attribute('data-metric','on-task-focus',timeout=15000)
    seek(page,23.5);expect(page.locator('.l1-film')).to_contain_text('Great work, Riley!')
    record('A normal-speed 33.4-second run completes once; a fresh run resets, and branch switching preserves the edited player name')
    page.get_by_label('Preview segment',exact=True).select_option('common')
    expect(page.locator('.l1-film')).to_have_attribute('data-phase','common',timeout=15000)
    page.get_by_role('button',name='Play video',exact=True).click()
    expect(page.get_by_test_id('completion-status')).to_have_text('Segment preview complete · no gameplay event sent',timeout=7000)
    record('The separate common segment plays to its end without emitting a gameplay completion event')
    page.set_viewport_size({'width':390,'height':900})
    page.goto('https://level1-animation.test/START-HERE.html',wait_until='networkidle')
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    expect(page.get_by_role('link')).to_have_count(6)
    page.get_by_role('link',name='Pre-class Preparation',exact=True).click()
    expect(page.locator('.l1-film')).to_have_attribute('data-metric','pre-class-preparation',timeout=15000)
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    page.get_by_label('Reduce motion',exact=True).check()
    seek(page,3.2);expect(page.locator('.l1-film')).to_contain_text('I finished everything on the list!')
    record('The six-entry launcher and original branch controls fit a phone viewport, and reduced-motion preview remains available')
    context.close();browser.close()
assert not errors,errors
assert not external,external
record('The exact offline animation archive makes no external asset requests and produces no browser runtime errors')
result={'passed':len(checks),'checks':checks,'runtimeErrors':errors,'externalRequests':external,'playback':'One complete normal-motion real-time run, all six branches checked at authored dialogue/ending frames, and a real-time common segment'}
(out/'level1-animation-preview-results.json').write_text(json.dumps(result,indent=2)+'\n')
