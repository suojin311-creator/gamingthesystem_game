"""Feedback regression: scoped headings, direct trials, original scene slots and visible holds."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
OUT=Path('test-results');OUT.mkdir(exist_ok=True)
HTML={str(level):Path(f'dist-level{level}/index.html').read_bytes() for level in [1,2,3]}
checks,errors,holds=[],[],{}
def record(text):checks.append(text);print('PASS',text,flush=True)
def advance(page,ms=8000):
 for _ in range(ms//100):page.clock.run_for(100);page.wait_for_timeout(5)
def wait_until(page,condition,limit=25000):
 for _ in range(limit//100):
  if condition():return
  advance(page,100)
 assert condition(),'Visible-time condition did not complete'
def start(browser,level=3,width=1366,motion='reduce'):
 context=browser.new_context(viewport={'width':width,'height':900 if width>520 else 844},reduced_motion=motion)
 context.set_offline(True);context.route('https://feedback13.test/**',lambda route:route.fulfill(status=200,content_type='text/html',body=HTML[str(level)]))
 page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.clock.install();page.goto('https://feedback13.test/',wait_until='networkidle')
 if level==1:page.get_by_role('button',name='Skip guide',exact=True).click()
 else:advance(page,5000);page.get_by_role('button',name='Choose priorities' if level==3 else 'Choose three metrics',exact=True).click()
 return context,page

def choose(page,level):
 for id in ['prep','part','focus']:page.get_by_test_id(f'level{level}-metric-'+id).click()
 if level==3:page.get_by_role('button',name='Set the weights',exact=True).click()
def move(page,id,value):
 page.get_by_test_id('weight-card-'+id).locator('input').evaluate("(e,v)=>{Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(e,v);e.dispatchEvent(new Event('input',{bubbles:true}))}",value)
def split(page,values):
 for id,value in zip(['prep','part'],values):move(page,id,value);page.get_by_test_id('confirm-'+id).click()
 expect(page.locator('.l3-weight-value')).to_have_text([str(v)+'%' for v in values])
 expect(page.get_by_role('button',name='Make a prediction',exact=True)).to_have_count(0)
def scene(page):
 page.get_by_role('button',name='Observe the class',exact=True).click()
 while page.get_by_role('button',name='Continue scene',exact=True).count():page.get_by_role('button',name='Continue scene',exact=True).click()
 page.get_by_role('button',name='Return to dashboard',exact=True).click()
def finish_trial(page):
 page.locator('.l3-publish').scroll_into_view_if_needed();advance(page,5000);scene(page)
 page.locator('.l3-results').scroll_into_view_if_needed();advance(page,12000)
 page.locator('.l3-bottom-dialogue').scroll_into_view_if_needed();advance(page,9000)
 expect(page.locator('.l3-result-pick,.l3-most-label,.l3-prediction')).to_have_count(0)
def run(page):page.get_by_role('button',name='Run evaluation',exact=True).click();finish_trial(page)
def observe2(page):
 scene(page);page.locator('.l2-observation-slot').scroll_into_view_if_needed();advance(page,8000)
 page.locator('.conversation').scroll_into_view_if_needed();advance(page,9000)

with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for level in [1,2,3]:
  for width in [1366,768,390,320]:
   context,page=start(browser,level,width)
   heading=page.locator('.workbench-heading' if level==1 else f'.l{level}-heading')
   expect(heading.locator('h1')).to_be_visible();expect(heading.locator('.chapter-number')).to_have_text(f'0{level}')
   box=heading.bounding_box();assert 50<=box['height']<100,(level,width,box)
   assert float(heading.locator('h1').evaluate('e=>getComputedStyle(e).fontSize').replace('px',''))<=31
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
   if level==1 and width in [1366,320]:page.screenshot(path=f'test-results/feedback13-header-{width}.png',full_page=True)
   context.close()
  record(f'Level {level} headings remain visible and compact at 1366/768/390/320px; transition styles cannot hide or enlarge the workbench title')
 context,page=start(browser);choose(page,3)
 page.get_by_test_id('weight-card-prep').locator('input').press('End');expect(page.locator('.l3-weight-value')).to_have_text(['98%','1%','1%'])
 page.get_by_test_id('confirm-prep').click();page.get_by_test_id('confirm-focus').click();page.get_by_role('button',name='Reset weights',exact=True).click()
 split(page,[61,38,1]);run(page)
 expect(page.locator('.l3-result-legend')).not_to_contain_text('PREDICTION')
 page.get_by_role('button',name='Try another split',exact=True).click();split(page,[40,30,30]);run(page)
 page.get_by_role('button',name='Compare the patterns',exact=True).click();expect(page.locator('.l3-compare-table thead th[data-run]')).to_have_count(2)
 record('Positive-weight bounds remain enforced; confirming runs directly into publication and two actual trials compare without any forecast screen or prediction column')
 context.close()
 for first,second,button,kind in [([70,20,10],[80,10,10],'What if they counted equally?','balance-check'),([34,33,33],[40,30,30],'What if one counted more?','contrast-check')]:
  context,page=start(browser);choose(page,3)
  for index,values in enumerate([first,second]):
   if index:page.get_by_role('button',name='Try another split',exact=True).click()
   split(page,values);run(page)
  page.get_by_role('button',name=button,exact=True).click();expect(page.locator('.level-three')).to_have_attribute('data-phase','publish');finish_trial(page)
  page.get_by_role('button',name='Compare the patterns',exact=True).click();expect(page.locator('.l3-compare-table thead th[data-run]')).to_have_count(3)
  expect(page.locator(f'.l3-compare-table thead th[data-kind="{kind}"]')).to_have_count(1)
  record(f'{kind} publishes directly after its explicit action and preserves both player attempts plus the reference')
  context.close()
 context,page=start(browser,2,motion='no-preference');choose(page,2)
 page.get_by_role('button',name='Run evaluation',exact=True).click();advance(page,6000);observe2(page)
 page.get_by_role('button',name='Cover the gaps',exact=True).click();page.get_by_role('button',name='Add remaining metrics',exact=True).click();advance(page,6000)
 page.get_by_role('button',name='Observe the class',exact=True).click()
 expect(page.get_by_test_id('level2-cinematic')).to_be_visible();expect(page.locator('.l2-peer-practice')).to_have_count(0)
 expect(page.get_by_role('heading',name='A new classroom routine.',exact=True)).to_have_count(0)
 for _ in range(2):page.get_by_role('button',name='Continue scene',exact=True).click()
 page.get_by_role('button',name='Return to dashboard',exact=True).click();page.locator('.l2-observation-slot').scroll_into_view_if_needed();advance(page,8000);page.locator('.conversation').scroll_into_view_if_needed();advance(page,9000)
 record('The six-metric placeholder uses the original simple scene; no added peer demonstration or new scene title remains')
 page.evaluate("""() => {
   window.growthEvents = [];
   const record = () => {
     const root = document.querySelector('.level-two');
     const action = document.querySelector('.l2-growth-action');
     const state = `${root.dataset.round}:${root.dataset.phase}:${action?.dataset.beat || ''}`;
     if (window.growthEvents.at(-1)?.state !== state)
       window.growthEvents.push({state, t: performance.now(), hidden: document.hidden});
   };
   new MutationObserver(record).observe(document.body, {subtree: true, childList: true, attributes: true});
   document.addEventListener('visibilitychange', () => {
     window.growthEvents.push({state: document.hidden ? 'hide' : 'show', t: performance.now(), hidden: document.hidden});
   });
 }""")
 page.get_by_role('button',name='Add more metrics',exact=True).click()
 values={'70'}
 for count in [10,25]:
  wait_until(page,lambda:page.locator(f'.l2-growth-action[data-growth="{count}"][data-beat="3"]').count()>0)
  page.locator('.l2-growth-action').scroll_into_view_if_needed();values.add(page.get_by_role('progressbar',name='Management satisfaction').get_attribute('aria-valuenow'))
  if count==10:
   page.evaluate("Object.defineProperty(document,'hidden',{configurable:true,value:true});document.dispatchEvent(new Event('visibilitychange'))")
   advance(page,8000);expect(page.locator('.level-two')).to_have_attribute('data-round','10')
   page.evaluate("delete document.hidden;document.dispatchEvent(new Event('visibilitychange'))")
  advance(page,2000);expect(page.locator('.level-two')).to_have_attribute('data-round',str(count))
  wait_until(page,lambda:page.locator('.level-two').get_attribute('data-round')!=str(count),3000)
  events=page.evaluate('growthEvents')
  begin=next(i for i,event in enumerate(events) if event['state']==f'{count}:observe:3')
  finish=next(i for i in range(begin+1,len(events)) if events[i]['state'].endswith(':evaluate:'))
  # Measure from the DOM's completed action, rather than a later scroll/assertion.
  # Browser scrolling itself consumes real time even while the test clock is installed.
  elapsed=sum(events[i+1]['t']-events[i]['t'] for i in range(begin,finish) if not events[i]['hidden'])
  assert 3400<=elapsed<=4100,(count,elapsed,events[begin:finish+1])
  holds[str(count)]=elapsed
 wait_until(page,lambda:page.get_by_role('button',name='Observe the class',exact=True).count()>0)
 values.add(page.get_by_role('progressbar',name='Management satisfaction').get_attribute('aria-valuenow'));assert values=={'70','77','82','86'},values
 expect(page.locator('.l2-matrix [data-active=true]')).to_have_count(100);advance(page,10000)
 expect(page.locator('.level-two')).to_have_attribute('data-phase','observe');expect(page.locator('.level-two')).to_have_attribute('data-round','100')
 record('The first two completed growth actions each hold about 3.5 visible seconds, pause in hidden tabs, retain every satisfaction checkpoint and still wait for Observe at 100')
 context.close()
 for width in [390,320]:
  context,page=start(browser,3,width);choose(page,3);split(page,[70,20,10]);run(page)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth');page.screenshot(path=f'test-results/feedback13-results-{width}.png',full_page=True);context.close()
 record('Restored three-column result layouts fit 390px and 320px with the prediction layer removed')
 browser.close()
assert not errors,errors
record('No runtime errors in scoped headers, positive bounds, direct trials, original scenes or longer growth holds')
(OUT/'learning-optimization-results.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'growthHoldsMs':holds,'runtimeErrors':errors},indent=2)+'\n')
