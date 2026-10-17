"""Opening-name handoff through the real Gameplay host. Requires npm run dev.

The form is a test harness for the supplied opening's playerName/draftName state;
the opening itself is not merged. The browser clock advances presentation waits.
"""
import itertools
import json
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

out = Path('test-results')
out.mkdir(exist_ok=True)
(out / 'identity-host.html').write_text('''<!doctype html><html lang="en"><body><div id="root"></div>
<script type="module">
import React, {useEffect, useState} from 'react';
import {createRoot} from 'react-dom/client';
import '/src/shared/styles/base.css';
import Gameplay from '/src/Gameplay.tsx';
window.requests = []; window.results = [];
const custom = location.hash.includes('partner');
const renderScene = (request, complete) => {
  window.requests.push(request);
  return React.createElement('section', {className:'partner-scene'},
    React.createElement('h2', null, request.sceneId),
    React.createElement('span', {className:'partner-player'}, request.playerName),
    React.createElement('button', {onClick: complete}, 'Finish partner scene'));
};
function Host() {
  const [draftName, setDraftName] = useState('');
  const [playerName, setPlayerName] = useState('');
  const [finished, setFinished] = useState(false);
  useEffect(() => {
    const fresh = event => {
      if (event.persisted) { setFinished(false); setPlayerName(''); setDraftName(''); }
    };
    window.addEventListener('pageshow', fresh);
    return () => window.removeEventListener('pageshow', fresh);
  }, []);
  if (finished) return React.createElement(Gameplay, {
    playerName, initialLevel: location.hash.includes('level2') ? 2 : 1,
    renderLevelOneCinematic: custom ? renderScene : undefined,
    renderLevelTwoCinematic: custom ? renderScene : undefined,
    onLevelOneComplete: result => window.results.push({level:1,result}),
    onLevelTwoComplete: result => window.results.push({level:2,result}),
  });
  return React.createElement('form', {onSubmit:event=>{
    event.preventDefault(); if (!draftName.trim()) return;
    setPlayerName(draftName.trim()); setFinished(true);
  }}, React.createElement('label', {htmlFor:'opening-name'}, 'Name on the desk'),
  React.createElement('input', {id:'opening-name',autoComplete:'off',maxLength:40,required:true,
    value:draftName,onChange:event=>setDraftName(event.target.value)}),
  React.createElement('button', {disabled:!draftName.trim()}, 'Finish opening'));
}
createRoot(document.getElementById('root')).render(React.createElement(Host));
</script></body></html>''')
checks, errors = [], []
runs = itertools.count()


def record(text):
    checks.append(text)
    print('PASS', text, flush=True)


def advance(page, seconds=30):
    for _ in range(seconds):
        page.clock.run_for(1000)
        page.wait_for_timeout(12)


def name_visible(page, name):
    expect(page.locator('.maya-bubble .speaker-name')).to_have_text(name)
    expect(page.locator('.maya-avatar')).to_have_text('')
    expect(page.locator('.maya-avatar svg')).to_have_attribute('data-character', 'teacher')
    if name != 'Maya': assert 'Maya' not in page.locator('body').inner_text()


def start(page, name, mode='partner', level=1):
    page.goto('http://127.0.0.1:5173/test-results/identity-host.html?run=' + str(next(runs)) + '#' + mode + ('-level2' if level == 2 else ''), wait_until='networkidle')
    page.get_by_label('Name on the desk').fill(name)
    page.get_by_role('button', name='Finish opening', exact=True).click()


def begin_one(page):
    page.get_by_test_id('metric-focus').click()
    page.get_by_role('button', name='Make a prediction', exact=True).click()
    page.get_by_label('What do you expect students to do?').fill('Students will think more deeply.')
    page.get_by_role('button', name='Run evaluation', exact=True).click()
    advance(page, 10)
    expect(page.locator('.maya-bubble p')).to_have_text('Looking good. I’ll check the classroom.')


def partner_scene(page, name):
    page.get_by_role('button', name='Observe the class', exact=True).click()
    expect(page.locator('.partner-player')).to_have_text(name)
    page.get_by_role('button', name='Finish partner scene', exact=True).click()
    advance(page)
    name_visible(page, name)


