"""Exercise the self-contained Level 3 build and its adaptive paths offline.
Presentation waits use the browser clock; real-time pacing is checked separately.
"""
import itertools
import json
import re
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

HTML = Path('dist-level3/index.html').read_bytes()
OUT = Path('test-results')
OUT.mkdir(exist_ok=True)
checks, errors = [], []
IDS = ['prep', 'part', 'focus', 'discuss', 'reflect', 'peer']


def record(name):
    checks.append(name)
    print('PASS', name, flush=True)


def advance(page, seconds=8):
    for _ in range(seconds):
        page.clock.run_for(1000)
        page.wait_for_timeout(15)


def begin(browser, width=1366, height=900, motion='reduce', script=None):
    context = browser.new_context(viewport={'width': width, 'height': height}, reduced_motion=motion)
    context.set_offline(True)
    context.route('https://level-three.test/**', lambda route: route.fulfill(status=200, content_type='text/html', body=HTML))
    if script: context.add_init_script(script)
    page = context.new_page()
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.clock.install()
    page.goto('https://level-three.test/', wait_until='networkidle')
    return context, page


def intro(page):
    advance(page)
    expect(page.locator('.level-three')).to_have_attribute('data-phase', 'intro')
    page.get_by_role('button', name='Choose priorities', exact=True).click()


def choose(page, ids=IDS[:3]):
    for id in ids: page.get_by_test_id('level3-metric-' + id).click()
    page.get_by_role('button', name='Set the weights', exact=True).click()


def set_weights(page, values, ids=IDS[:3]):
    for index, id in enumerate(ids):
        slider = page.get_by_label({'prep':'Pre-class Preparation','part':'In-class Participation','focus':'On-task Focus','discuss':'In-class Discussion Quality','reflect':'Learning Reflection Quality','peer':'Online Peer Response Quality'}[id] + ' weight', exact=True)
        if not slider.is_disabled():
            slider.evaluate('''(input, value) => {
              Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set.call(input, value);
              input.dispatchEvent(new Event('input', {bubbles:true}));
            }''', values[index])
        expect(page.get_by_test_id('weight-card-' + id).locator('output')).to_have_text(str(values[index]) + '%')
        if page.get_by_test_id('confirm-' + id).is_enabled(): page.get_by_test_id('confirm-' + id).click()
        expect(slider).to_be_disabled()
    expect(page.locator('.l3-weight-card[data-confirmed=true]')).to_have_count(3)


def finish_scene(page, expected=None):
    expect(page.get_by_test_id('level3-cinematic')).to_be_visible()
    shots = []
    while True:
        shots.append(page.get_by_test_id('level3-cinematic').get_attribute('data-shot-id'))
        next_button = page.get_by_role('button', name='Continue scene', exact=True)
        if not next_button.count(): break
        next_button.click()
    if expected: assert shots == expected, shots
    page.get_by_role('button', name='Return to dashboard', exact=True).click()
    page.locator('.l3-results').scroll_into_view_if_needed()
    advance(page, 12)
    expect(page.locator('.l3-run-rows [data-shown=true]')).to_have_count(3)


def run(page, expected=None):
    page.get_by_role('button', name='Run evaluation', exact=True).click()
    page.locator('.l3-publish').scroll_into_view_if_needed()
    advance(page, 4)
    expect(page.locator('.level-three')).to_have_attribute('data-phase', 'publish')
    page.get_by_role('button', name='Observe the class', exact=True).click()
    finish_scene(page, expected)


def no_overflow(page):
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), 'Horizontal overflow'
    assert page.evaluate('Array.from(document.images).every(image => image.complete && image.naturalWidth > 0)'), 'Missing artwork'


