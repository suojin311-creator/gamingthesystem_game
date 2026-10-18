"""Exercise satisfaction milestones on the exact offline preview HTMLs."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

OUT = Path('test-results'); OUT.mkdir(exist_ok=True)
HTML = {name: Path(build).read_bytes() for name, build in [
    ('full', 'dist/index.html'), ('2', 'dist-level2/index.html'), ('3', 'dist-level3/index.html')]}
checks, errors = [], []


def record(name):
    checks.append(name); print('PASS', name, flush=True)


def advance(page, seconds=12):
    for _ in range(seconds):
        page.clock.run_for(1000); page.wait_for_timeout(15)


def open_game(browser, mode='full', width=1366, clock=True):
    context = browser.new_context(viewport={'width': width, 'height': 950}, reduced_motion='reduce' if clock else 'no-preference')
    context.set_offline(True)
    context.route('https://management.test/**', lambda route: route.fulfill(status=200, content_type='text/html', body=HTML[mode]))
    page = context.new_page(); page.on('pageerror', lambda error: errors.append(str(error)))
    if clock: page.clock.install()
    page.goto('https://management.test/', wait_until='networkidle')
    return context, page


def satisfaction(page, value, state=None):
    bar = page.get_by_role('progressbar', name='Management satisfaction', exact=True)
    expect(bar).to_have_attribute('aria-valuenow', str(value))
    if state:
        expect(bar).to_have_attribute('aria-valuetext', state)
        expect(page.locator('.management-satisfaction-state')).to_have_text(state)
    assert not any(c.isdigit() for c in page.locator('.management-satisfaction-state').inner_text())
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    return bar


def scene(page, shots=3):
    for _ in range(shots - 1): page.get_by_role('button', name='Continue scene', exact=True).click()
    page.get_by_role('button', name='Return to dashboard', exact=True).click()
    advance(page, 24)


def set_split(page, values):
    for index, metric in enumerate(['prep', 'part']):
        page.get_by_test_id('weight-card-' + metric).locator('input').evaluate('''(input,value)=>{
          Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(input,value);
          input.dispatchEvent(new Event('input',{bubbles:true}));
        }''', values[index])
        page.get_by_test_id('confirm-' + metric).click()


def publish(page, before, after, state):
    page.get_by_role('button', name='Run evaluation', exact=True).click()
    satisfaction(page, before)
    page.locator('.l3-publish').scroll_into_view_if_needed(); advance(page, 5)
    satisfaction(page, after, state)
    expect(page.locator('.management-satisfaction-evidence')).to_have_text('3 priorities · 100% allocated')
    expect(page.locator('.l3-awaiting')).to_have_text('Awaiting observation')
    page.get_by_role('button', name='Observe the class', exact=True).click(); scene(page)
    satisfaction(page, after, state)


with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    context, page = open_game(browser)
    page.get_by_role('button', name='Skip guide', exact=True).click()
    satisfaction(page, 12, 'Awaiting results')
    page.get_by_test_id('metric-prep').click(); satisfaction(page, 12)
    page.get_by_role('button', name='Make a prediction', exact=True).click()
    page.get_by_label('What do you expect students to do?').fill('Students will understand the reading.')
    satisfaction(page, 12)
    page.get_by_role('button', name='Run evaluation', exact=True).click(); satisfaction(page, 12)
    advance(page, 8); satisfaction(page, 44, 'Satisfied')
    expect(page.locator('.management-satisfaction-evidence')).to_have_text('Reported score 88 · target met')
    record('Level 1 selection/prediction do not raise satisfaction; the completed target report does, with the reported score retained as small evidence')
    page.get_by_role('button', name='Observe the class', exact=True).click(); scene(page)
    satisfaction(page, 44); expect(page.locator('.student .learning-risk')).to_contain_text('Learning at risk')
    page.get_by_role('button', name='Replay scene', exact=True).click(); scene(page); satisfaction(page, 44)
    record('Observation and replay keep satisfaction unchanged while the student card exposes the learning risk')
    page.get_by_role('button', name='Continue to Level 2', exact=True).click(); advance(page, 8)
    page.get_by_role('button', name='Choose three metrics', exact=True).click()
    for metric in ['prep', 'part', 'focus']: page.get_by_test_id('level2-metric-' + metric).click()
    page.get_by_role('button', name='Run evaluation', exact=True).click(); satisfaction(page, 44, 'Satisfied')
    advance(page, 6); satisfaction(page, 60, 'Satisfied')
    page.get_by_role('button', name='Observe the class', exact=True).click(); scene(page)
    page.get_by_role('button', name='Replay scene', exact=True).click(); scene(page); satisfaction(page, 60)
    record('Level 1 → 2 preserves the 44 baseline; the three-metric report raises it to 60 once and replay adds nothing')
    page.get_by_role('button', name='Cover the gaps', exact=True).click(); satisfaction(page, 60)
    page.get_by_role('button', name='Add remaining metrics', exact=True).click(); satisfaction(page, 60)
    advance(page, 6); satisfaction(page, 70, 'Very satisfied')
    page.get_by_role('button', name='Observe the class', exact=True).click(); scene(page)
    for count, before, after in [(10, 70, 77), (25, 77, 82), (100, 82, 86)]:
        page.get_by_role('button', name='Add more metrics', exact=True).click(); satisfaction(page, before)
        advance(page, 12); satisfaction(page, after, 'Very satisfied')
        expect(page.locator('.l2-reported-count')).to_have_text(str(count))
        record(f'{count}-metric report raises satisfaction only after completion; its tracked count remains visible')
    page.get_by_role('button', name='Observe the class', exact=True).click(); scene(page, 2)
    satisfaction(page, 86)
    page.get_by_role('button', name='Continue to Level 3', exact=True).click(); advance(page, 8)
    page.get_by_role('button', name='Review priorities', exact=True).click()
    for metric in ['prep', 'part', 'focus']:
        expect(page.get_by_test_id('level3-metric-' + metric)).to_have_attribute('aria-pressed', 'true')
    page.get_by_role('button', name='Set the weights', exact=True).click()
    set_split(page, [70, 20, 10]); publish(page, 86, 90, 'Very satisfied')
    page.get_by_role('button', name='Replay scene', exact=True).click(); scene(page); satisfaction(page, 90)
    record('Level 2 → 3 retains its trio and 86 baseline; first publication rises to 90 and observing/replaying leaves it there')
    page.get_by_role('button', name='Try another split', exact=True).click()
    set_split(page, [80, 15, 5]); publish(page, 90, 93, 'Delighted')
    page.get_by_role('button', name='What if they counted equally?', exact=True).click(); satisfaction(page, 93)
    page.locator('.l3-publish').scroll_into_view_if_needed(); advance(page, 5); satisfaction(page, 95, 'Delighted')
    page.get_by_role('button', name='Observe the class', exact=True).click(); scene(page)
    page.get_by_role('button', name='Compare the patterns', exact=True).click(); advance(page, 4)
    satisfaction(page, 95, 'Delighted')
    expect(page.locator('.l3-compare-table thead th[data-run]')).to_have_count(3)
    page.screenshot(path=str(OUT / 'management-comparison-desktop.png'), full_page=True, animations='disabled')
    record('Second and reference publications make smaller increases; comparison preserves 95 and all three actual test records')
    page.reload(wait_until='networkidle'); page.get_by_role('button', name='Skip guide', exact=True).click()
    satisfaction(page, 12, 'Awaiting results'); context.close()
    record('A fresh connected-game visit resets to the existing Level 1 entry baseline')

    for width in [1366, 390, 320]:
        context, page = open_game(browser, '2', width)
        advance(page, 8); page.get_by_role('button', name='Choose three metrics', exact=True).click()
        for metric in ['prep', 'part', 'focus']: page.get_by_test_id('level2-metric-' + metric).click()
        page.get_by_role('button', name='Run evaluation', exact=True).click(); satisfaction(page, 44, 'Satisfied')
        advance(page, 6); satisfaction(page, 60)
        shared_size = page.locator('.management-satisfaction-state').evaluate('el=>getComputedStyle(el).fontSize')
        page.screenshot(path=str(OUT / f'management-level2-{width}.png'), full_page=True, animations='disabled'); context.close()
        context, page = open_game(browser, '3', width)
        advance(page, 8); page.get_by_role('button', name='Choose priorities', exact=True).click()
        for metric in ['prep', 'part', 'focus']: page.get_by_test_id('level3-metric-' + metric).click()
        page.get_by_role('button', name='Set the weights', exact=True).click()
        # Moving/resetting/confirming the allocation cannot create a report.
        set_split(page, [70, 20, 10]); page.get_by_role('button', name='Reset weights', exact=True).click()
        set_split(page, [34, 33, 33]); publish(page, 86, 90, 'Very satisfied')
        assert page.locator('.management-satisfaction-state').evaluate('el=>getComputedStyle(el).fontSize') == shared_size
        assert page.locator('.management-satisfaction-track > span').evaluate('el=>getComputedStyle(el).transitionDuration') == '0s'
        expect(page.locator('.l3-run-rows [data-effort=medium]')).to_have_count(3)
        page.screenshot(path=str(OUT / f'management-level3-{width}.png'), full_page=True, animations='disabled'); context.close()
        record(f'{width}px standalone chapters start at matching baselines, share readable satisfaction type and fit without overflow; near-even earns no bonus and reduced motion is immediate')

    context, page = open_game(browser, clock=False)
    page.get_by_role('button', name='Skip guide', exact=True).click()
    page.get_by_test_id('metric-prep').click(); page.get_by_role('button', name='Make a prediction', exact=True).click()
    page.get_by_label('What do you expect students to do?').fill('Understand the reading.')
    page.get_by_role('button', name='Run evaluation', exact=True).click()
    bar = page.get_by_role('progressbar', name='Management satisfaction')
    expect(bar).to_have_attribute('aria-valuenow', '44')
    page.wait_for_timeout(250)
    ratio = bar.locator('span').evaluate('el=>el.getBoundingClientRect().width/el.parentElement.getBoundingClientRect().width')
    assert .12 < ratio < .44, ratio
    page.wait_for_timeout(1000)
    final = bar.locator('span').evaluate('el=>el.getBoundingClientRect().width/el.parentElement.getBoundingClientRect().width')
    assert abs(final - .44) < .005, final
    record('With normal motion, a real report smoothly fills the existing bar over one second instead of jumping or refilling from zero')
    context.close(); browser.close()
assert not errors, errors
record('No runtime errors during satisfaction, replay, chapter handoff and responsive checks')
(OUT / 'management-satisfaction-results.json').write_text(json.dumps({'passed': len(checks), 'checks': checks, 'runtimeErrors': errors}, indent=2) + '\n')
