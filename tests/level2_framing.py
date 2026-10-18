"""Production checks for the earlier-level fixes and the six-metric hypothesis.
Exercises the unchanged continuous growth with explicit visible-time accounting.
"""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

OUT=Path('test-results');OUT.mkdir(exist_ok=True)
HTML={'2':Path('dist-level2/index.html').read_bytes(),'full':Path('dist/index.html').read_bytes()}
checks,errors,timings=[],[],{}
def record(text):checks.append(text);print('PASS',text,flush=True)
def advance(page,ms=8000):
    for _ in range(ms//100):page.clock.run_for(100);page.wait_for_timeout(3)
def until(page,condition,limit=20000):
    for _ in range(limit//100):
        if condition():return
        advance(page,100)
    assert condition(),'Expected visible-time state did not arrive'
def start(browser,mode='2',motion='no-preference',width=1366):
    context=browser.new_context(viewport={'width':width,'height':1000 if width>520 else 844},reduced_motion=motion)
    context.set_offline(True)
    context.route('https://earlier-levels.test/**',lambda route:route.fulfill(status=200,content_type='text/html',body=HTML[mode]))
    page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.clock.install()
    page.goto('https://earlier-levels.test/',wait_until='networkidle')
    return context,page
def return_scene(page):
    while page.get_by_role('button',name='Continue scene',exact=True).count():page.get_by_role('button',name='Continue scene',exact=True).click()
    page.get_by_role('button',name='Return to dashboard',exact=True).click()
def conversation(page):
    page.locator('.l2-observation-slot').scroll_into_view_if_needed();advance(page,6000)
    page.locator('.conversation').scroll_into_view_if_needed();advance(page,9000)
def reach_six(page,ids):
    advance(page,4000);page.get_by_role('button',name='Choose three metrics',exact=True).click()
    for id in ids:page.get_by_test_id('level2-metric-'+id).click()
    page.get_by_role('button',name='Run evaluation',exact=True).click();advance(page,6000)
    expect(page.get_by_role('heading',name='Would more metrics help Alex learn?',exact=True)).to_have_count(0)
    page.get_by_role('button',name='Observe the class',exact=True).click();return_scene(page);conversation(page)
    expect(page.get_by_role('button',name='Test more metrics',exact=True)).to_have_count(0)
    page.get_by_role('button',name='Cover the gaps',exact=True).click()
    missing=page.locator('.l2-missing li').all_text_contents();assert len(missing)==3
    page.get_by_role('button',name='Add remaining metrics',exact=True).click();advance(page,6000)
    expect(page.locator('.l2-evaluation-list [data-checked=true]')).to_have_count(6)
    page.get_by_role('button',name='Observe the class',exact=True).click();return_scene(page)
    # The hypothesis is page content, already present before the review dialogue.
    expect(page.get_by_role('heading',name='Would more metrics help Alex learn?',exact=True)).to_be_visible()
    expect(page.locator('.l2-growth-proposal')).to_have_text('6?')
    conversation(page)
    expect(page.get_by_role('button',name='Test more metrics',exact=True)).to_be_enabled()
def hide(page,value):
    page.evaluate("Object.defineProperty(document,'hidden',{configurable:true,value:true});document.dispatchEvent(new Event('visibilitychange'))" if value else "delete document.hidden;document.dispatchEvent(new Event('visibilitychange'))")
def begin_growth(page):
    page.get_by_role('button',name='Test more metrics',exact=True).click()
    until(page,lambda:page.locator('.l2-growth-action[data-growth="10"][data-beat="3"]').count()>0)
    page.locator('.l2-checklist').scroll_into_view_if_needed()

with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    context,page=start(browser,'full')
    page.get_by_role('button',name='Skip guide',exact=True).click()
    expect(page.get_by_role('heading',name='One metric.',exact=True)).to_be_visible()
    assert page.locator('.workbench-heading').bounding_box()['height']<100
    expect(page.locator('.phase-choose .action-row')).to_have_text('Make a prediction')
    page.get_by_test_id('metric-peer').click();page.get_by_role('button',name='Make a prediction',exact=True).click()
    field=page.get_by_label('What do you expect students to do?')
    field.fill('   ');field.press('Enter');expect(page.locator('.prediction-form')).to_be_visible()
    field.fill('New ideas');field.press('Shift+Enter');assert '\n' in field.input_value()
    field.evaluate("e=>e.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',isComposing:true,bubbles:true,cancelable:true}))")
    expect(page.locator('.prediction-form')).to_be_visible()
    field.fill('New ideas');expect(page.get_by_role('button',name='Run evaluation',exact=True)).to_be_enabled();field.press('Enter')
    expect(page.get_by_role('heading',name='Watch the score.',exact=True)).to_be_visible();advance(page,8000)
    notice=page.locator('.management-attention');expect(notice).to_have_count(1)
    assert notice.evaluate('e=>getComputedStyle(e).animationIterationCount')=='3'
    record('Level 1 retains a compact title, clean action footer, Enter submission, Shift+Enter and IME protection, the original button and three report-update pulses')
    page.get_by_role('button',name='Observe the class',exact=True).click()
    page.evaluate('''window.reviewTimes={};new MutationObserver(()=>{
      const mark=(name,selector)=>{if(document.querySelector(selector)&&window.reviewTimes[name]===undefined)window.reviewTimes[name]=performance.now()};
      mark('evidence','.observation-recap');mark('typing','.phase-review .maya-bubble.is-typing');mark('teacher','.phase-review .maya-bubble p');
      mark('alex','.phase-review .alex-bubble p');mark('last','.phase-review .alex-character[data-order="2"] p');mark('button','.level-finished');
    }).observe(document.body,{childList:true,subtree:true});''')
    return_scene(page)
    until(page,lambda:page.get_by_role('button',name='Continue to Level 2',exact=True).count()>0)
    t=page.evaluate('reviewTimes');timings['level1Review']=t
    assert 1550<=t['typing']-t['evidence']<=2900,t
    assert 250<=t['teacher']-t['typing']<=450,t
    assert 1300<=t['alex']-t['teacher']<=2700,t
    assert 0<=t['button']-t['last']<150,t
    expect(page.locator('.alex-bubble p')).to_have_count(2)
    page.get_by_role('button',name='Continue to Level 2',exact=True).click()
    expect(page.locator('.level-two')).to_have_attribute('data-phase','intro')
    expect(page.locator('.chapter-consequence')).to_contain_text('Replying to tick boxes.')
    record('Level 1 ending uses the existing brisk Level 2 pace, releases Continue with the second Alex reply and carries the actual unresolved behaviour into Level 2')
    context.close()

    context,page=start(browser)
    reach_six(page,['prep','part','focus'])
    for width in [1366,768,390,320]:
        page.set_viewport_size({'width':width,'height':1000 if width>520 else 844})
        page.locator('.l2-growth-question').scroll_into_view_if_needed()
        expect(page.get_by_role('heading',name='Would more metrics help Alex learn?',exact=True)).to_be_visible()
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
        page.screenshot(path=f'test-results/level2-question-{width}.png',full_page=True)
    expect(page.get_by_role('button',name='Restart',exact=True)).to_have_count(0)
    expect(page.get_by_role('button',name='Guide',exact=True)).to_have_count(0)
    advance(page,20000);expect(page.locator('.level-two')).to_have_attribute('data-round','6')
    expect(page.locator('.l2-growth-sequence')).to_have_count(0)
    record('After six are observed, a visible non-dialogue question and six-to-question-mark diagram frame the next experiment; it fits 1366/768/390/320px and waits for the player')
    page.set_viewport_size({'width':1366,'height':1000})
    page.evaluate('''window.growthTimeline=[];const capture=()=>{
      const root=document.querySelector('.level-two'),seq=document.querySelector('.l2-growth-sequence'),action=document.querySelector('.l2-growth-action');
      const state=`${root.dataset.round}:${seq?.dataset.state}:${action?.dataset.beat}`;
      if(window.growthTimeline.at(-1)?.state!==state)window.growthTimeline.push({state,t:performance.now()});
    };new MutationObserver(capture).observe(document.body,{childList:true,subtree:true,attributes:true});capture();''')
    begin_growth(page)
    expect(page.get_by_role('heading',name='Testing more metrics.',exact=True)).to_be_visible()
    page.evaluate('window.growthNodes=[document.querySelector(".l2-counter"),document.querySelector(".l2-matrix"),document.querySelector(".l2-checklist")]')
    until(page,lambda:page.locator('.l2-growth-sequence').get_attribute('data-state')=='leaving',6000)
    expect(page.locator('.l2-growth-beats [data-next=true]')).to_have_text('25')
    hide(page,True);advance(page,8000)
    expect(page.locator('.level-two')).to_have_attribute('data-round','10')
    expect(page.locator('.l2-growth-sequence')).to_have_attribute('data-state','leaving')
    assert page.locator('.l2-growth-action').evaluate('e=>getComputedStyle(e).animationPlayState')=='paused'
    hide(page,False)
    until(page,lambda:page.locator('.l2-growth-action[data-growth="25"][data-beat="3"]').count()>0)
    before=page.evaluate('({y:scrollY,h:document.querySelector(".l2-checklist").getBoundingClientRect().height})')
    assert page.evaluate('growthNodes.every(e=>e.isConnected)')
    until(page,lambda:page.locator('.l2-growth-sequence').get_attribute('data-state')=='leaving',6000)
    expect(page.locator('.l2-growth-beats [data-next=true]')).to_have_text('100')
    until(page,lambda:page.locator('.level-two').get_attribute('data-round')=='100',2000)
    after=page.evaluate('({y:scrollY,h:document.querySelector(".l2-checklist").getBoundingClientRect().height})')
    assert abs(before['y']-after['y'])<=1,(before,after)
    assert abs(before['h']-after['h'])<=1,(before,after)
    assert page.evaluate('growthNodes.every(e=>e.isConnected)')
    events=page.evaluate('growthTimeline')
    done=next(e for e in events if e['state']=='25:shown:3');leave=next(e for e in events if e['state']=='25:leaving:3')
    end=next(e for e in events if e['t']>leave['t'] and e['state'].startswith('100:'))
    hold,turn=leave['t']-done['t'],end['t']-leave['t']
    assert 3400<=hold<=4000,hold
    assert 650<=turn<=1100,turn
    timings['growth']={'holdMs':hold,'turnMs':turn,'before':before,'after':after}
    until(page,lambda:page.get_by_role('button',name='Observe the class',exact=True).count()>0)
    expect(page.locator('.l2-matrix [data-active=true]')).to_have_count(100)
    advance(page,9000);expect(page.locator('.level-two')).to_have_attribute('data-phase','observe')
    expect(page.locator('.level-two')).to_have_attribute('data-round','100')
    record('One Test more metrics action runs the same mounted 10→25→100 experiment; visible 3.5s holds, anticipated 0.7s turns, hidden-page pauses, stable scroll/height and final manual Observe remain intact')
    page.get_by_role('button',name='Observe the class',exact=True).click();return_scene(page);conversation(page)
    expect(page.get_by_role('heading',name='More metrics. Still chasing marks.',exact=True)).to_be_visible()
    expect(page.locator('.l2-observation')).to_contain_text('quickest way')
    expect(page.locator('.student-behaviour')).to_have_text('Doing the minimum becomes the strategy.')
    expect(page.get_by_role('button',name='Continue to Level 3',exact=True)).to_be_disabled()
    page.screenshot(path='test-results/level2-framing-result-1366.png',full_page=True)
    record('The hundred-item result answers the experiment with score-chasing evidence, preserves both perspectives and leaves the standalone Level 3 action reserved')
    context.close()

    for ids in [['discuss','reflect','peer'],['prep','reflect','peer']]:
        context,page=start(browser,motion='reduce',width=320)
        reach_six(page,ids)
        expect(page.locator('.alex-bubble p')).to_have_count(2)
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
        record('The '+('/'.join(ids))+' route reaches the same evidence-based six-metric question after its own trio observation')
        if ids[0]=='prep':
            begin_growth(page);geometry=[]
            for count in [10,25,100]:
                until(page,lambda:page.locator(f'.l2-growth-action[data-growth="{count}"][data-beat="3"]').count()>0)
                assert page.locator('.l2-growth-action').evaluate('e=>getComputedStyle(e).animationName')=='none'
                geometry.append(page.evaluate('({y:scrollY,h:document.querySelector(".l2-checklist").getBoundingClientRect().height})'))
            assert max(g['y'] for g in geometry)-min(g['y'] for g in geometry)<=8,geometry
            assert max(g['h'] for g in geometry)-min(g['h'] for g in geometry)<=1,geometry
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
            timings['phone']=geometry
            record('The reduced-motion 320px route keeps all three growth states readable with stable paper height and reading position')
        context.close()
    browser.close()
assert not errors,errors
record('No browser runtime errors in earlier-level controls, hypothesis framing, continuous growth or outcome feedback')
(OUT/'level2-framing-results.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'timings':timings,'runtimeErrors':errors},indent=2)+'\n')
