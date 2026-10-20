"""Check short reviews, criterion-based stopping and all visible trial records."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

OUT=Path('test-results');OUT.mkdir(exist_ok=True)
HTML=Path('dist-level3/index.html').read_bytes()
checks,errors=[],[]
IDS=['prep','part','focus']

def advance(page,seconds=12):
    for _ in range(seconds):page.clock.run_for(1000);page.wait_for_timeout(15)
def record(text):checks.append(text);print('PASS',text,flush=True)

def start(browser,ids=IDS,width=1366):
    context=browser.new_context(viewport={'width':width,'height':1000},reduced_motion='reduce')
    context.set_offline(True)
    context.route('https://dialogue.test/**',lambda route:route.fulfill(status=200,content_type='text/html',body=HTML))
    page=context.new_page();page.on('pageerror',lambda error:errors.append(str(error)));page.clock.install()
    page.goto('https://dialogue.test/',wait_until='networkidle');advance(page)
    page.get_by_role('button',name='Choose priorities',exact=True).click()
    for id in ids:page.get_by_test_id('level3-metric-'+id).click()
    page.get_by_role('button',name='Set the weights',exact=True).click()
    expect(page.locator('.l3-bottom-dialogue')).to_have_count(0)
    return context,page

def split(page,values,ids=IDS):
    for index,id in enumerate(ids[:2]):
        page.get_by_test_id('weight-card-'+id).locator('input').evaluate("(e,v)=>{Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(e,v);e.dispatchEvent(new Event('input',{bubbles:true}));}",values[index])
        page.get_by_test_id('confirm-'+id).click()

def chat(page):
    page.locator('.l3-bottom-dialogue').scroll_into_view_if_needed();advance(page)
    expect(page.locator('.alex-bubble p')).to_have_count(2)
    expect(page.locator('.maya-avatar svg')).to_have_attribute('data-character','teacher')
    expect(page.locator('.alex-character:not(.message-continuation) .avatar svg')).to_have_attribute('data-character','student')
    return page.locator('.maya-bubble p').inner_text(),page.locator('.alex-bubble p').all_inner_texts()

def publish(page):
    page.get_by_role('button',name='Run evaluation',exact=True).click()
    page.locator('.l3-publish').scroll_into_view_if_needed();advance(page,8)
    expect(page.locator('.l3-bottom-dialogue')).to_have_count(0)
    expect(page.locator('.level-three')).to_have_attribute('data-phase','publish')

def observe(page):
    page.get_by_role('button',name='Observe the class',exact=True).click()
    lines=[]
    for index in range(3):
        lines.append(page.locator('.l3-scene-caption p').inner_text())
        page.get_by_role('button',name='Continue scene' if index<2 else 'Return to dashboard',exact=True).click()
    page.locator('.l3-results').scroll_into_view_if_needed();advance(page)
    return lines,chat(page)

def fit_comparison(page,expected):
    expect(page.locator('.l3-bottom-dialogue')).to_have_count(0)
    expect(page.locator('.l3-compare-table tbody tr')).to_have_count(3)
    expect(page.locator('.l3-compare-table thead th[data-run]')).to_have_count(len(expected))
    for index,values in enumerate(expected):
        expect(page.locator(f'td[data-run="{index+1}"] .l3-row-weight')).to_have_text([str(v)+'%' for v in values])
    for width in [1366,768,390,320]:
        page.set_viewport_size({'width':width,'height':1000});advance(page,1)
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
        headings=page.locator('thead th[data-run]').all()
        colors=[h.evaluate('e=>getComputedStyle(e).backgroundColor') for h in headings]
        assert len(set(colors))==1,'Pattern headings must share a neutral background'
        for row in page.locator('tbody tr').all():
            expect(row.locator('th[scope=row]')).to_have_count(1)
            for cell,header in zip(row.locator('td').all(),headings):
                a=cell.bounding_box();b=header.bounding_box()
                assert abs(a['x']-b['x'])<=1 and abs(a['width']-b['width'])<=1
                assert cell.evaluate('e=>e.scrollWidth<=e.clientWidth+1')
        page.screenshot(path=str(OUT/f'focus-comparison-{len(expected)}-{width}.png'),full_page=True,animations='disabled')

with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    reviews=[]
    for values,expected in [([70,20,10],'Why leave the other two behind'),([45,45,10],'What happened to Focus'),([34,33,33],'What would you like to explore next')]:
        context,page=start(browser);split(page,values);publish(page)
        shots,result=observe(page);assert result[0].startswith(expected),result
        reviews.append(result)
        if values==[34,33,33]:
            expect(page.locator('.l3-routine-beat[data-shown=true]')).to_have_count(3)
            expect(page.locator('.l3-run-rows [data-effort=medium]')).to_have_count(3)
            expect(page.locator('.student-behaviour')).to_have_text('Stops when the criteria are met.')
            assert result[1]==['Does that earn extra points?','If not, I’m done. 😏']
            assert all(any(word in line.lower() for word in ['tick','mark','count']) for line in shots)
            page.screenshot(path=str(OUT/'focus-even-first-1366.png'),full_page=True,animations='disabled')
        record(f'{values}: operations stay free of dialogue; the sole short review fits the pattern, including the near-even stopping risk')
        context.close()
    assert len(set(r[0] for r in reviews))==3

    context,page=start(browser);split(page,[70,20,10]);publish(page);first_shots,first=observe(page)
    page.get_by_role('button',name='Try another split',exact=True).click();split(page,[80,10,10]);publish(page)
    second_shots,second=observe(page)
    assert second[0]=='New weights, same routine?' and all(a!=b for a,b in zip(first_shots,second_shots))
    page.get_by_role('button',name='What if they counted equally?',exact=True).click();advance(page,5);observe(page)
    page.get_by_role('button',name='Compare the patterns',exact=True).click();advance(page,2)
    fit_comparison(page,[[70,20,10],[80,10,10],[34,33,33]])
    record('Both player trials and the reference align under shared metric names at four widths; no near-even success colour or comparison dialogue')
    context.close()

    context,page=start(browser);split(page,[34,33,33]);publish(page);observe(page)
    page.get_by_role('button',name='Try another split',exact=True).click();split(page,[20,70,10]);publish(page);observe(page)
    page.get_by_role('button',name='Compare the patterns',exact=True).click();advance(page,2)
    fit_comparison(page,[[34,33,33],[20,70,10]])
    page.get_by_role('button',name='Step back and reflect',exact=True).click()
    expect(page.locator('.l3-scene-caption p')).to_contain_text('You moved your effort.')
    record('Near-even-first and concentrated-second trials retain their actual order and enter the brief response/theory sequence directly')
    context.close()

    signatures={}
    for trio in [IDS,['discuss','reflect','peer']]:
        context,page=start(browser,ids=trio);split(page,[34,33,33],ids=trio);publish(page)
        page.get_by_role('button',name='Observe the class',exact=True).click()
        for _ in range(2):page.get_by_role('button',name='Continue scene',exact=True).click()
        page.get_by_role('button',name='Return to dashboard',exact=True).click()
        advance(page,3)
        routine=page.get_by_test_id('criteria-stop');routine.scroll_into_view_if_needed()
        shown=page.locator('.l3-routine-beat[data-shown=true]').count()
        page.evaluate("Object.defineProperty(document,'hidden',{configurable:true,value:true});document.dispatchEvent(new Event('visibilitychange'))")
        advance(page,5);assert page.locator('.l3-routine-beat[data-shown=true]').count()==shown
        expect(page.locator('.maya-bubble p')).to_have_count(0)
        page.evaluate("delete document.hidden;document.dispatchEvent(new Event('visibilitychange'))");advance(page,4)
        expect(page.locator('.l3-routine-beat[data-shown=true]')).to_have_count(3)
        for id in trio:
            svg=page.locator(f'.task-scene[data-task="{id}"]')
            signatures[id]=svg.locator('path').evaluate_all('paths=>paths.map(p=>p.getAttribute("d")).join(";")')
        context.close()
    assert len(set(signatures.values()))==6
    record('All six metrics have different task artwork; the criteria → ticks → pack-up sequence pauses while hidden before the review can begin')
    browser.close()
assert not errors,errors
record('Focused Level 3 production checks have no runtime errors')
(OUT/'dialogue-browser-results.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'runtimeErrors':errors},indent=2)+'\n')
