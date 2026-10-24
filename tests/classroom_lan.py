"""Two independent browser processes play through the packaged game over LAN HTTP.

Pass the actual non-loopback classroom URL. A localhost-only test would hide the
secure-context failure this regression covers. The phone client emulates Chromium
touch/viewport; this is not a claim of testing a physical phone or Safari.
"""
import argparse
import json
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'test-results'
OUT.mkdir(exist_ok=True)
expect.set_options(timeout=30000)
helpers = (ROOT/'tests/release.py').read_text()
helpers = helpers[helpers.index('def advance('):helpers.index("if '--integrity-only' in sys.argv:")]


def client(base, mobile):
    name = 'phone-chromium' if mobile else 'desktop-chromium'
    errors, checks = [], []
    def record(text):
        checks.append(text)
        print(f'PASS [{name}] {text}', flush=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox', '--no-proxy-server'])
        context = browser.new_context(viewport={'width':390 if mobile else 1366, 'height':844 if mobile else 900}, is_mobile=mobile, has_touch=mobile)
        page = context.new_page()
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.on('crash', lambda _: errors.append('Renderer crashed'))
        page.add_init_script("""window.filmCompletions=[];
          addEventListener('message',event=>{
            if(event.data?.type==='complete' && event.source===document.querySelector('iframe')?.contentWindow)
              filmCompletions.push({channel:event.data.channel,runId:event.data.runId});
          });""")
        ns = {'expect':expect, 'checks':[], 're':re}
        exec(helpers, ns)
        advance = ns['advance']
        try:
            page.goto(base+'/game', wait_until='domcontentloaded', timeout=90000)
            expect(page.locator('.opening-scene .stage')).to_have_attribute('data-beat','title')
            capability = page.evaluate('({secure:isSecureContext,randomUUID:typeof crypto.randomUUID,getRandomValues:typeof crypto.getRandomValues})')
            assert not capability['secure'] and capability['randomUUID']=='undefined', capability
            record('Actual LAN HTTP is an insecure context without crypto.randomUUID')
            ns['opening'](page)
            page.clock.install()
            page.get_by_role('button', name='Skip guide', exact=True).click()
            metric = 'peer' if mobile else 'prep'
            page.get_by_test_id('metric-'+metric).click()
            page.get_by_role('button', name='Make a prediction', exact=True).click()
            page.get_by_label('How will students respond when this counts towards their marks?').fill('They will focus on this requirement.')
            page.get_by_role('button', name='View assessment results', exact=True).click()
            advance(page, 10)
            page.get_by_role('button', name='Look behind the result', exact=True).click()
            expect(page.frame_locator('iframe').locator('.l1-film')).to_be_visible()
            for _ in range(180):
                if not page.locator('.settlement-cinematic').count(): break
                page.clock.run_for(1000); page.wait_for_timeout(12)
            expect(page.locator('.l1-settlement')).to_be_visible()
            page.locator('.l1-settlement').scroll_into_view_if_needed()
            advance(page, 6)
            record('Opening, chosen Level 1 film and its results complete without a blank interface')
            page.get_by_role('button', name='Continue to Level 2', exact=True).click()
            advance(page, 8)
            expect(page.locator('.level-two')).to_have_attribute('data-phase','choose',timeout=8000)
            for metric in ['prep','part','focus']: page.get_by_test_id('level2-metric-'+metric).click()
            page.get_by_role('button', name='Run evaluation', exact=True).click()
            advance(page, 8)
            ns['finish_two'](page)
            record('Level 2 films at 3, 6 and 100 metrics finish and reach their result interfaces')
            page.get_by_role('button', name='Continue to Level 3', exact=True).click()
            ns['choose_three'](page)
            first, second = ([10,60,30],[60,30,10]) if mobile else ([60,30,10],[10,60,30])
            ns['weights_three'](page, first)
            page.get_by_role('button', name='Try another split', exact=True).click()
            ns['weights_three'](page, second)
            page.get_by_role('button', name='Compare the results', exact=True).click()
            expect(page.locator('.l3-compare-table td[data-run="1"] .l3-row-weight')).to_have_text([str(v)+'%' for v in first])
            expect(page.locator('.l3-compare-table td[data-run="2"] .l3-row-weight')).to_have_text([str(v)+'%' for v in second])
            record('Two Level 3 films and comparison retain this player’s distinct weight choices')
            page.get_by_role('button', name='Step back and reflect', exact=True).click()
            film = page.frame_locator('iframe[title="Ending animation"]')
            expect(film.locator('.ending-loading')).to_have_count(0)
            for _ in range(60):
                if page.locator('.ending-cinematic').get_attribute('data-finished')=='true': break
                page.clock.run_for(1000); page.wait_for_timeout(25)
            expect(page.locator('.ending-cinematic')).to_have_attribute('data-finished','true')
            expect(film.get_by_role('button', name='ENTER DESIGN LAB')).to_be_visible()
            completions = page.evaluate('filmCompletions')
            assert len(completions)==7, completions
            tokens = [c['runId'] for c in completions]
            assert len(set(tokens))==7, completions
            film.get_by_role('button', name='ENTER DESIGN LAB').click(force=True, no_wait_after=True)
            page.wait_for_timeout(500); page.clock.run_for(1000)
            page.wait_for_url(base+'/',timeout=30000)
            expect(page.locator('.intro')).to_be_visible()
            page.wait_for_function("!!sessionStorage.getItem('design-lab-participant')")
            participant = page.evaluate("sessionStorage.getItem('design-lab-participant')")
            assert not errors, errors
            record('Ending completes, enters the same Lab and receives its own participant identity; no runtime errors')
            return {'client':name,'capabilities':capability,'checks':checks,'runtimeErrors':errors,'completionTokens':tokens,'participantId':participant}
        except Exception:
            page.screenshot(path=str(OUT/f'lan-{name}-failure.png'))
            (OUT/f'lan-{name}-failure.json').write_text(json.dumps({'checks':checks,'errors':errors},indent=2))
            raise
        finally:
            context.close(); browser.close()


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--base-url',required=True)
    args=parser.parse_args();base=args.base_url.rstrip('/')
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures=[pool.submit(client,base,mobile) for mobile in [False,True]]
        results=[f.result() for f in futures]
    assert results[0]['participantId']!=results[1]['participantId']
    assert not set(results[0]['completionTokens'])&set(results[1]['completionTokens'])
    report={'passed':sum(len(r['checks']) for r in results)+1,'baseUrl':base,'clients':results,'isolation':'Independent browser processes, game choices, completion tokens and Lab participants','physicalPhoneTested':False,'nativeWindowsExecutionTested':False}
    (OUT/'classroom-lan-results.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS Both concurrent LAN clients keep independent game and Lab identities',flush=True)
