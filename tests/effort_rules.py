"""Production regressions for relative effort bands and score-based stopping."""
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
    run_sequence(page, [([49,26,25], ['high','low','low'],1), ([49,27,24], ['high','low','low'],1), ([45,45,10], ['high','high','low'],2)])
    compare(page)
    expect(page.locator('td[data-run="2"][data-effort-change=same]')).to_have_count(3)
    expect(page.locator('td[data-run="3"][data-effort-change=more]')).to_have_count(1)
    expect(page.locator('tr[data-metric=part] td[data-run="3"]')).to_have_attribute('data-effort','high')
    finish_theory(page, 'shifts effort')
    record('49/26/25 and49/27/24 keep one high/two low with no24/25 cliff;45/45/10 gives two high/one low, including correct coverage and final comparison')
    context.close()

    context, page = start(browser)
    run_sequence(page, [([40,30,30], ['medium']*3,3),([40,31,29],['high','medium','low'],2),([60,30,10],['high','medium','low'],2)])
    compare(page)
    expect(page.locator('tr[data-metric=part] td[data-run="2"]')).to_have_attribute('data-effort-change','same')
    expect(page.locator('td[data-run="3"][data-effort-change=same]')).to_have_count(3)
    finish_theory(page, 'shifts effort')
    record('The inclusive ten-point similarity and graduated high/medium/low route follow relative comparisons; raising30to31 never lowers that task’s effort')
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
