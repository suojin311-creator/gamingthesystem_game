"""Check the actual downloadable ZIP offline after packaging.
Reading intervals use the browser clock; level2.py checks them at real speed.
"""
import json
import re
import hashlib
import zipfile
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

checks, errors = [], []
artifacts = {}
manifest = json.loads(Path('play/LATEST.json').read_text())
assert {entry['html'] for entry in manifest['entries']} == {'Level1.html', 'Level2.html', 'Level3.html', 'Gaming-the-System.html'}
for entry in manifest['entries']:
    archive = Path('play') / entry['archive']
    with zipfile.ZipFile(archive) as bundle:
        assert bundle.testzip() is None
        assert set(bundle.namelist()) == {entry['html'], 'START-HERE.txt'}
        artifacts[entry['html']] = bundle.read(entry['html'])
        assert artifacts[entry['html']] == Path(entry['build']).read_bytes()
        assert entry['html'] in bundle.read('START-HERE.txt').decode()
    assert hashlib.sha256(artifacts[entry['html']]).hexdigest() == entry['htmlSha256']
    assert hashlib.sha256(archive.read_bytes()).hexdigest() == entry['zipSha256']
checks.append('All four latest ZIPs are intact, self-contained and byte-identical to their production builds and manifest')
review = manifest['reviewBundle']
with zipfile.ZipFile(Path('play') / review['archive']) as bundle:
    assert bundle.testzip() is None
    assert set(bundle.namelist()) == {'Level3/Level3.html', 'Full-game/Gaming-the-System.html', 'START-HERE.txt'}
    for name, html in [('Level3/Level3.html', 'Level3.html'), ('Full-game/Gaming-the-System.html', 'Gaming-the-System.html')]:
        assert bundle.read(name) == artifacts[html]
        assert hashlib.sha256(bundle.read(name)).hexdigest() == review['htmlSha256'][name]
assert hashlib.sha256((Path('play') / review['archive']).read_bytes()).hexdigest() == review['zipSha256']
checks.append('The review ZIP contains separate Level 3 and connected Levels 1–3 HTMLs, identical to their tested latest packages')


def advance(page, seconds=24):
    for _ in range(seconds):
        page.clock.run_for(1000)
        page.wait_for_timeout(12)


def scene(page, lines=3):
    page.get_by_role('button', name='Observe the class', exact=True).click()
    for _ in range(lines - 1): page.get_by_role('button', name='Continue scene', exact=True).click()
    page.get_by_role('button', name='Return to dashboard', exact=True).click()
    advance(page)


def level_one(page):
    expect(page.get_by_role('dialog', name='Workbench guide')).to_be_visible()
    page.get_by_role('button', name='Skip guide').click()
    page.get_by_test_id('metric-prep').click()
    page.get_by_role('button', name='Make a prediction', exact=True).click()
    page.get_by_label('What do you expect students to do?').fill('Students will explain the reading.')
    page.get_by_role('button', name='Run evaluation', exact=True).click()
    advance(page, 8)
    scene(page)
    expect(page.locator('.student .student-behaviour')).to_have_text('Skimming just to finish.')
    expect(page.locator('.alex-bubble p')).to_have_text(['I finished the whole list! 📋', 'The reading? I mostly skimmed it 😬'])
    expect(page.get_by_role('button', name='Continue to Level 2', exact=True)).to_be_visible()


def finish_two(page):
    scene(page)
    page.get_by_role('button', name='Cover the gaps', exact=True).click()
    page.get_by_role('button', name='Add remaining metrics', exact=True).click()
    advance(page, 6)
    scene(page)
    page.get_by_role('button', name='Add more metrics', exact=True).click()
    advance(page, 30)
    expect(page.locator('.l2-reported-count')).to_have_text('100')
    scene(page, lines=2)


def choose_three(page):
    advance(page,8)
    page.get_by_role('button',name=re.compile(r'^(Choose|Review) priorities$')).click()
    for id in ['prep','part','focus']:
        card=page.get_by_test_id('level3-metric-'+id)
        if card.get_attribute('aria-pressed')!='true':card.click()
    page.get_by_role('button',name='Set the weights',exact=True).click()


