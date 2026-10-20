"""Exercise the independent Level 2 ZIP offline, including real-time full playback."""
import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit
from zipfile import ZipFile

from playwright.sync_api import expect, sync_playwright

OUT = Path('test-results')
OUT.mkdir(exist_ok=True)
manifest = json.loads(Path('play/LEVEL2_ANIMATION_PREVIEW.json').read_text())
archive = Path('play') / manifest['archive']
assert hashlib.sha256(archive.read_bytes()).hexdigest() == manifest['zipSha256']
with ZipFile(archive) as bundle:
    assert bundle.testzip() is None
    assert set(bundle.namelist()) == {'START-HERE.html', 'START-HERE.txt', 'Level2-animation.html'}
    files = {name: bundle.read(name) for name in bundle.namelist()}
for name, data in files.items():
    assert hashlib.sha256(data).hexdigest() == manifest['fileSha256'][name]

checks, errors, external = [], [], []


def record(text):
    checks.append(text)
    print('PASS', text, flush=True)


record('The actual independent ZIP passes CRC and all recorded file/ZIP SHA-256 checks')
ORIGIN = 'https://level2-animation.test/'
cases = [
    ('visible-heavy', 'entry', 'three-checklist', 'visible-behaviour-heavy'),
    ('quality-heavy', 'entry', 'three-checklist', 'quality-depth-heavy'),
    ('mixed-broad', 'entry', 'three-checklist', 'mixed-broad'),
    ('six', 'six-checklist', 'expand', None),
    ('10', 'ten', 'ten', None),
    ('25', 'twenty-five', 'twenty-five', None),
    ('100', 'hundred', 'priority', None),
    ('final', 'perfect', 'priority', None),
    ('checking', 'checking', 'checking', None),
]