def placeholder_scene(page, name, level):
    page.get_by_role('button', name='Observe the class', exact=True).click()
    label = page.locator('.scene-caption .speaker-label' if level == 1 else '.l2-scene-caption > span')
    labels = []
    while True:
        labels.append(label.inner_text())
        if not page.get_by_role('button', name='Continue scene', exact=True).count(): break
        page.get_by_role('button', name='Continue scene', exact=True).click()
    assert name in labels and 'Alex' in labels, labels
    assert 'Maya' not in labels, labels
    page.get_by_role('button', name='Return to dashboard', exact=True).click()
    advance(page)
    name_visible(page, name)


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    context = browser.new_context(viewport={'width':1366,'height':900}, reduced_motion='reduce')
    # The host/levels must work without either storage API.
    context.add_init_script("for(const key of ['localStorage','sessionStorage'])Object.defineProperty(window,key,{get(){throw new Error('storage unavailable')}})")
    page = context.new_page()
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.clock.install()
    name = 'Jordan O’Neil'
    start(page, '  ' + name + '  ')
    guide = page.get_by_role('dialog', name='Workbench guide')
    for _ in range(3): guide.get_by_role('button', name='Next', exact=True).click()
    expect(guide).to_contain_text('Your conversation with Alex appears here.')
    assert 'Maya' not in guide.inner_text()
    guide.get_by_role('button', name='Start Level 1', exact=True).click()
    expect(page.get_by_role('status', name=name+' is typing')).to_be_visible()
    name_visible(page, name)
    record('Confirmed opening name reaches Level 1 labels, avatar and typing accessibility; guide has no fixed Maya name')

    expect(page.get_by_role('button', name='Restart', exact=True)).to_have_count(0)
    name_visible(page, name)
    begin_one(page)
    partner_scene(page, name)
    expect(page.locator('.alex-bubble .speaker-name').first).to_have_text('Alex')
    expect(page.locator('.alex-bubble p')).to_have_count(2)
    assert page.evaluate('window.results[0].result.metricId') == 'focus'
    record('Level 1 has no player restart; its custom cinematic retains playerName and Alex stays Alex')

    page.get_by_role('button', name='Continue to Level 2', exact=True).click()
    name_visible(page, name)
    advance(page, 1)
    expect(page.locator('.maya-bubble p')).to_have_text('One metric wasn’t enough. What if I tracked three?')
    advance(page, 8)
    name_visible(page, name)
    page.get_by_role('button', name='Choose three metrics', exact=True).click()
    expect(page.locator('.l2-previous')).to_contain_text('Focus')
    expect(page.locator('.conversation')).to_have_count(0)
    for id in ['prep','part','discuss']: page.get_by_test_id('level2-metric-'+id).click()
    page.get_by_role('button', name='Run evaluation', exact=True).click()
    advance(page, 6)
    partner_scene(page, name)
    page.get_by_role('button', name='Cover the gaps', exact=True).click()
    expect(page.get_by_role('heading', name='What am I still missing?', exact=True)).to_be_visible()
    record('Level 1 → Level 2 retains the same opening name and prior metric; choice/gap prompts retain the player perspective')

    page.get_by_role('button', name='Add remaining metrics', exact=True).click()
    advance(page, 6)
    partner_scene(page, name)
    expect(page.locator('.maya-bubble p')).to_have_text('Now all six count. Are you learning more, or just keeping up?')
    for count in [10,25,100]:
        page.get_by_role('button', name='Add more metrics', exact=True).click()
        advance(page)
        expect(page.locator('.l2-reported-count')).to_have_text(str(count))
    partner_scene(page, name)
    requests = page.evaluate('window.requests')
    assert {request['sceneId'] for request in requests} == {'level1.focus','level2.three.mixed','level2.six','level2.checklist'}
    assert all(request['playerName'] == name for request in requests), requests
    assert [item['level'] for item in page.evaluate('window.results')] == [1,2]
    record('Both levels and every custom cinematic slot share one name; the six-metric review addresses Alex; result callbacks still fire')

    expect(page.get_by_role('button', name='Restart', exact=True)).to_have_count(0)
    name_visible(page, name)
    page.reload(wait_until='networkidle')
    expect(page.get_by_label('Name on the desk')).to_have_value('')
    expect(page.locator('.game-page')).to_have_count(0)
    record('Level 2 has no player restart; reloading the full host returns to a fresh opening/name entry with storage blocked')

    start(page, 'Avery', mode='placeholder', level=2)
    page.evaluate("window.dispatchEvent(new PageTransitionEvent('pageshow', {persisted:true}))")
    expect(page.get_by_label('Name on the desk')).to_have_value('')
    expect(page.locator('.game-page')).to_have_count(0)
    record('Full-host restored-page reset returns to the opening and clears the previous identity')

    start(page, name, mode='placeholder')
    page.get_by_role('button', name='Skip guide', exact=True).click()
    begin_one(page)
    placeholder_scene(page, name, 1)
    page.get_by_role('button', name='Continue to Level 2', exact=True).click()
    advance(page, 8)
    page.get_by_role('button', name='Choose three metrics', exact=True).click()
    for id in ['discuss','reflect','peer']: page.get_by_test_id('level2-metric-'+id).click()
    page.get_by_role('button', name='Run evaluation', exact=True).click()
    advance(page, 6)
    placeholder_scene(page, name, 2)
    page.get_by_role('button', name='Cover the gaps', exact=True).click()
    page.get_by_role('button', name='Add remaining metrics', exact=True).click()
    advance(page, 6)
    placeholder_scene(page, name, 2)
    record('Built-in Level 1 and Level 2 three/six-metric placeholders display the opening name and keep Alex unchanged')

    for count in [10,25,100]:
        page.get_by_role('button', name='Add more metrics', exact=True).click()
        advance(page)
    page.get_by_role('button', name='Observe the class', exact=True).click()
    expect(page.locator('.l2-scene-caption > span')).to_have_text(name)
    page.get_by_role('button', name='Continue scene', exact=True).click()
    expect(page.locator('.l2-scene-caption > span')).to_have_text(name)
    page.get_by_role('button', name='Return to dashboard', exact=True).click()
    advance(page)
    name_visible(page, name)
    page.screenshot(path=str(out / 'player-name-level2.png'), full_page=True)
    record('Final Level 2 placeholder and closing player thought retain the same opening name')

    page.set_viewport_size({'width':320,'height':740})
    for sample in ['Alex', '<img src=x onerror=alert(1)>', 'W'*40]:
        start(page, sample, mode='placeholder', level=2)
        advance(page, 1)
        page.locator('.conversation').scroll_into_view_if_needed()
        name_visible(page, sample)
        assert page.locator('.speaker-name img').count() == 0
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        assert page.locator('.speaker-name').evaluate_all('(labels)=>labels.every(label=>label.scrollWidth<=label.clientWidth)')
    record('Names including Alex, HTML-like text and 40 unbroken characters render literally without horizontal overflow at 320px')
    context.close()
    browser.close()

assert not errors, errors
record('No runtime errors during opening-name integration checks')
(out / 'player-identity-results.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'runtimeErrors':errors},indent=2)+'\n')
