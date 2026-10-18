"""Production regressions for independent effort bands and score-based stopping."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
exec(Path('tests/player_experiments.py').read_text().split('with sync_playwright() as p:')[0])
checks, errors = [], []

def observed(page):
    return page.locator('.l3-run-rows li').evaluate_all('(nodes)=>nodes.map(e=>e.dataset.effort)')

def stop_check(page, covered):
    figure = page.get_by_test_id('criteria-stop')
    expect(figure).to_be_visible()
    expect(figure).to_have_attribute('data-covered-count', str(covered))
    expect(figure.locator('[data-mark-earned]')).to_have_count(covered)
    expect(figure.locator('.l3-routine-beat[data-shown=true]')).to_have_count(3)
    expect(figure).to_contain_text('Packs up. Stops.')
    assert 'all three requirements' not in figure.get_attribute('aria-label')

def run_sequence(page, sequence):
    for index, (values, expected, covered) in enumerate(sequence):
        set_weights(page, values); finish_run(page)
        assert observed(page) == expected, (values, observed(page))
        stop_check(page, covered)
        if index == 0:
            next_trial(page)
        elif index < len(sequence) - 1:
            compare(page); next_trial(page, optional=True)

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    context, page = start(browser)
    run_sequence(page, [([40, 30, 30], ['medium'] * 3, 3), ([40, 31, 29], ['medium'] * 3, 3), ([50, 25, 25], ['medium'] * 3, 3)])
    compare(page)
    expect(page.locator('.l3-compare-table thead th.near-even')).to_have_count(1)
    expect(page.locator('.l3-compare-table thead th.uneven')).to_have_count(2)
    expect(page.locator('td[data-effort-change=same]')).to_have_count(6)
    finish_theory(page, 'same effort pattern')
    record('40/30/30 → 40/31/29 → 50/25/25 preserves medium effort independently of the near-even label, and the optional three-test conclusion reports no invented change')
    context.close()

    context, page = start(browser)
    cases = [([67,25,8], ['high','medium','low'], 2), ([66,25,9], ['medium','medium','low'], 2), ([66,24,10], ['medium','low','low'], 1)]
    run_sequence(page, cases)
    compare(page)
    expect(page.locator('td[data-run="2"][data-effort-change=less]')).to_have_count(1)
    expect(page.locator('td[data-run="3"][data-effort-change=less]')).to_have_count(1)
    page.get_by_role('button', name='Watch Alex’s response', exact=True).click()
    expect(page.locator('.l3-scene-copy > p')).to_contain_text('shifts effort')
    record('Crossing 67/66 and 25/24 changes only the corresponding effort band; covered-task ticks and adjacent-trial comparison labels follow the actual observations')
    context.close()

    context, page = start(browser)
    run_sequence(page, [([70,20,10], ['high','low','low'], 1), ([34,33,33], ['medium']*3, 3), ([10,70,20], ['low','high','low'], 1)])
    compare(page)
    expect(page.locator('tr[data-metric=prep] td[data-run="2"]')).to_have_attribute('data-effort-change', 'less')
    expect(page.locator('tr[data-metric=part] td[data-run="3"]')).to_have_attribute('data-effort-change', 'more')
    finish_theory(page)
    record('A real uneven → even → shifted-uneven experiment acknowledges improved coverage while each tested distribution independently exposes score-based stopping')
    context.close()

    context, page = start(browser, 320, motion='no-preference')
    set_weights(page, [70,20,10]); finish_run(page); stop_check(page,1)
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    page.locator('.l3-criteria-stop').scroll_into_view_if_needed()
    page.screenshot(path='test-results/effort-rules-stopping-320.png', full_page=True)
    page.set_viewport_size({'width':1366,'height':900})
    page.screenshot(path='test-results/effort-rules-stopping-1366.png', full_page=True)
    record('Score-based stopping is readable in a 320px normal-motion phone route and desktop without horizontal overflow')
    context.close(); browser.close()
assert not errors, errors
record('No runtime errors in boundary observations, tick coverage, optional third trial, comparison or the theory endpoint')
Path('test-results/effort-browser-results.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'runtimeErrors':errors},indent=2)+'\n')
