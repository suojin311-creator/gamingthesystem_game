"""Real HTTP + Chromium checks against the embedded standalone server.

Writing is shortened via explicit CLI flags. Review is untimed and excludes authors;
the ranking uses its production 12-second hold and each question lasts four seconds.
"""
import argparse
import asyncio
import json
import socket
import subprocess
import time
from collections import Counter
from pathlib import Path
from playwright.async_api import async_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'build' / 'test-results'
OUT.mkdir(parents=True, exist_ok=True)
SCREEN = ROOT / 'docs'
SCREEN.mkdir(exist_ok=True)
checks, errors, external = [], [], []

def record(text):
    checks.append(text)
    print('PASS', text, flush=True)

def start_server(binary, writing=12, question=4):
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        port = sock.getsockname()[1]
    log = (OUT / f'server-{port}.log').open('w')
    process = subprocess.Popen([str(binary), '--port', str(port), '--no-browser', '--writing-seconds', str(writing), '--question-seconds', str(question)], stdout=log, stderr=subprocess.STDOUT)
    return process, log, f'http://127.0.0.1:{port}'

async def api(page, path='/api/state'):
    return await page.evaluate('''async path => {
      const response=await fetch(path,{headers:{'X-Participant':sessionStorage.getItem('design-lab-participant')||''}});
      if(!response.ok) throw new Error('HTTP '+response.status);
      return response.json();
    }''', path)

async def wait_api(page, predicate, timeout=15):
    until = time.monotonic() + timeout
    while time.monotonic() < until:
        state = await api(page)
        if predicate(state): return state
        await asyncio.sleep(.12)
    raise AssertionError('Timed out waiting for state: '+str(state))

async def visit(browser, base, path='/', width=1366):
    context = await browser.new_context(viewport={'width': width, 'height': 900})
    await context.add_init_script("""(()=>{
      window.ownReflection='';window.reviewed=[];window.selfExposures=[];
      setInterval(()=>{for(const e of document.querySelectorAll('.reflection-text')){
        if(e.textContent===ownReflection)selfExposures.push(e.textContent);
        if(!reviewed.includes(e.textContent))reviewed.push(e.textContent);
      }},16);
    })();""")
    page = await context.new_page()
    page.on('pageerror', lambda err: errors.append(str(err)))
    page.on('request', lambda req: external.append(req.url) if not req.url.startswith(base) else None)
    for attempt in range(60):
        try:
            await page.goto(base+path, wait_until='networkidle', timeout=8000)
            break
        except Exception:
            if attempt == 59: raise
            await asyncio.sleep(.1)
    if path=='/':
        await expect(page.locator('.intro')).to_be_visible(timeout=10000)
    else:
        await expect(page.get_by_role('heading', name='Ready when everyone is.', exact=True)).to_be_visible(timeout=10000)
    return context, page

async def drive(page, votes, first_bomb=False):
    used_bomb = False
    while True:
        s = await api(page)
        if s['phase']!='review' or s['finished']: return
        c = s['card']
        if c is None: return
        await expect(page.locator('.reflection .eyebrow')).to_have_text(c['label'],timeout=5000)
        assert c['text']!=await page.evaluate('ownReflection'),'An author received their own reflection'
        if not c['vote']:
            choice = 'bomb' if first_bomb and not used_bomb else 'flower'
            used_bomb = used_bomb or choice=='bomb'
            await page.get_by_role('button', name='Disagree' if choice=='bomb' else 'Agree', exact=True).click()
            votes.append((c['id'],choice))
        await wait_api(page,lambda s:s['phase']!='review' or s['finished'] or s['card']['id']!=c['id'],timeout=5)