with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1366, 'height': 900}, reduced_motion='no-preference')
    # Large inline artwork can take longer than the default navigation deadline.
    context.set_default_navigation_timeout(120000)
    context.set_default_timeout(15000)
    context.set_offline(True)

    def serve(route):
        url = urlsplit(route.request.url)
        data = files.get(url.path.lstrip('/')) if url.netloc == 'level2-animation.test' else None
        if data is None:
            external.append(route.request.url)
            route.abort()
        else:
            route.fulfill(status=200, content_type='text/html' if url.path.endswith('.html') else 'text/plain', body=data)

    context.route('**/*', serve)
    page = context.new_page()
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto(ORIGIN + 'START-HERE.html', wait_until='networkidle')
    links = page.locator('nav a')
    expect(links).to_have_count(10)
    for width in [1366, 390, 320]:
        page.set_viewport_size({'width': width, 'height': 900})
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    page.set_viewport_size({'width': 1366, 'height': 900})
    page.screenshot(path=str(OUT / 'level2-animation-launcher.png'), full_page=True)
    record('The offline launcher exposes all ten review entries and fits desktop and phone widths')

    for state, first, last, category in cases:
        page.goto(ORIGIN + f'Level2-animation.html?cinematic=level2&state={state}&paused=1', wait_until='networkidle')
        scene = page.locator('.l2-preview-stage > .l2-scene')
        footer = page.locator('.l2-preview-footer')
        expect(scene).to_have_attribute('data-shot', first)
        expect(footer).to_have_attribute('data-completion-count', '0')
        if category:
            expect(scene).to_have_attribute('data-category', category)
        page.wait_for_function('Array.from(document.images).every(image => image.complete && image.naturalWidth > 0)')
        page.wait_for_timeout(100)
        still = scene.inner_html()
        page.wait_for_timeout(180)
        assert scene.inner_html() == still, 'Paused playhead changed the rendered scene'
        page.get_by_label('Speed', exact=True).select_option('4')
        page.get_by_role('button', name='Play', exact=True).click()
        if category:
            expect(scene).to_have_attribute('data-shot', 'pattern')
            page.get_by_role('button', name='Pause', exact=True).click()
            page.screenshot(path=str(OUT / f'level2-animation-{state}.png'), full_page=True)
            page.get_by_role('button', name='Play', exact=True).click()
        expect(footer).to_have_attribute('data-completion-count', '1', timeout=20000)
        expect(scene).to_have_attribute('data-shot', last)
        expect(footer.locator('[role=status]')).to_have_attribute('data-complete', 'true')
        if last == 'priority':
            expect(page.get_by_label('Three empty priority slots').locator(':scope > div')).to_have_count(3)
        page.wait_for_timeout(160)
        expect(footer).to_have_attribute('data-completion-count', '1')
        page.get_by_role('button', name='Replay', exact=True).click()
        expect(footer).to_have_attribute('data-completion-count', '0')
        page.get_by_role('button', name='Pause', exact=True).click()
        expect(scene).to_have_attribute('data-shot', first)
        record(f'{state}: authored art loads, paused frames hold, 4x playback completes once and replay clears the result')

    slider = page.get_by_label('Preview time', exact=True)
    slider.press('End')
    expect(page.locator('.l2-preview-footer')).to_have_attribute('data-completion-count', '1')
    slider.press('Home')
    expect(page.locator('[data-checking-shot]')).to_have_attribute('data-checking-shot', 'look')
    record('The original time control seeks to completion and back to the starting shot with native keyboard input')
    for width in [390, 320]:
        page.set_viewport_size({'width': width, 'height': 900})
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        expect(page.get_by_role('button', name='Replay', exact=True)).to_be_visible()
    page.screenshot(path=str(OUT / 'level2-animation-phone.png'), full_page=True)
    record('The authored preview controls and 16:9 stage remain available without horizontal overflow on phones')
    page.set_viewport_size({'width': 1366, 'height': 900})
    page.get_by_role('link', name='All previews', exact=True).click()
    expect(page).to_have_url(ORIGIN + 'START-HERE.html')
    page.locator('a[href*="state=full"]').click()
    expect(page).to_have_url(ORIGIN + 'Level2-animation.html?cinematic=level2&state=full')
    expect(page.get_by_label('Speed', exact=True)).to_have_value('1')
    # One normal-speed continuous run exercises actual handoffs and the authored reading holds.
    expect(page.locator('.l2-checking-hand').first).to_be_visible(timeout=20000)
    page.screenshot(path=str(OUT / 'level2-animation-checking.png'), full_page=True)
    expect(page.locator('.l2-preview-stage > .l2-scene')).to_have_attribute('data-shot', 'reflection', timeout=75000)
    page.wait_for_timeout(2100)
    page.screenshot(path=str(OUT / 'level2-animation-reflection.png'), full_page=True)
    footer = page.locator('.l2-preview-footer')
    expect(footer).to_have_attribute('data-completion-count', '5', timeout=20000)
    ids = footer.get_attribute('data-completion-ids').split(',')
    assert len(ids) == len(set(ids)) == 5
    expect(page.locator('.l2-preview-stage > .l2-scene')).to_have_attribute('data-shot', 'priority')
    page.wait_for_timeout(1200)
    expect(footer).to_have_attribute('data-completion-count', '5')
    page.screenshot(path=str(OUT / 'level2-animation-full-ending.png'), full_page=True)
    record('The launcher opens the full chain offline; 1x playback traverses all five segments and completes each unique request exactly once')
    context.close()
    browser.close()

assert not errors, errors
assert not external, external
record('The exact packaged preview produces no browser runtime errors and requests no external assets')
(OUT / 'level2-animation-preview-results.json').write_text(json.dumps({
    'passed': len(checks), 'checks': checks, 'runtimeErrors': errors, 'externalRequests': external,
    'playback': 'Nine independent entries at 4x, pause/replay/keyboard seeking, and one continuous 1x full-chain playback',
}, indent=2) + '\n')
