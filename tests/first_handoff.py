"""Verify approved handoff and chapter wording in the actual complete game."""
import json,re,threading
from pathlib import Path
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'tests/release.py').read_text();ns={'expect':expect,'re':re,'checks':[]};exec(source[source.index('def advance('):source.index("if '--integrity-only' in sys.argv:")],ns)
class Handler(BaseHTTPRequestHandler):
 def do_GET(self):
  self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.end_headers();self.wfile.write((ROOT/'dist/index.html').read_bytes())
 def log_message(self,*a):pass
server=ThreadingHTTPServer(('127.0.0.1',0),Handler);threading.Thread(target=server.serve_forever,daemon=True).start();errors=[]
AUDIT='''window.entryAudit={};const sample=()=>{const chapter=document.querySelector('.chapter-transition');const q=chapter?.querySelector('.chapter-bridge p');if(q)entryAudit.question=q.textContent;const root=document.querySelector('.first-handoff');if(root?.dataset.entering==='true'&&!entryAudit.start)entryAudit.start=performance.now();if(document.querySelector('.workbench-guide[open]')&&!entryAudit.guide)entryAudit.guide=performance.now();if(document.querySelector('.gts-audio-controls'))entryAudit.floating=true;};new MutationObserver(sample).observe(document,{subtree:true,childList:true,attributes:true});addEventListener('animationend',e=>{if(e.animationName==='first-handoff-out')entryAudit.finished=performance.now();},true);'''
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);c=b.new_context(viewport={'width':1600,'height':1000});c.add_init_script(AUDIT);page=c.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(f'http://127.0.0.1:{server.server_port}',wait_until='networkidle');ns['opening'](page)
 expect(page.get_by_role('dialog',name='Workbench guide')).to_be_visible(timeout=3000)
 audit=page.evaluate('entryAudit');assert audit['question']=='Which metric would tell me the most?',audit
 assert 600<audit['finished']-audit['start']<1000,audit
 assert audit['guide']>audit['finished']+150,audit
 assert not audit.get('floating'),audit
 page.get_by_role('button',name='Skip guide',exact=True).click();expect(page.locator('.choice-grid .choice-card')).to_have_count(6)
 page.wait_for_timeout(1400);expect(page.get_by_role('dialog',name='Workbench guide')).to_have_count(0)
 assert not errors,errors;b.close()
server.shutdown();report={'checks':['Real opening carries player name through new metric chapter question and workbench.','Chapter/workbench overlap lasts about 0.7 seconds; automatic guide appears after the dissolve.','Guide skips normally without reopening; six real options remain; floating Sound absent.'],'timingsMs':audit,'runtimeErrors':errors}
(ROOT/'test-results/first-handoff.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
