"""Browser checks for Level 1. Requires Python Playwright and Chromium.

Start npm run dev, then run: python tests/smoke.py
Use --file dist/index.html to check the self-contained offline build as well.
"""
import argparse
import json
import re
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

parser = argparse.ArgumentParser()
parser.add_argument('--url', default='http://127.0.0.1:5173/')
parser.add_argument('--file')
parser.add_argument('--chromium', default='/usr/bin/chromium')
args = parser.parse_args()
# This managed cloud browser blocks file:// navigation. Serve the exact production
# bytes through Playwright's offline route, without a server or network access.
offline_html = Path(args.file).resolve().read_bytes() if args.file else None
url = 'https://level-one.test/' if args.file else args.url
output = Path(__file__).resolve().parents[1] / 'test-results'
output.mkdir(exist_ok=True)
cases = []
runtime_errors = []
KEY = 'gaming-the-system:level-one:v1'
metrics = [
    ('prep', 34, 88, 'I finished everything on the list!', 'Understanding still unclear'),
    ('part', 29, 85, 'I agree! Same here!', 'Depth still unclear'),
    ('focus', 41, 91, 'Look, I stayed on task the whole time!', 'Thinking still unclear'),
    ('discuss', 32, 84, 'Could you elaborate?', 'New ideas still unclear'),
    ('reflect', 38, 89, 'Before, I thought...', 'Changed thinking still unclear'),
    ('peer', 27, 86, 'Specific suggestion?', 'Exchange of ideas still unclear'),
]

def record(name):
    cases.append(name)
    print('PASS', name, flush=True)

def skip_guide(page):
    button = page.get_by_role('button', name='Skip guide')
    if button.count(): button.click()


def begin(context):
    if args.file:
        context.set_offline(True)
        context.route('https://level-one.test/**', lambda route: route.fulfill(status=200, content_type='text/html', body=offline_html))
    page = context.new_page()
    page.on('pageerror', lambda error: runtime_errors.append(str(error)))
    page.goto(url, wait_until='networkidle')
    skip_guide(page)
    return page

def fresh(page):
    page.evaluate('localStorage.clear()')
    page.reload(wait_until='networkidle')
    skip_guide(page)

def select(page, metric='prep', prediction='Students will explain their ideas more clearly.'):
    page.get_by_test_id('metric-' + metric).click()
    page.get_by_role('button', name='Make a prediction').click()
    page.get_by_label('What do you expect students to do?').fill(prediction)

def report_if_needed(page):
    expect(page.get_by_role('button', name='Observe the class')).to_be_enabled(timeout=12000)


def reveal_review(page, settle=True):
    expect(page.locator('.observation-recap')).to_be_visible(timeout=10000)
    expect(page.locator('.student')).to_contain_text('Unclear', timeout=10000)
    if settle:
        expect(page.get_by_role('button', name='Try more metrics')).to_be_enabled(timeout=15000)


def story_to_review(page):
    report_if_needed(page)
    page.get_by_role('button', name='Observe the class').click()
    expect(page.get_by_test_id('cinematic-placeholder')).to_be_visible()
    page.get_by_role('button', name='Continue scene').click()
    page.get_by_role('button', name='Continue scene').click()
    page.get_by_role('button', name='Return to dashboard').click()
    expect(page.get_by_role('heading', name='Look a little closer.')).to_be_visible()