async def ui_case(browser, binary):
    process,log,base=start_server(binary)
    contexts=[]
    try:
        ctx,host=await visit(browser,base,'/host');contexts.append(ctx)
        pages=[]
        for _ in range(3):
            ctx,page=await visit(browser,base);contexts.append(ctx);pages.append(page)
        await expect(host.locator('.host-stats').first).to_contain_text('03')
        await pages[0].screenshot(path=str(SCREEN/'01-waiting.png'),full_page=True)
        await host.screenshot(path=str(SCREEN/'00-host.png'),full_page=True)
        record('The local host and three independent participant browsers join without accounts or names; the anonymous showcase and ranking are announced')
        await host.get_by_role('button',name='Start writing',exact=True).click()
        await expect(pages[0].get_by_role('button',name='Join the audience',exact=True)).to_have_count(0)
        texts=[
          'Speaking often gets too much credit. Asking a useful question deserves more.',
          'Hours studied get too much credit. I would reward explaining an idea clearly.',
          'Likes reward what is easy to notice. I would give more credit to careful disagreement.',
        ]
        for i,page in enumerate(pages):
            await page.evaluate('text=>window.ownReflection=text',texts[i])
            await page.get_by_role('textbox',name='What is one change you would make to help Alex learn more deeply?',exact=True).fill(texts[i])
            if i==0: await page.screenshot(path=str(SCREEN/'02-writing.png'),full_page=True)
            await page.get_by_role('button',name='Submit',exact=True).click()
            await expect(page.get_by_role('heading',name='Submitted.',exact=True)).to_be_visible()
        await wait_api(pages[0],lambda s:s['phase']=='review',timeout=15)
        states=await asyncio.gather(*(api(p) for p in pages))
        assert all(s['reviewTotal']==2 and s['deadline']==0 for s in states)
        slow=0
        first=states[slow]['card'];started=time.monotonic()
        await expect(pages[slow].locator('.reflection')).to_be_visible()
        await pages[slow].screenshot(path=str(SCREEN/'03-voting.png'),full_page=True)
        record('The writing form has the agreed question without a helper line, accepts one reflection per person and starts the anonymous review automatically')
        votes=[]
        fast=[p for i,p in enumerate(pages) if i!=slow]
        await asyncio.gather(*(drive(p,votes,first_bomb=i==0) for i,p in enumerate(fast)))
        await expect(fast[0].get_by_role('heading',name='You’ve reached the end.',exact=True)).to_be_visible()
        assert (await api(pages[slow]))['phase']=='review'
        # A real browser must keep an unanswered card beyond the old ten seconds.
        await asyncio.sleep(max(0,11-(time.monotonic()-started)))
        unchanged=await api(pages[slow])
        assert unchanged['card']['id']==first['id'] and unchanged['phase']=='review'
        await expect(pages[slow].locator('.review-area .timer')).to_have_count(0)
        await expect(pages[slow].get_by_role('button',name='Next',exact=True)).to_have_count(0)
        record('Unanswered review remains in place beyond ten seconds, has no countdown/Next button, and faster voters wait')
        await drive(pages[slow],votes)
        ranking=await wait_api(pages[0],lambda s:s['phase']=='ranking')
        expected=Counter(id for id,choice in votes if choice=='flower')
        assert all(r['flowers']==expected[r['id']] for r in ranking['ranking']),ranking['ranking']
        await expect(pages[0].get_by_role('heading',name='Flowers received.',exact=True)).to_be_visible()
        await pages[0].screenshot(path=str(SCREEN/'04-ranking.png'),full_page=True)
        assert await pages[0].locator('.ranking button,.ranking input,.ranking a').count()==0
        record('Each author sees exactly two other reflections, choices advance automatically, and the frozen ranking counts flowers only')
        for i,page in enumerate(pages):
            audit=await page.evaluate('({reviewed,selfExposures})')
            assert not audit['selfExposures'] and len(audit['reviewed'])==2,(i,audit)
        assert ranking['deadline']-ranking['startedAt']==12000,ranking
        await expect(pages[0].locator('.scan-frame,[data-active]')).to_have_count(0)
        await pages[0].evaluate("""()=>{window.transitions={question1:false,question2:false,ending:false,quote:false,scroll:[]};window.visualTimer=setInterval(()=>{const root=document.querySelector('.presentation-stage');if(!root)return;const phase=root.dataset.presentation,h=root.querySelector('.question-overlay h1'),end=root.querySelector('.closing'),quote=root.querySelector('blockquote');const middle=e=>{const o=Number(getComputedStyle(e).opacity);return o>.02&&o<.98;};if(phase==='ranking')transitions.scroll.push(root.querySelector('.rank-window').scrollTop);if(h&&middle(h)&&h.textContent.startsWith('Did the most flowers'))transitions.question1=true;if(h&&middle(h)&&h.textContent.startsWith('Did knowing'))transitions.question2=true;if(end&&middle(end))transitions.ending=true;if(quote&&middle(quote))transitions.quote=true;},16);}""")
        await expect(pages[0].get_by_role('heading',name='Did the most flowers mean the deepest thinking?',exact=True)).to_be_visible(timeout=14000)
        q1=await api(pages[0]);assert q1['deadline']-q1['startedAt']==4000,q1
        first_visible=time.monotonic()
        await pages[0].screenshot(path=str(SCREEN/'05-question.png'),full_page=True)
        await expect(pages[0].get_by_role('heading',name='Did knowing there would be a ranking change what you wrote?',exact=True)).to_be_visible(timeout=5500)
        q2=await api(pages[0]);assert q2['deadline']-q2['startedAt']==4000,q2
        assert 3<time.monotonic()-first_visible<5.5
        second_visible=time.monotonic()
        await expect(host.get_by_role('button',name='Show Goodhart’s Law',exact=True)).to_have_count(0)
        await expect(pages[0].get_by_role('heading',name='Goodhart’s Law.',exact=True)).to_be_visible(timeout=5500)
        assert 3<time.monotonic()-second_visible<5.5
        await expect(pages[0].locator('.closing blockquote')).to_have_text('When a measure becomes a target, it ceases to be a good measure.')
        await asyncio.sleep(2.5)
        transition=await pages[0].evaluate('()=>{clearInterval(visualTimer);return transitions;}')
        assert all(transition[k] for k in ['question1','question2','ending','quote']),transition
        assert transition['scroll'] and max(transition['scroll'])==min(transition['scroll']),transition
        (OUT/'presentation-transition.json').write_text(json.dumps(transition,indent=2))
        image=pages[0].locator('.closing img')
        await expect(image).to_be_visible()
        assert await image.evaluate('e=>e.complete&&e.naturalWidth>0')
        await pages[0].screenshot(path=str(SCREEN/'06-closing.png'),full_page=True)
        for width,height in [(1366,768),(1024,768),(390,844)]:
            await pages[0].set_viewport_size({'width':width,'height':height})
            assert await pages[0].evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,height)
        record('Static ranking holds twelve seconds, questions cross-fade without background jumps, and Goodhart/quote reveal progressively without quotation marks')
        await host.get_by_role('button',name='Close classroom',exact=True).click()
        await host.get_by_role('dialog').get_by_role('button',name='Close classroom',exact=True).click()
        await expect(pages[0].get_by_role('heading',name='Thank you for taking part.',exact=True)).to_be_visible(timeout=3000)
        record('Host shutdown closes the classroom cleanly; state lives only in the running process')
    finally:
        for context in contexts: await context.close()
        if process.poll() is None:process.terminate()
        process.wait(timeout=10);log.close()

