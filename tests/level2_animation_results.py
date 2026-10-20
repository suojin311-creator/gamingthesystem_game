"""Check all three packaged post-film result layouts and production-only callbacks."""
import json
from pathlib import Path
from zipfile import ZipFile
from playwright.sync_api import sync_playwright, expect

OUT = Path('test-results')
with ZipFile('play/Level2-play.zip') as archive:
    html = archive.read('Level2.html')
checks, errors = [], []
def record(text):
    checks.append(text)
    print('PASS', text, flush=True)
def advance(page, seconds=8):
    for _ in range(seconds):
        page.clock.run_for(1000)
        page.wait_for_timeout(20)
def warning(page, count):
    card=page.locator('.l2-results .l2-students')
    def state():return card.evaluate("e=>getComputedStyle(e,'::after').animationPlayState")
    def wait_state(value):
        for _ in range(30):
            if state()==value:return
            page.wait_for_timeout(40)
        assert state()==value
    if count==3:
        page.set_viewport_size({'width':390,'height':600})
        page.evaluate('scrollTo(0,0)')
        wait_state('paused')
        before=card.evaluate("e=>e.getAnimations({subtree:true}).find(a=>a.animationName==='l2-student-warning').currentTime")
        page.wait_for_timeout(300)
        after=card.evaluate("e=>e.getAnimations({subtree:true}).find(a=>a.animationName==='l2-student-warning').currentTime")
        assert abs(after-before)<50
    card.scroll_into_view_if_needed();wait_state('running')
    if count==3:
        page.evaluate("Object.defineProperty(document,'hidden',{configurable:true,value:true});document.dispatchEvent(new Event('visibilitychange'))")
        wait_state('paused')
        before=card.evaluate("e=>e.getAnimations({subtree:true}).find(a=>a.animationName==='l2-student-warning').currentTime")
        page.wait_for_timeout(300)
        after=card.evaluate("e=>e.getAnimations({subtree:true}).find(a=>a.animationName==='l2-student-warning').currentTime")
        assert abs(after-before)<50
        page.evaluate("delete document.hidden;document.dispatchEvent(new Event('visibilitychange'))")
        wait_state('running')
    for _ in range(20):
        if float(card.evaluate("e=>getComputedStyle(e,'::after').opacity"))>.8:
            page.screenshot(path=str(OUT/f'level2-student-warning-{count}.png'),full_page=True)
            break
        page.wait_for_timeout(40)
    else:raise AssertionError('Students outline never became visible')
    page.wait_for_timeout(2600)
    events=page.evaluate('(count)=>window.studentWarningEvents.filter(e=>e.round===String(count))',count)
    assert [e['type'] for e in events]==['animationiteration','animationiteration','animationend'],events
    assert float(card.evaluate("e=>getComputedStyle(e,'::after').opacity"))==0
    record(f'{count}-metric Students warning visibly pulses three times and stops' + ('; offscreen/hidden time is held' if count==3 else ''))
