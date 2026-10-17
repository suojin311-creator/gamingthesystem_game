"""Measure equivalent interface roles in the three actual production entries."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
out=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width,height in [(1366,900),(390,844),(320,740)]:
  for level in [1,2,3]:
   context=browser.new_context(viewport={'width':width,'height':height},reduced_motion='reduce')
   html=Path(f'dist-level{level}/index.html').read_bytes()
   context.route('https://audit.test/**',lambda route,request,body=html:route.fulfill(status=200,content_type='text/html',body=body))
   page=context.new_page();page.clock.install();page.goto('https://audit.test/',wait_until='networkidle')
   if level==1:page.get_by_role('button',name='Skip guide',exact=True).click()
   else:
    for _ in range(10):page.clock.run_for(1000);page.wait_for_timeout(15)
    page.get_by_role('button',name='Choose three metrics' if level==2 else 'Choose priorities',exact=True).click()
   selectors={1:{'chapter':'.chapter-heading h1','step':'.stepper li','metric':'.metric-card h3','description':'.metric-card p','heading':'.section-intro h2'},2:{'chapter':'.l2-heading h1','step':'.l2-stepper li','metric':'.l2-metric-card h3','description':'.l2-metric-card p','heading':'.section-intro h2'},3:{'chapter':'.l3-heading h1','step':'.l3-stepper li','metric':'.l3-metric-card h3','description':'.l3-metric-card p','heading':'.section-intro h2'}}[level]
   selectors['button']='.primary-button'
   sizes={k:page.locator(s).first.evaluate('element=>getComputedStyle(element).fontSize') for k,s in selectors.items()}
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
   assert page.get_by_role('button',name='Restart',exact=True).count()==0
   out.append({'viewport':width,'level':level,'sizes':sizes});context.close()
 browser.close()
checks=[]
for width in [1366,390,320]:
 samples=[entry['sizes'] for entry in out if entry['viewport']==width]
 assert len(samples)==3 and all(sample==samples[0] for sample in samples)
 assert samples[0]['metric']=='16px'
 checks.append(f'{width}px: equivalent chapter/step/metric/description/heading/button sizes match across all three levels, metric names are 16px, no Restart controls or overflow')
Path('test-results/typography-results.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'measurements':out},indent=2)+'\n')
for check in checks:print('PASS',check)
