"""Real browser checks for one recap focus, reading time, chat order and audio."""
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
    expect(page.get_by_role('button', name='Continue to Level 2')).to_be_visible(timeout=22000)
    expect(page.get_by_role('button', name='Continue to Level 2')).to_be_enabled()

timeline_probe = '''
window.reviewTimeline = {};
new MutationObserver(() => {
  if (!document.querySelector('.phase-review')) return;
  const mark = (name, selector) => {
    if (document.querySelector(selector) && window.reviewTimeline[name] === undefined) window.reviewTimeline[name] = performance.now();
  };
  mark('finding', '.observation-recap');
  mark('student', '.student.has-evidence');
  mark('mayaTyping', '.maya-bubble.is-typing');
  mark('maya', '.maya-bubble p');
  mark('alexTyping', '.alex-bubble.is-typing');
  mark('alex', '.alex-bubble p');
  mark('alexSecond', '.alex-character[data-order="2"] .alex-bubble p');
  mark('completed', '.level-finished');
}).observe(document.body, {childList:true, subtree:true, attributes:true});
'''

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
    expect(page.locator('label[for=prediction]')).to_have_class('sr-only')
    expect(page.get_by_text('One sentence, before this becomes the target.', exact=True)).to_have_count(0)
    expect(page.locator('#prediction')).to_have_attribute('aria-describedby', 'prediction-count')
    record('Prediction page removes the repeated visible prompt and helper while retaining its accessible input label')
    page.get_by_label('What do you expect students to do?').fill('Students will understand the reading.')
    page.get_by_role('button', name='Run evaluation').click()
    expect(page.get_by_role('button', name='Observe the class')).to_be_disabled()
    expect(page.locator('.after-score')).to_contain_text('88')
    expect(page.locator('.university-value')).to_have_count(0)
    expect(page.get_by_role('button', name='Observe the class')).to_be_enabled(timeout=5000)
    assert page.get_by_role('button', name='Pause updates').count() == 0
    assert page.get_by_role('button', name='Resume updates').count() == 0
    expect(page.get_by_role('heading', name='Management’s view', exact=True)).to_be_visible()
    record('Score and management feedback advance automatically without pause controls')

    expect(page.locator('.university')).to_have_attribute('data-updated', 'true')
    expect(page.locator('.university-value')).to_contain_text('88')
    assert page.evaluate('window.audioStarts.some(n => Math.abs(n.frequency - 523.25) < 0.1 && n.state === "running")')
    assert page.evaluate('window.audioStarts.some(n => n.frequency === 420)')
    assert page.evaluate('window.feedbackMasterGains.some(gain => gain > 0.12 && gain < 0.14)')
    page.screenshot(path=str(out / 'feedback-report.png'), full_page=True)
    record('Actual Web Audio plays count and success cues at the increased master gain')

    expect(page.locator('.university')).to_have_attribute('data-updated', 'false', timeout=5000)
    expect(page.locator('.new-badge')).to_have_count(0)
    record('Management emphasis ends after one cue and the score remains available')

    page.get_by_role('button', name='Observe the class').click()
    page.evaluate(timeline_probe)
    before_group = page.evaluate('window.audioStarts.length')
    finish_scene(page)
    expect(page.locator('.observation-recap')).to_have_count(0)
    expect(page.locator('.student')).to_contain_text('Not observed yet')
    expect(page.locator('.observation-recap > p')).to_have_text('Students complete the preparation, but some skim just enough to meet the requirement.', timeout=5000)
    expect(page.locator('.student-behaviour')).to_have_text('Skimming just to finish.')
    expect(page.locator('.learning-risk strong')).to_have_text('Learning at risk')
    assert page.locator('.student-behaviour').evaluate('e=>parseFloat(getComputedStyle(e).fontSize)') > page.locator('.learning-risk strong').evaluate('e=>parseFloat(getComputedStyle(e).fontSize)') * 1.8
    expect(page.locator('.observation-recap p')).to_have_count(1)
    expect(page.locator('.observation-recap details')).to_have_count(0)
    expect(page.locator('.student .new-badge')).to_have_count(0)
    assert 'just-updated' not in page.locator('.student').get_attribute('class')
    assert page.get_by_text('More context', exact=True).count() == 0
    assert page.get_by_text('Close details', exact=True).count() == 0
    assert page.get_by_role('button', name='Reveal observation').count() == 0
    assert page.get_by_role('button', name='See student response').count() == 0
    assert page.evaluate('window.audioStarts.slice(' + str(before_group) + ').map(n => n.frequency)') == [360]
    stamps = page.evaluate('window.reviewTimeline')
    assert abs(stamps['student'] - stamps['finding']) < 100, stamps
    assert page.locator('.phase-review .dialogue-character').count() == 0
    record('One evidence paragraph and student summary arrive together with one cue and no duplicate text or controls')

    expect(page.get_by_role('status', name='Maya is typing')).to_be_visible(timeout=10000)
    stamps = page.evaluate('window.reviewTimeline')
    assert 1500 <= stamps['mayaTyping'] - stamps['finding'] < 2900, stamps
    record('Level 1 starts its review with the same 1.6–2.8 second evidence wait as Level 2')
    expect(page.locator('.alex-character')).to_have_count(0)
    expect(page.locator('.maya-bubble p')).to_have_text('Alex, how did you get through the reading so quickly?')
    expect(page.get_by_role('status', name='Alex is typing')).to_be_visible(timeout=6000)
    expect(page.locator('.maya-bubble p')).to_be_visible()
    page.screenshot(path=str(out / 'feedback-typing.png'), full_page=True)
    settle(page)
    maya = page.locator('.maya-character').bounding_box()
    alex = page.locator('.alex-character').first.bounding_box()
    decision = page.locator('.decision-area').bounding_box()
    assert maya['x'] >= decision['x'] and alex['x'] + alex['width'] <= decision['x'] + decision['width']
    assert maya['y'] + maya['height'] <= alex['y']
    assert maya['x'] < alex['x']
    assert page.locator('body').bounding_box()['height'] <= 768
    stamps = page.evaluate('window.reviewTimeline')
    assert 1300 <= stamps['alexTyping'] - stamps['maya'] <= 2600, stamps
    assert 0 <= stamps['completed'] - stamps['alexSecond'] < 180, stamps
    expect(page.locator('.alex-bubble p')).to_have_text(['I finished the whole list! 📋', 'The reading? I mostly skimmed it 😬'])
    expect(page.locator('.message-continuation .avatar')).to_have_css('visibility', 'hidden')
    expect(page.locator('.message-continuation .speaker-name')).to_have_class('speaker-name sr-only')
    page.screenshot(path=str(out / 'feedback-review.png'), full_page=True)
    record('Replies stay in the main column; messages use the Level 2 reading rhythm and continuation appears with the second Alex reply')

    page.get_by_role('button', name='Sound on', exact=True).click()
    before = page.evaluate('window.audioStarts.length')
    page.get_by_role('button', name='Replay scene').click()
    finish_scene(page)
    settle(page)
    assert page.evaluate('window.audioStarts.length') == before
    record('Mute suppresses all subsequent cues within the current game')

    page.get_by_role('button', name='Sound off', exact=True).click()
    page.get_by_role('button', name='Replay scene').click()
    finish_scene(page)
    expect(page.locator('.observation-recap')).to_be_visible(timeout=5000)
    assert page.evaluate('window.audioStarts.some(n => n.frequency === 360 && n.state === "running")')
    record('Unmuting restores actual Web Audio feedback')
    page.get_by_role('button', name='Guide', exact=True).click()
    page.wait_for_timeout(2000)
    expect(page.locator('.phase-review .dialogue-character')).to_have_count(0)
    page.get_by_role('button', name='Skip guide').click()
    settle(page)
    expect(page.locator('.observation-recap > p')).to_contain_text('Students complete the preparation')
    record('Guide temporarily holds the reading sequence and closing it resumes automatically')

    small = make_context(browser, viewport={'width': 390, 'height': 300}, reduced_motion='reduce')
    tab = small.new_page()
    tab.goto(url, wait_until='networkidle')
    tab.get_by_role('button', name='Skip guide').click()
    tab.get_by_test_id('metric-prep').click()
    tab.get_by_role('button', name='Make a prediction').click()
    tab.get_by_label('What do you expect students to do?').fill('Students will understand.')
    tab.get_by_role('button', name='Run evaluation').click()
    scene_to_review(tab)
    tab.evaluate('window.scrollTo(0, document.body.scrollHeight)')
    assert tab.evaluate('document.querySelector(".prediction-recap").getBoundingClientRect().bottom <= 0')
    tab.wait_for_timeout(1300)
    assert tab.locator('.observation-recap').count() == 0
    tab.locator('.prediction-recap').scroll_into_view_if_needed()
    settle(tab)
    record('Off-screen recap waits, then resumes reading and brings replies into view without visiting the sidebar')
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
