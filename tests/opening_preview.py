"""Exercise the uploaded partner opening from the actual self-contained review ZIP."""
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile
from playwright.sync_api import sync_playwright, expect

root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / 'play/OPENING_PREVIEW.json').read_text())
archive = root / 'play' / manifest['archive']
checks, errors, external_requests = [], [], []
out = root / 'test-results'
out.mkdir(exist_ok=True)

def record(text):
    checks.append(text)
    print('PASS', text, flush=True)

def advance(page, milliseconds):
    page.wait_for_timeout(milliseconds)

assert hashlib.sha256(archive.read_bytes()).hexdigest() == manifest['zipSha256']
with ZipFile(archive) as bundle:
    assert bundle.testzip() is None
    html = bundle.read(manifest['html'])
    assert hashlib.sha256(html).hexdigest() == manifest['htmlSha256']
    assert '解压后' in bundle.read('START-HERE.txt').decode()
record('The opening preview ZIP is intact and its self-contained HTML matches the recorded build hash')

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    context = browser.new_context(viewport={'width':1366, 'height':900}, reduced_motion='no-preference')
    context.set_offline(True)
    def route(request):
        if request.request.url == 'https://opening-preview.test/':
            request.fulfill(status=200, content_type='text/html', body=html)
        else:
            external_requests.append(request.request.url)
            request.abort()
    context.route('**/*', route)
    page = context.new_page()
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto('https://opening-preview.test/', wait_until='networkidle')
    stage = page.locator('.stage')
    expect(stage).to_have_attribute('data-beat','title')
    expect(page.get_by_role('button',name='START GAME',exact=True)).to_be_enabled()
    assert page.locator('.office-background').evaluate('e=>e.complete && e.naturalWidth>0')
    advance(page,4000)
    page.wait_for_function("Number(getComputedStyle(document.querySelector('.title-overlay')).opacity) > .95")
    page.screenshot(path=str(out/'opening-preview-title.png'))
    page.get_by_role('button',name='START GAME',exact=True).click()
    advance(page,2500)
    expect(stage).to_have_attribute('data-beat','identity')
    expect(page.get_by_role('button',name='TAKE YOUR SEAT',exact=True)).to_be_disabled()
    page.get_by_label('What name should we put on it?').fill('  Riley  ')
    page.get_by_label('What name should we put on it?').press('Enter')
    advance(page,8000)
    expect(stage).to_have_attribute('data-beat','notification')
    page.get_by_role('button',name='University Management').click()
    advance(page,5500)
    expect(stage).to_have_attribute('data-beat','ready')
    expect(page.locator('.salutation')).to_have_text('Dear Riley,')
    page.wait_for_function("Number(getComputedStyle(document.querySelector('.email')).opacity) > .95")
    page.screenshot(path=str(out/'opening-preview-email.png'))
    record('The normal-motion title, name entry with Enter and personalised office email run from the actual ZIP offline')
    page.get_by_role('button',name='VISIT CLASSROOM',exact=True).click()
    advance(page,10000)
    expect(stage).to_have_attribute('data-beat','classroom')
    world = page.locator('.classroom-world')
    expect(world).to_have_attribute('data-phase','explore')
    for student in ['phone','sleeping','unprepared']:
        page.locator('.hotspot-'+student).click()
        advance(page,1750)
        expect(world).to_have_attribute('data-phase','response')
        response = {'phone':'Just one more message...', 'sleeping':'Zzz...', 'unprepared':"I don't know where to start."}[student]
        expect(page.locator('.student-dialogue').filter(has_text=response)).to_be_visible()
        advance(page,5000)
        expect(page.locator('.hotspot-'+student)).to_have_attribute('data-inspected','true')
    advance(page,5000)
    expect(world).to_have_attribute('data-phase','exitCue')
    page.screenshot(path=str(out/'opening-preview-classroom.png'))
    record('All three original student interactions complete and unlock Return to Office only after all are inspected')
    page.get_by_role('button',name='RETURN TO OFFICE',exact=True).click()
    advance(page,5000)
    expect(stage).to_have_attribute('data-beat','officeEnd')
    expect(page.get_by_role('button',name='REPLAY OPENING',exact=True)).to_be_visible()
    page.screenshot(path=str(out/'opening-preview-end.png'))
    page.get_by_role('button',name='REPLAY OPENING',exact=True).click()
    advance(page,3000)
    expect(stage).to_have_attribute('data-beat','title')
    page.get_by_role('button',name='START GAME',exact=True).click()
    advance(page,2500)
    expect(page.get_by_label('What name should we put on it?')).to_have_value('')
    record('The original ending and Replay Opening work and replay clears the entered name')
    assert not errors, errors
    assert not external_requests, external_requests
    record('The standalone preview makes no external asset requests and has no browser runtime errors')
    context.close()
    browser.close()
(out/'opening-preview-results.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'runtimeErrors':errors,'externalRequests':external_requests},indent=2)+'\n')
