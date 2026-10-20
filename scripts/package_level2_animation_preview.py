"""Package the independent authored Level 2 review; never replace game archives."""
import hashlib
import html
import json
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PIN = 'c8c1c83456c4e67cf627df399bfb67b3a9792adb'
build, source = (Path(arg).resolve() for arg in sys.argv[1:])
commit = subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip()
assert commit == PIN, 'Review and pin the new delivery before packaging it.'
subprocess.run(['git', '-C', str(source), 'diff', '--exit-code', 'HEAD'], check=True)
source_hash = hashlib.sha256()
source_files = subprocess.check_output(['git', '-C', str(source), 'ls-files', '-z']).decode().split('\0')[:-1]
for name in sorted(source_files):
    source_hash.update(name.encode() + b'\0' + (source / name).read_bytes() + b'\0')

entries = [
    ('完整串联 / Full chain', 'full', '三项 → 六项 → 10 → 25 → 100 → 结尾；默认混合指标示例。'),
    ('可见行为指标 / Visible', 'visible-heavy', 'Preparation、Participation、Focus 三项分支。'),
    ('质量深度指标 / Quality', 'quality-heavy', 'Discussion、Reflection、Peer response 三项分支。'),
    ('混合指标 / Mixed', 'mixed-broad', 'Preparation、Discussion、Peer response 三项分支。'),
    ('六项指标 / Six', 'six', '六项清单及继续增加指标的过渡。'),
    ('10 项要求', '10', '完成要求并补上遗漏。'),
    ('25 项要求', '25', '用证据对应更多评价要求。'),
    ('100 项＋结尾', '100', '填补剩余空缺、反思与优先级过渡。'),
    ('只看结尾 / Final conflict', 'final', '完整清单、教师反思及三项优先级画面。'),
    ('勾选动作 / Checking', 'checking', 'Alex 看清单、落笔勾选和表情动作。'),
]
links = '\n'.join(
    f'<a href="Level2-animation.html?cinematic=level2&amp;state={state}"><strong>{html.escape(label)}</strong><span>{html.escape(description)}</span></a>'
    for label, state, description in entries
)
launcher = f'''<!doctype html>
<html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Level 2 动画预览</title>
<style>
*{{box-sizing:border-box}}body{{margin:0;background:#f2e8d6;color:#302a23;font:16px/1.6 system-ui,sans-serif}}
main{{max-width:960px;margin:auto;padding:32px 20px}}h1{{font:36px/1.2 Georgia,serif}}p{{max-width:760px}}
nav{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,250px),1fr));gap:14px;margin:24px 0}}
a{{display:block;padding:18px;background:#fffaf0;border:1px solid #c5af8f;border-radius:8px;color:inherit;text-decoration:none}}
a:first-child{{background:#934f43;color:#fff7e6}}a:focus-visible{{outline:3px solid #42697b;outline-offset:3px}}
strong,span{{display:block}}span{{font-size:14px;margin-top:8px}}small{{color:#61574a}}code{{overflow-wrap:anywhere}}
</style><main><h1>Level 2 动画预览</h1>
<p>先看“完整串联”，也可单独查看各片段。播放后可暂停、重播、拖动进度，或切换 1×／2×／4× 速度。建议先用 1× 观看。</p>
<p>这是同伴的最新动画候选版，供合并前审阅。片段之间的游戏衔接为演示；当前未提供音频素材，播放为静音。现有游戏未改动。</p>
<nav aria-label="Level 2 animation previews">{links}</nav>
<p>解压整个 ZIP 后，用 Chrome 或 Edge 打开本页；下载后无需联网。电脑横屏更适合观看原 16:9 画面。</p>
<small>来源：Mg614/gaming-the-system · feature/cinematic-level2-consequences · <code>{PIN[:7]}</code></small>
</main></html>'''.encode()
instructions = '''Level 2 动画独立预览 / Independent animation review

解压整个 ZIP，用 Chrome 或 Edge 打开 START-HERE.html，先选“完整串联”。
Extract the entire ZIP and open START-HERE.html in Chrome or Edge.
Choose Full chain first; use the original Pause/Replay/Speed/time controls as needed.
All animation and artwork are embedded. No installation or Internet is required.
No audio assets were supplied; this preview is silent.

This is the partner's visual-acceptance candidate, not an integrated gameplay release.
Animation timing, dialogue and artwork are unchanged. The standalone entry and
return-to-launcher link are adapted in memory only for offline review.
Full chain simulates gameplay handoffs. The existing game is unchanged.
Source: Mg614/gaming-the-system
Branch: feature/cinematic-level2-consequences
Commit: c8c1c83456c4e67cf627df399bfb67b3a9792adb
'''.encode()
files = {'START-HERE.html': launcher, 'Level2-animation.html': (build / 'index.html').read_bytes(), 'START-HERE.txt': instructions}
archive = ROOT / 'play/Level2-animation-preview.zip'
with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
    for name, data in files.items():
        info = zipfile.ZipInfo(name)
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o644 << 16
        bundle.writestr(info, data, compresslevel=9)
report = {
    'sourceRepository': 'https://github.com/Mg614/gaming-the-system',
    'sourceBranch': 'feature/cinematic-level2-consequences', 'sourceCommit': commit,
    'sourceFilesSha256': source_hash.hexdigest(), 'unchangedUpstreamFiles': len(source_files),
    'archive': archive.name, 'zipSha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
    'html': 'Level2-animation.html', 'htmlSha256': hashlib.sha256(files['Level2-animation.html']).hexdigest(),
    'fileSha256': {name: hashlib.sha256(data).hexdigest() for name, data in files.items()},
    'scope': 'Independent candidate review; original animation, no gameplay integration or upstream writes',
    'build': {'config': 'scripts/level2-animation-preview.config.mjs', 'adaptations': ['Standalone authored Level2DevPreview entry', 'Opening link returns to the offline launcher']},
    'entries': [{'label': label, 'state': state} for label, state, _ in entries],
    'audio': 'No source audio assets; silent',
}
(ROOT / 'play/LEVEL2_ANIMATION_PREVIEW.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(f'Packaged {archive.name}: {archive.stat().st_size / 1024 / 1024:.1f} MiB; {len(entries)} review entries')
