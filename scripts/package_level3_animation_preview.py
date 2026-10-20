"""Export the exact game-adapted Level 3A film for offline review."""
import hashlib,json,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
build=Path(sys.argv[1])
film=json.loads((ROOT/'node_modules/.cache/level3-cinematic/manifest.json').read_text())
links=''.join(f'<a href="Level3A-animation.html?group={group}&amp;pattern={pattern}">{label} · {title}</a>' for group,label in [('first','Preparation / Discussion / Peer response'),('second','Participation / Focus / Reflection')] for pattern,title in [('shared','Shared attention'),('one','One priority'),('two','Two priorities'),('graded','Graduated priorities')])
launcher=('''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Level 3A 动画预览</title><style>body{background:#f2e8d6;color:#302a23;font:16px/1.6 system-ui;margin:32px auto;padding:0 20px;max-width:960px}h1{font:36px Georgia}nav{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr));gap:12px}a{display:block;padding:18px;background:#fffaf0;border:1px solid #c5af8f;color:inherit;text-decoration:none}a:focus-visible{outline:3px solid #42697b}</style><h1>Level 3A 动画预览</h1><p>解压后直接打开本页。每组连续播放三个实际游戏状态，可暂停、重播和拖动进度。镜头按当前游戏的相对权重规则匹配；仅使用 Level 3A。进入后可切换强调的指标，查看全部表现。</p><nav>'''+links+'''</nav><p>左上角显示当前指标，Alex 字幕使用浅蓝色。已剪去数值页、独立人像及无关切镜。当前没有音频素材。</p></html>''').encode()
files={'START-HERE.html':launcher,'Level3A-animation.html':(build/'index.html').read_bytes(),'START-HERE.txt':'解压整个 ZIP，用 Chrome 或 Edge 打开 START-HERE.html。\nNo installation or Internet required. All animation assets are embedded.\n'.encode()}
archive=ROOT/'play/Level3A-animation-preview.zip'
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for name,data in files.items():
  info=zipfile.ZipInfo(name);info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16;z.writestr(info,data,compresslevel=9)
sha=lambda b:hashlib.sha256(b).hexdigest()
report={'sourceRepository':'https://github.com/Mg614/gaming-the-system','sourceBranch':'feature/cinematic-level3-metric-adaptations','sourceCommit':film['partnerSourceCommit'],'archive':archive.name,'zipSha256':sha(archive.read_bytes()),'html':'Level3A-animation.html','htmlSha256':sha(files['Level3A-animation.html']),'fileSha256':{n:sha(b) for n,b in files.items()},'film':film,'scope':'Only Level 3A weighted-task scenes; comparison/theory remain their existing game placeholders. No Level 3B.','audio':'No source audio assets; silent'}
(ROOT/'play/LEVEL3A_ANIMATION_PREVIEW.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(f'Packaged {archive.name}: {archive.stat().st_size/1024/1024:.1f} MiB')
