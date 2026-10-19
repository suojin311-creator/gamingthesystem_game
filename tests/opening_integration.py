"""Normal-speed visual cues, inspection gating and real opening → Gameplay handoff.

Requires the main Vite entry on 5173. --packaged uses the actual full-game ZIP.
"""
import json
import sys
import time
from pathlib import Path
from zipfile import ZipFile
from playwright.sync_api import sync_playwright, expect

out = Path('test-results')
out.mkdir(exist_ok=True)
checks, errors, external = [], [], []
packaged = '--packaged' in sys.argv
html = None
if packaged:
    with ZipFile('play/Full-game-play.zip') as archive:
        html = archive.read('Gaming-the-System.html')

def record(text):
    checks.append(text)
    print('PASS', text, flush=True)

def start(browser, width=1366, *, motion='no-preference', touch=False):
    context = browser.new_context(viewport={'width':width,'height':900}, reduced_motion=motion, has_touch=touch)
    if packaged:
        context.set_offline(True)
        def serve(route):
            if route.request.url == 'https://opening-integrated.test/':
                route.fulfill(status=200, content_type='text/html', body=html)
            else:
                external.append(route.request.url)
                route.abort()
        context.route('**/*', serve)
    page = context.new_page()
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto('https://opening-integrated.test/' if packaged else 'http://127.0.0.1:5173/', wait_until='networkidle')
    return context,page

def enter_classroom(page, name, *, touch=False):
    page.get_by_role('button',name='START GAME',exact=True).click()
    expect(page.locator('.stage')).to_have_attribute('data-beat','identity')
    page.get_by_label('What name should we put on it?').fill(name)
    page.get_by_label('What name should we put on it?').press('Enter')
    mail=page.get_by_role('button',name='Open urgent email from University Management',exact=True)
    expect(mail).to_be_visible(timeout=6000)
    expect(mail.locator('.opening-email-cue')).to_be_visible()
    if touch: mail.tap()
    else: mail.click()
    expect(page.locator('.salutation')).to_have_text('Dear '+name.strip()+',')
    visit=page.get_by_role('button',name='VISIT CLASSROOM',exact=True)
    expect(visit).to_be_enabled(timeout=4000)
    visit.click()
    world=page.locator('.classroom-world')
    expect(world).to_have_attribute('data-phase','explore',timeout=5000)
    return world

