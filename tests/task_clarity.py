"""Focused production checks for readable task prompts and unambiguous comparisons."""
import json,re
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
HTML=Path('dist-level3/index.html').read_bytes();checks=[];errors=[]
def record(text):checks.append(text);print('PASS',text,flush=True)
def advance(page,ms=8000):
 for _ in range(ms//500):page.clock.run_for(500);page.wait_for_timeout(8)
def move(page,id,value):
 page.get_by_test_id('weight-card-'+id).locator('input').evaluate("(e,v)=>{Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(e,v);e.dispatchEvent(new Event('input',{bubbles:true}))}",value)
def confirm(page):
 page.get_by_test_id('confirm-prep').click();page.get_by_test_id('confirm-peer').click()
def run(page):
 page.get_by_role('button',name='Run evaluation',exact=True).click();page.locator('.l3-publish').scroll_into_view_if_needed();advance(page,5000)
 page.get_by_role('button',name='Observe the class',exact=True).click()
 for _ in range(2):page.get_by_role('button',name='Continue scene',exact=True).click()
 page.get_by_role('button',name='Return to dashboard',exact=True).click();page.locator('.l3-results').scroll_into_view_if_needed();advance(page,14000)
 page.locator('.l3-bottom-dialogue').scroll_into_view_if_needed();advance(page,8000)
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 context=browser.new_context(viewport={'width':1366,'height':900},reduced_motion='no-preference');context.set_offline(True)
 context.route('https://clarity15.test/**',lambda route:route.fulfill(status=200,content_type='text/html',body=HTML))
 page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.clock.install();page.goto('https://clarity15.test/',wait_until='networkidle');advance(page,5000)
 page.get_by_role('button',name='Choose priorities',exact=True).click()
 for id in ['prep','part','peer']:page.get_by_test_id('level3-metric-'+id).click()
 page.get_by_role('button',name='Set the weights',exact=True).click();page.get_by_role('button',name='Skip guide',exact=True).click()
 prompt=page.locator('.l3-experiment');expect(prompt).to_have_attribute('data-attention','true')
 style=prompt.evaluate('e=>{const s=getComputedStyle(e);return {name:s.animationName,count:s.animationIterationCount,border:s.borderLeftWidth}}')
 assert style=={'name':'l3-task-attention','count':'3','border':'4px'},style
 page.evaluate("Object.defineProperty(document,'hidden',{configurable:true,value:true});document.dispatchEvent(new Event('visibilitychange'))")
 page.wait_for_function("getComputedStyle(document.querySelector('.l3-experiment')).animationPlayState==='paused'")
 page.wait_for_timeout(2600);expect(prompt).to_have_attribute('data-attention','true')
 page.evaluate("delete document.hidden;document.dispatchEvent(new Event('visibilitychange'))")
 expect(prompt).to_have_attribute('data-attention','false',timeout=4000)
 assert prompt.locator('p').evaluate('e=>parseFloat(getComputedStyle(e).fontSize)')>=21
 record('The task is a prominent 24px question card with a four-pixel accent and three finite pulses; hidden time pauses the animation and the card stays readable after it ends')
 move(page,'prep',43);page.get_by_test_id('confirm-prep').click();move(page,'part',29);page.get_by_test_id('confirm-part').click();run(page)
 page.get_by_role('button',name='Adjust the weights',exact=True).click()
 expect(prompt.locator('p')).to_have_text('What if Participation and Peer response counted more?')
 button=page.get_by_role('button',name='Apply suggested weights',exact=True);expect(button).to_be_visible();expect(prompt).to_contain_text('Sets the sliders; you confirm.')
 page.screenshot(path='test-results/task-clarity-prompt-1366.png',full_page=True)
 button.click();expect(page.locator('.l3-weight-value')).to_have_text(['34%','33%','33%']);expect(page.locator('.l3-weight-card[data-confirmed=true]')).to_have_count(0)
 expect(page.get_by_role('button',name='Run evaluation',exact=True)).to_be_disabled();expect(prompt).to_contain_text('Weights set. Adjust or confirm.');expect(prompt).to_have_attribute('data-attention','false')
 move(page,'prep',40);expect(page.locator('.l3-weight-value')).to_have_text(['40%','30%','30%']);button.click();confirm(page);run(page)
 record('The shorter targeted question and Apply suggested weights button load editable values, announce the result, stop the attention cue and still require manual confirmation')
 page.get_by_role('button',name='Test your explanation',exact=True).click();page.emulate_media(reduced_motion='reduce')
 assert prompt.evaluate('e=>getComputedStyle(e).animationName')=='l3-task-still'
 assert prompt.evaluate('e=>getComputedStyle(e).animationIterationCount')=='1'
 page.set_viewport_size({'width':320,'height':844});page.screenshot(path='test-results/task-clarity-prompt-320.png',full_page=True)
 assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
 button.click();expect(page.locator('.l3-weight-value')).to_have_text(['28%','43%','29%']);confirm(page);run(page)
 record('Reduced motion uses one steady outline, and the 320px task card and explicit suggestion button remain readable and usable')
 page.get_by_role('button',name='Compare the patterns',exact=True).click()
 expected={'prep':['baseline','same','less'],'part':['baseline','more','same'],'peer':['baseline','more','less']}
 for id,values in expected.items():
  cells=page.locator(f'.l3-compare-table tr[data-metric="{id}"] td')
  assert [c.get_attribute('data-effort-change') for c in cells.all()]==values
  for c,change in zip(cells.all(),values):
   expect(c.locator('.l3-effort-change')).to_contain_text({'baseline':'First result','same':'Same effort','more':'More effort','less':'Less effort'}[change])
   assert c.evaluate('e=>getComputedStyle(e).boxShadow')=='none'
   assert c.evaluate('e=>getComputedStyle(e).backgroundColor')=='rgba(0, 0, 0, 0)'
 expect(page.locator('.l3-comparison-basis')).to_have_text(['Starting observation','Effort vs First test','Effort vs Second test'])
 expect(page.locator('.l3-compare-table tr[data-metric="prep"] td[data-run="2"]')).to_contain_text('34%')
 expect(page.locator('.l3-compare-table tr[data-metric="part"] td[data-run="3"]')).to_contain_text('43%')
 record('The exact reported three-trial example names every comparison baseline and labels increases, decreases and equal effort even when weights change; ambiguous full-cell highlighting is removed')
 for width in [1366,768,390,320]:
  page.set_viewport_size({'width':width,'height':900 if width>520 else 844})
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  for cell in page.locator('.l3-compare-table tbody td').all():
   expect(cell.locator('.l3-effort-change')).to_be_visible()
   assert cell.locator('.l3-effort-change').evaluate('e=>e.scrollWidth<=e.clientWidth')
  page.screenshot(path=f'test-results/task-clarity-comparison-{width}.png',full_page=True)
 record('All three records, comparison bases and change labels fit 1366/768/390/320px without horizontal overflow')
 context.close();browser.close()
assert not errors,errors
record('No runtime errors in task animation, editable suggestions, three actual trials or responsive comparison')
Path('test-results/task-clarity-results.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'runtimeErrors':errors},indent=2)+'\n')
