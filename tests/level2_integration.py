"""Partner scene contract, completion lifecycle and Level 2 audio/visibility checks.
Requires npm run dev. Presentation timing is covered at real speed in level2.py;
this host-contract check uses Playwright's browser clock to advance reading beats.
"""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

out = Path('test-results')
out.mkdir(exist_ok=True)
harness = out / 'level2-host.html'
harness.write_text('''<!doctype html><html lang="en"><body><div id="root"></div>
<script type="module">
import React from 'react';
import {createRoot} from 'react-dom/client';
import '/src/shared/styles/base.css';
import LevelTwo from '/src/levels/level2/LevelTwo.tsx';
window.requests = []; window.results = [];
createRoot(document.getElementById('root')).render(React.createElement(LevelTwo, {
  playerName: 'Jordan', previousMetricId: 'peer',
  renderCinematic: (request, complete) => {
    window.requests.push(request);
    return React.createElement('section', {className:'partner-scene'},
      React.createElement('h2', null, request.sceneId),
      React.createElement('button', {onClick: complete}, 'Finish partner scene'));
  },
  onComplete: result => window.results.push(result)
}));
</script></body></html>''')
checks, errors = [], []


def record(name):
    checks.append(name)
    print('PASS', name, flush=True)


def advance(page, seconds=24):
    for _ in range(seconds):
        page.clock.run_for(1000)
        page.wait_for_timeout(12)


def finish_scene(page):
    page.get_by_role('button', name='Observe the class', exact=True).click()
    expect(page.get_by_role('button', name='Finish partner scene', exact=True)).to_be_visible()
    page.get_by_role('button', name='Finish partner scene', exact=True).click()
    advance(page)