def no_overflow(page):
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), 'Horizontal overflow'
    assert page.evaluate('Array.from(document.images).every(i => i.complete && i.naturalWidth > 0)'), 'Missing image'

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=args.chromium, headless=True, args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1440, 'height': 1000}, reduced_motion='reduce')
    page = begin(context)
    fresh(page)
    expect(page.get_by_role('button', name='Make a prediction')).to_be_disabled()
    assert not re.search(r'[\u4e00-\u9fff]', page.locator('body').inner_text())
    assert 'Narration' not in page.locator('body').inner_text()
    record('Empty selection is blocked; player interface is English without author notes')
    page.screenshot(path=str(output / 'desktop-choose.png'), full_page=True)

    for metric_id, before, after, first_line, uncertainty in metrics:
        fresh(page)
        prediction = 'Students will explore ideas instead of only ticking boxes.'
        select(page, metric_id, prediction)
        expect(page.get_by_label('What do you expect students to do?')).to_be_focused()
        page.get_by_role('button', name='Run evaluation').click()
        expect(page.get_by_role('button', name='Observe the class')).to_be_enabled(timeout=12000)
        expect(page.locator('.after-score')).to_contain_text(str(after))
        expect(page.locator('.before-score')).to_contain_text(str(before))
        expect(page.locator('.student')).to_contain_text('Not observed yet')
        report_if_needed(page)
        page.get_by_role('button', name='Observe the class').click()
        expect(page.locator('.scene-caption')).to_contain_text(first_line)
        assert prediction not in page.locator('.interlude').inner_text()
        assert 'reported score' not in page.locator('.interlude').inner_text().lower()
        page.get_by_role('button', name='Continue scene').click()
        page.get_by_role('button', name='Continue scene').click()
        page.get_by_role('button', name='Return to dashboard').click()
        expect(page.locator('.prediction-recap')).to_contain_text(prediction)
        reveal_review(page)
        expect(page.locator('.student .sr-only')).to_have_text(uncertainty)
        expect(page.locator('.university-value')).to_contain_text(str(after))
        page.reload(wait_until='networkidle')
        expect(page.get_by_role('heading', name='Look a little closer.')).to_be_visible()
        expect(page.locator('.prediction-recap')).to_contain_text(prediction)
        no_overflow(page)
        reveal_review(page)
        if metric_id == 'part':
            page.screenshot(path=str(output / 'desktop-review.png'), full_page=True)
        page.get_by_role('button', name='Try more metrics').click()
        expect(page.get_by_role('heading', name='What if we measured more than one?')).to_be_visible()
        page.get_by_role('button', name='Review this experiment').click()
        expect(page.get_by_role('heading', name='Look a little closer.')).to_be_visible()
        record(f'{metric_id}: correct score, story, evidence, saved prediction, reload, and completion')

    fresh(page)
    select(page, 'prep', '   ')
    expect(page.get_by_role('button', name='Run evaluation')).to_be_disabled()
    field = page.get_by_label('What do you expect students to do?')
    field.fill('x' * 101)
    assert len(field.input_value()) == 100
    expect(page.locator('#prediction-count')).to_contain_text('100')
    field.fill('<img src=x onerror=alert(1)> & "ideas"')
    page.reload(wait_until='networkidle')
    expect(field).to_have_value('<img src=x onerror=alert(1)> & "ideas"')
    page.get_by_role('button', name='Run evaluation').click()
    story_to_review(page)
    assert page.locator('.prediction-recap img').count() == 0
    expect(page.locator('.prediction-recap')).to_contain_text('<img src=x onerror=alert(1)>')
    record('Prediction validation: whitespace, 100-character limit, reload, literal rendering')

    page.get_by_role('button', name='Restart', exact=True).click()
    expect(page.get_by_role('dialog')).to_be_visible()
    expect(page.get_by_role('button', name='Keep playing')).to_be_focused()
    page.keyboard.press('Escape')
    expect(page.get_by_role('dialog')).not_to_be_visible()
    expect(page.get_by_role('heading', name='Look a little closer.')).to_be_visible()
    page.get_by_role('button', name='Restart', exact=True).click()
    page.get_by_role('button', name='Restart level 1').click()
    expect(page.get_by_role('button', name='Make a prediction')).to_be_disabled()
    assert page.locator('.metric-card[aria-pressed=true]').count() == 0
    record('Restart cancellation preserves progress; confirmed restart clears only this game')

    page.get_by_test_id('metric-focus').focus()
    page.keyboard.press('Enter')
    expect(page.get_by_test_id('metric-focus')).to_have_attribute('aria-pressed', 'true')
    page.get_by_role('button', name='Make a prediction').focus()
    page.keyboard.press('Enter')
    expect(field).to_be_focused()
    field.fill('Students will think carefully.')
    page.get_by_role('button', name='Back to metrics').click()
    page.get_by_role('button', name='Make a prediction').click()
    expect(field).to_have_value('Students will think carefully.')
    page.get_by_role('button', name='Back to metrics').click()
    page.get_by_test_id('metric-peer').click()
    page.get_by_role('button', name='Make a prediction').click()
    expect(field).to_have_value('')
    record('Keyboard selection and focus; changing metric resets the previous prediction')

    for bad in ['{broken', json.dumps({'version': 1, 'phase': 'review', 'metricId': 'unknown', 'prediction': 'abc'}), json.dumps({'version': 1, 'phase': 'review', 'metricId': 'prep', 'prediction': '  '})]:
        page.evaluate('(args) => localStorage.setItem(args[0], args[1])', [KEY, bad])
        page.reload(wait_until='networkidle')
        expect(page.get_by_role('heading', name='What will you measure?')).to_be_visible()
    record('Corrupt or incompatible saves recover to a playable start')

    fresh(page)
    select(page, 'discuss')
    page.get_by_role('button', name='Run evaluation').click()
    report_if_needed(page)
    page.get_by_role('button', name='Observe the class').click()
    page.get_by_role('button', name='Continue scene').click()
    page.reload(wait_until='networkidle')
    expect(page.locator('.scene-caption')).to_contain_text('Could you elaborate?')
    record('Refreshing a story restarts the selected interlude without losing the prediction')

    for width, height in [(1366, 768), (1024, 768), (768, 1024), (390, 844), (375, 667), (320, 640)]:
        mobile = browser.new_context(viewport={'width': width, 'height': height}, reduced_motion='reduce', has_touch=width < 800)
        tab = begin(mobile)
        fresh(tab)
        no_overflow(tab)
        select(tab, 'peer')
        no_overflow(tab)
        tab.get_by_role('button', name='Run evaluation').click()
        no_overflow(tab)
        story_to_review(tab)
        reveal_review(tab)
        no_overflow(tab)
        if width == 390:
            tab.screenshot(path=str(output / 'mobile-review.png'), full_page=True)
        mobile.close()
        record(f'Layout and functional flow at {width} × {height}, including touch and reduced motion')

    blocked = browser.new_context(reduced_motion='reduce')
    blocked.add_init_script("Object.defineProperty(Storage.prototype, 'setItem', {value() { throw new Error('storage blocked'); }});")
    blocked_page = begin(blocked)
    expect(blocked_page.locator('.storage-notice')).to_contain_text('Progress can’t be saved', timeout=5000)
    select(blocked_page, 'part')
    blocked_page.get_by_role('button', name='Run evaluation').click()
    story_to_review(blocked_page)
    blocked.close()
    record('Unavailable browser storage is reported and does not block gameplay')

    if not args.file:
        harness = output / 'integration.html'
        harness.write_text('''<!doctype html><html lang="en"><body><div id="root"></div>
<script type="module">
import React from 'react';
import {createRoot} from 'react-dom/client';
import LevelOne from '/src/LevelOne.tsx';
import '/src/styles.css';
const root = createRoot(document.getElementById('root'));
root.render(React.createElement(LevelOne, {
  playerName: 'Jordan', persist: false, showIntro: false,
  renderCinematic: (request, complete) => {
    window.storyRequest = request;
    return React.createElement('section', null,
      React.createElement('h2', null, 'Partner cinematic'),
      React.createElement('button', {onClick: complete}, 'Finish partner scene'));
  },
  onComplete: result => {
    window.levelResult = result;
    root.render(React.createElement('h1', null, 'Host received Level 1'));
  }
}));
</script></body></html>''')
        host = context.new_page()
        host.goto(args.url.rstrip('/') + '/test-results/integration.html', wait_until='networkidle')
        expect(host.locator('.speaker-name')).to_have_text('Jordan')
        select(host, 'focus', 'Students will concentrate on the task.')
        host.get_by_role('button', name='Run evaluation').click()
        report_if_needed(host)
        host.get_by_role('button', name='Observe the class').click()
        expect(host.get_by_role('heading', name='Partner cinematic')).to_be_visible()
        assert host.evaluate('window.storyRequest') == {'sceneId': 'level1.focus', 'metricId': 'focus'}
        assert host.get_by_test_id('cinematic-placeholder').count() == 0
        host.get_by_role('button', name='Finish partner scene').click()
        expect(host.locator('.prediction-recap')).to_contain_text('Students will concentrate on the task.')
        reveal_review(host)
        host.get_by_role('button', name='Try more metrics').click()
        expect(host.get_by_role('heading', name='Host received Level 1')).to_be_visible()
        assert host.evaluate('window.levelResult') == {
            'metricId': 'focus', 'prediction': 'Students will concentrate on the task.',
            'reportedScore': {'before': 41, 'after': 91, 'target': 70}}
        host.close()
        record('Partner cinematic renderer and host completion callback work with the selected branch')

    assert not runtime_errors, runtime_errors
    record('No uncaught browser errors')
    context.close()
    browser.close()

(output / ('offline-results.json' if args.file else 'smoke-results.json')).write_text(json.dumps({'passed': len(cases), 'checks': cases, 'runtime_errors': runtime_errors}, indent=2))
print(f'{len(cases)} checks passed.')
