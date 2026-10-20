"""Offline production checks for three purposeful trials, live controls and smooth escalation."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
OUT=Path('test-results');OUT.mkdir(exist_ok=True)
HTML={str(level):Path(f'dist-level{level}/index.html').read_bytes() for level in [1,2,3]}
checks,errors,timings=[],[],{}
def record(text):checks.append(text);print('PASS',text,flush=True)
def advance(page,ms=8000):
 for _ in range(ms//100):page.clock.run_for(100);page.wait_for_timeout(3)
def until(page,condition,limit=25000):
 for _ in range(limit//100):
  if condition():return
  advance(page,100)
 assert condition(),'Visible-time sequence did not complete'
def start(browser,level=3,width=1366,motion='reduce'):
 context=browser.new_context(viewport={'width':width,'height':900 if width>520 else 844},reduced_motion=motion)
 context.set_offline(True);context.route('https://scaffold14.test/**',lambda route:route.fulfill(status=200,content_type='text/html',body=HTML[str(level)]))
 page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.clock.install();page.goto('https://scaffold14.test/',wait_until='networkidle')
 if level==1:page.get_by_role('button',name='Skip guide',exact=True).click()
 else:advance(page,5000);page.get_by_role('button',name='Choose priorities' if level==3 else 'Choose three metrics',exact=True).click()
 return context,page
def choose(page,level=3):
 for id in ['prep','part','focus']:page.get_by_test_id(f'level{level}-metric-'+id).click()
 if level==3:page.get_by_role('button',name='Set the weights',exact=True).click()
def move(page,id,value):
 page.get_by_test_id('weight-card-'+id).locator('input').evaluate("(e,v)=>{Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(e,v);e.dispatchEvent(new Event('input',{bubbles:true}))}",value)
def split(page,values):
 for id,value in zip(['prep','part'],values):move(page,id,value);page.get_by_test_id('confirm-'+id).click()
 expect(page.locator('.l3-weight-value')).to_have_text([str(value)+'%' for value in values])
def scene(page):
 page.get_by_role('button',name='Observe the class',exact=True).click()
 while page.get_by_role('button',name='Continue scene',exact=True).count():page.get_by_role('button',name='Continue scene',exact=True).click()
 page.get_by_role('button',name='Return to dashboard',exact=True).click()
def run(page):
 page.get_by_role('button',name='Run evaluation',exact=True).click();page.locator('.l3-publish').scroll_into_view_if_needed();advance(page,5000);scene(page)
 page.locator('.l3-results').scroll_into_view_if_needed();advance(page,12000);page.locator('.l3-bottom-dialogue').scroll_into_view_if_needed();advance(page,8000)
def finish2(page):
 scene(page);page.locator('.l2-observation-slot').scroll_into_view_if_needed();advance(page,8000);page.locator('.conversation').scroll_into_view_if_needed();advance(page,8000)
def growth(page):
 choose(page,2);page.get_by_role('button',name='Run evaluation',exact=True).click();advance(page,6000);finish2(page)
 page.get_by_role('button',name='Cover the gaps',exact=True).click();page.get_by_role('button',name='Add remaining metrics',exact=True).click();advance(page,6000);finish2(page)
 page.get_by_role('button',name='Add more metrics',exact=True).click()
def hide(page,hidden):
 page.evaluate("Object.defineProperty(document,'hidden',{configurable:true,value:true});document.dispatchEvent(new Event('visibilitychange'))" if hidden else "delete document.hidden;document.dispatchEvent(new Event('visibilitychange'))")

with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 context,page=start(browser);choose(page)
 expect(page.get_by_role('complementary',name='Weight guide')).to_have_attribute('data-step','0')
 page.get_by_test_id('weight-card-prep').locator('input').press('ArrowRight')
 expect(page.locator('.l3-weight-guide')).to_have_attribute('data-step','1')
 expect(page.get_by_test_id('weight-card-prep')).to_have_attribute('data-guide','confirm')
 move(page,'prep',80);expect(page.get_by_role('button',name='Run evaluation',exact=True)).to_be_disabled()
 page.get_by_test_id('confirm-prep').click();expect(page.locator('.l3-weight-guide')).to_have_attribute('data-step','2')
 move(page,'part',15);expect(page.locator('.l3-weight-value')).to_have_text(['80%','15%','5%'])
 page.get_by_test_id('confirm-focus').click();expect(page.locator('.l3-weight-guide')).to_have_attribute('data-step','3')
 expect(page.get_by_test_id('confirm-part')).to_have_text('Auto-confirmed');expect(page.get_by_role('button',name='Run evaluation',exact=True)).to_be_enabled()
 run(page);expect(page.locator('.l3-weight-guide')).to_have_count(0)
 expect(page.locator('.l3-row-weight')).to_have_text(['80%','15%','5%'])
 page.get_by_role('button',name='Adjust the weights',exact=True).click();expect(page.locator('.l3-weight-guide')).to_have_count(0)
 expect(page.locator('.l3-weight-value')).to_have_text(['80%','15%','5%'])
 page.get_by_role('button',name='Guide',exact=True).click();expect(page.locator('.l3-weight-guide')).to_have_attribute('data-step','0')
 page.get_by_role('button',name='Skip guide',exact=True).click();move(page,'prep',40)
 page.get_by_role('button',name='Guide',exact=True).click();expect(page.locator('.l3-weight-guide')).to_have_attribute('data-step','1')
 page.keyboard.press('Escape');expect(page.locator('.l3-weight-guide')).to_have_count(0);expect(page.locator('.l3-weight-value')).to_have_text(['40%','30%','30%'])
 record('The once-per-visit guide follows real keyboard/slider/confirmation actions, explains the linked pair, preserves actual first-trial values and supports Skip, Escape and reopening without resetting weights')
 context.close()
 routes=[('one-higher',[70,20,10],[34,33,33],[20,60,20],'redirect'),('two-higher',[45,45,10],[34,33,33],[10,45,45],'redirect'),('near-even',[34,33,33],[70,20,10],[20,60,20],'redirect'),('both-uneven',[70,20,10],[45,45,10],[31,35,34],'balance'),('both-near-even',[34,33,33],[40,30,30],[61,38,1],'contrast')]
 for name,first,second,third,purpose in routes:
  context,page=start(browser);choose(page);split(page,first);run(page)
  page.get_by_role('button',name='Adjust the weights',exact=True).click();expect(page.locator('.l3-experiment')).to_have_attribute('data-purpose','adjust')
  expect(page.locator('.l3-weight-guide')).to_have_count(0);split(page,second);run(page)
  expect(page.get_by_role('button',name='Compare the patterns',exact=True)).to_have_count(0)
  page.get_by_role('button',name='Test your explanation',exact=True).click();expect(page.locator('.l3-experiment')).to_have_attribute('data-purpose',purpose)
  expect(page.locator('.l3-weight-value')).to_have_text([str(v)+'%' for v in second])
  page.get_by_role('button',name='Apply suggested weights',exact=True).click();expect(page.get_by_role('button',name='Run evaluation',exact=True)).to_be_disabled()
  page.get_by_role('button',name='Reset weights',exact=True).click();expect(page.locator('.l3-weight-value')).to_have_text([str(v)+'%' for v in second])
  split(page,third);run(page);page.get_by_role('button',name='Compare the patterns',exact=True).click()
  expect(page.locator('.l3-compare-table thead th[data-kind="player"]')).to_have_count(3);expect(page.locator('.l3-compare-table thead th[data-run="3"]')).to_contain_text('Third test')
  for round,values in enumerate([first,second,third],1):expect(page.locator(f'.l3-compare-table td[data-run="{round}"] .l3-row-weight')).to_have_text([str(v)+'%' for v in values])
  page.get_by_role('button',name='Step back and reflect',exact=True).click()
  page.get_by_role('button',name='Continue scene',exact=True).click();page.get_by_role('button',name='Continue scene',exact=True).click();page.get_by_role('button',name='Reveal Goodhart’s Law',exact=True).click()
  expect(page.locator('.level-three')).to_have_attribute('data-phase','theory')
  record(f'{name}: three distinct player-confirmed tests use the {purpose} verification, retain every actual trial and reach the existing theory placeholder')
  context.close()
 for width in [1366,768,390,320]:
  context,page=start(browser,width=width);choose(page)
  page.screenshot(path=f'test-results/scaffolding-guide-{width}.png',full_page=True)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  expect(page.locator('.l3-heading h1')).to_be_visible();assert page.locator('.l3-heading').bounding_box()['height']<100
  page.get_by_role('button',name='Skip guide',exact=True).click();split(page,[34,33,33])
  page.get_by_role('button',name='Guide',exact=True).click();expect(page.locator('.l3-weight-guide')).to_have_attribute('data-step','3')
  page.get_by_role('button',name='Reset weights',exact=True).click();expect(page.locator('.l3-weight-guide')).to_have_attribute('data-step','0')
  page.get_by_role('button',name='Skip guide',exact=True).click()
  context.close()
 record('Guide, skipped/default confirmations, reopening and reset remain usable at 1366/768/390/320px without overflow or hidden headers')
 context,page=start(browser,2,motion='no-preference');growth(page)
 until(page,lambda:page.locator('.l2-growth-action[data-growth="10"][data-beat="3"]').count()>0)
 page.locator('.l2-checklist').scroll_into_view_if_needed()
 page.evaluate("""() => {
  window.growthNodes=[document.querySelector('.l2-counter'),document.querySelector('.l2-matrix'),document.querySelector('.l2-checklist')];
  window.growthEvents=[];
  const record=()=>{const root=document.querySelector('.level-two'),seq=document.querySelector('.l2-growth-sequence'),action=document.querySelector('.l2-growth-action');const state=`${root.dataset.round}:${seq?.dataset.state}:${action?.dataset.beat}`;
   if(window.growthEvents.at(-1)?.state!==state)window.growthEvents.push({state,t:performance.now(),hidden:document.hidden,scroll:scrollY});};
  new MutationObserver(record).observe(document.body,{subtree:true,attributes:true,childList:true});record();
  document.addEventListener('visibilitychange',()=>window.growthEvents.push({state:document.hidden?'hide':'show',t:performance.now(),hidden:document.hidden,scroll:scrollY}));
 }""")
 # Observe the next completed state from its actual start for precise hold timing.
 until(page,lambda:page.locator('.l2-growth-sequence').get_attribute('data-state')=='leaving',6000)
 expect(page.locator('.l2-growth-beats [data-next=true]')).to_have_text('25')
 page.screenshot(path='test-results/scaffolding-growth-leaving.png',full_page=True)
 hide(page,True);advance(page,8000);expect(page.locator('.level-two')).to_have_attribute('data-round','10')
 assert page.locator('.l2-growth-action').evaluate('e=>getComputedStyle(e).animationPlayState')=='paused'
 hide(page,False)
 until(page,lambda:page.locator('.l2-growth-action[data-growth="25"][data-beat="3"]').count()>0)
 page.evaluate('window.geometry={scroll:scrollY,rect:document.querySelector(".l2-checklist").getBoundingClientRect().toJSON()}')
 assert page.evaluate('growthNodes.every(e=>e.isConnected)')
 until(page,lambda:page.locator('.l2-growth-sequence').get_attribute('data-state')=='leaving',6000)
 before=page.evaluate('({scroll:scrollY,rect:document.querySelector(".l2-checklist").getBoundingClientRect().toJSON()})')
 assert abs(before['scroll']-page.evaluate('geometry.scroll'))<=1
 expect(page.locator('.l2-growth-beats [data-next=true]')).to_have_text('100')
 until(page,lambda:page.locator('.level-two').get_attribute('data-round')=='100',2000)
 after=page.evaluate('({scroll:scrollY,rect:document.querySelector(".l2-checklist").getBoundingClientRect().toJSON()})')
 assert abs(before['scroll']-after['scroll'])<=1,(before,after)
 assert abs(before['rect']['height']-after['rect']['height'])<=1,(before,after)
 assert page.evaluate('growthNodes.every(e=>e.isConnected)')
 events=page.evaluate('growthEvents');begin=next(i for i,e in enumerate(events) if e['state']=='25:shown:3');leave=next(i for i,e in enumerate(events) if e['state']=='25:leaving:3')
 hold=events[leave]['t']-events[begin]['t'];assert 3400<=hold<=4000,hold
 end=next(i for i in range(leave+1,len(events)) if events[i]['state'].startswith('100:'))
 turn=events[end]['t']-events[leave]['t'];assert 650<=turn<=1100,turn
 timings.update(holdMs=hold,turnMs=turn)
 until(page,lambda:page.get_by_role('button',name='Observe the class',exact=True).count()>0)
 expect(page.locator('.l2-matrix [data-active=true]')).to_have_count(100)
 advance(page,9000);expect(page.locator('.level-two')).to_have_attribute('data-phase','observe');expect(page.locator('.level-two')).to_have_attribute('data-round','100')
 record('Normal-motion escalation preserves the same counter/matrix/paper nodes, scroll and card height, holds content for 3.5 seconds, anticipates each next node and turns for 0.7 seconds; hidden tabs pause the turn and 100 still waits for Observe')
 context.close()
 context,page=start(browser,2,width=320,motion='reduce');growth(page)
 phone_geometry=[]
 for count in [10,25,100]:
  until(page,lambda:page.locator(f'.l2-growth-action[data-growth="{count}"][data-beat="3"]').count()>0,16000)
  phone_geometry.append(page.evaluate('({scroll:scrollY,height:document.querySelector(".l2-checklist").getBoundingClientRect().height})'))
  assert page.locator('.l2-growth-action').evaluate('e=>getComputedStyle(e).animationName')=='none'
  if count==25:page.screenshot(path='test-results/scaffolding-growth-reduced-320.png',full_page=True)
 assert max(g['height'] for g in phone_geometry)-min(g['height'] for g in phone_geometry)<=1,phone_geometry
 # Native viewport settling may move a few pixels; a line-sized jump must fail.
 assert max(g['scroll'] for g in phone_geometry)-min(g['scroll'] for g in phone_geometry)<=8,phone_geometry
 assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
 until(page,lambda:page.get_by_role('button',name='Observe the class',exact=True).count()>0)
 timings['phoneGeometry']=phone_geometry
 record('At 320px, all three growth states keep the same paper height and retain the reading position within 8px despite caption wrapping; reduced motion keeps the holds and final manual Observe with no moving paper')
 context.close();browser.close()
assert not errors,errors
record('No runtime errors in guide actions, all adaptive third-test routes, original placeholder endpoints or continuous escalation')
(OUT/'learning-optimization-results.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'timings':timings,'runtimeErrors':errors},indent=2)+'\n')
