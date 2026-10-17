"""Real browser checks for automatic recaps, pause/resume, chat timing and audio."""
import argparse
import json
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

parser = argparse.ArgumentParser()
parser.add_argument('--file')
parser.add_argument('--url', default='http://127.0.0.1:5173/')
args = parser.parse_args()
artifact = Path(args.file).resolve().read_bytes() if args.file else None
url = 'https://level-one.test/' if args.file else args.url
out = Path(__file__).resolve().parents[1] / 'test-results'
checks = []
errors = []
audio_probe = '''
window.audioStarts = [];
window.feedbackMasterGains = [];
const originalConnect = AudioNode.prototype.connect;
AudioNode.prototype.connect = function(destination, ...args) {
  if (this instanceof GainNode && destination instanceof AudioDestinationNode) window.feedbackMasterGains.push(this.gain.value);
  return originalConnect.call(this, destination, ...args);
};
window.scheduledAudioValues = new WeakMap();
const originalSetValue = AudioParam.prototype.setValueAtTime;
AudioParam.prototype.setValueAtTime = function(value, ...args) {
  window.scheduledAudioValues.set(this, value);
  return originalSetValue.call(this, value, ...args);
};
const originalStart = OscillatorNode.prototype.start;
OscillatorNode.prototype.start = function(...args) {
  window.audioStarts.push({frequency: window.scheduledAudioValues.get(this.frequency) ?? this.frequency.value, state: this.context.state});
  return originalStart.apply(this, args);
};
'''

def record(name):
    checks.append(name)
    print('PASS', name, flush=True)

def make_context(browser, **kwargs):
    context = browser.new_context(**kwargs)
    if artifact:
        context.set_offline(True)
        context.route('https://level-one.test/**', lambda r: r.fulfill(status=200, content_type='text/html', body=artifact))
    return context

def scene_to_review(page):
    page.get_by_role('button', name='Observe the class').click()
    finish_scene(page)

def finish_scene(page):
    page.get_by_role('button', name='Continue scene').click()
    page.get_by_role('button', name='Continue scene').click()
    page.get_by_role('button', name='Return to dashboard').click()