with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    context,page=start(browser)
    world=enter_classroom(page,'  Chen Li  ')
    markers=page.locator('.opening-student-marker .opening-interaction-cue[data-complete=false]')
    expect(markers).to_have_count(3)
    for marker in markers.all(): expect(marker).to_be_visible()
    expect(page.get_by_role('img',name='Observe all three students: 0 of 3 complete')).to_be_visible()
    look=page.locator('.classroom-look')
    expect(look).to_be_visible()
    assert look.evaluate('e=>parseFloat(getComputedStyle(e).fontSize)') >= 22
    expect(page.get_by_role('button',name='RETURN TO OFFICE')).to_have_count(0)
    page.screenshot(path=str(out/'opening-integrated-students-1366.png'))
    record('Email and all three unseen students have visible non-text arrow cues; Look around is larger and all three completion slots are visible')
    durations=[]
    for index,student in enumerate(['phone','unprepared','sleeping']):
        before=time.monotonic()
        page.locator('.hotspot-'+student).click()
        expect(world).to_have_attribute('data-phase','response',timeout=1000)
        text={'phone':'Just one more message...','unprepared':"I don't know where to start.",'sleeping':'Zzz...'}[student]
        expect(page.locator('.student-dialogue').filter(has_text=text)).to_be_visible()
        expect(page.locator('.student-hotspot:enabled')).to_have_count(0)
        if index<2:
            expect(world).to_have_attribute('data-phase','explore',timeout=3000)
            durations.append(time.monotonic()-before)
            expect(markers).to_have_count(2-index)
            for marker in markers.all():expect(marker).to_be_visible()
            expect(page.locator('.opening-student-marker .opening-interaction-cue[data-complete=true]')).to_have_count(index+1)
            expect(page.get_by_role('button',name='RETURN TO OFFICE')).to_have_count(0)
        else:
            expect(world).to_have_attribute('data-phase','exitCue',timeout=5000)
    assert all(2.1 <= duration < 3.3 for duration in durations),durations
    expect(page.get_by_role('img',name='Observe all three students: 3 of 3 complete')).to_be_visible()
    expect(page.locator('.opening-observation-progress > span[data-complete=true]')).to_have_count(3)
    record('Inspections take about 2.4 seconds, lock overlapping input, and replace only observed students’ arrows with checks; all three are required')
    page.get_by_role('button',name='RETURN TO OFFICE').press('Enter')
    expect(page.locator('.stage')).to_have_attribute('data-beat','officeEnd',timeout=3000)
    expect(page.locator('.level-one')).to_have_count(0)
    expect(page.locator('.opening-handoff')).to_contain_text('LEVEL 01')
    expect(page.locator('.opening-handoff h1')).to_have_text('One metric.')
    page.screenshot(path=str(out/'opening-integrated-handoff.png'))
    page.get_by_role('button',name='Choose a metric',exact=True).click()
    expect(page.locator('.opening-scene')).to_have_count(0)
    expect(page.get_by_role('dialog',name='Workbench guide')).to_be_visible()
    page.get_by_role('button',name='Skip guide',exact=True).click()
    expect(page.locator('.maya-bubble .speaker-name')).to_have_text('Chen Li')
    expect(page.locator('.maya-avatar svg')).to_have_attribute('data-character','teacher')
    page.get_by_test_id('metric-prep').click()
    button=page.get_by_role('button',name='Make a prediction',exact=True)
    assert button.evaluate('e=>getComputedStyle(e).backgroundColor')=='rgb(173, 88, 64)'
    record('The office handoff names Level 1, enters real Gameplay once with the trimmed name and role portrait, and preserves the game’s coral button style')
    page.get_by_role('button',name='Sound on',exact=True).click()
    page.evaluate("window.dispatchEvent(new PageTransitionEvent('pageshow',{persisted:true}))")
    expect(page.locator('.stage')).to_have_attribute('data-beat','title')
    expect(page.locator('.level-one')).to_have_count(0)
    page.get_by_role('button',name='START GAME',exact=True).click()
    expect(page.get_by_label('What name should we put on it?')).to_have_value('')
    record('Restoring a closed combined page resets to the opening and clears the prior player identity')
    context.close()
    context,page=start(browser,390,motion='reduce',touch=True)
    world=enter_classroom(page,'Ari',touch=True)
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    expect(page.locator('.opening-student-marker .opening-interaction-cue[data-complete=false]')).to_have_count(3)
    assert page.locator('.opening-interaction-cue svg').last.evaluate('e=>getComputedStyle(e).animationName')=='none'
    for marker in page.locator('.opening-student-marker').all():
        box=marker.bounding_box()
        assert box and box['x']>=0 and box['x']+box['width']<=390
    page.screenshot(path=str(out/'opening-integrated-students-390.png'))
    page.locator('.hotspot-sleeping').tap()
    expect(world).to_have_attribute('data-phase','explore',timeout=3000)
    expect(page.locator('.opening-student-marker .opening-interaction-cue[data-complete=false]')).to_have_count(2)
    expect(page.get_by_role('button',name='RETURN TO OFFICE')).to_have_count(0)
    record('Touch inspection, static reduced-motion cues and enlarged guidance work at 390px without overflow or early progression')
    context.close();browser.close()
assert not errors,errors
assert not external,external
record('Opening integration has no browser runtime errors'+(' or external asset requests in the actual offline ZIP' if packaged else ''))
name='opening-integrated-package-results.json' if packaged else 'opening-integration-results.json'
(out/name).write_text(json.dumps({'passed':len(checks),'checks':checks,'runtimeErrors':errors,'externalRequests':external,'normalInspectionSeconds':durations},indent=2)+'\n')
