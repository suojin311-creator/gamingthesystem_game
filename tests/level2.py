"""Exercise the actual bundled Level 2 offline, including its Level 1 handoff.

python tests/level2.py --file dist-level2/index.html --full-file dist/index.html
"""
import argparse
import itertools
import json
import re
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

parser = argparse.ArgumentParser()
parser.add_argument('--file', default='dist-level2/index.html')
parser.add_argument('--full-file', default='dist/index.html')
args = parser.parse_args()
output = Path('test-results')
output.mkdir(exist_ok=True)
cases, errors = [], []
IDS = ['prep', 'part', 'focus', 'discuss', 'reflect', 'peer']
NAMES = ['Pre-class Preparation', 'In-class Participation', 'On-task Focus', 'In-class Discussion Quality', 'Learning Reflection Quality', 'Online Peer Response Quality']


def record(name):
    cases.append(name)
    print('PASS', name, flush=True)


def load(browser, file=args.file, width=1440, height=1000, motion='reduce'):
    context = browser.new_context(viewport={'width': width, 'height': height}, reduced_motion=motion)
    context.set_offline(True)
    body = Path(file).read_bytes()
    context.route('https://game.test/**', lambda route: route.fulfill(status=200, content_type='text/html', body=body))
    page = context.new_page()
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto('https://game.test/', wait_until='networkidle')
    return context, page


def choose(page, ids):
    page.get_by_role('button', name='Choose three metrics', exact=True).click()
    for id in ids: page.get_by_test_id('level2-metric-' + id).click()
    page.get_by_role('button', name='Run evaluation', exact=True).click()


def scene(page, lines=3):
    page.get_by_role('button', name='Observe the class', exact=True).click()
    expect(page.get_by_test_id('level2-cinematic')).to_be_visible()
    for _ in range(lines - 1): page.get_by_role('button', name='Continue scene', exact=True).click()
    page.get_by_role('button', name='Return to dashboard', exact=True).click()


def core_ready(page, action):
    expect(page.locator('.l2-observation')).to_be_visible(timeout=8000)
    page.locator('.conversation').scroll_into_view_if_needed()
    expect(page.get_by_role('button', name=action, exact=True)).to_be_visible(timeout=25000)