def watch(page, count):
    page.get_by_role('button', name='Observe the class', exact=True).click()
    frame = page.frame_locator('iframe[title="Level 2 classroom animation"]')
    expect(frame.locator('.l2-film')).to_be_visible(timeout=30000)
    assert frame.locator('.l2-film').get_attribute('data-player-name') == 'Maya'
    if count == 3:
        expect(frame.locator('.l2-spoken [role=status]')).to_have_text('I’ve completed all three requirements!')
    # Parent-window and stale iframe messages must not complete the active film.
    page.evaluate("window.postMessage({channel:'level2-cinematic',type:'complete',runId:'stale'},'*')")
    frame.locator('.l2-film').evaluate("()=>parent.postMessage({channel:'level2-cinematic',type:'complete',runId:'stale'},'*')")
    expect(page.locator('.level2-cinematic')).to_have_count(1)
    for _ in range(50):
        if not page.locator('.level2-cinematic').count(): break
        page.clock.run_for(1000)
        page.wait_for_timeout(60)
    expect(page.locator('.level2-cinematic')).to_have_count(0, timeout=30000)
    advance(page)
    expect(page.locator('.l2-results .l2-observation')).to_be_visible()
    expect(page.locator('.level-two .conversation')).to_have_count(0)
    expect(page.locator('.l2-results .l2-perspective')).to_have_count(2)
    warning(page,count)
    for width in [1366, 768, 390, 320]:
        page.set_viewport_size({'width': width, 'height': 1000})
        page.wait_for_timeout(80)
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), width
        evidence = page.locator('.l2-results .l2-observation').bounding_box()
        management = page.locator('.l2-results .l2-management').bounding_box()
        students = page.locator('.l2-results .l2-students').bounding_box()
        assert management['y'] >= evidence['y'] + evidence['height'] - 1
        if width > 600:
            assert abs(management['y'] - students['y']) < 1
            assert abs(management['width'] - students['width']) < 1
        else:
            assert students['y'] >= management['y'] + management['height'] - 1
        page.screenshot(path=str(OUT / f'level2-results-{count}-{width}.png'), full_page=True)
    page.set_viewport_size({'width': 1366, 'height': 1000})
    record(f'{count}-metric result has the existing observation and two equal cards, no chat, safe callbacks and no overflow at 1366/768/390/320px')

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1366, 'height': 1000})
    context.set_default_navigation_timeout(120000)
    context.set_default_timeout(15000)
    context.set_offline(True)
    context.route('https://level2-results.test/**', lambda route: route.fulfill(status=200, content_type='text/html', body=html))
    page = context.new_page()
    page.add_init_script("""window.studentWarningEvents=[];for(const type of ['animationiteration','animationend'])addEventListener(type,event=>{if(event.animationName==='l2-student-warning')window.studentWarningEvents.push({type,round:event.target.dataset.round})});""")
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.clock.install()
    page.goto('https://level2-results.test/', wait_until='networkidle')
    advance(page)
    page.get_by_role('button', name='Choose three metrics', exact=True).click()
    for id in ['discuss', 'reflect', 'peer']:
        page.get_by_test_id('level2-metric-' + id).click()
    page.get_by_role('button', name='Run evaluation', exact=True).click()
    advance(page)
    expect(page.locator('.level-two')).to_have_attribute('data-branch', 'quality')
    watch(page, 3)
    page.get_by_role('button', name='Cover the gaps', exact=True).click()
    expect(page.locator('.level-two')).to_have_attribute('data-phase','evaluate')
    expect(page.locator('.level-two')).to_have_attribute('data-round','6')
    expect(page.get_by_role('button', name='Add remaining metrics', exact=True)).to_have_count(0)
    expect(page.get_by_role('checkbox')).to_have_count(6)
    expect(page.locator('.l2-gap-metric[aria-checked=true]:disabled')).to_have_count(3)
    observe=page.get_by_role('button',name='Observe the class',exact=True)
    expect(observe).to_be_disabled()
    advance(page)
    expect(page.locator('.l2-gap-metric[aria-checked=false]')).to_have_count(3)
    pending=[box.get_attribute('data-testid') for box in page.locator('.l2-gap-metric[aria-checked=false]').all()]
    for index,test_id in enumerate(pending):
        expect(observe).to_be_disabled()
        page.get_by_test_id(test_id).click()
        if index<2:expect(observe).to_be_disabled()
    expect(observe).to_be_enabled()
    page.get_by_test_id(pending[-1]).click();expect(observe).to_be_disabled()
    page.get_by_test_id(pending[-1]).click();expect(observe).to_be_enabled()
    expect(page.get_by_role('heading',name='Six metrics. Six green ticks.',exact=True)).to_be_visible()
    expect(page.locator('body')).not_to_contain_text('Illustrative outcomes')
    page.screenshot(path=str(OUT/'level2-six-manual-complete.png'),full_page=True)
    record('Cover the gaps directly opens six cards; the original three stay checked, only player input checks the rest, and all three are required to enable Observe')
    advance(page)
    watch(page, 6)
    expect(page.get_by_role('heading', name='Would more metrics help Alex learn?', exact=True)).to_be_visible()
    page.get_by_role('button', name='Test more metrics', exact=True).click()
    advance(page, 40)
    expect(page.locator('.level-two')).to_have_attribute('data-round', '100')
    expect(page.locator('.level2-cinematic')).to_have_count(0)
    record('The original game alone performs continuous 10/25/100 growth without inserting any extra movie')
    watch(page, 100)
    page.emulate_media(reduced_motion='reduce')
    card=page.locator('.l2-results .l2-students')
    assert card.evaluate("e=>getComputedStyle(e,'::after').animationName")=='none'
    assert card.evaluate("e=>getComputedStyle(e,'::after').opacity")=='1'
    record('Reduced motion retains a steady Students outline without flashing')
    expect(page.get_by_role('heading', name='More metrics. Still chasing marks.', exact=True)).to_be_visible()
    expect(page.get_by_role('button', name='Continue to Level 3', exact=True)).to_be_disabled()
    context.close()
    browser.close()
assert not errors, errors
record('The actual standalone ZIP retains its ending and produces no browser errors')
(OUT / 'level2-animation-results-layout.json').write_text(json.dumps({'passed': len(checks), 'checks': checks, 'runtimeErrors': errors}, indent=2) + '\n')
