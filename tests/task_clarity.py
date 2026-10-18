"""Readable evidence-led questions, optional hints, spotlight layout and honest comparisons."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
exec(Path('tests/player_experiments.py').read_text().split('with sync_playwright() as p:')[0])
checks, errors = [], []

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    context, page = start(browser, motion='no-preference')
    prompt = page.locator('.l3-experiment')
    expect(prompt).to_have_attribute('data-attention', 'true')
    style = prompt.evaluate('e=>{const s=getComputedStyle(e);return {name:s.animationName,count:s.animationIterationCount,border:s.borderLeftWidth}}')
    assert style == {'name':'l3-task-attention','count':'3','border':'4px'}, style
    page.evaluate("Object.defineProperty(document,'hidden',{configurable:true,value:true});document.dispatchEvent(new Event('visibilitychange'))")
    page.wait_for_function("getComputedStyle(document.querySelector('.l3-experiment')).animationPlayState==='paused'")
    advance(page, 3000)
    expect(prompt).to_have_attribute('data-attention', 'true')
    page.evaluate("delete document.hidden;document.dispatchEvent(new Event('visibilitychange'))")
    advance(page, 3000)
    expect(prompt).to_have_attribute('data-attention', 'false')
    expect(prompt.get_by_role('radio')).to_have_count(0)
    expect(prompt.locator('.l3-experiment-question .eyebrow')).to_have_count(0)
    expect(page.locator('.l3-allocation')).to_have_count(0)
    record('The evidence question retains three finite attention pulses, pauses on hidden pages and never becomes a mandatory goal questionnaire')
    initial = page.locator('.l3-weight-value').all_text_contents()
    expect(prompt.locator('details')).not_to_have_attribute('open','')
    prompt.locator('summary').click()
    hint_paragraph = prompt.locator('details > p')
    assert hint_paragraph.evaluate('e=>e.getBoundingClientRect().height<=parseFloat(getComputedStyle(e).lineHeight)+1')
    hint = prompt.locator('details').inner_text()
    assert '%' not in hint and '34 / 33 / 33' not in hint, hint
    assert page.locator('.l3-weight-value').all_text_contents() == initial
    expect(page.get_by_role('button', name='Apply suggested weights', exact=True)).to_have_count(0)
    record('Strategy help remains collapsed and optional; opening it supplies contextual words without choosing or changing an allocation')
    set_weights(page, [70,20,10]); finish_run(page); next_trial(page)
    last = page.get_by_role('group', name='Last observation', exact=True)
    expect(last).to_be_visible()
    expect(last.locator('.l3-stopping-reminder')).to_have_text('Stopped after earning the marks he wanted.')
    for name, label in [('Preparation','Intense effort'),('Participation','Minimum effort'),('Focus','Minimum effort')]:
        expect(last).to_contain_text(name)
        expect(last).to_contain_text(label)
    question_one = prompt.locator('#experiment-question').inner_text()
    assert '?' in question_one and len(question_one.split()) <= 24, question_one
    expect(page.locator('.l3-weight-value')).to_have_text(['70%','20%','10%'])
    expect(page.locator('.l3-weight-card[data-confirmed=true]')).to_have_count(0)
    page.screenshot(path='test-results/task-clarity-prompt-1366.png', full_page=True)
    record('The second editor retains the previous allocation and shows all three actual effort observations beside a short next question')
    set_weights(page, [34,33,33]); finish_run(page); compare(page); next_trial(page, optional=True)
    question_two = prompt.locator('#experiment-question').inner_text()
    assert question_two != question_one, (question_one, question_two)
    expect(last).to_contain_text('Steady effort')
    expect(last).not_to_contain_text('Minimum effort')
    expect(last.locator('.l3-stopping-reminder')).to_be_visible()
    expect(prompt.locator('#experiment-question')).to_contain_text('stopped')
    prompt.locator('summary').click()
    assert hint_paragraph.evaluate('e=>e.getBoundingClientRect().height<=parseFloat(getComputedStyle(e).lineHeight)+1')
    page.emulate_media(reduced_motion='reduce')
    assert prompt.evaluate('e=>getComputedStyle(e).animationName') == 'l3-task-still'
    assert prompt.evaluate('e=>getComputedStyle(e).animationIterationCount') == '1'
    for width in [1366,768,390,320]:
        page.set_viewport_size({'width':width,'height':900})
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
        page.screenshot(path=f'test-results/task-clarity-prompt-{width}.png', full_page=True)
    record('The optional third editor responds to the latest all-medium evidence rather than repeating the old low-effort prompt; reduced motion and 1366/768/390/320px remain usable')
    set_weights(page, [10,70,20]); finish_run(page); compare(page)
    expected = {'prep':['baseline','less','less'], 'part':['baseline','more','more'], 'focus':['baseline','more','less']}
    for metric, values in expected.items():
        cells = page.locator(f'.l3-compare-table tr[data-metric="{metric}"] td')
        assert [cell.get_attribute('data-effort-change') for cell in cells.all()] == values
        for cell, change in zip(cells.all(), values):
            expect(cell.locator('.l3-effort-change')).to_contain_text({'baseline':'First result','same':'Same effort','more':'More effort','less':'Less effort'}[change])
            assert cell.evaluate('e=>getComputedStyle(e).boxShadow') == 'none'
            assert cell.evaluate('e=>getComputedStyle(e).backgroundColor') == 'rgba(0, 0, 0, 0)'
    expect(page.locator('.l3-comparison-basis')).to_have_text(['Starting observation','Effort vs First test','Effort vs Second test'])
    for width in [1366,768,390,320]:
        page.set_viewport_size({'width':width,'height':900})
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
        for cell in page.locator('.l3-compare-table tbody td').all():
            assert cell.locator('.l3-effort-change').evaluate('e=>e.scrollWidth<=e.clientWidth')
        page.screenshot(path=f'test-results/task-clarity-comparison-{width}.png', full_page=True)
    record('Every comparison cell names its effort change against the immediately previous actual test, with explicit baselines and no ambiguous whole-cell highlighting at desktop or phone widths')
    context.close()

    trio = ('focus', 'reflect', 'peer')
    context, page = start(browser, metric_ids=trio)
    set_weights(page, [34,33,33], trio); finish_run(page); next_trial(page)
    expect(page.locator('#experiment-question')).to_have_text('Can new weights make Alex go further?')
    last = page.get_by_role('group', name='Last observation', exact=True)
    expect(last.locator('li[data-effort=medium]')).to_have_count(3)
    expect(last.locator('.l3-stopping-reminder')).to_be_visible()
    expect(page.locator('.l3-experiment-question .eyebrow')).to_have_count(0)
    expect(page.locator('.l3-allocation')).to_have_count(0)
    page.locator('.l3-strategy-hint summary').click()
    hint_paragraph = page.locator('.l3-strategy-hint > p')
    assert hint_paragraph.evaluate('e=>e.getBoundingClientRect().height<=parseFloat(getComputedStyle(e).lineHeight)+1')
    page.screenshot(path='test-results/feedback20-editor-1366.png', full_page=True)
    page.set_viewport_size({'width':320,'height':900})
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    page.screenshot(path='test-results/feedback20-editor-320.png', full_page=True)
    set_weights(page, [49,26,25], trio); finish_run(page); compare(page); next_trial(page, optional=True)
    set_weights(page, [49,27,24], trio); finish_run(page); compare(page)
    for metric, effort in [('focus','high'),('reflect','low'),('peer','low')]:
        for index in [2,3]:
            expect(page.locator(f'tr[data-metric={metric}] td[data-run="{index}"]')).to_have_attribute('data-effort',effort)
        expect(page.locator(f'tr[data-metric={metric}] td[data-run="3"]')).to_have_attribute('data-effort-change','same')
    record('Shared attention retains the explicit stopping concern and concise help; 49/26/25 and49/27/24 both show one high/two low with no invented 24/25 cliff')
    context.close()

    context, page = start(browser, 320, skip_guide=False)
    guide = page.get_by_role('dialog', name='Weight guide', exact=True)
    for width in [320,390,768,1366]:
        page.set_viewport_size({'width':width,'height':900})
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
        for index in range(4):
            expect(guide).to_be_visible()
            rect = guide.bounding_box()
            assert rect and rect['x'] >= -1 and rect['x'] + rect['width'] <= width + 1, (width,rect)
            button = guide.get_by_role('button', name='Next' if index < 3 else 'Try your weights', exact=True)
            expect(button).to_be_visible()
            assert button.bounding_box()['height'] >= 24
            if index < 3: button.click()
        page.screenshot(path=f'test-results/task-clarity-guide-{width}.png', full_page=True)
        for _ in range(3): guide.get_by_role('button', name='Back', exact=True).click()
    page.keyboard.press('Tab')
    assert guide.evaluate('e=>e.contains(document.activeElement)')
    page.keyboard.press('Shift+Tab')
    assert guide.evaluate('e=>e.contains(document.activeElement)')
    page.get_by_role('button', name='Skip guide', exact=True).click()
    expect(guide).to_have_count(0)
    expect(page.locator('.l3-weight-card[data-confirmed=true]')).to_have_count(0)
    record('All four spotlight explanations fit phone, tablet and desktop, trap keyboard focus and can be skipped without altering allocation or confirmations')
    context.close(); browser.close()
assert not errors, errors
record('No runtime errors in evidence prompts, optional hints, responsive spotlight guidance or adjacent-test comparisons')
Path('test-results/task-clarity-results.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'runtimeErrors':errors},indent=2)+'\n')