with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    context, page = begin(browser)
    expect(page.get_by_role('heading', name='The weighting trap.')).to_be_visible()
    expect(page.get_by_role('button', name='Guide', exact=True)).to_have_count(0)
    intro(page)
    expect(page.get_by_role('button', name='Set the weights', exact=True)).to_be_disabled()
    for id in IDS[:3]: page.get_by_test_id('level3-metric-' + id).click()
    page.get_by_test_id('level3-metric-peer').click(force=True)
    expect(page.locator('.l3-metric-card[aria-pressed=true]')).to_have_count(3)
    expect(page.locator('.l3-status')).to_contain_text('Deselect one')
    page.get_by_test_id('level3-metric-focus').click()
    page.get_by_test_id('level3-metric-peer').click()
    expect(page.get_by_test_id('level3-metric-peer')).to_have_attribute('aria-pressed','true')
    record('Dedicated Level 3 chapter dialogue waits for its button; selection enforces exactly three and allows swaps')
    context.close()

    context, page = begin(browser)
    intro(page); choose(page)
    slider = page.get_by_label('Pre-class Preparation weight', exact=True)
    slider.focus(); page.keyboard.press('End')
    expect(page.get_by_test_id('weight-card-prep').locator('output')).to_have_text('100%')
    expect(page.get_by_test_id('weight-card-part').locator('output')).to_have_text('0%')
    page.get_by_role('button', name='Reset weights', exact=True).click()
    slider.evaluate("(input)=>{Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(input,80);input.dispatchEvent(new Event('input',{bubbles:true}));}")
    page.get_by_test_id('confirm-prep').click()
    expect(slider).to_be_disabled()
    second = page.get_by_label('In-class Participation weight', exact=True)
    third = page.get_by_label('On-task Focus weight', exact=True)
    expect(second).to_be_enabled(); expect(third).to_be_enabled()
    second.focus();page.keyboard.press('ArrowRight')
    expect(page.get_by_test_id('weight-card-part').locator('output')).to_have_text('11%')
    expect(page.get_by_test_id('weight-card-focus').locator('output')).to_have_text('9%')
    second.evaluate("(input)=>{Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(input,15);input.dispatchEvent(new Event('input',{bubbles:true}));}")
    expect(page.get_by_test_id('weight-card-focus').locator('output')).to_have_text('5%')
    expect(page.get_by_role('button', name='Run evaluation', exact=True)).to_be_disabled()
    page.get_by_test_id('confirm-focus').click()
    expect(second).to_be_disabled();expect(third).to_be_disabled()
    expect(page.get_by_test_id('confirm-part')).to_have_text('Auto-confirmed')
    expect(page.get_by_role('button', name='Run evaluation', exact=True)).to_be_enabled()
    page.get_by_role('button', name='Reset weights', exact=True).click()
    expect(page.locator('.l3-weight-card[data-confirmed=true]')).to_have_count(0)
    expect(slider).to_be_enabled()
    record('80/10/10 allows either remaining slider to move to 15/5; confirming the rightmost card auto-confirms the middle card')
    set_weights(page, [70,20,10])
    advance(page,1)
    page.screenshot(path=str(OUT / 'level3-weights-desktop.png'), full_page=True, animations='disabled')
    run(page, ['level3.prep.high','level3.part.low','level3.focus.low'])
    expect(page.locator('.student-behaviour')).to_have_text('Low-weight areas get less attention.')
    expect(page.locator('.l3-finding')).to_contain_text('70%')
    record('70/20/10 waits for Observe the class, plays exactly three matching intensity shots and reveals classroom responses sequentially')
    page.get_by_role('button', name='Try a better balance', exact=True).click()
    set_weights(page, [70,20,10])
    expect(page.get_by_role('button', name='Run evaluation', exact=True)).to_be_disabled()
    expect(page.locator('.l3-editor-status')).to_contain_text('Make the split more even.')
    page.get_by_role('button', name='Reset weights', exact=True).click()
    set_weights(page, [34,33,33])
    run(page, ['level3.prep.medium','level3.part.medium','level3.focus.medium'])
    page.get_by_role('button', name='Compare the patterns', exact=True).click()
    expect(page.locator('.l3-comparison-card')).to_have_count(2)
    expect(page.locator('.near-even .l3-row-weight')).to_have_text(['34%','33%','33%'])
    expect(page.locator('.uneven .l3-row-weight')).to_have_text(['70%','20%','10%'])
    expect(page.locator('.near-even [data-effort=medium]')).to_have_count(3)
    advance(page,1)
    page.screenshot(path=str(OUT / 'level3-compare-desktop.png'), full_page=True, animations='disabled')
    record('Uneven-first path requires an improved split and compares the actual first run with the near-even second run')
    assert 'Goodhart' not in page.locator('body').inner_text()
    page.get_by_role('button', name='Watch Alex’s response', exact=True).click()
    while page.get_by_role('button', name='Continue scene', exact=True).count(): page.get_by_role('button', name='Continue scene', exact=True).click()
    page.get_by_role('button', name='Reveal Goodhart’s Law', exact=True).click()
    assert 'Goodhart' not in page.locator('.l3-scene-copy').inner_text()
    page.get_by_role('button', name='Continue scene', exact=True).click()
    expect(page.get_by_role('heading', name='Goodhart’s Law', exact=True)).to_be_visible()
    page.get_by_role('button', name='Enter Design Lab', exact=True).click()
    expect(page.get_by_test_id('design-lab-entry')).to_be_visible()
    expect(page.locator('.level-three')).to_have_count(0)
    assert 'The experiment is complete' not in page.locator('body').inner_text()
    record('Alex’s response leads to the final theory reveal, then directly enters the reserved Design Lab without a completion page')
    context.close()

    context, page = begin(browser)
    intro(page); choose(page); set_weights(page,[34,33,33]); run(page)
    page.get_by_role('button', name='Create a contrast', exact=True).click()
    set_weights(page,[34,33,33])
    expect(page.get_by_role('button', name='Run evaluation', exact=True)).to_be_disabled()
    expect(page.locator('.l3-editor-status')).to_contain_text('20 points')
    page.get_by_role('button', name='Reset weights', exact=True).click()
    set_weights(page,[70,20,10]); run(page)
    page.get_by_role('button', name='Compare the patterns', exact=True).click()
    expect(page.locator('.near-even .eyebrow')).to_have_text('YOUR TEST · ROUND 1')
    expect(page.locator('.uneven .eyebrow')).to_have_text('YOUR TEST · ROUND 2')
    record('Near-even-first path requires a clear contrast and compares both player-tested runs without a redundant third round')
    context.close()

    context, page = begin(browser)
    intro(page); choose(page); set_weights(page,[70,20,10]); run(page)
    page.get_by_role('button', name='Try a better balance', exact=True).click()
    set_weights(page,[50,30,20]); run(page)
    expect(page.locator('.maya-bubble p')).to_have_text('It’s still uneven. I’ll test a nearly equal split.')
    expect(page.locator('.alex-bubble p')).to_have_text('About a third each? Okay! 🧮')
    expect(page.locator('.level-three')).to_have_attribute('data-round','2')
    page.get_by_role('button', name='Test 34 / 33 / 33', exact=True).click()
    page.locator('.l3-publish').scroll_into_view_if_needed(); advance(page,4)
    page.get_by_role('button', name='Observe the class', exact=True).click()
    finish_scene(page,['level3.prep.medium','level3.part.medium','level3.focus.medium'])
    expect(page.locator('.l3-round-label')).to_have_text('BALANCE CHECK · 34 / 33 / 33')
    page.get_by_role('button', name='Compare the patterns', exact=True).click()
    expect(page.locator('.near-even .eyebrow')).to_have_text('BALANCE CHECK')
    expect(page.locator('.uneven .l3-row-weight')).to_have_text(['70%','20%','10%'])
    record('A partial rebalance leads to an explicit 34/33/33 balance check, with the original uneven run retained for comparison')
    context.close()

    for ids in itertools.combinations(IDS,3):
        context,page=begin(browser)
        intro(page);choose(page,ids);set_weights(page,[34,33,33],ids)
        run(page,[f'level3.{id}.medium' for id in ids])
        assert [row.get_attribute('data-metric') for row in page.locator('.l3-run-rows li').all()] == list(ids)
        no_overflow(page)
        record('Priority trio ' + '+'.join(ids) + ' uses the selected metrics and the near-even intensity override')
        context.close()

    for width,height in [(1366,768),(768,1024),(390,844),(320,640)]:
        context,page=begin(browser,width,height,motion='no-preference')
        intro(page); no_overflow(page); choose(page); no_overflow(page)
        set_weights(page,[70,20,10]); no_overflow(page); run(page); no_overflow(page)
        page.get_by_role('button',name='Try a better balance',exact=True).click()
        set_weights(page,[34,33,33]);run(page)
        page.get_by_role('button',name='Compare the patterns',exact=True).click();no_overflow(page)
        if width==390:
            advance(page,1)
            page.screenshot(path=str(OUT/'level3-compare-mobile.png'),full_page=True, animations='disabled')
        page.reload(wait_until='networkidle')
        expect(page.locator('.level-three')).to_have_attribute('data-phase','intro')
        page.evaluate("window.dispatchEvent(new PageTransitionEvent('pageshow',{persisted:true}))")
        expect(page.locator('.level-three')).to_have_attribute('data-phase','intro')
        record(f'{width}px normal-motion playthrough and comparison have no overflow; reload and restored pages restart')
        context.close()

    context,page=begin(browser)
    intro(page);choose(page);set_weights(page,[70,20,10])
    page.get_by_role('button',name='Run evaluation',exact=True).click()
    page.get_by_role('button',name='Restart',exact=True).click()
    before=page.locator('.l3-publish [data-published=true]').count()
    advance(page,8)
    expect(page.get_by_role('dialog')).to_be_visible()
    assert page.locator('.l3-publish [data-published=true]').count()==before
    page.keyboard.press('Escape');advance(page,4);page.get_by_role('button',name='Observe the class',exact=True).click();finish_scene(page)
    page.get_by_role('button',name='Restart',exact=True).click()
    page.get_by_role('button',name='Restart Level 3',exact=True).click()
    expect(page.locator('.level-three')).to_have_attribute('data-phase','intro')
    record('Restart dialog holds publication beats; Escape resumes and confirmed restart clears both runs and selections')
    context.close()

    context,page=begin(browser,script="for (const name of ['localStorage','sessionStorage']) Object.defineProperty(window,name,{get(){throw new Error('blocked storage');}}); Object.defineProperty(window,'AudioContext',{value:undefined});")
    intro(page);choose(page);set_weights(page,[34,33,33]);run(page)
    expect(page.get_by_role('button',name='No audio',exact=True)).to_be_disabled()
    assert not re.search(r'[\u4e00-\u9fff]',page.locator('body').inner_text())
    record('All-English Level 3 remains playable without browser storage or Web Audio')
    context.close();browser.close()
assert not errors,errors
record('No browser runtime errors across all offline Level 3 paths')
(OUT/'level3-results.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'runtimeErrors':errors},indent=2)+'\n')
