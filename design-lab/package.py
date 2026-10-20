"""Build the self-contained Windows launcher and package only this feature."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import struct
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / 'design-lab'
BUILD = LAB / 'build'
BUILD.mkdir(exist_ok=True)
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--standalone', action='store_true', help='Build only the current Design Lab, without the game.')
args = parser.parse_args()
go = os.environ.get('DESIGN_LAB_GO') or shutil.which('go')
if not go:
    raise SystemExit('Go 1.22+ is needed to build the Windows program. Set DESIGN_LAB_GO if necessary.')
version = subprocess.run([go, 'version'], capture_output=True, text=True, check=True).stdout.strip()
if not version.startswith('go version go'):
    raise SystemExit('DESIGN_LAB_GO must point at the Go compiler.')
web = LAB / 'web'
build_source = LAB
if args.standalone:
    subprocess.run(['npm', 'run', 'lab:check'], cwd=ROOT, check=True)
    web = BUILD / 'standalone-web'
    subprocess.run(['node', str(ROOT/'node_modules/vite/bin/vite.js'), 'build', '--config', 'design-lab/vite.config.ts', '--outDir', str(web)], cwd=ROOT, env={**os.environ, 'VITE_LAB_STANDALONE':'true'}, check=True)
    build_source = BUILD / 'standalone-go'
    build_source.mkdir(exist_ok=True)
    for path in LAB.glob('*.go'):
        shutil.copy2(path, build_source/path.name)
    shutil.copy2(LAB/'go.mod', build_source/'go.mod')
    shutil.copytree(web, build_source/'web', dirs_exist_ok=True)
if not (web/'index.html').is_file() or not (web/'goodhart.png').is_file():
    raise SystemExit('Run npm run lab:build first.')
env = {**os.environ, 'GOOS':'windows', 'GOARCH':'amd64', 'CGO_ENABLED':'0', 'GOTOOLCHAIN':'local'}
classroom=(web/'game.html.gz').is_file()
assert not args.standalone or not classroom, 'Standalone package must not contain the game'
exeName='Start-Gaming-the-System.exe' if classroom else 'Start-Design-Lab.exe'
exe = BUILD / exeName
subprocess.run([go,'build','-trimpath','-ldflags=-s -w','-o',str(exe),'.'], cwd=build_source, env=env, check=True)
data = exe.read_bytes()
assert data[:2] == b'MZ'
offset = struct.unpack_from('<I',data,0x3c)[0]
assert data[offset:offset+4] == b'PE\0\0'
assert struct.unpack_from('<H',data,offset+4)[0] == 0x8664,'Expected Windows x64'
for path in sorted(p for p in web.rglob('*') if p.is_file()):
    assert path.read_bytes() in data, f'Embedded asset is missing: {path.name}'

notices = ['DESIGN LAB - THIRD PARTY NOTICES\n\nThe portrait is an AI-generated editorial illustration, not a historical photograph.\n']
go_root = Path(subprocess.check_output([go,'env','GOROOT'],text=True).strip())
notices.append('GO STANDARD LIBRARY / RUNTIME\n'+(go_root/'LICENSE').read_text())
for name in ['react','react-dom','scheduler','framer-motion','motion-dom','motion-utils','tslib']:
    pkg = ROOT/'node_modules'/name
    licenses = [p for p in pkg.glob('*') if p.is_file() and p.name.lower().startswith('license')]
    for license_file in licenses:
        notices.append(name.upper()+'\n'+license_file.read_text())
files = {
    exeName:data,
    'START-HERE.html':(LAB/('START-HERE-standalone.html' if args.standalone else 'START-HERE.html')).read_bytes(),
    'README.txt':(LAB/('README-Windows-standalone.txt' if args.standalone else 'README-Windows.txt')).read_bytes(),
    'THIRD-PARTY-NOTICES.txt':'\n\n'.join(notices).encode(),
}
sha = lambda b:hashlib.sha256(b).hexdigest()
files['SHA256SUMS.txt']=''.join(f'{sha(body)}  {name}\n' for name,body in files.items()).encode()
archive = ROOT/'play'/('Gaming-the-System-classroom.zip' if classroom else 'Design-Lab-local.zip')
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as bundle:
    for name,body in files.items():bundle.writestr(name,body)
with zipfile.ZipFile(archive) as bundle:
    assert bundle.testzip() is None
    for name,body in files.items():assert bundle.read(name)==body
source_paths = sorted(p for p in LAB.rglob('*') if p.is_file() and p.name != 'VALIDATION.json' and not any(part in {'web','build','__pycache__','docs'} for part in p.relative_to(LAB).parts))
h=hashlib.sha256()
for path in source_paths:h.update(str(path.relative_to(ROOT)).encode()+b'\0'+path.read_bytes()+b'\0')
report = {
    'branch':subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip(),'archive':archive.name,'zipSha256':sha(archive.read_bytes()),
    'sourceSha256':h.hexdigest(),'toolchain':version,'target':'windows/amd64','selfContained':True,
    'embeddedWebSha256':{str(p.relative_to(web)):sha(p.read_bytes()) for p in sorted(web.rglob('*')) if p.is_file()},
    'files':{name:sha(body) for name,body in files.items()},
    'windowsBinaryChecks':['PE x64 header verified','All built web assets and illustration embedded byte-for-byte','CGO disabled; no Python/Node.js runtime or paid service required'],
    'nativeWindowsExecutionTested':False,
}
(ROOT/'play'/('CLASSROOM_PREVIEW.json' if classroom else 'DESIGN_LAB_LOCAL.json')).write_text(json.dumps(report,indent=2)+'\n')
assert archive.stat().st_size < 100*1024*1024, 'Archive exceeds GitHub single-file limit'
print(f'Packaged {archive.name}: {archive.stat().st_size/1024/1024:.1f} MB; Windows x64 PE and embedded resources verified.')
