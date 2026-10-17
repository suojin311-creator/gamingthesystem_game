"""Publish the three latest offline previews from one set of production builds.

Run via npm run package:previews so changes to shared components reach every entry.
Versioned ZIPs are historical records and are deliberately left untouched.
"""
import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAY = ROOT / 'play'
ENTRIES = [
    ('Level1-play.zip', 'Level1.html', 'dist-level1/index.html',
     'Level 1 only. Continue to Level 2 is reserved and disabled.'),
    ('Level2-play.zip', 'Level2.html', 'dist-level2/index.html',
     'Start directly at Level 2. Level 3 is reserved.'),
    ('Full-game-play.zip', 'Gaming-the-System.html', 'dist/index.html',
     'Start at Level 1, then choose Continue to Level 2 to keep playing.'),
]


def digest(data):
    return hashlib.sha256(data).hexdigest()


# Load all builds before replacing any published entry.
builds = {path: (ROOT / path).read_bytes() for _, _, path, _ in ENTRIES}
source_paths = sorted(path for path in (ROOT / 'src').rglob('*')
                      if path.is_file() and path.suffix in {'.ts', '.tsx', '.css', '.png'})
source_paths += [ROOT / name for name in ['index.html', 'vite.config.ts', 'package.json', 'package-lock.json']]
source_hash = hashlib.sha256()
for path in source_paths:
    source_hash.update(str(path.relative_to(ROOT)).encode() + b'\0')
    source_hash.update(path.read_bytes() + b'\0')

manifest = {'sourceSha256': source_hash.hexdigest(), 'entries': []}
for archive, html, build, description in ENTRIES:
    instruction = (
        f'Gaming the System\n\n{description}\n\n'
        f'Extract this ZIP, then open {html} in Chrome or Edge.\n'
        'No installation or internet connection is needed after download.\n'
        'Closing or reloading starts a fresh game.\n'
        'The opening and final cinematics remain separate; scenes are placeholders.\n'
    )
    with zipfile.ZipFile(PLAY / archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
        for name, data in [(html, builds[build]), ('START-HERE.txt', instruction.encode())]:
            info = zipfile.ZipInfo(name)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            bundle.writestr(info, data, compresslevel=9)
    manifest['entries'].append({
        'archive': archive, 'html': html, 'build': build,
        'htmlSha256': digest(builds[build]),
        'zipSha256': digest((PLAY / archive).read_bytes()),
    })
    print(f'Packaged {archive}: {html}')
(PLAY / 'LATEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
