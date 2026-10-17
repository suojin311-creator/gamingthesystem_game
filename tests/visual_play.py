"""Production checks for compact cards, selection trays and visible consequences."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

OUT=Path('test-results');OUT.mkdir(exist_ok=True)
ART={i:Path(f'dist-level{i}/index.html').read_bytes() for i in [1,2,3]}
checks,errors=[],[]
IDS=['prep','part','focus','discuss','reflect','peer']
SHORT=['Preparation','Participation','Focus','Discussion','Reflection','Peer response']


def record(text):checks.append(text);print('PASS',text,flush=True)


def advance(page,seconds=10):
 for _ in range(seconds):page.clock.run_for(1000);page.wait_for_timeout(15)


def open_game(browser,level,width=1366,motion='reduce'):
 context=browser.new_context(viewport={'width':width,'height':1000},reduced_motion=motion)
 context.set_offline(True);context.route('https://visual.test/**',lambda r:r.fulfill(status=200,content_type='text/html',body=ART[level]))
 page=context.new_page();page.on('pageerror',lambda error:errors.append(str(error)));page.clock.install()
 page.goto('https://visual.test/',wait_until='networkidle')
 if level==1:page.get_by_role('button',name='Skip guide',exact=True).click()
 else:
  advance(page);page.get_by_role('button',name='Choose three metrics' if level==2 else 'Choose priorities',exact=True).click()
 return context,page


def card(page,level,id):return page.get_by_test_id(('' if level==1 else f'level{level}-')+'metric-'+id)


def fit(page):
 assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
 assert page.locator('.choice-card p').count()==0
 for element in page.locator('.choice-card, .choice-slot').all():
  assert element.evaluate('e=>e.scrollWidth<=e.clientWidth+1'),element.evaluate('e=>({html:e.outerHTML,width:e.clientWidth,scroll:e.scrollWidth})')


def finish_scene(page,shots=3):
 for _ in range(shots-1):page.get_by_role('button',name='Continue scene',exact=True).click()
 page.get_by_role('button',name='Return to dashboard',exact=True).click();advance(page,24)


def weights(page,values):
 for index,id in enumerate(IDS[:2]):
  page.get_by_test_id('weight-card-'+id).locator('input').evaluate("(e,v)=>{Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(e,v);e.dispatchEvent(new Event('input',{bubbles:true}));}",values[index])
  page.get_by_test_id('confirm-'+id).click()


def run_three(page):
 page.get_by_role('button',name='Run evaluation',exact=True).click();page.locator('.l3-publish').scroll_into_view_if_needed();advance(page,5)
 expect(page.locator('.task-scene')).to_have_count(0)
 page.get_by_role('button',name='Observe the class',exact=True).click();finish_scene(page)


with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width in [1366,768,390,320]:
  for level in [1,2,3]:
   context,page=open_game(browser,level,width)
   expect(page.locator('.choice-card h3')).to_have_text(SHORT)
   expect(page.locator('.choice-slots li')).to_have_count(1 if level==1 else 3)
   for index,id in enumerate(IDS):
    expect(card(page,level,id)).to_have_attribute('aria-label',['Pre-class Preparation','In-class Participation','On-task Focus','In-class Discussion Quality','Learning Reflection Quality','Online Peer Response Quality'][index])
   card(page,level,'prep').focus();page.keyboard.press('Enter')
   expect(page.locator('.choice-slot[data-filled=true]')).to_have_count(1)
   expect(page.locator('.choice-detail strong')).to_have_text('Pre-class Preparation')
   expect(page.locator('.choice-detail p')).to_have_text('Finish the preparation.')
   page.get_by_role('button',name='Remove Preparation',exact=True).click()
   expect(card(page,level,'prep')).to_have_attribute('aria-pressed','false')
   expect(page.locator('.choice-slot[data-filled=true]')).to_have_count(0)
   for id in (['prep'] if level==1 else IDS[:3]):card(page,level,id).click()
   if level!=1:
    card(page,level,'discuss').dispatch_event('click')
    expect(page.locator('.choice-hint')).to_contain_text('Deselect one')
    expect(page.locator('.choice-slot[data-filled=true]')).to_have_count(3)
    page.get_by_role('button',name='Review Preparation',exact=True).click()
    expect(page.locator('.choice-detail strong')).to_have_text('Pre-class Preparation')
    page.get_by_role('button',name='Remove Participation',exact=True).click();card(page,level,'peer').click()
    expect(page.locator('.choice-detail strong')).to_have_text('Online Peer Response Quality')
   expect(page.locator('.action-row')).not_to_contain_text('Choose 1 of 6')
   assert not page.locator('.action-row').evaluate("e=>Array.from(e.children).some(c=>c.tagName!=='BUTTON'&&c.textContent.trim())")
   fit(page)
   if width in [1366,320]:page.screenshot(path=str(OUT/f'visual-choice-level{level}-{width}.png'),full_page=True,animations='disabled')
   context.close()
  record(f'{width}px: all three levels show six short icon cards, correct empty/filled slots, keyboard selection, removal, full-definition review and no repeated footer hints or overflow')

 context,page=open_game(browser,1)
 card(page,1,'prep').click();page.get_by_role('button',name='Make a prediction',exact=True).click()
 page.get_by_label('What do you expect students to do?').fill('Understand the reading.')
 page.get_by_role('button',name='Run evaluation',exact=True).click();advance(page,8)
 expect(page.locator('.action-row')).not_to_contain_text('Ready to visit')
 page.get_by_role('button',name='Observe the class',exact=True).click();finish_scene(page)
 expect(page.locator('.observation-copy')).to_have_text('Students complete the preparation, but some skim just enough to meet the requirement.')
 expect(page.locator('.observation-copy strong')).to_have_text('but some skim just enough to meet the requirement.')
 expect(page.locator('.observation-notebook > span')).to_have_count(1)
 page.screenshot(path=str(OUT/'visual-level1-observation.png'),full_page=True,animations='disabled');context.close()
 record('Level 1 retains the player prediction and actual evidence, with a task vignette and separate visual emphasis for the behavioural consequence')

 context,page=open_game(browser,2)
 for id in IDS[:3]:card(page,2,id).click()
 page.get_by_role('button',name='Run evaluation',exact=True).click();advance(page,6)
 expect(page.locator('.l2-eval-name')).to_have_text(SHORT[:3]);expect(page.locator('.l2-evaluation .observation-notebook')).to_have_count(0)
 page.get_by_role('button',name='Observe the class',exact=True).click();finish_scene(page)
 expect(page.locator('.observation-copy')).to_have_text('Students look prepared, active and focused. Some focus only on what gets checked.')
 expect(page.locator('.observation-notebook > span')).to_have_count(3)
 expect(page.locator('.observation-outside > .icon')).to_have_count(3)
 page.screenshot(path=str(OUT/'visual-level2-observation.png'),full_page=True,animations='disabled')
 page.get_by_role('button',name='Cover the gaps',exact=True).click();page.get_by_role('button',name='Add remaining metrics',exact=True).click();advance(page,6)
 page.get_by_role('button',name='Observe the class',exact=True).click();finish_scene(page)
 expect(page.locator('.observation-notebook > span')).to_have_count(6)
 expect(page.locator('.observation-outside')).to_have_count(0)
 record('Level 2 core reports use short names; observation clearly distinguishes the three tracked and three untracked areas, then all six, with shorter two-part evidence')
 for count in [10,25,100]:
  page.get_by_role('button',name='Add more metrics',exact=True).click();advance(page,15)
  expect(page.locator('.l2-matrix [data-active=true]')).to_have_count(count)
  expect(page.locator('.l2-checklist-stack')).to_have_attribute('data-load',str(count))
  expect(page.locator('.l2-checklist-stack li[data-shown=true]')).to_have_count(3)
  pseudo=page.locator('.l2-checklist-stack').evaluate("e=>[getComputedStyle(e,'::before').opacity,getComputedStyle(e,'::after').opacity]")
  assert pseudo==(['0','0'] if count==10 else ['1','0'] if count==25 else ['1','1']),pseudo
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  page.screenshot(path=str(OUT/f'visual-level2-pile-{count}.png'),full_page=True,animations='disabled')
 context.close();record('10 → 25 → 100 grows the checkbox field and physical paper pile; each existing action still reveals and ticks in order')

 for width in [1366,768,390,320]:
  context,page=open_game(browser,3,width)
  for id in IDS[:3]:card(page,3,id).click()
  page.get_by_role('button',name='Set the weights',exact=True).click();weights(page,[70,20,10]);run_three(page)
  expect(page.locator('.task-scene-high')).to_have_count(1);expect(page.locator('.task-scene-low')).to_have_count(2)
  expect(page.locator('.l3-effort-label')).to_have_text(['Intense effort','Minimum effort','Minimum effort'])
  for row in page.locator('.l3-run-rows li').all():
   assert row.get_attribute('data-effort') in row.locator('.task-scene').get_attribute('class')
  page.screenshot(path=str(OUT/f'visual-level3-result-{width}.png'),full_page=True,animations='disabled')
  page.get_by_role('button',name='Try another split',exact=True).click();weights(page,[34,33,33]);run_three(page)
  page.get_by_role('button',name='Compare the patterns',exact=True).click();advance(page,3)
  expect(page.locator('.task-scene')).to_have_count(6)
  expect(page.locator('.task-scene-medium')).to_have_count(3)
  expect(page.locator('.near-even .l3-row-weight')).to_have_text(['34%','33%','33%'])
  expect(page.locator('.uneven .l3-row-weight')).to_have_text(['70%','20%','10%'])
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  page.screenshot(path=str(OUT/f'visual-level3-compare-{width}.png'),full_page=True,animations='disabled');context.close()
  record(f'{width}px: each revealed Alex vignette matches the actual qualitative effort; both tested splits and quiet weight labels remain readable without overflow')

 for branch,trio,evidence in [
  ('quality', ['discuss','reflect','peer'], 'Discussions and written work look stronger. Some repeat the patterns that earn points.'),
  ('mixed', ['prep','discuss','peer'], 'Three areas of engagement improve. Other learning gets less attention.'),
 ]:
  context,page=open_game(browser,2)
  for id in trio:card(page,2,id).click()
  page.get_by_role('button',name='Run evaluation',exact=True).click();advance(page,6)
  expect(page.locator('.level-two')).to_have_attribute('data-branch',branch)
  page.get_by_role('button',name='Observe the class',exact=True).click();finish_scene(page)
  expect(page.locator('.observation-copy')).to_have_text(evidence)
  expect(page.locator('.observation-notebook > span')).to_have_count(3)
  context.close();record(f'{branch} trio retains its own short evidence and the actual three tracked notebook categories')

 # Real animation inspection uses production bytes with normal motion.
 context,page=open_game(browser,1,motion='no-preference')
 card(page,1,'prep').click()
 expect(page.locator('.metric-card-flight')).to_have_count(1)
 # The flight is cosmetic: it cannot hold up the enabled primary action.
 expect(page.get_by_role('button',name='Make a prediction',exact=True)).to_be_enabled()
 expect(page.locator('.choice-slot[data-filled=true]')).to_have_count(1)
 advance(page,2);page.wait_for_timeout(500)
 expect(page.locator('.metric-card-flight')).to_have_count(0)
 context.close();record('Normal-motion selection lands in its slot and cleans up its temporary flight without delaying the next action')
 browser.close()
assert not errors,errors
record('No runtime errors in the visual interaction and responsive production checks')
(OUT/'visual-play-results.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'runtimeErrors':errors},indent=2)+'\n')
