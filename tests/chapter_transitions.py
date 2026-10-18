"""Chapter pacing, unresolved recap, explicit entry, audio and responsive layout.
Uses the exact production HTML offline; partner/name handoff is covered separately.
"""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

OUT = Path('test-results'); OUT.mkdir(exist_ok=True)
HTML = {key: Path(path).read_bytes() for key, path in [('full','dist/index.html'),('2','dist-level2/index.html'),('3','dist-level3/index.html')]}
checks, errors, timings = [], [], {}
def record(text): checks.append(text); print('PASS', text, flush=True)
def advance(page, ms):
    for _ in range(ms // 100): page.clock.run_for(100); page.wait_for_timeout(8)
def start(browser, mode='2', motion='no-preference', width=1366, script=None):
    context = browser.new_context(viewport={'width':width,'height':900 if width>520 else 844}, reduced_motion=motion)
    context.set_offline(True)
    context.route('https://chapter.test/**', lambda route: route.fulfill(status=200, content_type='text/html', body=HTML[mode]))
    context.add_init_script("""window.chapterTimes={};new MutationObserver(()=>{const beat=document.querySelector('.chapter-transition')?.dataset.beat;if(beat){if(window.chapterTimes.start===undefined)window.chapterTimes.start=performance.now();if(window.chapterTimes[beat]===undefined)window.chapterTimes[beat]=performance.now()}}).observe(document,{childList:true,subtree:true,attributes:true,attributeFilter:['data-beat']});""")
    if script: context.add_init_script(script)
    page=context.new_page(); page.on('pageerror',lambda error: errors.append(str(error))); page.clock.install()
    page.goto('https://chapter.test/',wait_until='networkidle'); return context,page

def finish_scene(page):
    for _ in range(2): page.get_by_role('button',name='Continue scene',exact=True).click()
    page.get_by_role('button',name='Return to dashboard',exact=True).click()

AUDIO = '''window.chapterAudio={contexts:0,notes:[],paper:0,stoppedPaper:0};
const NativeAudio=window.AudioContext;window.AudioContext=class extends NativeAudio{constructor(...args){super(...args);window.chapterAudio.contexts++}};
const oldOsc=NativeAudio.prototype.createOscillator, oldBuffer=NativeAudio.prototype.createBufferSource;
NativeAudio.prototype.createOscillator=function(){const o=oldOsc.call(this),start=o.start.bind(o),set=o.frequency.setValueAtTime.bind(o.frequency);let frequency=0;
o.frequency.setValueAtTime=(value,...args)=>{frequency=value;return set(value,...args)};o.start=(...args)=>{window.chapterAudio.notes.push(frequency);return start(...args)};return o};
NativeAudio.prototype.createBufferSource=function(){const o=oldBuffer.call(this),start=o.start.bind(o),stop=o.stop.bind(o);o.start=(...args)=>{window.chapterAudio.paper++;return start(...args)};o.stop=(...args)=>{window.chapterAudio.stoppedPaper++;return stop(...args)};return o};'''

with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    context,page=start(browser)
    root=page.locator('.chapter-transition'); expect(root).to_have_attribute('data-beat','hold')
    expect(page.locator('.chapter-single')).to_be_visible()
    expect(page.get_by_role('heading',name='More metrics.',exact=True)).to_have_count(0)
    advance(page,1100); expect(root).to_have_attribute('data-beat','turn')
    expect(page.get_by_role('group',name='Three empty metric slots')).to_be_visible()
    assert page.locator('.chapter-new-card[data-metric]').count()==0
    advance(page,1000); expect(root).to_have_attribute('data-beat','chapter')
    expect(page.get_by_role('heading',name='More metrics.',exact=True)).to_be_visible()
    expect(page.locator('.chapter-actions button')).to_have_count(0)
    advance(page,1200); expect(root).to_have_attribute('data-beat','ready')
    t=page.evaluate('window.chapterTimes'); timings['standalone2']=t
    assert 800<=t['turn']-t['start']<=1150,t
    assert 950<=t['chapter']-t['turn']<=1250,t
    assert 1050<=t['ready']-t['chapter']<=1400,t
    expect(page.locator('.chapter-bridge .maya-bubble p')).to_have_count(1)
    expect(page.locator('.alex-bubble')).to_have_count(0)
    expect(page.locator('.l2-heading,.l2-stepper')).to_have_count(0)
    advance(page,20000); expect(page.locator('.level-two')).to_have_attribute('data-phase','intro')
    page.get_by_role('button',name='Choose three metrics',exact=True).click()
    expect(page.locator('.l2-heading,.l2-stepper')).to_have_count(2)
    expect(page.locator('.l2-metric-card[aria-pressed=true]')).to_have_count(0)
    record('Three visible beats take about three seconds; a prominent chapter replaces the old intro, shortens dialogue and waits for explicit entry into three empty slots')
    context.close()

    context,page=start(browser,'3'); advance(page,3500)
    expect(page.get_by_role('heading',name='The weighting trap.',exact=True)).to_be_visible()
    expect(page.locator('.chapter-new-card')).to_have_count(3)
    assert page.locator('.chapter-new-card[data-metric]').count()==0
    assert page.locator('.chapter-transition input').count()==0
    page.get_by_role('button',name='Choose priorities',exact=True).click()
    expect(page.locator('.l3-metric-card[aria-pressed=true]')).to_have_count(0)
    record('Standalone Level 3 shows unassigned priority cards and starts empty; chapter slider artwork cannot change any weights')
    context.close()

    context,page=start(browser)
    page.evaluate("Object.defineProperty(document,'hidden',{configurable:true,value:true});document.dispatchEvent(new Event('visibilitychange'))")
    advance(page,8000); expect(page.locator('.chapter-transition')).to_have_attribute('data-beat','hold')
    page.evaluate("delete document.hidden;document.dispatchEvent(new Event('visibilitychange'))")
    advance(page,1100); expect(page.locator('.chapter-transition')).to_have_attribute('data-beat','turn')
    page.evaluate("Object.defineProperty(document,'hidden',{configurable:true,value:true});document.dispatchEvent(new Event('visibilitychange'))")
    expect(page.locator('.chapter-new-card').first).to_have_css('animation-play-state','paused')
    before=page.locator('.chapter-new-card').first.evaluate('e=>e.getAnimations()[0].currentTime')
    page.wait_for_timeout(120)
    after=page.locator('.chapter-new-card').first.evaluate('e=>e.getAnimations()[0].currentTime')
    assert abs(after-before)<25,(before,after)
    advance(page,8000); expect(page.locator('.chapter-transition')).to_have_attribute('data-beat','turn')
    page.evaluate("delete document.hidden;document.dispatchEvent(new Event('visibilitychange'))")
    advance(page,2500); expect(page.locator('.chapter-transition')).to_have_attribute('data-beat','ready')
    record('Hidden tabs pause both the visible-time beats and the card animations, then resume without skipping the chapter')
    context.close()

    context,page=start(browser)
    page.locator('.chapter-transition').evaluate("e=>e.style.marginTop='2200px'")
    page.wait_for_timeout(100); advance(page,8000)
    expect(page.locator('.chapter-transition')).to_have_attribute('data-beat','hold')
    page.locator('.chapter-transition').evaluate("e=>e.style.marginTop=''")
    page.locator('.chapter-transition').scroll_into_view_if_needed(); advance(page,3500)
    expect(page.locator('.chapter-transition')).to_have_attribute('data-beat','ready')
    record('A chapter moved off screen holds its pending information until it becomes visible again')
    context.close()

    context,page=start(browser,'3',motion='reduce'); advance(page,3500)
    for selector in ['.chapter-heading','.chapter-new-card','.chapter-outgoing','.chapter-entry']:
        expect(page.locator(selector).first).to_have_css('animation-name','none')
    page.get_by_role('button',name='Choose priorities',exact=True).focus(); page.keyboard.press('Enter')
    expect(page.locator('.level-three')).to_have_attribute('data-phase','choose')
    record('Reduced motion removes movement while retaining the chapter sequence; keyboard entry works')
    context.close()

    context,page=start(browser,script="Object.defineProperty(window,'AudioContext',{value:undefined})")
    advance(page,3500); expect(page.get_by_role('button',name='No audio',exact=True)).to_be_disabled()
    page.get_by_role('button',name='Choose three metrics',exact=True).click()
    expect(page.locator('.level-two')).to_have_attribute('data-phase','choose')
    record('No AudioContext or autoplay permission is needed to see the full transition and enter the next chapter')
    context.close()

    context,page=start(browser,'full',script=AUDIO)
    page.get_by_role('button',name='Skip guide',exact=True).click()
    page.get_by_test_id('metric-peer').click(); page.get_by_role('button',name='Make a prediction',exact=True).click()
    page.get_by_label('What do you expect students to do?').fill('New ideas.')
    page.get_by_role('button',name='Run evaluation',exact=True).click(); advance(page,8000)
    page.get_by_role('button',name='Observe the class',exact=True).click(); finish_scene(page); advance(page,11000)
    before=page.evaluate('structuredClone(window.chapterAudio)')
    assert before['contexts']==1,before
    page.get_by_role('button',name='Continue to Level 2',exact=True).click()
    expect(page.locator('.chapter-single')).to_contain_text('Peer response')
    expect(page.locator('.chapter-consequence')).to_have_text('Replying to tick boxes.')
    advance(page,3500)
    after=page.evaluate('structuredClone(window.chapterAudio)')
    assert after['contexts']==1,after
    assert after['paper']-before['paper']==1,(before,after)
    assert after['notes'][len(before['notes']):]==[196,174.61],(before,after)
    advance(page,20000)
    assert page.evaluate('window.chapterAudio')==after
    page.get_by_role('button',name='Choose three metrics',exact=True).click()
    expect(page.locator('.l2-metric-card[aria-pressed=true]')).to_have_count(0)
    record('Real Level 1 handoff carries its chosen card and actual negative observation; one rustle and a low descending tone reuse the unlocked audio context without reward sounds or looping')
    context.close()

    context,page=start(browser,script=AUDIO)
    page.get_by_role('button',name='Sound on',exact=True).click()
    advance(page,3500)
    assert page.evaluate('window.chapterAudio.notes')==[]
    assert page.evaluate('window.chapterAudio.paper')==0
    expect(page.locator('.chapter-transition')).to_have_attribute('data-beat','ready')
    record('Sound off suppresses both chapter cues while the complete visual sequence and entry button still appear')
    context.close()

    context,page=start(browser,script=AUDIO)
    page.get_by_role('button',name='Sound on',exact=True).click()
    page.get_by_role('button',name='Sound off',exact=True).click()
    advance(page,1000)
    assert page.evaluate('window.chapterAudio.paper')==1
    page.get_by_role('button',name='Sound on',exact=True).click()
    assert page.evaluate('window.chapterAudio.stoppedPaper')==1
    advance(page,3000)
    assert page.evaluate('window.chapterAudio.notes')==[]
    record('Muting during the paper movement stops its active sound immediately and suppresses the later chapter tone')
    context.close()

    for mode in ['2','3']:
        for width in [1366,768,390,320]:
            context,page=start(browser,mode,width=width); advance(page,3500); page.wait_for_timeout(500)
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(mode,width)
            cards=page.locator('.chapter-new-card').evaluate_all('es=>es.map(e=>({left:e.getBoundingClientRect().left,right:e.getBoundingClientRect().right}))')
            assert all(card['left']>=0 and card['right']<=width for card in cards),(mode,width,cards)
            page.locator('.chapter-actions button').scroll_into_view_if_needed()
            expect(page.locator('.chapter-actions button')).to_be_in_viewport()
            if width in [1366,320]: page.screenshot(path=f'test-results/chapter-production-{mode}-{width}.png',full_page=True)
            context.close()
        record(f'Level {mode} chapter and three cards fit 1366/768/390/320px, with a reachable entry button')
    browser.close()
assert not errors, errors
record('No runtime errors in normal/reduced motion, audio fallback, hidden-page and offline chapter checks')
(OUT/'chapter-transition-results.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'timings':timings,'runtimeErrors':errors},indent=2)+'\n')
