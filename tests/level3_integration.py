"""Partner/name contracts, Level 2 handoff, real-time pacing and audio. Requires Vite."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

OUT=Path('test-results');OUT.mkdir(exist_ok=True)
(OUT/'level3-host.html').write_text('''<!doctype html><html lang="en"><body><div id="root"></div>
<script type="module">
import React from 'react';import {createRoot} from 'react-dom/client';
import '/src/shared/styles/base.css';import Gameplay from '/src/Gameplay.tsx';
window.requests=[];window.results=[];window.designLabCount=0;
const query=new URLSearchParams(location.search);
const renderScene=(request,complete)=>{
  window.requests.push(request);
  return React.createElement('section',{className:'partner-scene'},
    React.createElement('h2',null,request.sceneId),
    React.createElement('p',{className:'partner-name'},request.playerName),
    React.createElement('button',{onClick:complete},'Finish partner scene'));
};
createRoot(document.getElementById('root')).render(React.createElement(Gameplay,{
  playerName:query.get('name')||'Riley',initialLevel:query.get('level')==='2'?2:3,
  renderLevelTwoCinematic:renderScene,renderLevelThreeCinematic:renderScene,
  onLevelTwoComplete:result=>window.results.push({level:2,result}),
  onLevelThreeComplete:result=>window.results.push({level:3,result}),
  onDesignLab:()=>window.designLabCount++,
}));
</script></body></html>''')
checks,errors=[],[]


def record(name): checks.append(name);print('PASS',name,flush=True)


def advance(page,seconds=12):
    for _ in range(seconds): page.clock.run_for(1000);page.wait_for_timeout(15)


def start(browser,level=3,script=None,clock=True):
    context=browser.new_context(viewport={'width':1366,'height':900},reduced_motion='reduce')
    if script: context.add_init_script(script)
    page=context.new_page();page.on('pageerror',lambda error:errors.append(str(error)))
    if clock: page.clock.install()
    page.goto(f'http://127.0.0.1:5173/test-results/level3-host.html?level={level}',wait_until='networkidle')
    return context,page


def choose(page):
    page.get_by_role('button',name='Choose priorities',exact=True).click()
    for id in ['prep','part','focus']: page.get_by_test_id('level3-metric-'+id).click()
    page.get_by_role('button',name='Set the weights',exact=True).click()


def weights(page,values):
    for index,id in enumerate(['prep','part','focus']):
        card=page.get_by_test_id('weight-card-'+id)
        if not card.locator('input').is_disabled():
            card.locator('input').evaluate('''(input,value)=>{Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(input,value);input.dispatchEvent(new Event('input',{bubbles:true}));}''',values[index])
        expect(card.locator('output')).to_have_text(str(values[index])+'%')
        page.get_by_test_id('confirm-'+id).click()


def publish(page):
    page.get_by_role('button',name='Run evaluation',exact=True).click()
    page.locator('.l3-publish').scroll_into_view_if_needed();advance(page,4)
    expect(page.locator('.partner-name')).to_have_text('Riley')
    page.get_by_role('button',name='Finish partner scene',exact=True).click()
    advance(page,5)


with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    context,page=start(browser)
    advance(page);expect(page.locator('.maya-bubble .speaker-name')).to_have_text('Riley')
    expect(page.locator('.maya-avatar')).to_have_text('R');assert 'Maya' not in page.locator('body').inner_text()
    choose(page);weights(page,[70,20,10]);publish(page)
    request=page.evaluate('window.requests.at(-1)')
    assert request['sceneId']=='level3.weights' and request['playerName']=='Riley'
    assert [shot['sceneId'] for shot in request['shots']]==['level3.prep.high','level3.part.low','level3.focus.low']
    assert request['runs'][0]['weights']==[70,20,10]
    record('Opening-supplied player name reaches Level 3 labels, avatar and the three weighted partner shots')
    page.get_by_role('button',name='Try a better balance',exact=True).click()
    weights(page,[34,33,33]);publish(page)
    page.get_by_role('button',name='Compare the patterns',exact=True).click();advance(page,3)
    results=page.evaluate('window.results')
    assert len(results)==1 and results[0]['level']==3
    result=results[0]['result'];assert result['runs'][0]['weights']==[70,20,10]
    assert result['compared']['nearEven']['weights']==[34,33,33]
    assert result['compared']['uneven']['weights']==[70,20,10]
    record('Level 3 completes once with immutable tested runs and an explicit near-even/uneven comparison payload')
    page.get_by_role('button',name='Watch Alex’s response',exact=True).click()
    assert page.evaluate('window.requests.at(-1).sceneId')=='level3.compare'
    page.get_by_role('button',name='Finish partner scene',exact=True).click()
    assert page.evaluate('window.requests.at(-1).sceneId')=='theory.reveal'
    page.get_by_role('button',name='Finish partner scene',exact=True).click()
    page.get_by_role('button',name='Go to Design Lab',exact=True).click()
    assert page.evaluate('window.designLabCount')==1
    page.get_by_role('button',name='Review the comparison',exact=True).click();advance(page,3)
    assert page.evaluate('window.results.length')==1
    record('Comparison and theory renderers return correctly; replay does not duplicate completion and the optional Design Lab callback works')
    context.close()

    context,page=start(browser,level=2);advance(page,10)
    page.get_by_role('button',name='Sound on',exact=True).click()
    page.get_by_role('button',name='Choose three metrics',exact=True).click()
    for id in ['prep','part','focus']:page.get_by_test_id('level2-metric-'+id).click()
    page.get_by_role('button',name='Run evaluation',exact=True).click();advance(page,6)
    def scene_two():
        page.get_by_role('button',name='Observe the class',exact=True).click()
        expect(page.locator('.partner-name')).to_have_text('Riley')
        page.get_by_role('button',name='Finish partner scene',exact=True).click();advance(page,14)
    scene_two();page.get_by_role('button',name='Cover the gaps',exact=True).click()
    page.get_by_role('button',name='Add remaining metrics',exact=True).click();advance(page,6);scene_two()
    for count in [10,25,100]:
        page.get_by_role('button',name='Add more metrics',exact=True).click();advance(page,12)
    scene_two()
    page.get_by_role('button',name='Continue to Level 3',exact=True).click();advance(page,8)
    expect(page.locator('.level-three')).to_have_attribute('data-phase','intro')
    expect(page.locator('.maya-bubble .speaker-name')).to_have_text('Riley')
    expect(page.get_by_role('button',name='Sound off',exact=True)).to_be_visible()
    assert len([item for item in page.evaluate('window.results') if item['level']==2])==1
    record('Real Gameplay host carries the opening name and sound preference from Level 2 into the new Level 3 chapter')
    page.reload(wait_until='networkidle')
    expect(page.locator('.level-two')).to_have_attribute('data-phase','intro')
    record('Reloading the connected host starts fresh from its configured entry level')
    context.close()

    context,page=start(browser);advance(page);choose(page);weights(page,[70,20,10])
    page.get_by_role('button',name='Run evaluation',exact=True).click()
    page.evaluate("Object.defineProperty(document,'hidden',{configurable:true,value:true});document.dispatchEvent(new Event('visibilitychange'))")
    shown=page.locator('.l3-publish [data-published=true]').count();advance(page,8)
    assert page.locator('.l3-publish [data-published=true]').count()==shown
    page.evaluate("delete document.hidden;document.dispatchEvent(new Event('visibilitychange'))");advance(page,4)
    expect(page.locator('.partner-name')).to_have_text('Riley')
    record('Hidden-page publication holds its visible-time sequence and resumes without skipping the three weights')
    context.close()

    audio_script='''window.oscillatorStarts=0;const old=AudioContext.prototype.createOscillator;
    AudioContext.prototype.createOscillator=function(){const oscillator=old.call(this);const start=oscillator.start.bind(oscillator);oscillator.start=(...args)=>{window.oscillatorStarts++;return start(...args)};return oscillator};'''
    context,page=start(browser,script=audio_script,clock=False)
    expect(page.get_by_role('button',name='Choose priorities',exact=True)).to_be_visible(timeout=12000)
    choose(page);weights(page,[70,20,10])
    page.evaluate('''window.publicationTimes=[];window.resultTimes=[];
    new MutationObserver(records=>{for(const record of records){
      if(record.attributeName==='data-published'&&record.target.dataset.published==='true')window.publicationTimes.push(performance.now());
      if(record.attributeName==='data-shown'&&record.target.dataset.shown==='true')window.resultTimes.push(performance.now());
    }}).observe(document.body,{subtree:true,attributes:true,attributeFilter:['data-published','data-shown']});
    window.runStarted=performance.now();''')
    page.get_by_role('button',name='Run evaluation',exact=True).click()
    expect(page.get_by_role('button',name='Finish partner scene',exact=True)).to_be_visible(timeout=8000)
    times=page.evaluate('window.publicationTimes.map(time=>time-window.runStarted)')
    assert len(times)==3 and times[0]>=450 and all(400<=times[i+1]-times[i]<=1600 for i in range(2)),times
    assert page.evaluate('window.oscillatorStarts')>0
    page.get_by_role('button',name='Sound on',exact=True).click();muted=page.evaluate('window.oscillatorStarts')
    page.get_by_role('button',name='Finish partner scene',exact=True).click()
    expect(page.locator('.l3-run-rows [data-shown=true]')).to_have_count(3,timeout=6500)
    result_times=page.evaluate('window.resultTimes')
    assert len(result_times)==3 and all(550<=result_times[i+1]-result_times[i]<=1600 for i in range(2)),result_times
    assert page.evaluate('window.oscillatorStarts')==muted
    record('Real-time publication and evidence arrive one at a time; Web Audio cues play and Sound off silences later updates')
    context.close();browser.close()
assert not errors,errors
record('No browser errors in partner, chapter handoff or real-time audio checks')
(OUT/'level3-integration-results.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'runtimeErrors':errors},indent=2)+'\n')
