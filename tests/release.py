"""Check the actual downloadable ZIP offline after packaging.
Reading intervals use the browser clock; level2.py checks them at real speed.
"""
import json
import hashlib
import zipfile
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

checks, errors = [], []
artifacts = {}
manifest = json.loads(Path('play/LATEST.json').read_text())
assert {entry['html'] for entry in manifest['entries']} == {'Level1.html', 'Level2.html', 'Gaming-the-System.html'}
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
checks.append('All three latest ZIPs are intact, self-contained and byte-identical to their production builds and manifest')


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


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1366, 'height': 768})
    context.set_offline(True)
    context.route('https://release.test/**', lambda route: route.fulfill(status=200, content_type='text/html', body=artifacts['Level2.html']))
    page = context.new_page()
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.clock.install()
    page.goto('https://release.test/', wait_until='networkidle')
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
    for count in [10, 25, 100]:
        page.get_by_role('button', name='Add more metrics', exact=True).click()
        advance(page)
        expect(page.locator('.l2-reported-count')).to_have_text(str(count))
        expect(page.locator('.l2-matrix [data-active=true]')).to_have_count(count)
    scene(page, lines=2)
    expect(page.get_by_role('button', name='Continue to Level 3', exact=True)).to_be_disabled()
    expect(page.get_by_role('button', name='Guide', exact=True)).to_have_count(0)
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    checks.append('Packaged Level2.html completes 3 → 6 → 10 → 25 → 100 offline with normal motion')
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
