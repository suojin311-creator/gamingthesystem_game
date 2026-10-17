"""Read the dialogue that players actually see in the packaged Level 3."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

OUT=Path('test-results'); OUT.mkdir(exist_ok=True)
HTML=Path('dist-level3/index.html').read_bytes()
checks,errors=[],[]
IDS=['prep','part','focus']

def advance(page,seconds=12):
    for _ in range(seconds): page.clock.run_for(1000);page.wait_for_timeout(15)

def record(text): checks.append(text);print('PASS',text,flush=True)

def start(browser,width=1366):
    context=browser.new_context(viewport={'width':width,'height':1000},reduced_motion='reduce')
    context.set_offline(True)
    context.route('https://dialogue.test/**',lambda route:route.fulfill(status=200,content_type='text/html',body=HTML))
    page=context.new_page();page.on('pageerror',lambda error:errors.append(str(error)));page.clock.install()
    page.goto('https://dialogue.test/',wait_until='networkidle');advance(page)
    page.get_by_role('button',name='Choose priorities',exact=True).click()
    for id in IDS:page.get_by_test_id('level3-metric-'+id).click()
    page.get_by_role('button',name='Set the weights',exact=True).click()
    return context,page

def split(page,values):
    for index,id in enumerate(IDS[:2]):
        page.get_by_test_id('weight-card-'+id).locator('input').evaluate("(e,v)=>{Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(e,v);e.dispatchEvent(new Event('input',{bubbles:true}));}",values[index])
        page.get_by_test_id('confirm-'+id).click()

def chat(page):
    page.locator('.l3-bottom-dialogue').scroll_into_view_if_needed();advance(page)
    expect(page.locator('.alex-bubble p')).to_have_count(2)
    expect(page.locator('.maya-avatar svg')).to_have_attribute('data-character','teacher')
    expect(page.locator('.alex-character:not(.message-continuation) .avatar svg')).to_have_attribute('data-character','student')
    expect(page.locator('.avatar')).to_have_text(['','',''])
    teacher=page.locator('.maya-bubble p').inner_text()
    alex=page.locator('.alex-bubble p').all_inner_texts()
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    return teacher,alex

def publish(page):
    page.get_by_role('button',name='Run evaluation',exact=True).click()
    page.locator('.l3-publish').scroll_into_view_if_needed();advance(page,5)
    return chat(page)

def observe(page):
    page.get_by_role('button',name='Observe the class',exact=True).click()
    lines=[]
    for index in range(3):
        lines.append(page.locator('.l3-scene-caption p').inner_text())
        page.get_by_role('button',name='Continue scene' if index<2 else 'Return to dashboard',exact=True).click()
    page.locator('.l3-results').scroll_into_view_if_needed();advance(page)
    return lines,chat(page)

with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    published=[];review=[]
    for values,expected in [([70,20,10],'Preparation counts most'),([45,45,10],'Preparation and Participation count more'),([34,33,33],'These three count about the same')]:
        context,page=start(browser);split(page,values)
        first=publish(page);assert first[0].startswith(expected),first
        published.append(first)
        if values==[34,33,33]:
            assert 'most points' not in ' '.join(first[1])
            page.screenshot(path=str(OUT/'dialogue-even-published-1366.png'),full_page=True,animations='disabled')
            page.set_viewport_size({'width':320,'height':740});advance(page,1)
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
            page.screenshot(path=str(OUT/'dialogue-even-published-320.png'),full_page=True,animations='disabled')
        _,result=observe(page);review.append(result)
        record(f'{values}: publication plan and teacher review match the selected weight pattern; two Alex replies and distinct name-independent portraits are visible')
        context.close()
    assert len(set(item[0] for item in published))==3 and len(set(item[0] for item in review))==3

    context,page=start(browser);split(page,[70,20,10]);first=publish(page);shots,first_review=observe(page)
    page.get_by_role('button',name='Try another split',exact=True).click();split(page,[80,10,10]);second=publish(page)
    assert second!=first and 'Still Preparation first!' in second[1][0]
    repeated_shots,second_review=observe(page)
    assert all(a!=b for a,b in zip(shots,repeated_shots))
    assert second_review[0]=='The weights moved, but your effort looks similar. Why?'
    page.get_by_role('button',name='What if they counted equally?',exact=True).click()
    page.locator('.l3-publish').scroll_into_view_if_needed();advance(page,5)
    reference=chat(page);assert reference not in [first,second]
    observe(page)
    page.get_by_role('button',name='Compare the patterns',exact=True).click();comparison=chat(page)
    assert comparison[0].startswith('Your effort is more balanced now.')
    page.screenshot(path=str(OUT/'dialogue-three-run-comparison.png'),full_page=True,animations='disabled')
    record('Two concentrated trials acknowledge unchanged effort, use fresh classroom replies, retain both trials and offer a different near-even reference exchange')
    context.close()

    context,page=start(browser);split(page,[34,33,33]);publish(page);observe(page)
    page.get_by_role('button',name='Try another split',exact=True).click();split(page,[20,70,10]);changed=publish(page)
    assert 'I’m switching to Participation!' in changed[1][0]
    observe(page)
    page.get_by_role('button',name='Compare the patterns',exact=True).click();comparison=chat(page)
    assert 'You shifted toward Participation.' in comparison[0]
    page.get_by_role('button',name='Watch Alex’s response',exact=True).click()
    expect(page.locator('.l3-scene-caption p')).to_contain_text('Making Participation worth more pulled your attention there.')
    record('Near-even-first trial followed by a new leading priority describes concentration correctly in both workbench and final cinematic')
    context.close();browser.close()
assert not errors,errors
record('Dialogue branch browser checks have no runtime errors')
(OUT/'dialogue-browser-results.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'runtimeErrors':errors},indent=2)+'\n')
