"""Check the actual downloadable ZIP offline after packaging.
Reading intervals use the browser clock; level2.py checks them at real speed.
"""
import json
import zipfile
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

archive = Path('play/Level2-play-v6.zip')
checks, errors = [], []
with zipfile.ZipFile(archive) as bundle:
    assert bundle.testzip() is None
    artifacts = {name: bundle.read(name) for name in ['Level2.html', 'Levels1-and-2.html']}
    assert artifacts['Level2.html'] == Path('dist-level2/index.html').read_bytes()
    assert artifacts['Levels1-and-2.html'] == Path('dist/index.html').read_bytes()
checks.append('ZIP integrity and byte identity with both production builds')


def advance(page, seconds=24):
    for _ in range(seconds):
        page.clock.run_for(1000)
        page.wait_for_timeout(12)


def scene(page, lines=3):
    page.get_by_role('button', name='Observe the class', exact=True).click()
    for _ in range(lines - 1): page.get_by_role('button', name='Continue scene', exact=True).click()
    page.get_by_role('button', name='Return to dashboard', exact=True).click()
    advance(page)


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
    context.route('https://release.test/**', lambda route: route.fulfill(status=200, content_type='text/html', body=artifacts['Levels1-and-2.html']))
    page = context.new_page()
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto('https://release.test/', wait_until='networkidle')
    expect(page.get_by_role('dialog', name='Workbench guide')).to_be_visible()
    expect(page.locator('.level-one')).to_be_visible()
    checks.append('Packaged Levels1-and-2.html starts at Level 1 with its guide')
    context.close()
    browser.close()
assert not errors, errors
checks.append('Packaged entries have no browser runtime errors')
Path('test-results/release-results.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'runtimeErrors':errors},indent=2)+'\n')
for check in checks: print('PASS',check)
