"""Player-led Level 3 paths in the production HTML: two observations, optional third."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

HTML = Path('dist-level3/index.html').read_bytes()
checks, errors = [], []
Path('test-results').mkdir(exist_ok=True)

def record(text):
    checks.append(text)
    print('PASS', text, flush=True)

def advance(page, ms=8000):
    for _ in range(ms // 500):
        page.clock.run_for(500)
        page.wait_for_timeout(8)

def slider(page, metric, value):
    page.get_by_test_id('weight-card-' + metric).locator('input').evaluate(
        "(e,v)=>{Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(e,v);e.dispatchEvent(new Event('input',{bubbles:true}))}", value)

def set_weights(page, values, metric_ids=('prep', 'part', 'focus')):
    for index, metric in enumerate(metric_ids):
        node = page.get_by_test_id('weight-card-' + metric)
        if not node.locator('input').is_disabled():
            slider(page, metric, values[index])
        expect(node.locator('output')).to_have_text(f'{values[index]}%')
        button = page.get_by_test_id('confirm-' + metric)
        if button.is_enabled():
            button.click()

def finish_run(page):
    page.get_by_role('button', name='Run evaluation', exact=True).click()
    page.locator('.l3-publish').scroll_into_view_if_needed()
    advance(page, 5000)
    expect(page.locator('.level-three')).to_have_attribute('data-phase', 'publish')
    page.get_by_role('button', name='Observe the class', exact=True).click()
    for _ in range(2):
        page.get_by_role('button', name='Continue scene', exact=True).click()
    page.get_by_role('button', name='Return to dashboard', exact=True).click()
    page.locator('.l3-results').scroll_into_view_if_needed()
    advance(page, 14000)
    page.locator('.l3-criteria-stop').scroll_into_view_if_needed()
    advance(page, 4000)
    expect(page.locator('.l3-routine-beat[data-shown=true]')).to_have_count(3)
    page.locator('.l3-bottom-dialogue').scroll_into_view_if_needed()
    advance(page, 8000)
    expect(page.locator('.alex-bubble p')).to_have_count(2)

def start(browser, width=1366, *, height=900, skip_guide=True, motion='reduce', metric_ids=('prep', 'part', 'focus')):
    context = browser.new_context(viewport={'width': width, 'height': height}, reduced_motion=motion)
    context.set_offline(True)
    context.route('https://level3-player-path.test/**', lambda route: route.fulfill(status=200, content_type='text/html', body=HTML))
    page = context.new_page()
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.clock.install()
    page.goto('https://level3-player-path.test/', wait_until='networkidle')
    advance(page)
    page.get_by_role('button', name='Choose priorities', exact=True).click()
    for metric in metric_ids:
        page.get_by_test_id('level3-metric-' + metric).click()
    page.get_by_role('button', name='Set the weights', exact=True).click()
    if skip_guide:
        page.get_by_role('button', name='Skip guide', exact=True).click()
    return context, page

def next_trial(page, *, optional=False):
    page.get_by_role('button', name='Test another idea' if optional else 'Try another split', exact=True).click()

def compare(page):
    page.get_by_role('button', name='Compare the results', exact=True).click()

def finish_theory(page, closing_text=None):
    page.get_by_role('button', name='Watch Alex’s response', exact=True).click()
    if closing_text:
        expect(page.locator('.l3-scene-copy > p')).to_contain_text(closing_text)
    for _ in range(2):
        page.get_by_role('button', name='Continue scene', exact=True).click()
    page.get_by_role('button', name='Reveal Goodhart’s Law', exact=True).click()
    page.get_by_role('button', name='Continue scene', exact=True).click()
    expect(page.locator('.l3-preview-end')).to_have_text('End of preview')
    expect(page.locator('.level-three')).to_have_attribute('data-phase', 'theory')

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    context, page = start(browser, skip_guide=False)
    guide = page.get_by_role('dialog', name='Weight guide', exact=True)
    expect(guide).to_be_visible()
    assert guide.evaluate('e=>e.matches(":modal")')
    initial = page.locator('.l3-weight-value').all_text_contents()
    assert initial == ['—', '—', '—']
    expect(guide).to_contain_text('Move a slider')
    page.get_by_role('button', name='Next', exact=True).click()
    expect(guide).to_contain_text('Confirm')
    page.get_by_role('button', name='Back', exact=True).click()
    expect(guide).to_contain_text('Move a slider')
    page.keyboard.press('Escape')
    expect(guide).to_have_count(0)
    assert page.locator('.l3-weight-value').all_text_contents() == initial
    expect(page.locator('.l3-weight-card[data-confirmed=true]')).to_have_count(0)
    assert page.evaluate("document.activeElement.matches('.guide-button, .l3-weight-card input:not(:disabled)')")
    record('The first-use spotlight guide supports Next, Back and Escape without changing or confirming player weights; closing returns focus to an available workbench control')
    expect(page.locator('#experiment-question')).to_have_text('How would you split the 100%?')
    expect(page.get_by_role('group', name='Last observation', exact=True)).to_have_count(0)
    expect(page.get_by_role('button', name='Run evaluation', exact=True)).to_be_disabled()
    for button in page.locator('.l3-weight-card button').all(): expect(button).to_be_disabled()
    for field in page.locator('.l3-weight-card input').all():
        assert field.input_value() == '0'
        expect(field).to_have_attribute('aria-valuetext', 'Not assigned. Move this slider to start.')
    page.locator('.l3-strategy-hint summary').click()
    expect(page.locator('.l3-strategy-hint')).to_contain_text('Move any slider to start.')
    advance(page, 12000)
    expect(page.locator('.l3-weight-value')).to_have_text(['—', '—', '—'])
    expect(page.locator('.level-three')).to_have_attribute('data-round', '0')
    page.locator('.l3-strategy-hint summary').click()
    record('The first editor stays genuinely unassigned through waiting, guide and hint use, with no percentages, confirmations, result record or runnable default')
    slider(page, 'prep', 70)
    values = page.locator('.l3-weight-value').all_text_contents()
    page.get_by_role('button', name='Guide', exact=True).click()
    for _ in range(3):
        page.get_by_role('button', name='Next', exact=True).click()
    page.get_by_role('button', name='Try your weights', exact=True).click()
    assert page.locator('.l3-weight-value').all_text_contents() == values
    expect(page.locator('.l3-weight-card[data-confirmed=true]')).to_have_count(0)
    expect(page.get_by_role('button', name='Guide', exact=True)).to_be_focused()
    expect(page.get_by_role('radio')).to_have_count(0)
    expect(page.get_by_role('button', name='Apply suggested weights', exact=True)).to_have_count(0)
    set_weights(page, [70, 20, 10])
    expect(page.get_by_role('button', name='Run evaluation', exact=True)).to_be_enabled()
    record('Reopening and completing the operation-only guide preserves edits; confirmed positive weights can run without an abstract goal choice or preset button')
    page.get_by_role('button', name='Reset weights', exact=True).click()
    expect(page.locator('.l3-weight-value')).to_have_text(['—', '—', '—'])
    expect(page.locator('.l3-weight-card[data-confirmed=true]')).to_have_count(0)
    expect(page.get_by_role('button', name='Run evaluation', exact=True)).to_be_disabled()
    expect(page.locator('.level-three')).to_have_attribute('data-round', '0')
    set_weights(page, [70,20,10])
    record('Reset before the first run returns to blank without recording an experiment, while a deliberate non-even allocation can still be confirmed directly')
    finish_run(page)
    expect(page.get_by_role('button', name='Try another split', exact=True)).to_be_visible()
    expect(page.get_by_role('button', name='Compare the results', exact=True)).to_have_count(0)
    next_trial(page)
    expect(guide).to_have_count(0)
    expect(page.locator('.l3-weight-value')).to_have_text(['70%', '20%', '10%'])
    expect(page.locator('.l3-weight-card[data-confirmed=true]')).to_have_count(0)
    slider(page, 'part', 40)
    page.get_by_test_id('confirm-part').click()
    page.get_by_role('button', name='Reset weights', exact=True).click()
    expect(page.locator('.l3-weight-value')).to_have_text(['70%', '20%', '10%'])
    expect(page.locator('.l3-weight-card[data-confirmed=true]')).to_have_count(0)
    expect(page.locator('.level-three')).to_have_attribute('data-round', '1')
    expect(page.locator('.l3-strategy-hint')).not_to_have_attribute('open', '')
    set_weights(page, [34, 33, 33])
    finish_run(page)
    compare(page)
    expect(page.locator('.l3-compare-table thead th[data-kind=player]')).to_have_count(2)
    expect(page.get_by_role('radio')).to_have_count(0)
    expect(page.get_by_role('button', name='Watch Alex’s response', exact=True)).to_be_enabled()
    expect(page.get_by_role('button', name='Test another idea', exact=True)).to_be_visible()
    page.screenshot(path='test-results/player-experiments-two-tests-1366.png', full_page=True)
    finish_theory(page)
    record('An uneven first attempt can be rebalanced immediately; two actual observations compare and reach the theory without a forced third trial or final verdict')
    context.close()

    context, page = start(browser)
    set_weights(page, [34, 33, 33]); finish_run(page); next_trial(page)
    set_weights(page, [36, 32, 32]); finish_run(page); compare(page)
    expect(page.locator('td[data-effort-change=same]')).to_have_count(3)
    finish_theory(page, 'same effort pattern')
    record('A player who starts evenly can finish after another all-medium split; the unchanged evidence is accepted and the closing response does not invent a change')
    context.close()

    context, page = start(browser)
    for index, values in enumerate([[34, 33, 33], [36, 32, 32]]):
        set_weights(page, values); finish_run(page)
        if index == 0: next_trial(page)
    compare(page); next_trial(page, optional=True)
    slider(page, 'prep', 70)
    page.get_by_test_id('confirm-prep').click()
    page.get_by_role('button', name='Guide', exact=True).click()
    for _ in range(3):
        page.get_by_role('button', name='Next', exact=True).click()
    spotlight = page.locator('.l3-tour-spotlight').bounding_box()
    run_button = page.locator('.l3-run-action .primary-button').bounding_box()
    back_button = page.locator('.l3-run-action .text-button').bounding_box()
    def covers_center(target):
        x, y = target['x'] + target['width']/2, target['y'] + target['height']/2
        return spotlight['x'] <= x <= spotlight['x'] + spotlight['width'] and spotlight['y'] <= y <= spotlight['y'] + spotlight['height']
    assert covers_center(run_button) and not covers_center(back_button), (spotlight, run_button, back_button)
    page.get_by_role('button', name='Try your weights', exact=True).click()
    page.get_by_role('button', name='Back to comparison', exact=True).click()
    expect(page.locator('.l3-compare-table thead th[data-kind=player]')).to_have_count(2)
    expect(page.get_by_role('button', name='Watch Alex’s response', exact=True)).to_be_enabled()
    next_trial(page, optional=True)
    expect(page.locator('.l3-weight-value')).to_have_text(['36%', '32%', '32%'])
    expect(page.locator('.l3-weight-card[data-confirmed=true]')).to_have_count(0)
    set_weights(page, [34, 33, 33])
    expect(page.get_by_role('button', name='Run evaluation', exact=True)).to_be_disabled()
    expect(page.locator('.l3-edit-error')).to_contain_text('already')
    page.get_by_role('button', name='Reset weights', exact=True).click()
    set_weights(page, [31, 35, 34]); finish_run(page); compare(page)
    expect(page.locator('.l3-compare-table thead th[data-kind=player]')).to_have_count(3)
    expect(page.locator('td[data-effort-change=same]')).to_have_count(6)
    expect(page.get_by_role('button', name='Test another idea', exact=True)).to_have_count(0)
    for width in [1366, 768, 390, 320]:
        page.set_viewport_size({'width': width, 'height': 900})
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
        page.screenshot(path=f'test-results/player-experiments-comparison-{width}.png', full_page=True)
    finish_theory(page)
    record('A third experiment can be cancelled after editing without creating a record, then reopened; distinct same-band trials remain valid, exact repeats are rejected and no fourth-test loop appears')
    context.close()

    context, page = start(browser)
    set_weights(page, [70, 20, 10]); finish_run(page); next_trial(page)
    set_weights(page, [10, 70, 20]); finish_run(page); compare(page)
    expect(page.locator('.l3-compare-table thead th.uneven')).to_have_count(2)
    expect(page.locator('tr[data-metric=prep] td[data-run="2"]')).to_have_attribute('data-effort-change', 'less')
    expect(page.locator('tr[data-metric=part] td[data-run="2"]')).to_have_attribute('data-effort-change', 'more')
    finish_theory(page)
    record('Two deliberately uneven experiments can compare and finish; no hidden requirement forces near-even weights or an automatic reference example')
    context.close()

    for index, metric in enumerate(['prep', 'part', 'focus']):
        width = 320 if index == 2 else 1366
        context, page = start(browser, width, motion='no-preference')
        expect(page.locator('.l3-weight-card[data-assigned=false]')).to_have_count(3)
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
        if index in [0,2]: page.screenshot(path=f'test-results/unassigned-editor-{width}.png', full_page=True)
        field = page.get_by_test_id('weight-card-' + metric).locator('input')
        field.focus(); field.press('ArrowRight')
        values = [int(value.rstrip('%')) for value in page.locator('.l3-weight-value').all_text_contents()]
        assert values[index] == 1 and sum(values) == 100 and min(values) >= 1, values
        field.press('End')
        values = [int(value.rstrip('%')) for value in page.locator('.l3-weight-value').all_text_contents()]
        assert values[index] == 98 and sum(values) == 100 and min(values) == 1, values
        field.press('Home')
        values = [int(value.rstrip('%')) for value in page.locator('.l3-weight-value').all_text_contents()]
        assert values[index] == 1 and sum(values) == 100 and min(values) >= 1, values
        page.get_by_role('button', name='Reset weights', exact=True).click()
        expect(page.locator('.l3-weight-value')).to_have_text(['—','—','—'])
        field.scroll_into_view_if_needed()
        rect = field.bounding_box()
        field.click(position={'x':rect['width']*.6,'y':rect['height']/2})
        values = [int(value.rstrip('%')) for value in page.locator('.l3-weight-value').all_text_contents()]
        assert sum(values) == 100 and min(values) >= 1, values
        page.reload(wait_until='networkidle')
        expect(page.locator('.level-three')).to_have_attribute('data-phase','intro')
        context.close()
    record('Any of the three cards can start by real keyboard or pointer input; positive bounds hold after initialization and reset, desktop/phone layouts fit, and reload begins a fresh visit')

    context, page = start(browser)
    set_weights(page, [98, 1, 1])
    expect(page.get_by_role('button', name='Run evaluation', exact=True)).to_be_enabled()
    assert all(int(value.rstrip('%')) >= 1 for value in page.locator('.l3-weight-value').all_text_contents())
    finish_run(page)
    expect(page.get_by_test_id('criteria-stop')).to_have_attribute('data-covered-count', '1')
    record('The widest valid allocation remains 98/1/1, totals 100 and observes one covered task without any zero-weight route')
    context.close(); browser.close()
assert not errors, errors
record('No runtime errors in the guide, first-even and first-uneven paths, optional third experiment, positive bounds or theory endpoint')
Path('test-results/player-experiments-results.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'runtimeErrors':errors},indent=2)+'\n')