def settle(page):
    expect(page.get_by_role('button', name='Try more metrics')).to_be_enabled(timeout=16000)

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--no-sandbox'])
    context = make_context(browser, viewport={'width': 1366, 'height': 768})
    context.add_init_script(audio_probe)
    page = context.new_page()
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(url, wait_until='networkidle')
    page.get_by_role('button', name='Skip guide').click()
    page.get_by_test_id('metric-prep').click()
    page.get_by_role('button', name='Make a prediction').click()
    expect(page.get_by_role('status', name='Maya is typing')).to_be_visible()
    page.get_by_label('What do you expect students to do?').fill('Students will understand the reading.')
    page.get_by_role('button', name='Run evaluation').click()
    expect(page.get_by_role('button', name='Observe the class')).to_be_disabled()
    expect(page.locator('.after-score')).to_contain_text('88')
    page.get_by_role('button', name='Pause updates').click()
    expect(page.locator('.university-value')).to_have_count(0)
    page.wait_for_timeout(1200)
    expect(page.locator('.university-value')).to_have_count(0)
    page.get_by_role('button', name='Resume updates').click()
    expect(page.get_by_role('button', name='Observe the class')).to_be_enabled(timeout=5000)
    record('Score animates, then university updates automatically; Pause holds the next beat')

    expect(page.locator('.university')).to_have_attribute('data-updated', 'true')
    expect(page.locator('.university-value')).to_contain_text('88')
    assert page.evaluate('window.audioStarts.some(n => Math.abs(n.frequency - 523.25) < 0.1 && n.state === "running")')
    assert page.evaluate('window.audioStarts.some(n => n.frequency === 420)')
    assert page.evaluate('window.feedbackMasterGains.some(gain => gain > 0.12 && gain < 0.14)')
    page.screenshot(path=str(out / 'feedback-report.png'), full_page=True)
    record('Actual Web Audio plays count and success cues at the increased master gain')

    scene_to_review(page)
    expect(page.locator('.observation-recap')).to_have_count(0)
    expect(page.locator('.student')).to_contain_text('Not observed yet')
    expect(page.locator('.observation-recap')).to_contain_text('The checklist is complete.', timeout=5000)
    expect(page.locator('.student')).to_contain_text('Not observed yet')
    expect(page.locator('.uncertainty')).to_have_text('Unclear', timeout=5000)
    expect(page.locator('.student')).to_have_attribute('data-updated', 'true')
    assert page.get_by_role('button', name='Reveal observation').count() == 0
    assert page.get_by_role('button', name='See student response').count() == 0
    assert page.evaluate('window.audioStarts.some(n => n.frequency === 360) && window.audioStarts.some(n => n.frequency === 392)')
    record('Scene completion automatically recalls the finding, then student status, with distinct cues')

    expect(page.get_by_role('status', name='Maya is typing')).to_be_visible(timeout=5000)
    expect(page.locator('.alex-character')).to_have_count(0)
    expect(page.locator('.maya-bubble p')).to_have_text('The score is up. What about learning?')
    expect(page.get_by_role('status', name='Alex is typing')).to_be_visible(timeout=4000)
    expect(page.locator('.maya-bubble p')).to_be_visible()
    page.screenshot(path=str(out / 'feedback-typing.png'), full_page=True)
    settle(page)
    maya = page.locator('.maya-character').bounding_box()
    alex = page.locator('.alex-character').bounding_box()
    assert maya['y'] + maya['height'] <= alex['y']
    assert maya['x'] < alex['x']
    assert page.locator('body').bounding_box()['height'] <= 768
    page.screenshot(path=str(out / 'feedback-review.png'), full_page=True)
    record('Typing and replies follow the recap automatically; Maya stays above Alex on a laptop')

    page.get_by_role('button', name='Sound on', exact=True).click()
    before = page.evaluate('window.audioStarts.length')
    page.get_by_role('button', name='Replay scene').click()
    finish_scene(page)
    settle(page)
    assert page.evaluate('window.audioStarts.length') == before
    page.reload(wait_until='networkidle')
    expect(page.get_by_role('button', name='Sound off', exact=True)).to_be_visible()
    record('Mute suppresses automatic update cues and survives reload')

    page.get_by_role('button', name='Sound off', exact=True).click()
    page.get_by_role('button', name='Replay scene').click()
    finish_scene(page)
    expect(page.locator('.observation-recap')).to_be_visible(timeout=5000)
    assert page.evaluate('window.audioStarts.some(n => n.frequency === 360 && n.state === "running")')
    record('Unmuting restores actual Web Audio feedback')
    page.get_by_text('More context', exact=True).click()
    expect(page.get_by_role('button', name='Resume updates')).to_be_visible()
    page.wait_for_timeout(2000)
    expect(page.locator('.student')).to_contain_text('Not observed yet')
    page.get_by_role('button', name='Resume updates').click()
    expect(page.locator('.uncertainty')).to_have_text('Unclear', timeout=5000)
    record('Reading optional context pauses the presentation until Resume')

    small = make_context(browser, viewport={'width': 390, 'height': 300}, reduced_motion='reduce')
    tab = small.new_page()
    tab.goto(url, wait_until='networkidle')
    tab.get_by_role('button', name='Skip guide').click()
    tab.evaluate('''localStorage.setItem('gaming-the-system:level-one:v1', JSON.stringify({version:1, phase:'review',metricId:'prep',prediction:'Students will understand.',resultReported:true,reviewStep:0}))''')
    tab.reload(wait_until='networkidle')
    tab.evaluate('window.scrollTo(0, document.body.scrollHeight)')
    assert tab.evaluate('document.querySelector(".prediction-recap").getBoundingClientRect().bottom <= 0')
    tab.wait_for_timeout(1300)
    assert tab.locator('.observation-recap').count() == 0
    tab.locator('.prediction-recap').scroll_into_view_if_needed()
    settle(tab)
    record('Off-screen recap waits, then resumes and brings student status and replies into view')
    small.close()

    silent = make_context(browser, reduced_motion='reduce')
    silent.add_init_script("Object.defineProperty(window, 'AudioContext', {value: undefined});")
    quiet = silent.new_page()
    quiet.goto(url, wait_until='networkidle')
    quiet.get_by_role('button', name='Skip guide').click()
    expect(quiet.get_by_role('button', name='No audio')).to_be_disabled()
    quiet.get_by_test_id('metric-part').click()
    quiet.get_by_role('button', name='Make a prediction').click()
    quiet.get_by_label('What do you expect students to do?').fill('Students will share ideas.')
    quiet.get_by_role('button', name='Run evaluation').click()
    expect(quiet.get_by_role('button', name='Observe the class')).to_be_enabled(timeout=8000)
    silent.close()
    record('Browsers without Web Audio retain the complete visual sequence')

    assert not errors, errors
    context.close()
    browser.close()

name = 'feedback-offline-results.json' if args.file else 'feedback-results.json'
(out / name).write_text(json.dumps({'passed': len(checks), 'checks': checks, 'runtime_errors': errors}, indent=2))
print(f'{len(checks)} feedback checks passed.')
