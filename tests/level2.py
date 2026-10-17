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


def load(browser, file=args.file, width=1440, height=1000, motion='reduce', observe_intro=False):
    context = browser.new_context(viewport={'width': width, 'height': height}, reduced_motion=motion)
    context.set_offline(True)
    body = Path(file).read_bytes()
    context.route('https://game.test/**', lambda route: route.fulfill(status=200, content_type='text/html', body=body))
    page = context.new_page()
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto('https://game.test/', wait_until='networkidle')
    if file == args.file and not observe_intro:
        page.get_by_role('button', name='Choose three metrics', exact=True).click()
        expect(page.locator('.level-two')).to_have_attribute('data-phase', 'choose')
    return context, page


def choose(page, ids):
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
    expect(page.get_by_role('button', name=action, exact=True)).to_be_visible(timeout=8000)


def layout(page):
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), 'Horizontal overflow'
    assert page.evaluate('Array.from(document.images).every(i => i.complete && i.naturalWidth > 0)'), 'Missing image'


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--no-sandbox'])
    context, page = load(browser, observe_intro=True)
    expect(page.get_by_role('region', name='Level 2 introduction')).to_be_visible()
    expect(page.locator('.l2-intro h2')).to_have_text('LEVEL 2')
    expect(page.locator('.l2-metric-card')).to_have_count(0)
    expect(page.get_by_test_id('level2-choice-checklist')).to_have_count(0)
    expect(page.locator('.maya-bubble p')).to_have_text('One metric wasn’t enough. What if I tracked three?', timeout=4000)
    expect(page.locator('.alex-bubble p')).to_have_text(['Three? Easy 😎', 'Just tell me what gets the points.'], timeout=6000)
    expect(page.locator('.alex-character.message-continuation')).to_have_count(1)
    expect(page.locator('.alex-character.message-continuation .avatar')).to_have_css('visibility', 'hidden')
    expect(page.locator('.level-two')).to_have_attribute('data-phase', 'intro')
    expect(page.get_by_role('button', name='Choose three metrics', exact=True)).to_be_visible()
    page.wait_for_timeout(5000)
    expect(page.locator('.level-two')).to_have_attribute('data-phase', 'intro')
    expect(page.locator('.l2-metric-card')).to_have_count(0)
    page.screenshot(path=str(output / 'level2-dialogue-transition.png'), full_page=True)
    page.get_by_role('button', name='Choose three metrics', exact=True).click()
    expect(page.get_by_role('heading', name='Which three will you track?')).to_be_visible()
    expect(page.locator('.l2-intro')).to_have_count(0)
    expect(page.locator('.conversation')).to_have_count(0)
    expect(page.locator('.l2-metric-card')).to_have_count(6)
    expect(page.get_by_role('button', name='Choose three metrics', exact=True)).to_have_count(0)
    record('Level 2 introduction shows a lower-right next button with Alex’s reply and remains until the player clicks it')
    page.get_by_test_id('level2-metric-prep').click()
    expect(page.get_by_test_id('level2-metric-prep')).to_have_attribute('aria-pressed', 'true')
    checklist = page.get_by_test_id('level2-choice-checklist')
    expect(checklist).to_contain_text('ALEX’S CHECKLIST')
    expect(checklist).to_contain_text('Preparation')
    expect(checklist.locator('[data-checked=true]')).to_have_count(1)
    expect(checklist).to_contain_text('1 / 3 selected')
    boxes = checklist.locator('li').all()
    positions = [box.bounding_box() for box in boxes]
    assert all(positions[index + 1]['y'] > positions[index]['y'] for index in [0,1])
    page.get_by_test_id('level2-metric-prep').click()
    expect(checklist).to_contain_text('0 / 3 selected')
    expect(checklist.locator('[data-checked=true]')).to_have_count(0)
    record('Alex’s Checklist uses the later vertical format and ticks exactly the current metric choices')
    expect(page.get_by_role('button', name='Guide', exact=True)).to_have_count(0)
    page.screenshot(path=str(output / 'level2-intro.png'), full_page=True)
    choose(page, IDS[:2] + ['discuss'])
    expect(page.locator('.level-two')).to_have_attribute('data-branch', 'mixed')
    expect(page.get_by_role('button', name='Observe the class', exact=True)).to_be_enabled(timeout=7000)
    expect(page.get_by_test_id('level2-choice-checklist')).to_have_count(0)
    expect(page.locator('.l2-evaluation .l2-checklist')).to_have_count(0)
    record('Three-metric evaluation shows its changing metrics without a duplicate checklist')
    record('Offline Level 2 entry without Guide and mixed evaluation')
    page.evaluate('''window.observationTimeline = {};
new MutationObserver(() => {
  const root = document.querySelector('.level-two[data-phase="observe"], .level-two[data-phase="complete"]');
  if (!root || root.querySelector('.l2-checklist')) return;
  const key = `${root.dataset.phase}:${root.dataset.round}`;
  const timeline = window.observationTimeline[key] ||= {};
  for (const [name, selector] of Object.entries({finding:'.l2-observation', maya:'.maya-bubble p', alex:'.alex-bubble p', alexFinal:'.alex-character[data-order="2"] .alex-bubble p', button:'.l2-decision .action-row .button'})) {
    if (root.querySelector(selector)) timeline[name] ??= performance.now();
  }
}).observe(document, {childList:true, subtree:true, attributes:true});''')
    scene(page)
    expect(page.locator('.l2-observation')).to_be_visible(timeout=8000)
    expect(page.locator('.learning-risk strong')).to_have_text('Learning at risk')
    expect(page.locator('.student-behaviour')).to_have_text('Untracked areas get overlooked.')
    assert page.locator('.l2-observed-round').count() == 0
    assert page.locator('.student-behaviour').evaluate('e => parseFloat(getComputedStyle(e).fontSize)') > page.locator('.learning-risk strong').evaluate('e => parseFloat(getComputedStyle(e).fontSize)') * 1.8
    record('Student behaviour is the main text, with Learning at risk as a smaller supporting label')
    # The finding is readable before either character starts typing.
    expect(page.locator('.conversation .dialogue-character')).to_have_count(0)
    assert not page.get_by_role('button', name='Cover the gaps', exact=True).count()
    page.wait_for_timeout(600)
    expect(page.locator('.conversation .dialogue-character')).to_have_count(0)
    record('Finding precedes dialogue and next action')
    expect(page.get_by_role('button', name='Restart', exact=True)).to_have_count(0)
    expect(page.get_by_role('dialog')).to_have_count(0)
    record('Player view has no Restart control or restart dialog')
    core_ready(page, 'Cover the gaps')
    stamps = page.evaluate('window.observationTimeline["observe:3"]')
    assert 900 <= stamps['alex'] - stamps['maya'] < 2500, stamps
    assert 0 <= stamps['button'] - stamps['alexFinal'] < 180, stamps
    expect(page.locator('.maya-bubble p')).to_have_text('Alex, Discussion, Reflection, and Peer response still matter. Where did they fit in?')
    expect(page.locator('.alex-bubble p')).to_have_text(['Looking busy was the mission, right? 🧐', 'I left Discussion, Reflection, and Peer response for later.'])
    record('Cover the gaps appears with Alex’s second reply; the dialogue explicitly identifies the other three areas')
    page.screenshot(path=str(output / 'level2-three-observation.png'), full_page=True)
    page.get_by_role('button', name='Cover the gaps', exact=True).click()
    expect(page.locator('.l2-covered li')).to_have_count(3)
    expect(page.locator('.l2-missing li')).to_have_count(3)
    assert 'Pre-class Preparation' in page.locator('.l2-covered').inner_text()
    for name in [NAMES[2], NAMES[4], NAMES[5]]: expect(page.locator('.l2-missing')).to_contain_text(name)
    expect(page.locator('.l2-gap-warning')).to_have_text('3 areas untracked')
    assert page.locator('.l2-missing li').first.evaluate('e => parseFloat(getComputedStyle(e).fontSize)') >= page.locator('.l2-covered li').first.evaluate('e => parseFloat(getComputedStyle(e).fontSize)') * 1.25
    page.screenshot(path=str(output / 'level2-gap-warning.png'), full_page=True)
    record('Gap view shows exactly the three unselected areas')
    record('Untracked areas have a larger type size and a prominent warning')
    page.get_by_role('button', name='Add remaining metrics', exact=True).click()
    expect(page.locator('.l2-students')).to_contain_text('Awaiting observation')
    expect(page.locator('.l2-students')).to_have_attribute('data-round', '6')
    expect(page.locator('.l2-management')).to_have_attribute('data-round', '6')
    expect(page.locator('.learning-risk')).to_have_count(0)
    expect(page.locator('.l2-evaluation-list li')).to_have_count(6)
    expect(page.get_by_test_id('level2-choice-checklist')).to_have_count(0)
    expect(page.locator('.l2-evaluation-list [data-checked=true]')).to_have_count(6, timeout=6000)
    expect(page.get_by_role('button', name='Observe the class', exact=True)).to_be_enabled(timeout=6000)
    expect(page.locator('.l2-reported-count')).to_have_text('6')
    expect(page.locator('.l2-evaluation .l2-checklist')).to_have_count(0)
    record('Six-metric evaluation also omits the duplicate checklist and retains all six green results')
    expect(page.locator('.l2-students')).to_contain_text('Awaiting observation')
    page.screenshot(path=str(output / 'level2-six-pending.png'), full_page=True)
    record('Six-metric report and pending student card share the current round without stale observations')
    record('Six-metric evaluation retains first three and adds the missing three')
    scene(page)
    expect(page.locator('.l2-observation')).to_contain_text('Meeting the criteria becomes the task', timeout=8000)
    expect(page.locator('.student-behaviour')).to_have_text('Meeting criteria becomes the goal.')
    core_ready(page, 'Add more metrics')
    stamps = page.evaluate('window.observationTimeline["observe:6"]')
    assert stamps['alex'] - stamps['finding'] < 5500, stamps
    assert 0 <= stamps['button'] - stamps['alexFinal'] < 180, stamps
    expect(page.locator('.alex-bubble p')).to_have_text(['Keeping up! There’s a box for everything now. 😅', 'I’m getting quick at ticking them off.'])
    record('Six-metric dialogue reflects keeping up with the expanded criteria, and releases the next action with its second Alex message')
    page.get_by_role('button', name='Sound on', exact=True).click()
    expect(page.get_by_role('button', name='Sound off', exact=True)).to_be_visible()
    page.evaluate('''window.checklistTimeline = {};
new MutationObserver(() => {
  const root = document.querySelector('.level-two[data-phase="observe"]');
  if (!root || !root.querySelector('.l2-checklist')) return;
  const count = root.dataset.round;
  const timeline = window.checklistTimeline[count] ||= {rows: []};
  root.querySelectorAll('.l2-checklist li[data-shown="true"]').forEach((row, index) => {
    timeline.rows[index] ??= performance.now();
  });
  if (root.querySelector('.l2-decision .action-row .primary-button')) timeline.ready ??= performance.now();
}).observe(document, {childList: true, subtree: true, attributes: true});''')
    for count, label, observation in [(10, 'Completing requirements', 'Ticking boxes takes priority.'), (25, 'Managing criteria', 'Optimizing for the criteria takes priority.'), (100, 'Optimizing the checklist', 'Doing the minimum becomes the strategy.')]:
        page.get_by_role('button', name='Add more metrics', exact=True).click()
        expect(page.locator('.level-two')).to_have_attribute('data-round', str(count))
        expect(page.locator('.l2-students')).to_contain_text('Awaiting observation')
        expect(page.locator('.l2-students')).to_have_attribute('data-observed', 'false')
        expect(page.locator('.l2-checklist')).to_contain_text(label, timeout=10000)
        expect(page.locator('.l2-checklist [data-shown=true]')).to_have_count(3, timeout=5000)
        expect(page.locator('.l2-check-box[data-checked=true] .icon')).to_have_count(3)
        expect(page.locator('.l2-reported-count')).to_have_text(str(count))
        expect(page.locator('.learning-risk strong')).to_have_text('Learning at risk')
        expect(page.locator('.student-behaviour')).to_have_text(observation)
        expect(page.locator('.l2-students')).to_have_attribute('data-round', str(count))
        expect(page.locator('.l2-matrix [data-active=true]')).to_have_count(count)
        page.locator('.l2-checklist').scroll_into_view_if_needed()
        action = 'Observe the class' if count == 100 else 'Add more metrics'
        expect(page.get_by_role('button', name=action, exact=True)).to_be_visible(timeout=2500)
        stamps = page.evaluate(f'window.checklistTimeline[{count}]')
        assert len(stamps['rows']) == 3, stamps
        assert all(stamps['rows'][index + 1] - stamps['rows'][index] >= 450 for index in [0, 1]), stamps
        assert 900 <= stamps['ready'] - stamps['rows'][2] < 2300, stamps
        page.screenshot(path=str(output / f'level2-{count}.png'), full_page=True)
        layout(page)
        record(f'{count} metrics automatically reveal the matching student checklist')
        record(f'{count} metrics: action items tick in sequence and next button opens about one second after the last')
    scene(page, lines=2)
    core_ready(page, 'Continue to Level 3')
    expect(page.get_by_role('button', name='Continue to Level 3', exact=True)).to_be_disabled()
    page.screenshot(path=str(output / 'level2-finish.png'), full_page=True)
    text = page.locator('main').inner_text()
    assert not re.search(r'[\u4e00-\u9fff]', text)
    assert 'Goodhart' not in text
    record('Level 2 ends at weighting question with Level 3 reserved and all-English UI')
    expect(page.get_by_role('button', name='Restart', exact=True)).to_have_count(0)
    assert page.evaluate('localStorage.length === 0 && sessionStorage.length === 0')
    record('Finished player view has no restart entry and does not save progress in storage')
    context.close()

    context, page = load(browser)
    run = page.get_by_role('button', name='Run evaluation', exact=True)
    expect(run).to_be_disabled()
    for id in IDS[:3]: page.get_by_test_id('level2-metric-' + id).click()
    expect(run).to_be_enabled()
    # A disabled-by-limit card cannot become a fourth choice; a selected card remains swappable.
    page.get_by_test_id('level2-metric-discuss').dispatch_event('click')
    expect(page.locator('.l2-metric-card[aria-pressed=true]')).to_have_count(3)
    expect(page.locator('.choice-hint')).to_contain_text('Deselect one')
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
            expect(page.locator('.l2-observation')).to_contain_text('Students look prepared' if branch == 'visible' else 'patterns that earn points', timeout=8000)
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
        page.get_by_role('button', name='Cover the gaps', exact=True).click()
        expect(page.locator('.l2-gap-warning')).to_be_visible()
        layout(page)
        page.screenshot(path=str(output / f'level2-gaps-{width}.png'), full_page=True)
        if width == 1366:
            page.wait_for_timeout(2200)
            animations = page.locator('.l2-missing').evaluate('(node)=>node.getAnimations().map(a=>({time:a.currentTime,iterations:a.effect.getTiming().iterations===Infinity}))')
            assert any(animation['iterations'] and animation['time'] > 2000 for animation in animations), animations
            assert page.locator('.l2-missing').evaluate('node=>getComputedStyle(node).animationDuration') == '1.25s'
            assert page.locator('.l2-missing').evaluate('node=>parseFloat(getComputedStyle(node).borderTopWidth)') >= 3
            assert page.locator('.l2-gap-warning > .icon').evaluate('node=>getComputedStyle(node).animationIterationCount') == 'infinite'
            first_border = page.locator('.l2-missing').evaluate('node=>getComputedStyle(node).borderTopColor')
            page.wait_for_timeout(400)
            second_border = page.locator('.l2-missing').evaluate('node=>getComputedStyle(node).borderTopColor')
            assert first_border != second_border, [first_border, second_border]
            record('Untracked-area border keeps breathing after its first cycle, changing border colour without moving text')
        record(f'{width}px layout, normal motion and automatic dialogue')
        page.reload(wait_until='networkidle')
        expect(page.locator('.level-two')).to_have_attribute('data-phase', 'intro')
        page.get_by_role('button', name='Choose three metrics', exact=True).click()
        expect(page.locator('.level-two')).to_have_attribute('data-phase', 'choose')
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
    page.get_by_role('button', name='Choose three metrics', exact=True).click()
    expect(page.locator('.level-two')).to_have_attribute('data-phase', 'choose')
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
