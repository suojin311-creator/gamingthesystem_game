"""Regression checks for the user's weighting controls and visual feedback."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

OUT=Path('test-results');OUT.mkdir(exist_ok=True)
ARTIFACTS={str(level):Path(f'dist-level{level}/index.html').read_bytes() for level in [1,2,3]}
IDS=['prep','part','focus']
checks,errors=[],[]


def record(name): checks.append(name);print('PASS',name,flush=True)


def advance(page,seconds=8):
    for _ in range(seconds):page.clock.run_for(1000);page.wait_for_timeout(15)


def open_level(browser,level=3,width=1366,height=900):
    context=browser.new_context(viewport={'width':width,'height':height},reduced_motion='reduce')
    context.set_offline(True)
    context.route('https://feedback.test/**',lambda route:route.fulfill(status=200,content_type='text/html',body=ARTIFACTS[str(level)]))
    page=context.new_page();page.on('pageerror',lambda error:errors.append(str(error)));page.clock.install()
    page.goto('https://feedback.test/',wait_until='networkidle')
    if level==3:
        advance(page);page.get_by_role('button',name='Choose priorities',exact=True).click()
        for id in IDS:page.get_by_test_id('level3-metric-'+id).click()
        page.get_by_role('button',name='Set the weights',exact=True).click()
    return context,page


def move(page,index,value):
    page.get_by_test_id('weight-card-'+IDS[index]).locator('input').evaluate('''(input,value)=>{
      Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(input,value);
      input.dispatchEvent(new Event('input',{bubbles:true}));
    }''',value)


def confirm(page,index):page.get_by_test_id('confirm-'+IDS[index]).click()


def split(page,values):
    move(page,0,values[0]);confirm(page,0);move(page,1,values[1]);confirm(page,1)


def observe(page):
    page.get_by_role('button',name='Observe the class',exact=True).click()
    for _ in range(2):page.get_by_role('button',name='Continue scene',exact=True).click()
    page.get_by_role('button',name='Return to dashboard',exact=True).click()
    page.locator('.l3-results').scroll_into_view_if_needed();advance(page,12)


def run(page):
    page.get_by_role('button',name='Run evaluation',exact=True).click()
    page.locator('.l3-publish').scroll_into_view_if_needed();advance(page,5)
    observe(page)


def aligned(page):
    for table in page.locator('.l3-run-table').all():
        weight_header=table.locator('.l3-result-legend > span').nth(1).bounding_box()
        response_header=table.locator('.l3-result-legend > span').nth(2).bounding_box()
        for row in table.locator('.l3-run-rows li').all():
            weight=row.locator('.l3-row-weight').bounding_box()
            response=row.locator('.l3-effort').bounding_box()
            assert abs(weight['x']+weight['width']/2-weight_header['x']-weight_header['width']/2)<1
            assert abs(response['x']-response_header['x'])<1
            assert row.locator('.l3-row-weight').evaluate("element=>parseFloat(getComputedStyle(element).borderRightWidth)")>=1


with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    context,page=open_level(browser,1)
    page.get_by_role('button',name='Skip guide',exact=True).click()
    metric_size=page.locator('.metric-card h3').first.evaluate('element=>getComputedStyle(element).fontSize')
    assert metric_size=='16px';context.close()
    context,page=open_level(browser,2)
    advance(page);page.get_by_role('button',name='Choose three metrics',exact=True).click()
    assert page.locator('.l2-metric-card h3').first.evaluate('element=>getComputedStyle(element).fontSize')==metric_size
    for id in IDS:page.get_by_test_id('level2-metric-'+id).click()
    page.get_by_role('button',name='Run evaluation',exact=True).click();advance(page,5)
    assert page.locator('.l2-eval-name').first.evaluate('element=>getComputedStyle(element).fontSize')==metric_size
    context.close()

    context,page=open_level(browser)
    page.locator('.l3-bottom-dialogue').scroll_into_view_if_needed();advance(page,1)
    expect(page.locator('.l3-bottom-dialogue .maya-bubble p')).to_have_text('Alex, how will you decide which tasks to focus on?')
    assert page.locator('.l3-decision .conversation').count()==0
    assert page.locator('.l3-bottom-dialogue').bounding_box()['y']>=page.locator('.l3-body').bounding_box()['y']+page.locator('.l3-body').bounding_box()['height']-1
    assert page.locator('.l3-editor-tools').bounding_box()['y']<page.locator('.l3-decision .action-row').bounding_box()['y']
    assert page.locator('.l3-weight-card h3').first.evaluate('element=>getComputedStyle(element).fontSize')==metric_size
    assert page.locator('.l3-bottom-dialogue .speech-bubble p').evaluate('element=>getComputedStyle(element).fontSize')=='15px'
    record('Metric names match Levels 1/2; Reset stays above the action row and the player uses the shared bottom dialogue region and bubble size')
    page.screenshot(path=str(OUT/'level3-feedback-weights.png'),full_page=True,animations='disabled')
    context.close()

    for first in range(3):
        for clicked in [index for index in range(3) if index!=first]:
            context,page=open_level(browser)
            move(page,first,80);confirm(page,first)
            other=next(index for index in range(3) if index not in [first,clicked])
            expect(page.get_by_test_id('weight-card-'+IDS[clicked]).locator('input')).to_be_enabled()
            expect(page.get_by_test_id('weight-card-'+IDS[other]).locator('input')).to_be_enabled()
            move(page,clicked,15)
            expect(page.get_by_test_id('weight-card-'+IDS[first]).locator('output')).to_have_text('80%')
            expect(page.get_by_test_id('weight-card-'+IDS[other]).locator('output')).to_have_text('5%')
            confirm(page,clicked)
            expect(page.get_by_test_id('confirm-'+IDS[other])).to_have_text('Auto-confirmed')
            expect(page.get_by_test_id('confirm-'+IDS[other])).to_be_disabled()
            expect(page.get_by_role('button',name='Run evaluation',exact=True)).to_be_enabled()
            record(f'80/15/5 keeps both remainders editable and confirms the final pair: first {IDS[first]}, then {IDS[clicked]}')
            context.close()

    context,page=open_level(browser)
    split(page,[80,15,5])
    page.get_by_role('button',name='Run evaluation',exact=True).click()
    page.locator('.l3-publish').scroll_into_view_if_needed();advance(page,20)
    expect(page.locator('.level-three')).to_have_attribute('data-phase','publish')
    expect(page.get_by_role('button',name='Observe the class',exact=True)).to_be_enabled()
    expect(page.locator('.l3-perspective')).to_have_count(2)
    expect(page.locator('.management-satisfaction-state')).to_have_text('Very satisfied')
    expect(page.locator('.management-satisfaction-evidence')).to_have_text('3 priorities · 100% allocated')
    expect(page.locator('.l3-awaiting')).to_have_text('Awaiting observation')
    expect(page.locator('.student-behaviour')).to_have_count(0)
    page.screenshot(path=str(OUT/'level3-feedback-published.png'),full_page=True,animations='disabled')
    record('Published weights remain until an explicit Observe click, with Management and Students cards showing the same current round')
    observe(page);aligned(page)
    assert 'Illustrative behaviour' not in page.locator('body').inner_text()
    assert page.locator('.l3-row-metric').first.evaluate('element=>getComputedStyle(element).fontSize')==metric_size
    page.screenshot(path=str(OUT/'level3-feedback-results.png'),full_page=True,animations='disabled')
    record('Results remove the requested note and align weights/responses with their headings and a visible vertical divider')
    context.close()

    for width,height in [(768,1024),(390,844),(320,640)]:
        context,page=open_level(browser,width=width,height=height)
        split(page,[80,15,5]);run(page);aligned(page)
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
        page.get_by_role('button',name='Try another split',exact=True).click()
        split(page,[34,33,33]);run(page)
        page.get_by_role('button',name='Compare the patterns',exact=True).click();advance(page,1);aligned(page)
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
        assert page.locator('.l3-row-metric').first.evaluate('element=>parseFloat(getComputedStyle(element).fontSize)')>=14
        expect(page.locator('.l3-comparison-card > p')).to_have_count(0)
        expect(page.locator('.l3-finding')).to_have_count(0)
        if width==390:page.screenshot(path=str(OUT/'level3-feedback-mobile.png'),full_page=True,animations='disabled')
        record(f'{width}px results and comparisons keep readable type, aligned labelled columns, no repeated summaries and no horizontal overflow')
        context.close()
    for values,near_even in [([40,30,30],True),([40,31,29],False)]:
        context,page=open_level(browser)
        split(page,values);run(page)
        button='Try another split' if near_even else 'Try another split'
        expect(page.get_by_role('button',name=button,exact=True)).to_be_visible()
        if near_even:expect(page.locator('.l3-run-rows [data-effort=medium]')).to_have_count(3)
        record(f'First test {values}: the inclusive 10-point boundary selects the correct next task')
        context.close()

    for values,near_even in [([38,33,29],True),([40,30,30],True),([40,31,29],False)]:
        context,page=open_level(browser)
        split(page,[70,20,10]);run(page)
        page.get_by_role('button',name='Try another split',exact=True).click()
        split(page,values);run(page)
        if near_even:
            expect(page.get_by_role('button',name='What if they counted equally?',exact=True)).to_have_count(0)
            expect(page.locator('.l3-run-rows [data-effort=medium]')).to_have_count(3)
            page.get_by_role('button',name='Compare the patterns',exact=True).click()
            expect(page.locator('.near-even .l3-row-weight')).to_have_text([str(value)+'%' for value in values])
            expect(page.locator('.near-even .eyebrow')).to_have_text('YOUR SECOND TEST')
        else:
            expect(page.get_by_role('button',name='What if they counted equally?',exact=True)).to_be_visible()
            expect(page.locator('.maya-bubble p')).to_have_text('Alex, what if all three counted equally?')
        record(f'Second test {values}: '+('compares the player’s actual near-even run without a third test' if near_even else 'offers the explained optional balance check beyond 10 points'))
        context.close()
    context,page=open_level(browser)
    expect(page.locator('.l3-decision .action-row')).not_to_contain_text('Choose any three')
    split(page,[76,6,18]);run(page)
    expect(page.locator('.l3-finding')).to_have_count(0)
    expect(page.locator('.thought-bubble, .thought-cloud, .thought-label')).to_have_count(0)
    expect(page.locator('.maya-bubble p')).to_have_text('Alex, why did you focus on some tasks more than others?')
    expect(page.locator('.alex-bubble p')).to_have_text(['Preparation is worth more points. 🥇','Participation and Focus? I only did the basics.'])
    expect(page.locator('.l3-bottom-dialogue .alex-bubble p')).to_have_count(2)
    assert page.locator('.l3-effort-label').first.evaluate('e=>parseFloat(getComputedStyle(e).fontWeight)')<=600
    assert page.locator('.l3-row-weight').first.evaluate('e=>parseFloat(getComputedStyle(e).fontSize)')>=20
    expect(page.locator('.l3-bottom-dialogue .alex-character.message-continuation')).to_have_count(1)
    page.screenshot(path=str(OUT/'level3-conversation-and-clean-results.png'),full_page=True,animations='disabled')
    record('Ordinary teacher/Alex speech bubbles form a connected exchange; duplicate summaries are absent and result type is balanced')
    page.get_by_role('button',name='Try another split',exact=True).click()
    split(page,[80,10,10]);run(page)
    page.get_by_role('button',name='What if they counted equally?',exact=True).click()
    page.locator('.l3-publish').scroll_into_view_if_needed();advance(page,5);observe(page)
    page.get_by_role('button',name='Compare the patterns',exact=True).click();advance(page,1)
    expect(page.locator('.l3-comparison-card')).to_have_count(3)
    for index,expected in [(1,['76%','6%','18%']),(2,['80%','10%','10%']),(3,['34%','33%','33%'])]:
        expect(page.locator(f'[data-run="{index}"] .l3-row-weight')).to_have_text(expected)
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    aligned(page)
    expect(page.locator('.l3-comparison-card > p')).to_have_count(0)
    expect(page.locator('.l3-finding')).to_have_count(0)
    assert page.locator('.l3-only-action').evaluate("row=>Array.from(row.children).filter(e=>e.tagName!=='BUTTON').every(e=>!e.textContent.trim())")
    page.screenshot(path=str(OUT/'level3-three-tests-desktop.png'),full_page=True,animations='disabled')
    page.set_viewport_size({'width':320,'height':740});advance(page,1);aligned(page)
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    page.screenshot(path=str(OUT/'level3-three-tests-mobile.png'),full_page=True,animations='disabled')
    record('A more uneven second attempt is allowed; all two player tests plus the reference stay visible on desktop and 320px')
    context.close()

    context,page=open_level(browser)
    split(page,[34,33,33]);run(page)
    page.get_by_role('button',name='Try another split',exact=True).click()
    split(page,[40,30,30]);run(page)
    page.get_by_role('button',name='What if one counted more?',exact=True).click()
    page.locator('.l3-publish').scroll_into_view_if_needed();advance(page,5);observe(page)
    page.get_by_role('button',name='Compare the patterns',exact=True).click()
    expect(page.locator('.l3-comparison-card')).to_have_count(3)
    expect(page.locator('[data-run="3"]')).to_have_attribute('data-kind','contrast-check')
    expect(page.locator('[data-run="3"] .l3-row-weight')).to_have_text(['70%','20%','10%'])
    record('Two near-even player tests offer an explicitly labelled uneven reference and retain all three actual splits')
    context.close()
    browser.close()
assert not errors,errors
record('No runtime errors in the feedback regressions')
(OUT/'level3-feedback-results.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'runtimeErrors':errors},indent=2)+'\n')