def play_level(page, ids):
    advance(page, 8)
    for id in ids: page.get_by_test_id('level2-metric-' + id).click()
    page.get_by_role('button', name='Run evaluation', exact=True).click()
    advance(page, 6)
    finish_scene(page)
    page.get_by_role('button', name='Cover the gaps', exact=True).click()
    page.get_by_role('button', name='Add remaining metrics', exact=True).click()
    advance(page, 6)
    finish_scene(page)
    for count in [10, 25, 100]:
        page.get_by_role('button', name='Add more metrics', exact=True).click()
        advance(page)
        expect(page.locator('.l2-checklist [data-shown=true]')).to_have_count(3)
        expect(page.locator('.l2-reported-count')).to_have_text(str(count))
    finish_scene(page)
    expect(page.get_by_role('button', name='Continue to Level 3', exact=True)).to_be_visible()


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1440, 'height': 1000}, reduced_motion='reduce')
    context.add_init_script('''window.notes=[];
const start=OscillatorNode.prototype.start;
const set=AudioParam.prototype.setValueAtTime;
const values=new WeakMap();
AudioParam.prototype.setValueAtTime=function(value,...args){values.set(this,value);return set.call(this,value,...args);};
OscillatorNode.prototype.start=function(...args){window.notes.push(values.get(this.frequency));return start.apply(this,args);};''')
    page = context.new_page()
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.clock.install()
    page.goto('http://127.0.0.1:5173/test-results/level2-host.html', wait_until='networkidle')
    expect(page.locator('.level-two')).to_have_attribute('data-phase', 'intro')
    advance(page, 8)
    expect(page.locator('.l2-previous')).to_contain_text('Peer response')
    play_level(page, ['discuss', 'reflect', 'peer'])
    results = page.evaluate('window.results')
    assert results == [{'selectedMetricIds': ['discuss', 'reflect', 'peer'], 'branch': 'quality', 'metricsTracked': 100}], results
    requests = page.evaluate('window.requests')
    assert {request['sceneId'] for request in requests} == {'level2.three.quality', 'level2.six', 'level2.checklist'}, requests
    assert all(request['selectedMetricIds'] == ['discuss', 'reflect', 'peer'] for request in requests)
    assert all(request['branch'] == 'quality' for request in requests)
    assert all(request['playerName'] == 'Jordan' for request in requests)
    assert not page.get_by_test_id('level2-cinematic').count()
    expect(page.locator('.maya-bubble .speaker-name')).to_have_text('Jordan')
    record('Partner replaces all three scene slots; original trio, branch and custom name retained')
    record('Completion reports exact result once after final reading')
    notes = page.evaluate('window.notes')
    assert all(frequency in notes for frequency in [420, 523.25, 659.25, 783.99, 360, 600]), notes
    record('Level 2 emits actual count, success, evidence and softer message cues')
    page.get_by_role('button', name='Sound on', exact=True).click()
    note_count = page.evaluate('window.notes.length')
    page.get_by_role('button', name='Replay scene', exact=True).click()
    page.get_by_role('button', name='Finish partner scene', exact=True).click()
    advance(page)
    assert page.evaluate('window.results.length') == 1
    assert page.evaluate('window.notes.length') == note_count
    record('Final replay retains completion count and mute suppresses new cues')
    page.get_by_role('button', name='Restart', exact=True).click()
    page.get_by_role('button', name='Restart Level 2', exact=True).click()
    play_level(page, ['prep', 'part', 'focus'])
    assert page.evaluate('window.results.length') == 2
    assert page.evaluate('window.results[1].branch') == 'visible'
    record('Restart clears the original trio and permits a new completion')
    context.close()

    # Hold a core update when hidden and hold the growth counter under a modal.
    context = browser.new_context(viewport={'width': 1440, 'height': 1000})
    page = context.new_page()
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.clock.install()
    page.goto('http://127.0.0.1:5173/test-results/level2-host.html', wait_until='networkidle')
    expect(page.locator('.level-two')).to_have_attribute('data-phase', 'intro')
    page.evaluate("Object.defineProperty(document,'hidden',{configurable:true,value:true});document.dispatchEvent(new Event('visibilitychange'))")
    advance(page, 8)
    expect(page.locator('.level-two')).to_have_attribute('data-phase', 'intro')
    page.evaluate("Object.defineProperty(document,'hidden',{configurable:true,value:false});document.dispatchEvent(new Event('visibilitychange'))")
    page.get_by_role('button', name='Restart', exact=True).click()
    advance(page, 8)
    expect(page.locator('.level-two')).to_have_attribute('data-phase', 'intro')
    page.keyboard.press('Escape')
    advance(page, 8)
    expect(page.locator('.level-two')).to_have_attribute('data-phase', 'choose')
    record('Chapter dialogue waits while the tab is hidden or restart dialog is open, then automatically opens metric selection')
    for id in ['prep', 'part', 'focus']: page.get_by_test_id('level2-metric-' + id).click()
    page.get_by_role('button', name='Run evaluation', exact=True).click()
    page.evaluate("Object.defineProperty(document,'hidden',{configurable:true,value:true});document.dispatchEvent(new Event('visibilitychange'))")
    advance(page, 6)
    assert page.locator('.l2-evaluation-list [data-checked=true]').count() == 0
    page.evaluate("Object.defineProperty(document,'hidden',{configurable:true,value:false});document.dispatchEvent(new Event('visibilitychange'))")
    advance(page, 6)
    expect(page.get_by_role('button', name='Observe the class', exact=True)).to_be_enabled()
    record('Hidden tab holds metric updates and resumes them on return')
    finish_scene(page)
    page.get_by_role('button', name='Cover the gaps', exact=True).click()
    page.get_by_role('button', name='Add remaining metrics', exact=True).click()
    advance(page, 6)
    finish_scene(page)
    page.get_by_role('button', name='Add more metrics', exact=True).click()
    page.get_by_role('button', name='Restart', exact=True).click()
    frozen = page.locator('.l2-counter-value strong').inner_text()
    advance(page, 5)
    assert page.locator('.l2-counter-value strong').inner_text() == frozen
    expect(page.locator('.level-two')).to_have_attribute('data-phase', 'evaluate')
    page.keyboard.press('Escape')
    advance(page)
    expect(page.locator('.l2-checklist')).to_contain_text('Completing requirements')
    record('Growth counter and automatic observation wait while restart confirmation is open')
    page.get_by_role('button', name='Add more metrics', exact=True).click()
    for _ in range(80):
        page.clock.run_for(100)
        page.wait_for_timeout(12)
        if page.locator('.l2-checklist li[data-shown=true]').count() == 3: break
    expect(page.locator('.l2-checklist li[data-shown=true]')).to_have_count(3)
    expect(page.get_by_role('button', name='Add more metrics', exact=True)).to_have_count(0)
    page.get_by_role('button', name='Restart', exact=True).click()
    advance(page, 5)
    expect(page.get_by_role('button', name='Add more metrics', exact=True)).to_have_count(0)
    page.keyboard.press('Escape')
    advance(page, 2)
    expect(page.get_by_role('button', name='Add more metrics', exact=True)).to_be_enabled()
    record('The shortened next-button wait pauses under restart confirmation and resumes after closing it')
    context.close()

    context = browser.new_context(viewport={'width': 320, 'height': 740}, reduced_motion='reduce')
    page = context.new_page()
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.clock.install()
    page.goto('http://127.0.0.1:5173/test-results/level2-host.html', wait_until='networkidle')
    play_level(page, ['prep', 'reflect', 'peer'])
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    page.screenshot(path=str(out / 'level2-complete-320.png'), full_page=True)
    record('Complete expansion and partner-scene flow works at 320px')
    context.close()
    browser.close()

assert not errors, errors
(out / 'level2-integration-results.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'runtimeErrors':errors},indent=2)+'\n')
print(f'{len(checks)} integration checks passed', flush=True)
