"""Focused production checks for update attention, Enter, pace and table headers."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

OUT=Path('test-results');OUT.mkdir(exist_ok=True)
HTML={name:Path(path).read_bytes() for name,path in [('full','dist/index.html'),('2','dist-level2/index.html'),('3','dist-level3/index.html')]}
checks,errors=[],[]
def record(text):checks.append(text);print('PASS',text,flush=True)
def advance(page,seconds=8):
    for _ in range(seconds):page.clock.run_for(1000);page.wait_for_timeout(12)
def start(browser,mode='full',motion='no-preference'):
    context=browser.new_context(viewport={'width':1366,'height':1000},reduced_motion=motion)
    context.set_offline(True)
    context.route('https://feedback-v10.test/**',lambda route:route.fulfill(status=200,content_type='text/html',body=HTML[mode]))
    page=context.new_page();page.on('pageerror',lambda error:errors.append(str(error)));page.clock.install()
    page.goto('https://feedback-v10.test/',wait_until='networkidle');return context,page

def pulse(page,hidden=False,reduced=False):
    notice=page.locator('.management-attention');expect(notice).to_have_count(1)
    notice.scroll_into_view_if_needed()
    page.wait_for_function("document.querySelector('.management-attention').style.animationPlayState==='running'")
    timing=notice.evaluate("e=>{const a=e.getAnimations()[0];return {name:getComputedStyle(e).animationName,iterations:a.effect.getTiming().iterations,duration:a.effect.getTiming().duration}}")
    assert timing['iterations']==(1 if reduced else 3),timing
    assert timing['duration']==(1950 if reduced else 650),timing
    if hidden:
        page.evaluate("Object.defineProperty(document,'hidden',{configurable:true,value:true});document.dispatchEvent(new Event('visibilitychange'))")
        expect(notice).to_have_css('animation-play-state','paused')
        before=notice.evaluate('e=>e.getAnimations()[0].currentTime');page.wait_for_timeout(120)
        after=notice.evaluate('e=>e.getAnimations()[0].currentTime');assert abs(after-before)<25,(before,after)
        page.evaluate("delete document.hidden;document.dispatchEvent(new Event('visibilitychange'))")
        expect(notice).to_have_css('animation-play-state','running')
    notice.evaluate('e=>e.getAnimations()[0].finish()')
    expect(notice).to_have_count(0)

def finish_scene(page):
    for _ in range(2):page.get_by_role('button',name='Continue scene',exact=True).click()
    page.get_by_role('button',name='Return to dashboard',exact=True).click()

def evaluate_three(page,values):
    for id,value in zip(['prep','part'],values):
        page.get_by_test_id('weight-card-'+id).locator('input').evaluate("(e,v)=>{Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(e,v);e.dispatchEvent(new Event('input',{bubbles:true}));}",value)
        page.get_by_test_id('confirm-'+id).click()
    page.get_by_role('button',name='Run evaluation',exact=True).click()
    page.locator('.l3-publish').scroll_into_view_if_needed();advance(page,5);pulse(page)
    page.get_by_role('button',name='Observe the class',exact=True).click();finish_scene(page)
    page.locator('.l3-results').scroll_into_view_if_needed();advance(page,12)

with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    context,page=start(browser)
    page.get_by_role('button',name='Skip guide',exact=True).click()
    expect(page.locator('.management-attention')).to_have_count(0)
    page.get_by_test_id('metric-peer').click();page.get_by_role('button',name='Make a prediction',exact=True).click()
    field=page.get_by_label('What do you expect students to do?')
    field.fill('   ');field.press('Enter');expect(page.locator('.prediction-form')).to_be_visible()
    field.fill('New ideas');field.press('Shift+Enter');assert '\n' in field.input_value()
    assert field.evaluate("e=>e.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',isComposing:true,bubbles:true,cancelable:true}))")
    expect(page.locator('.prediction-form')).to_be_visible()
    record('Blank Enter cannot submit; Shift+Enter remains a newline and an IME-confirming Enter is not intercepted')
    field.fill('New ideas');expect(page.get_by_role('button',name='Run evaluation',exact=True)).to_be_enabled();field.press('Enter')
    expect(page.get_by_role('heading',name='Watch the score.')).to_be_visible()
    advance(page,8);pulse(page,hidden=True)
    record('Valid Enter runs the existing evaluation form; the original button remains, and the first real report pulses three times with hidden-page pause')
    page.get_by_role('button',name='Observe the class',exact=True).click()
    page.evaluate('''window.reviewTimes={};new MutationObserver(()=>{
      const mark=(name,selector)=>{if(document.querySelector(selector)&&window.reviewTimes[name]===undefined)window.reviewTimes[name]=performance.now()};
      mark('evidence','.observation-recap');mark('typing','.phase-review .maya-bubble.is-typing');
      mark('teacher','.phase-review .maya-bubble p');mark('alex','.phase-review .alex-bubble p');
      mark('last','.phase-review .alex-character[data-order="2"] p');mark('button','.level-finished');
    }).observe(document.body,{childList:true,subtree:true});''')
    finish_scene(page)
    for _ in range(220):
        if page.get_by_role('button',name='Continue to Level 2',exact=True).count():break
        page.clock.run_for(50);page.wait_for_timeout(5)
    expect(page.get_by_role('button',name='Continue to Level 2',exact=True)).to_be_visible()
    times=page.evaluate('window.reviewTimes')
    assert 1550<=times['typing']-times['evidence']<=2900,times
    assert 250<=times['teacher']-times['typing']<=400,times
    assert 1300<=times['alex']-times['teacher']<=2600,times
    assert 0<=times['button']-times['last']<100,times
    expect(page.locator('.alex-bubble p')).to_have_count(2)
    expect(page.locator('.management-attention')).to_have_count(0)
    page.get_by_role('button',name='Continue to Level 2',exact=True).click();advance(page)
    page.get_by_role('button',name='Choose three metrics',exact=True).click()
    expect(page.locator('.l2-previous')).to_contain_text('Peer response')
    record('Level 1 review uses Level 2 timing and releases Continue with the last Alex reply; immediate continuation retains the selected metric')
    for id in ['prep','part','focus']:page.get_by_test_id('level2-metric-'+id).click()
    page.get_by_role('button',name='Run evaluation',exact=True).click();advance(page,5);pulse(page)
    page.get_by_role('button',name='Observe the class',exact=True).click();finish_scene(page);advance(page,12)
    expect(page.locator('.management-attention')).to_have_count(0)
    page.get_by_role('button',name='Cover the gaps',exact=True).click()
    page.get_by_role('button',name='Add remaining metrics',exact=True).click();advance(page,5);pulse(page)
    record('Level 2 report changes also pulse three times, while remounting the same report for classroom observation does not flash again')
    context.close()

    context,page=start(browser,'full',motion='reduce')
    page.get_by_role('button',name='Skip guide',exact=True).click();page.get_by_test_id('metric-prep').click()
    page.get_by_role('button',name='Make a prediction',exact=True).click()
    page.get_by_label('What do you expect students to do?').fill('Understand the reading.')
    page.get_by_role('button',name='Run evaluation',exact=True).click();advance(page,8);pulse(page,reduced=True)
    record('Reduced motion keeps the update cue as one steady outline; clicking the retained submit button still evaluates')
    context.close()

    context,page=start(browser,'3');advance(page)
    page.get_by_role('button',name='Choose priorities',exact=True).click()
    for id in ['prep','part','focus']:page.get_by_test_id('level3-metric-'+id).click()
    page.get_by_role('button',name='Set the weights',exact=True).click()
    evaluate_three(page,[70,20]);page.get_by_role('button',name='Try another split',exact=True).click()
    evaluate_three(page,[80,10]);assert page.locator('.management-satisfaction-state').inner_text()=='Delighted'
    page.get_by_role('button',name='What if they counted equally?',exact=True).click()
    page.locator('.l3-publish').scroll_into_view_if_needed();advance(page,5)
    assert page.locator('.management-satisfaction-state').inner_text()=='Delighted';pulse(page)
    page.get_by_role('button',name='Observe the class',exact=True).click();finish_scene(page)
    page.locator('.l3-results').scroll_into_view_if_needed();advance(page,12)
    page.get_by_role('button',name='Compare the patterns',exact=True).click()
    expect(page.locator('.management-attention')).to_have_count(0)
    for width,size in [(1366,'12px'),(390,'11px'),(320,'11px')]:
        page.set_viewport_size({'width':width,'height':1000});advance(page,1)
        for selector in ['thead th[data-run] .eyebrow','thead th[data-run] small']:
            for item in page.locator(selector).all():expect(item).to_have_css('font-size',size)
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
        page.screenshot(path=str(OUT/f'interface-feedback-headers-{width}.png'),full_page=True,animations='disabled')
    record('All Level 3 publications pulse, including a new value with the same Delighted label; comparison/replay values do not add a cue')
    record('Enlarged trial/pattern headers fit the three-record comparison on desktop, 390px and 320px')
    context.close();browser.close()
assert not errors,errors
record('Focused interface checks have no runtime errors')
(OUT/'interface-feedback-results.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'reviewTimes':times,'runtimeErrors':errors},indent=2)+'\n')