async def class_case(browser,binary):
    process,log,base=start_server(binary,writing=25)
    contexts=[]
    try:
        ctx,host=await visit(browser,base,'/host');contexts.append(ctx)
        sem=asyncio.Semaphore(5)
        async def create():
            async with sem:return await visit(browser,base,width=1024)
        pairs=await asyncio.gather(*(create() for _ in range(21)))
        contexts.extend(c for c,p in pairs);pages=[p for c,p in pairs]
        state=await api(host,'/api/host/state');assert state['joined']==21,state
        await host.get_by_role('button',name='Start writing',exact=True).click()
        async def write(i,page):
            await page.evaluate('text=>window.ownReflection=text',f'Perspective {i+1}: reward thoughtful questions more than the number of answers.')
            await page.get_by_role('textbox',name='What is one change you would make to help Alex learn more deeply?',exact=True).fill(f'Perspective {i+1}: reward thoughtful questions more than the number of answers.')
            await page.get_by_role('button',name='Submit',exact=True).click()
        await asyncio.gather(*(write(i,p) for i,p in enumerate(pages)))
        await wait_api(pages[0],lambda s:s['phase']=='review',timeout=30)
        before=time.monotonic();votes=[]
        await asyncio.gather(*(drive(p,votes) for p in pages))
        elapsed=time.monotonic()-before
        s=await wait_api(pages[0],lambda s:s['phase']=='ranking',timeout=5)
        assert len(votes)==420,len(votes)
        assert len(s['ranking'])==21
        assert all(r['flowers']==20 and r['rank']==1 for r in s['ranking']),s['ranking']
        for page in pages:
            result=await api(page)
            assert result['ranking']==s['ranking'],'participants saw different final rankings'
            audit=await page.evaluate('({reviewed,selfExposures})')
            assert not audit['selfExposures'] and len(audit['reviewed'])==20,audit
        record(f'21 simultaneous independent browsers submit and complete 420 others-only card views / 420 votes in {elapsed:.1f}s, receiving the same exact tied ranking')
        await expect(pages[0].locator('.ranking')).to_be_visible()
        await pages[0].screenshot(path=str(SCREEN/'07-class-of-21.png'),full_page=True)
    finally:
        for context in contexts:await context.close()
        if process.poll() is None:process.terminate()
        process.wait(timeout=10);log.close()

async def main(args):
    binary=Path(args.binary).resolve()
    async with async_playwright() as p:
        browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-background-timer-throttling','--disable-renderer-backgrounding','--disable-backgrounding-occluded-windows'])
        if args.scenario in ['ui','all']:await ui_case(browser,binary)
        if args.scenario in ['class','all']:await class_case(browser,binary)
        await browser.close()
    assert not errors,errors
    assert not external,external
    record('No browser runtime errors or requests to external services')
    report={'passed':len(checks),'checks':checks,'runtimeErrors':errors,'externalRequests':external,'scenario':args.scenario,'platform':'Linux server binary and Chromium; Windows PE cross-build is validated separately'}
    (OUT/f'browser-{args.scenario}.json').write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--binary',default=str(ROOT/'build/design-lab-linux'));parser.add_argument('--scenario',choices=['ui','class','all'],default='all')
    asyncio.run(main(parser.parse_args()))
