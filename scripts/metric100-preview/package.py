import hashlib,json,sys
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
root=Path(__file__).resolve().parents[2];build=Path(sys.argv[1]);sha=lambda b:hashlib.sha256(b).hexdigest()
files={
 'START-HERE.html':b'<!doctype html><html lang="en"><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=Level2-100metrics.html"><title>100 metric animation</title><a href="Level2-100metrics.html">Open animation preview</a></html>',
 'Level2-100metrics.html':(build/'index.html').read_bytes(),
 'START-HERE.txt':('100 metric animation review\n\nExtract this ZIP, then open START-HERE.html in Chrome or Edge.\nStarts with the original criteria-checking insert, retains the full paper, then begins the original conversation captions one second after entering its scene. Stops at the final dialogue, with no priorities page.\nReview controls: bottom left, Pause / Play / Replay / time.\nAll artwork is embedded; no installation or Internet is needed. No audio was supplied.\nStandalone review only; the game and its current ZIPs are unchanged.\nOriginal: Mg614/gaming-the-system / feature/cinematic-level2-consequences / c8c1c83456c4e67cf627df399bfb67b3a9792adb\n').encode()
}
archive=root/'play/Level2-100metrics-preview.zip'
with ZipFile(archive,'w',compression=ZIP_DEFLATED,compresslevel=9) as z:
 for name,data in files.items():z.writestr(name,data)
with ZipFile(archive) as z:assert z.testzip() is None
report={**json.loads((build/'source-manifest.json').read_text()),'archive':archive.name,'zipSha256':sha(archive.read_bytes()),'fileSha256':{n:sha(b) for n,b in files.items()},'scope':'Independent 100 metric review; current game/Level2 preview archives unchanged.'}
(root/'play/LEVEL2_100METRICS_PREVIEW.json').write_text(json.dumps(report,indent=2)+'\n')
print(f'Packaged {archive.name}: {archive.stat().st_size/1024/1024:.1f} MiB')