def layout(page):
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), 'Horizontal overflow'
    assert page.evaluate('Array.from(document.images).every(i => i.complete && i.naturalWidth > 0)'), 'Missing image'


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--no-sandbox'])
    context, page = load(browser)
    expect(page.get_by_role('heading', name='What if we measured more than one?')).to_be_visible()
    page.screenshot(path=str(output / 'level2-intro.png'), full_page=True)
    choose(page, IDS[:2] + ['discuss'])
    expect(page.locator('.level-two')).to_have_attribute('data-branch', 'mixed')
    expect(page.get_by_role('button', name='Observe the class', exact=True)).to_be_enabled(timeout=7000)
    record('Offline direct entry and mixed evaluation')
    scene(page)
    expect(page.locator('.l2-observation')).to_be_visible(timeout=8000)
    # The finding is readable before either character starts typing.
    expect(page.locator('.conversation .dialogue-character')).to_have_count(0)
    assert not page.get_by_role('button', name='Cover the gaps', exact=True).count()
    page.wait_for_timeout(2200)
    expect(page.locator('.conversation .dialogue-character')).to_have_count(0)
    record('Finding precedes dialogue and next action')
    page.get_by_role('button', name='Guide', exact=True).click()
    page.wait_for_timeout(5500)
    expect(page.locator('.conversation .dialogue-character')).to_have_count(0)
    page.keyboard.press('Escape')
    expect(page.get_by_role('dialog')).not_to_be_visible()
    expect(page.get_by_role('button', name='Guide', exact=True)).to_be_focused()
    record('Guide freezes the reading sequence and restores keyboard focus')
    core_ready(page, 'Cover the gaps')
    page.screenshot(path=str(output / 'level2-three-observation.png'), full_page=True)
    page.get_by_role('button', name='Cover the gaps', exact=True).click()
    expect(page.locator('.l2-covered li')).to_have_count(3)
    expect(page.locator('.l2-missing li')).to_have_count(3)
    assert 'Pre-class Preparation' in page.locator('.l2-covered').inner_text()
    for name in [NAMES[2], NAMES[4], NAMES[5]]: expect(page.locator('.l2-missing')).to_contain_text(name)
    record('Gap view shows exactly the three unselected areas')
    page.get_by_role('button', name='Add the other three', exact=True).click()
    expect(page.locator('.l2-evaluation-list li')).to_have_count(6)
    expect(page.locator('.l2-evaluation-list [data-checked=true]')).to_have_count(6, timeout=6000)
    expect(page.get_by_role('button', name='Observe the class', exact=True)).to_be_enabled(timeout=6000)
    record('Six-metric evaluation retains first three and adds the missing three')
    scene(page)
    expect(page.locator('.l2-observation')).to_contain_text('system is becoming part of the task', timeout=8000)
    core_ready(page, 'Add more metrics')
    page.get_by_role('button', name='Sound on', exact=True).click()
    expect(page.get_by_role('button', name='Sound off', exact=True)).to_be_visible()
    for count, label, focus in [(10, 'Completing requirements', 'Requirements'), (25, 'Managing criteria', 'Criteria'), (100, 'Optimizing the checklist', 'Checklist')]:
        page.get_by_role('button', name='Add more metrics', exact=True).click()
        expect(page.locator('.level-two')).to_have_attribute('data-round', str(count))
        expect(page.locator('.l2-checklist')).to_contain_text(label, timeout=10000)
        expect(page.locator('.l2-checklist [data-shown=true]')).to_have_count(3, timeout=5000)
        expect(page.locator('.l2-reported-count')).to_have_text(str(count))
        expect(page.locator('.l2-student-focus')).to_have_text(focus)
        expect(page.locator('.l2-matrix [data-active=true]')).to_have_count(count)
        page.locator('.l2-checklist').scroll_into_view_if_needed()
        action = 'Observe the class' if count == 100 else 'Add more metrics'
        expect(page.get_by_role('button', name=action, exact=True)).to_be_visible(timeout=14000)
        page.screenshot(path=str(output / f'level2-{count}.png'), full_page=True)
        layout(page)
        record(f'{count} metrics automatically reveal the matching student checklist')
    scene(page, lines=2)
    core_ready(page, 'Continue to Level 3')
    expect(page.get_by_role('button', name='Continue to Level 3', exact=True)).to_be_disabled()
    page.screenshot(path=str(output / 'level2-finish.png'), full_page=True)
    text = page.locator('main').inner_text()
    assert not re.search(r'[\u4e00-\u9fff]', text)
    assert 'Goodhart' not in text
    record('Level 2 ends at weighting question with Level 3 reserved and all-English UI')
    page.get_by_role('button', name='Restart', exact=True).click()
    page.get_by_role('button', name='Keep playing', exact=True).click()
    expect(page.get_by_role('button', name='Restart', exact=True)).to_be_focused()
    expect(page.locator('.level-two')).to_have_attribute('data-phase', 'complete')
    page.get_by_role('button', name='Restart', exact=True).click()
    page.get_by_role('button', name='Restart Level 2', exact=True).click()
    expect(page.locator('.level-two')).to_have_attribute('data-phase', 'intro')
    expect(page.get_by_role('button', name='Sound on', exact=True)).to_be_visible()
    assert page.evaluate('localStorage.length === 0 && sessionStorage.length === 0')
    record('Restart cancels safely or clears progress without persistent saves')
    context.close()

    context, page = load(browser)
    page.get_by_role('button', name='Choose three metrics', exact=True).click()
    run = page.get_by_role('button', name='Run evaluation', exact=True)
    expect(run).to_be_disabled()
    for id in IDS[:3]: page.get_by_test_id('level2-metric-' + id).click()
    expect(run).to_be_enabled()
    # A disabled-by-limit card cannot become a fourth choice; a selected card remains swappable.
    page.get_by_test_id('level2-metric-discuss').dispatch_event('click')
    expect(page.locator('.l2-metric-card[aria-pressed=true]')).to_have_count(3)
    expect(page.get_by_role('status')).to_contain_text('Deselect one')
    page.get_by_test_id('level2-metric-prep').click()
    expect(run).to_be_disabled()
    page.get_by_test_id('level2-metric-discuss').click()
    expect(run).to_be_enabled()
    record('Exactly-three limit, selection hint and deselect-to-swap')
    page.screenshot(path=str(output / 'level2-selection.png'), full_page=True)
    context.close()

    for trio in itertools.combinations(IDS, 3):
        context, page = load(browser)
        choose(page, trio)
        branch = 'visible' if list(trio) == IDS[:3] else 'quality' if list(trio) == IDS[3:] else 'mixed'
        expect(page.locator('.level-two')).to_have_attribute('data-branch', branch)
        expect(page.locator('.l2-evaluation-list li')).to_have_count(3)
        expect(page.get_by_role('button', name='Observe the class', exact=True)).to_be_enabled(timeout=7000)
        if branch in ['visible', 'quality']:
            scene(page)
            expect(page.locator('.l2-observation')).to_contain_text('visible focus' if branch == 'visible' else 'patterns that score well', timeout=8000)
        record(f'Trio {"+".join(trio)} routes to {branch} outcome')
        context.close()

    for width, height in [(1366, 768), (768, 1024), (390, 844), (320, 740)]:
        context, page = load(browser, width=width, height=height, motion='no-preference')
        layout(page)
        choose(page, IDS[:3])
        expect(page.get_by_role('button', name='Observe the class', exact=True)).to_be_enabled(timeout=10000)
        layout(page)
        page.screenshot(path=str(output / f'level2-{width}.png'), full_page=True)
        scene(page)
        core_ready(page, 'Cover the gaps')
        layout(page)
        page.screenshot(path=str(output / f'level2-observation-{width}.png'), full_page=True)
        record(f'{width}px layout, normal motion and automatic dialogue')
        page.reload(wait_until='networkidle')
        expect(page.locator('.level-two')).to_have_attribute('data-phase', 'intro')
        choose(page, IDS[:3])
        page.evaluate("window.dispatchEvent(new PageTransitionEvent('pageshow', {persisted: true}))")
        expect(page.locator('.level-two')).to_have_attribute('data-phase', 'intro')
        record(f'{width}px reload and restored tab start fresh')
        context.close()

    context, page = load(browser, args.full_file)
    page.get_by_role('button', name='Skip guide', exact=True).click()
    page.get_by_test_id('metric-prep').click()
    page.get_by_role('button', name='Make a prediction', exact=True).click()
    page.get_by_label('What do you expect students to do?').fill('Understand the lesson before class.')
    page.get_by_role('button', name='Run evaluation', exact=True).click()
    expect(page.get_by_role('button', name='Observe the class', exact=True)).to_be_enabled(timeout=10000)
    page.get_by_role('button', name='Observe the class', exact=True).click()
    for _ in range(2): page.get_by_role('button', name='Continue scene', exact=True).click()
    page.get_by_role('button', name='Return to dashboard', exact=True).click()
    expect(page.get_by_role('button', name='Continue to Level 2', exact=True)).to_be_enabled(timeout=30000)
    page.get_by_role('button', name='Sound on', exact=True).click()
    page.get_by_role('button', name='Continue to Level 2', exact=True).click()
    expect(page.locator('.level-two')).to_have_attribute('data-phase', 'intro')
    expect(page.locator('.l2-previous')).to_contain_text('Preparation')
    expect(page.get_by_role('button', name='Sound off', exact=True)).to_be_visible()
    page.reload(wait_until='networkidle')
    expect(page.locator('.level-one')).to_be_visible()
    record('Full game carries Level 1 context and sound preference to Level 2; refresh restarts full game')
    context.close()
    browser.close()

assert not errors, errors
record('No browser runtime errors across all offline playthroughs')
(output / 'level2-results.json').write_text(json.dumps({'passed': len(cases), 'cases': cases, 'runtimeErrors': errors}, indent=2) + '\n')
print(f'{len(cases)} checks passed', flush=True)
