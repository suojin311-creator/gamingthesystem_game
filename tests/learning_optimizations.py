"""Focused production coverage for positive weights, forecasts, social practice and growth."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
OUT=Path('test-results');OUT.mkdir(exist_ok=True)
HTML={str(level):Path(f'dist-level{level}/index.html').read_bytes() for level in [2,3]}
checks,errors=[],[]
def record(text):checks.append(text);print('PASS',text,flush=True)
def advance(page,seconds=8):
 for _ in range(seconds):page.clock.run_for(1000);page.wait_for_timeout(12)
def start(browser,level=3,width=1366,motion='reduce'):
 context=browser.new_context(viewport={'width':width,'height':900 if width>520 else 844},reduced_motion=motion)
 context.set_offline(True);context.route('https://learning.test/**',lambda route:route.fulfill(status=200,content_type='text/html',body=HTML[str(level)]))
 page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.clock.install();page.goto('https://learning.test/',wait_until='networkidle');advance(page,5)
 page.get_by_role('button',name='Choose priorities' if level==3 else 'Choose three metrics',exact=True).click()
 for id in ['prep','part','focus']:page.get_by_test_id(f'level{level}-metric-'+id).click()
 if level==3:page.get_by_role('button',name='Set the weights',exact=True).click()
 return context,page

def move(page,id,value):
 page.get_by_test_id('weight-card-'+id).locator('input').evaluate("(e,v)=>{Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(e,v);e.dispatchEvent(new Event('input',{bubbles:true}))}",value)
def split(page,values):
 for id,value in zip(['prep','part'],values):move(page,id,value);page.get_by_test_id('confirm-'+id).click()
 expect(page.locator('.l3-weight-value')).to_have_text([str(v)+'%' for v in values])
def forecast(page,picks):
 page.get_by_role('button',name='Make a prediction',exact=True).click();expect(page.get_by_role('button',name='Run evaluation',exact=True)).to_be_disabled()
 for id in picks:page.get_by_test_id('predict-'+id).click()
def scene(page):
 page.get_by_role('button',name='Observe the class',exact=True).click()
 while page.get_by_role('button',name='Continue scene',exact=True).count():page.get_by_role('button',name='Continue scene',exact=True).click()
 page.get_by_role('button',name='Return to dashboard',exact=True).click()
def result(page):
 page.get_by_role('button',name='Run evaluation',exact=True).click();page.locator('.l3-publish').scroll_into_view_if_needed();advance(page,5);scene(page)
 page.locator('.l3-results').scroll_into_view_if_needed();advance(page,12)
 page.locator('.l3-bottom-dialogue').scroll_into_view_if_needed();advance(page,9)
def observe2(page):
 scene(page);page.locator('.l2-observation-slot').scroll_into_view_if_needed();advance(page,8)
 page.locator('.conversation').scroll_into_view_if_needed();advance(page,9)
def six(page):
 page.get_by_role('button',name='Run evaluation',exact=True).click();advance(page,6);observe2(page)
 page.get_by_role('button',name='Cover the gaps',exact=True).click();page.get_by_role('button',name='Add remaining metrics',exact=True).click();advance(page,6)
def check_result(page,picks,most):
 assert [e.get_attribute('data-metric') for e in page.locator('.l3-run-rows [data-predicted=true]').all()]==picks
 assert [e.get_attribute('data-metric') for e in page.locator('.l3-run-rows [data-most=true]').all()]==most
 assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')

with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 context,page=start(browser)
 slider=page.get_by_test_id('weight-card-prep').locator('input');slider.press('End');expect(page.locator('.l3-weight-value')).to_have_text(['98%','1%','1%'])
 page.get_by_test_id('confirm-prep').click();expect(page.get_by_test_id('weight-card-part').locator('input')).to_have_attribute('max','1')
 page.get_by_test_id('confirm-focus').click();expect(page.get_by_test_id('weight-card-part')).to_have_attribute('data-auto-confirmed','true')
 page.get_by_role('button',name='Reset weights',exact=True).click();split(page,[61,38,1])
 expect(page.get_by_test_id('weight-card-focus').locator('input')).to_have_attribute('min','1')
 record('Keyboard and native slider bounds reserve at least 1%; 98/1/1 and 61/38/1 remain valid, with either final confirmation locking the pair')
 forecast(page,['prep','part']);page.get_by_test_id('predict-part').click()
 expect(page.get_by_test_id('predict-prep')).to_have_attribute('aria-pressed','true');expect(page.get_by_test_id('predict-part')).to_have_attribute('aria-pressed','false')
 page.get_by_role('button',name='Back to weights',exact=True).click();page.get_by_role('button',name='Make a prediction',exact=True).click()
 expect(page.locator('.l3-prediction-card[aria-pressed=true]')).to_have_count(0);expect(page.get_by_role('button',name='Run evaluation',exact=True)).to_be_disabled()
 page.get_by_test_id('predict-prep').focus();page.keyboard.press('Space');result(page);check_result(page,['prep'],['prep','part'])
 record('Forecasts require a deliberate selection, allow toggling and keyboard input, reset on re-entry and compare against tied actual effort without a correctness reward')
 before=page.get_by_role('progressbar',name='Management satisfaction').get_attribute('aria-valuenow')
 page.get_by_role('button',name='Replay scene',exact=True).click()
 while page.get_by_role('button',name='Continue scene',exact=True).count():page.get_by_role('button',name='Continue scene',exact=True).click()
 page.get_by_role('button',name='Return to dashboard',exact=True).click();page.locator('.l3-results').scroll_into_view_if_needed();advance(page,12);page.locator('.l3-bottom-dialogue').scroll_into_view_if_needed();advance(page,9)
 check_result(page,['prep'],['prep','part']);assert page.get_by_role('progressbar',name='Management satisfaction').get_attribute('aria-valuenow')==before
 page.get_by_role('button',name='Try another split',exact=True).click();split(page,[40,30,30]);forecast(page,['prep','part','focus']);result(page);check_result(page,['prep','part','focus'],['prep','part','focus'])
 page.get_by_role('button',name='Compare the patterns',exact=True).click();expect(page.locator('.l3-compare-table thead th[data-run]')).to_have_count(2)
 record('Replay preserves the recorded forecast and satisfaction; a fresh near-even prediction can select all three, and both actual tests reach comparison')
 context.close()
 for first,second,button,kind in [([70,20,10],[80,10,10],'What if they counted equally?','balance-check'),([34,33,33],[40,30,30],'What if one counted more?','contrast-check')]:
  context,page=start(browser)
  for index,values in enumerate([first,second]):
   if index:page.get_by_role('button',name='Try another split',exact=True).click()
   split(page,values);forecast(page,['focus']);result(page)
  page.get_by_role('button',name=button,exact=True).click();expect(page.locator('.level-three')).to_have_attribute('data-phase','predict')
  expect(page.get_by_role('button',name='Run evaluation',exact=True)).to_be_disabled();expect(page.locator('.l3-prediction-card[aria-pressed=true]')).to_have_count(0)
  page.get_by_test_id('predict-part').click();page.get_by_test_id('predict-focus').click();result(page)
  page.get_by_role('button',name='Compare the patterns',exact=True).click();expect(page.locator('.l3-compare-table thead th[data-run]')).to_have_count(3)
  expect(page.locator(f'.l3-compare-table thead th[data-kind="{kind}"]')).to_have_count(1)
  record(f'{kind} stays explicit, asks for its own forecast and retains both player tests alongside the reference')
  context.close()
 context,page=start(browser,level=2,motion='no-preference');six(page)
 page.get_by_role('button',name='Observe the class',exact=True).click()
 for beat in range(3):
  expect(page.locator('.l2-peer-practice')).to_have_attribute('data-beat',str(beat))
  if beat==1:expect(page.locator('.l2-scene-caption > span')).to_have_text('Classmate');expect(page.locator('.l2-phrase-copy')).to_be_visible()
  if beat==2:expect(page.locator('.l2-content-question')).to_be_visible();expect(page.locator('.l2-phrase-copy b')).to_have_text('✓')
  if beat<2:page.get_by_role('button',name='Continue scene',exact=True).click()
 page.screenshot(path='test-results/learning-peer-1366.png',full_page=True)
 page.get_by_role('button',name='Return to dashboard',exact=True).click();page.locator('.l2-observation-slot').scroll_into_view_if_needed();advance(page,8);page.locator('.conversation').scroll_into_view_if_needed();advance(page,9)
 record('The six-metric scene visibly shares and copies a scoring phrase, lets the classmate ask a content question and leaves it open while both collect ticks')
 page.get_by_role('button',name='Add more metrics',exact=True).click()
 page.evaluate("Object.defineProperty(document,'hidden',{configurable:true,value:true});document.dispatchEvent(new Event('visibilitychange'))")
 advance(page,8);expect(page.locator('.level-two')).to_have_attribute('data-round','10');expect(page.get_by_role('progressbar',name='Management satisfaction')).to_have_attribute('aria-valuenow','70')
 page.evaluate("delete document.hidden;document.dispatchEvent(new Event('visibilitychange'))");page.locator('.l2-counter').scroll_into_view_if_needed()
 seen=set();values=set()
 for _ in range(180):
  page.clock.run_for(200);page.wait_for_timeout(9)
  if page.locator('.l2-growth-action').count():
   page.locator('.l2-growth-action').scroll_into_view_if_needed();seen.add(page.locator('.l2-growth-action').get_attribute('data-growth'))
  values.add(page.get_by_role('progressbar',name='Management satisfaction').get_attribute('aria-valuenow'))
  if page.get_by_role('button',name='Observe the class',exact=True).count():break
 assert seen=={'10','25','100'},seen;assert values=={'70','77','82','86'},values
 expect(page.locator('.l2-matrix [data-active=true]')).to_have_count(100);expect(page.get_by_role('button',name='Add more metrics',exact=True)).to_have_count(0)
 advance(page,15);expect(page.locator('.level-two')).to_have_attribute('data-phase','observe');expect(page.locator('.level-two')).to_have_attribute('data-round','100')
 record('One growth action passes 10/25/100 and each satisfaction checkpoint; hidden time holds, no repeated Add button is needed and the final classroom observation still waits for a click')
 context.close()
 for width in [768,390,320]:
  context,page=start(browser,width=width);split(page,[70,20,10]);forecast(page,['focus'])
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth');page.screenshot(path=f'test-results/learning-predict-{width}.png',full_page=True)
  result(page);check_result(page,['focus'],['prep']);page.screenshot(path=f'test-results/learning-result-{width}.png',full_page=True);context.close()
  context,page=start(browser,level=2,width=width);six(page);page.get_by_role('button',name='Observe the class',exact=True).click();page.get_by_role('button',name='Continue scene',exact=True).click()
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  boxes=page.locator('.l2-peer-person,.l2-phrase-card,.l2-phrase-copy').evaluate_all('es=>es.map(e=>({x:e.getBoundingClientRect().x,y:e.getBoundingClientRect().y,r:e.getBoundingClientRect().right,b:e.getBoundingClientRect().bottom}))')
  if width<=520:assert all(boxes[i]['b']<boxes[1]['y'] for i in [0,3]),boxes
  page.screenshot(path=f'test-results/learning-peer-{width}.png',full_page=True);context.close()
  record(f'{width}px forecasts, result markers and peer scene fit without horizontal overflow; phone portraits remain clear of the phrase cards')
 browser.close()
assert not errors,errors
record('No runtime errors in offline forecasts, positive-weight extremes, reference routes, social scene or continuous growth')
(OUT/'learning-optimization-results.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'runtimeErrors':errors},indent=2)+'\n')
