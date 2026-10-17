"""Publish the latest offline previews from one set of production builds.

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
     'Level 2 only. Continue to Level 3 is reserved and disabled in this standalone entry.'),
    ('Level3-play.zip', 'Level3.html', 'dist-level3/index.html',
     'Level 3 only. Choose priorities, set weights and compare Alex’s responses. Design Lab is reserved.'),
    ('Full-game-play.zip', 'Gaming-the-System.html', 'dist/index.html',
     'Start at Level 1, then continue to Level 2 and Level 3 in the same open game.'),
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

# One review download contains both requested entry points from the same builds.
review_archive = 'Level3-and-Full-game-play.zip'
review_files = {
    'Level3/Level3.html': builds['dist-level3/index.html'],
    'Full-game/Gaming-the-System.html': builds['dist/index.html'],
}
review_instruction = (
    'Gaming the System — latest review package\n\n'
    '1. Level 3 only: open Level3/Level3.html\n'
    '2. Levels 1 -> 2 -> 3: open Full-game/Gaming-the-System.html\n\n'
    'Extract the entire ZIP first, then open either HTML in Chrome or Edge.\n'
    'Both entries use the same latest gameplay. No installation or internet is needed.\n'
    'The combined game carries your Level 2 choices into Level 3; you can change them.\n'
    'Previews stop at the final theory placeholder. Restart is not available.\n'
)
with zipfile.ZipFile(PLAY / review_archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
    for name, data in [*review_files.items(), ('START-HERE.txt', review_instruction.encode())]:
        info = zipfile.ZipInfo(name)
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o644 << 16
        bundle.writestr(info, data, compresslevel=9)
manifest['reviewBundle'] = {
    'archive': review_archive,
    'zipSha256': digest((PLAY / review_archive).read_bytes()),
    'htmlSha256': {name: digest(data) for name, data in review_files.items()},
}
print(f'Packaged {review_archive}: standalone Level 3 and connected Levels 1–3')
(PLAY / 'LATEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
