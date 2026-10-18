"""Production regression for independent effort bands and score-based stopping."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
# Reuse real slider/confirm/observation operations; do not mount test-only state.
exec(Path('tests/player_experiments.py').read_text().split('with sync_playwright() as p:')[0])
checks=[];errors=[]
def record(text):checks.append(text);print('PASS',text,flush=True)
def observed(page):return page.locator('.l3-run-rows li').evaluate_all('(nodes)=>nodes.map(e=>e.dataset.effort)')
def start_trial(page,weights,aim='Give all three attention'):
 page.get_by_role('radio',name=aim,exact=True).check();set_weights(page,weights);finish_run(page)
def next_trial(page,index):page.get_by_role('button',name='Adjust the weights' if index==0 else 'Test your explanation',exact=True).click()
def stop_check(page,covered):
 figure=page.get_by_test_id('criteria-stop');expect(figure).to_be_visible()
 expect(figure).to_have_attribute('data-covered-count',str(covered))
 expect(figure.locator('[data-mark-earned]')).to_have_count(covered)
 expect(figure.locator('.l3-routine-beat[data-shown=true]')).to_have_count(3)
 expect(figure).to_contain_text('Packs up. Stops.')
 assert 'all three requirements' not in figure.get_attribute('aria-label')

with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 context,page=start(browser);page.get_by_role('button',name='Skip guide',exact=True).click()
 for i,weights in enumerate([[40,30,30],[40,31,29],[50,25,25]]):
  start_trial(page,weights);assert observed(page)==['medium']*3;stop_check(page,3)
  expect(page.locator('.l3-trial-finding')).to_contain_text('All three received attention')
  expect(page.locator('.l3-perspectives .student')).to_contain_text('Stops when the criteria are met')
  assert 'minimum effort' not in page.locator('.l3-trial-finding').inner_text().lower()
  if i<2:next_trial(page,i)
 page.get_by_role('button',name='Compare the patterns',exact=True).click()
 expect(page.locator('.l3-compare-table thead th.near-even')).to_have_count(1)
 expect(page.locator('.l3-compare-table thead th.uneven')).to_have_count(2)
 expect(page.locator('td[data-effort-change=same]')).to_have_count(6)
 page.get_by_role('radio',name='Keep this split for now',exact=True).check();page.get_by_role('button',name='Watch Alex’s response',exact=True).click()
 expect(page.locator('.l3-scene-copy > p')).to_contain_text('same effort pattern')
 assert 'shifts effort' not in page.locator('.l3-scene-copy > p').inner_text()
 record('40/30/30 → 40/31/29 preserves effort after a share increase; uneven 50/25/25 acknowledges attention across all three without a near-even override or false change claim')
 context.close()
 context,page=start(browser);page.get_by_role('button',name='Skip guide',exact=True).click()
 cases=[([67,25,8],['high','medium','low'],2),([66,25,9],['medium','medium','low'],2),([66,24,10],['medium','low','low'],1)]
 for i,(weights,expected,covered) in enumerate(cases):
  start_trial(page,weights);assert observed(page)==expected;stop_check(page,covered)
  finding=page.locator('.l3-trial-finding').inner_text()
  assert 'Focus' in finding
  assert ('Participation' in finding)==(weights[1]<25)
  assert 'Preparation' not in finding
  expect(page.locator('.l3-perspectives .student')).to_contain_text('Low-weight areas get less attention')
  if i<2:next_trial(page,i)
 page.get_by_role('button',name='Compare the patterns',exact=True).click()
 expect(page.locator('td[data-run="2"][data-effort-change=less]')).to_have_count(1)
 expect(page.locator('td[data-run="3"][data-effort-change=less]')).to_have_count(1)
 page.get_by_role('radio',name='I’d rethink this setup',exact=True).check();page.get_by_role('button',name='Watch Alex’s response',exact=True).click()
 expect(page.locator('.l3-scene-copy > p')).to_contain_text('shifts effort')
 record('67/66 and 25/24 boundary crossings affect only the corresponding effort bands; every uneven result stops for marks, with low-effort tasks left unticked and accurately named')
 context.close()
 context,page=start(browser);page.get_by_role('button',name='Skip guide',exact=True).click()
 for i,weights in enumerate([[70,20,10],[34,33,33],[10,70,20]]):
  start_trial(page,weights,'Shift Alex’s priority');stop_check(page,3 if i==1 else 1)
  if i<2:next_trial(page,i)
 expect(page.locator('.alex-bubble p').first).to_contain_text('Participation first this time')
 assert 'still put' not in page.locator('.alex-bubble p').first.inner_text()
 page.get_by_role('button',name='Compare the patterns',exact=True).click()
 expect(page.locator('.l3-compare-table tr[data-metric=prep] td[data-run="2"]')).to_have_attribute('data-effort-change','less')
 expect(page.locator('.l3-compare-table tr[data-metric=part] td[data-run="3"]')).to_have_attribute('data-effort-change','more')
 page.get_by_role('radio',name='Keep this split for now',exact=True).check();page.get_by_role('button',name='Watch Alex’s response',exact=True).click()
 for _ in range(2):page.get_by_role('button',name='Continue scene',exact=True).click()
 page.get_by_role('button',name='Reveal Goodhart’s Law',exact=True).click();page.get_by_role('button',name='Continue scene',exact=True).click()
 expect(page.locator('.l3-preview-end')).to_have_text('End of preview')
 record('A real high/low → all-medium → shifted high/low route compares actual changes, describes the newly prioritized task correctly and ends at the theory placeholder')
 context.close()
 # A normal-motion phone route verifies the now-universal closing figure remains readable.
 context,page=start(browser,320);page.emulate_media(reduced_motion='no-preference');page.get_by_role('button',name='Skip guide',exact=True).click()
 start_trial(page,[70,20,10]);stop_check(page,1)
 assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
 page.locator('.l3-criteria-stop').scroll_into_view_if_needed();page.screenshot(path='test-results/effort-rules-stopping-320.png',full_page=True)
 page.set_viewport_size({'width':1366,'height':900});page.screenshot(path='test-results/effort-rules-stopping-1366.png',full_page=True)
 record('The universal score-based stopping observation fits a 320px normal-motion phone route and desktop without horizontal overflow')
 context.close();browser.close()
assert not errors,errors
record('No runtime errors in independent effort bands, boundary observations, tick coverage, comparison or the final theory endpoint')
Path('test-results/effort-browser-results.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'runtimeErrors':errors},indent=2)+'\n')
