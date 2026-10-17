"""Real browser checks for staggered reveals, chat timing, and Web Audio feedback."""
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
    page.get_by_role('button', name='Continue scene').click()
    page.get_by_role('button', name='Continue scene').click()
    page.get_by_role('button', name='Return to dashboard').click()

def settle(page):
    page.locator('.dialogue-strip').scroll_into_view_if_needed()
    expect(page.get_by_role('button', name='Try more metrics')).to_be_enabled(timeout=7000)

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--no-sandbox'])
    context = make_context(browser, viewport={'width': 1366, 'height': 768})
    context.add_init_script(audio_probe)
    page = context.new_page()
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(url, wait_until='networkidle')
    page.get_by_test_id('metric-prep').click()
    page.get_by_role('button', name='Make a prediction').click()
    expect(page.get_by_role('status', name='Maya is typing')).to_be_visible()
    page.get_by_label('What do you expect students to do?').fill('Students will understand the reading.')
    page.get_by_role('button', name='Run evaluation').click()
    expect(page.get_by_role('button', name='See university response')).to_be_disabled()
    expect(page.get_by_role('button', name='See university response')).to_be_enabled()
    expect(page.locator('.after-score')).to_contain_text('88')
    expect(page.locator('.university-value')).to_have_count(0)
    page.wait_for_timeout(600)
    expect(page.locator('.university-value')).to_have_count(0)
    record('Score animates first; university response waits for a deliberate click')

    page.get_by_role('button', name='See university response').click()
    expect(page.locator('.university')).to_have_attribute('data-updated', 'true')
    expect(page.locator('.university-value')).to_contain_text('88')
    assert page.evaluate('window.audioStarts.some(n => Math.abs(n.frequency - 523.25) < 0.1 && n.state === "running")')
    assert page.evaluate('window.audioStarts.some(n => n.frequency === 420)')
    page.screenshot(path=str(out / 'feedback-report.png'), full_page=True)
    record('Live Web Audio plays count ticks and a distinct success chime after user input')

    scene_to_review(page)
    expect(page.locator('.observation-recap')).to_have_count(0)
    expect(page.locator('.student')).to_contain_text('Not observed yet')
    page.get_by_role('button', name='Reveal observation').click()
    expect(page.locator('.observation-recap')).to_contain_text('The checklist is complete.')
    expect(page.locator('.student')).to_contain_text('Not observed yet')
    page.get_by_role('button', name='See student response').click()
    expect(page.locator('.student')).to_have_attribute('data-updated', 'true')
    expect(page.locator('.uncertainty')).to_have_text('Unclear')
    assert page.evaluate('window.audioStarts.some(n => n.frequency === 360) && window.audioStarts.some(n => n.frequency === 392)')
    record('Observation and student status reveal separately with different update sounds')

    page.locator('.dialogue-strip').scroll_into_view_if_needed()
    expect(page.get_by_role('status', name='Maya is typing')).to_be_visible()
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
    record('Typing precedes each message; Maya stays above Alex, with both readable on a laptop')

    page.get_by_role('button', name='Sound on', exact=True).click()
    expect(page.get_by_role('button', name='Sound off', exact=True)).to_have_attribute('aria-pressed', 'false')
    before = page.evaluate('window.audioStarts.length')
    page.get_by_role('button', name='Replay scene').click()
    page.get_by_role('button', name='Continue scene').click()
    page.get_by_role('button', name='Continue scene').click()
    page.get_by_role('button', name='Return to dashboard').click()
    page.get_by_role('button', name='Reveal observation').click()
    page.get_by_role('button', name='See student response').click()
    settle(page)
    assert page.evaluate('window.audioStarts.length') == before
    page.reload(wait_until='networkidle')
    expect(page.get_by_role('button', name='Sound off', exact=True)).to_be_visible()
    record('Mute suppresses every subsequent cue and survives reload')

    page.get_by_role('button', name='Sound off', exact=True).click()
    page.get_by_role('button', name='Replay scene').click()
    page.get_by_role('button', name='Continue scene').click()
    page.get_by_role('button', name='Continue scene').click()
    page.get_by_role('button', name='Return to dashboard').click()
    page.get_by_role('button', name='Reveal observation').click()
    assert page.evaluate('window.audioStarts.some(n => n.frequency === 360 && n.state === "running")')
    record('Unmuting restores actual Web Audio feedback')

    small = make_context(browser, viewport={'width': 390, 'height': 600}, reduced_motion='reduce')
    tab = small.new_page()
    tab.goto(url, wait_until='networkidle')
    tab.evaluate('''localStorage.setItem('gaming-the-system:level-one:v1', JSON.stringify({version:1, phase:'review',metricId:'prep',prediction:'Students will understand.',resultReported:true,reviewStep:2}))''')
    tab.reload(wait_until='networkidle')
    tab.evaluate('window.scrollTo(0,0)')
    tab.wait_for_timeout(1000)
    assert tab.locator('.maya-bubble p').count() == 0
    tab.get_by_role('button', name='Read replies').click()
    settle(tab)
    record('Off-screen dialogue waits; Read replies brings it into view and resumes the sequence')
    small.close()

    silent = make_context(browser, reduced_motion='reduce')
    silent.add_init_script("Object.defineProperty(window, 'AudioContext', {value: undefined});")
    quiet = silent.new_page()
    quiet.goto(url, wait_until='networkidle')
    expect(quiet.get_by_role('button', name='No audio')).to_be_disabled()
    quiet.get_by_test_id('metric-part').click()
    quiet.get_by_role('button', name='Make a prediction').click()
    quiet.get_by_label('What do you expect students to do?').fill('Students will share ideas.')
    quiet.get_by_role('button', name='Run evaluation').click()
    quiet.get_by_role('button', name='See university response').click()
    expect(quiet.get_by_role('button', name='Observe the class')).to_be_enabled()
    silent.close()
    record('Browsers without Web Audio still have the complete visual flow')

    assert not errors, errors
    context.close()
    browser.close()

name = 'feedback-offline-results.json' if args.file else 'feedback-results.json'
(out / name).write_text(json.dumps({'passed': len(checks), 'checks': checks, 'runtime_errors': errors}, indent=2))
print(f'{len(checks)} feedback checks passed.')