def weights_three(page, values):
    for index,id in enumerate(['prep','part','focus']):
        slider=page.get_by_test_id('weight-card-'+id).locator('input')
        if not slider.is_disabled():slider.evaluate('''(input,value)=>{Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(input,value);input.dispatchEvent(new Event('input',{bubbles:true}));}''', values[index])
        if page.get_by_test_id('confirm-'+id).is_enabled(): page.get_by_test_id('confirm-'+id).click()
    page.get_by_role('button',name='Make a prediction',exact=True).click()
    page.get_by_test_id('predict-prep').click()
    page.get_by_role('button',name='Run evaluation',exact=True).click()
    page.locator('.l3-publish').scroll_into_view_if_needed();advance(page,5)
    page.get_by_role('button',name='Observe the class',exact=True).click()
    for _ in range(2):page.get_by_role('button',name='Continue scene',exact=True).click()
    page.get_by_role('button',name='Return to dashboard',exact=True).click()
    page.locator('.l3-results').scroll_into_view_if_needed();advance(page,12)


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1366, 'height': 768})
    context.set_offline(True)
    context.route('https://release.test/**', lambda route: route.fulfill(status=200, content_type='text/html', body=artifacts['Level2.html']))
    page = context.new_page()
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.clock.install()
    page.goto('https://release.test/', wait_until='networkidle')
    expect(page.get_by_role('button',name='Restart',exact=True)).to_have_count(0)
    expect(page).to_have_title('Gaming the System')
    expect(page.locator('.level-two')).to_have_attribute('data-phase', 'intro')
    advance(page, 8)
    expect(page.locator('.level-two')).to_have_attribute('data-phase', 'intro')
    page.get_by_role('button', name='Choose three metrics', exact=True).click()
    expect(page.locator('.level-two')).to_have_attribute('data-phase', 'choose')
    expect(page.get_by_role('button', name='Guide', exact=True)).to_have_count(0)
    for id in ['prep', 'part', 'focus']: page.get_by_test_id('level2-metric-' + id).click()
    page.get_by_role('button', name='Run evaluation', exact=True).click()
    advance(page, 6)
    scene(page)
    page.get_by_role('button', name='Cover the gaps', exact=True).click()
    page.get_by_role('button', name='Add remaining metrics', exact=True).click()
    advance(page, 6)
    scene(page)
    page.get_by_role('button', name='Add more metrics', exact=True).click()
    advance(page, 30)
    expect(page.locator('.l2-reported-count')).to_have_text('100')
    expect(page.locator('.l2-matrix [data-active=true]')).to_have_count(100)
    scene(page, lines=2)
    expect(page.get_by_role('button', name='Continue to Level 3', exact=True)).to_be_disabled()
    expect(page.get_by_role('button', name='Guide', exact=True)).to_have_count(0)
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    checks.append('Packaged Level2.html completes 3 → 6 → 10 → 25 → 100 offline with normal motion')
    context.close()
    context = browser.new_context()
    context.set_offline(True)
    context.route('https://release.test/**', lambda route: route.fulfill(status=200, content_type='text/html', body=artifacts['Level3.html']))
    page = context.new_page()
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.clock.install()
    page.goto('https://release.test/', wait_until='networkidle')
    choose_three(page);weights_three(page,[34,33,33])
    page.get_by_role('button',name='Try another split',exact=True).click()
    weights_three(page,[70,20,10])
    page.get_by_role('button',name='Compare the patterns',exact=True).click()
    expect(page.locator('.near-even .l3-row-weight')).to_have_text(['34%','33%','33%'])
    expect(page.locator('.uneven .l3-row-weight')).to_have_text(['70%','20%','10%'])
    checks.append('Packaged standalone Level3.html completes both weight tests and compares the actual results offline')
    context.close()
    context = browser.new_context()
    context.set_offline(True)
    context.route('https://release.test/**', lambda route: route.fulfill(status=200, content_type='text/html', body=artifacts['Level1.html']))
    page = context.new_page()
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.clock.install()
    page.goto('https://release.test/', wait_until='networkidle')
    level_one(page)
    expect(page.get_by_role('button', name='Continue to Level 2', exact=True)).to_be_disabled()
    expect(page.locator('.level-two')).to_have_count(0)
    page.get_by_role('button', name='Replay scene', exact=True).click()
    expect(page.get_by_test_id('cinematic-placeholder')).to_be_visible()
    checks.append('Packaged Level1.html includes the latest behaviour and two replies, stops after Level 1 and permits replay')
    page.reload(wait_until='networkidle')
    expect(page.get_by_role('dialog', name='Workbench guide')).to_be_visible()
    expect(page.locator('.level-one')).to_be_visible()
    checks.append('Standalone Level 1 reload starts a fresh Level 1 run')
    context.close()
    context = browser.new_context()
    context.set_offline(True)
    context.route('https://release.test/**', lambda route: route.fulfill(status=200, content_type='text/html', body=artifacts['Gaming-the-System.html']))
    page = context.new_page()
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.clock.install()
    page.goto('https://release.test/', wait_until='networkidle')
    level_one(page)
    page.get_by_role('button', name='Sound on', exact=True).click()
    page.get_by_role('button', name='Continue to Level 2', exact=True).click()
    expect(page.locator('.level-two')).to_have_attribute('data-phase', 'intro')
    expect(page.get_by_role('button', name='Sound off', exact=True)).to_be_visible()
    advance(page, 8)
    page.get_by_role('button', name='Choose three metrics', exact=True).click()
    for id in ['prep', 'part', 'focus']: page.get_by_test_id('level2-metric-' + id).click()
    page.get_by_role('button', name='Run evaluation', exact=True).click()
    advance(page, 6)
    expect(page.locator('.l2-reported-count')).to_have_text('3')
    checks.append('Packaged combined game continues from the current Level 1 into playable Level 2 and keeps sound preference')
    finish_two(page)
    page.get_by_role('button',name='Continue to Level 3',exact=True).click()
    expect(page.locator('.level-three')).to_have_attribute('data-phase','intro')
    expect(page.get_by_role('button',name='Sound off',exact=True)).to_be_visible()
    choose_three(page);weights_three(page,[70,20,10])
    expect(page.get_by_role('button',name='Try another split',exact=True)).to_be_visible()
    checks.append('Packaged combined game connects Level 1 → Level 2 → playable Level 3 in one open run')
    page.reload(wait_until='networkidle')
    expect(page.get_by_role('dialog', name='Workbench guide')).to_be_visible()
    expect(page.locator('.level-one')).to_be_visible()
    checks.append('Combined preview reload starts from Level 1 rather than restoring Level 2')
    context.close()
    browser.close()
assert not errors, errors
checks.append('Packaged entries have no browser runtime errors')
Path('test-results').mkdir(exist_ok=True)
Path('test-results/release-results.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'runtimeErrors':errors},indent=2)+'\n')
for check in checks: print('PASS',check)
