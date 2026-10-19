"""Play the exact player-facing ZIP offline, without test clocks or hidden seek controls."""
import hashlib
import json
import time
from pathlib import Path
from urllib.parse import unquote, urlsplit
from zipfile import ZipFile

from playwright.sync_api import expect, sync_playwright


root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / 'play/LEVEL1_SETTLEMENT_PREVIEW.json').read_text())
archive = root / 'play' / manifest['archive']
out = root / 'test-results'
out.mkdir(exist_ok=True)
origin = 'https://level1-settlement.test'
checks, errors, external_requests = [], [], []
durations, playback = {}, {}
screenshots = []
diagnostics = []

metrics = [
    ('peer', 'online-peer-response-quality', 'Online Peer Response Quality', 27, 86,
     'Replying to tick boxes.', 'Specific suggestion? Check. Follow-up question? Check!'),
    ('prep', 'pre-class-preparation', 'Pre-class Preparation', 34, 88,
     'Skimming just to finish.', 'I finished everything on the list!'),
    ('part', 'in-class-participation', 'In-class Participation', 29, 85,
     'More talk. Little explanation.', 'I agree! Same here!'),
    ('focus', 'on-task-focus', 'On-task Focus', 41, 91,
     'Looking busy takes priority.', 'Look, I stayed on task the whole time!'),
    ('discuss', 'in-class-discussion-quality', 'In-class Discussion Quality', 32, 84,
     'Discussion turns formulaic.', 'Could you elaborate? I’d like to build on that.'),
    ('reflect', 'learning-reflection-quality', 'Learning Reflection Quality', 38, 89,
     'Repeating safe reflection patterns.', 'Before, I thought... Now, I think...'),
]
common = 'Professor! I figured out exactly what you were looking for!'
prediction = 'I expect better ideas — keep my prediction exactly as written.'


def record(message):
    checks.append(message)
    print('PASS', message, flush=True)


def no_horizontal_overflow(page):
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), page.viewport_size


def observe_text(page, frame, text, timeout=6000):
    try:
        expect(frame.locator('.l1-film')).to_contain_text(text, timeout=timeout)
    except BaseException:
        # Preserve playback evidence before Playwright closes the browser.
        for document in page.frames:
            diagnostics.append(document.evaluate('''() => ({
                url: location.href,
                hidden: document.hidden,
                metric: document.querySelector('.l1-film')?.dataset.metric,
                phase: document.querySelector('.l1-film')?.dataset.phase,
                filmText: document.querySelector('.settlement-film')?.innerText,
                buttons: [...document.querySelectorAll('button')].map(button => ({
                    label: button.getAttribute('aria-label'),
                    title: button.getAttribute('title'), text: button.innerText
                }))
            })'''))
        screenshot(page, 'level1-settlement-preview-failure.png')
        raise


def begin(page, metric):
    id, cinematic_id, *_ = metric
    expect(page.get_by_role('heading', name='What will you measure?', exact=True)).to_be_visible()
    expect(page.locator('[data-testid^="metric-"]:not([data-testid="metric-choice-tray"])')).to_have_count(6)
    page.get_by_test_id('metric-' + id).click()
    page.get_by_role('button', name='Make a prediction', exact=True).click()
    page.get_by_label('What do you expect students to do?', exact=True).fill(prediction)
    button = page.get_by_role('button', name='Run evaluation', exact=True)
    button_box = button.bounding_box()
    row_box = page.locator('.prediction-actions').bounding_box()
    assert abs(button_box['x'] + button_box['width'] - row_box['x'] - row_box['width']) <= 2
    expect(page.locator('.stepper li > span:last-child')).to_have_text(['Choose', 'Predict', 'Evaluate', 'Observe'])
    button.click()
    expect(page.locator('.score-paper')).to_be_visible()
    expect(page.locator('.score-paper .before-score')).to_contain_text(str(metric[3]))
    expect(page.locator('.score-paper .after-score')).to_contain_text(str(metric[4]))
    expect(page.get_by_role('heading', name='Target achieved.', exact=True)).to_be_visible(timeout=8000)
    expect(page.locator('.stepper [aria-current="step"]')).to_contain_text('Evaluate')
    expect(page.locator('.score-paper')).to_contain_text('Target 70')
    expect(page.locator('.score-paper')).to_contain_text('Illustrative score')
    expect(page.locator('[role="progressbar"][aria-label="Management satisfaction"]')).to_have_attribute('aria-valuenow', '44')
    expect(page.locator('iframe')).to_have_count(0)
    observe = page.get_by_role('button', name='Observe the class', exact=True)
    expect(observe).to_be_enabled()
    page.evaluate('''() => {
      window.__filmAudit = {samples: [], issues: []};
      window.__settlementAudit = {samples: [], barEnd: null};
      window.__settlementProbe?.disconnect();
      cancelAnimationFrame(window.__settlementRaf);
      let sampling = false;
      const sampleSettlement = () => {
        const recap = document.querySelector('.l1-settlement');
        if (!recap) { sampling = false; return; }
        const track = recap.querySelector('.management-satisfaction-track');
        const fill = track.firstElementChild;
        window.__settlementAudit.samples.push({time: performance.now(),
          stage: recap.dataset.stage,
          replay: recap.querySelector('.management-satisfaction').dataset.replayState,
          width: fill.getBoundingClientRect().width / track.getBoundingClientRect().width,
          student: !!recap.querySelector('.student-behaviour'),
          waiting: !!recap.querySelector('.pending-title')});
        if (recap.dataset.stage !== 'observed') window.__settlementRaf = requestAnimationFrame(sampleSettlement);
        else sampling = false;
      };
      window.__settlementProbe = new MutationObserver(() => {
        if (!sampling && document.querySelector('.l1-settlement')) {
          sampling = true;
          window.__settlementRaf = requestAnimationFrame(sampleSettlement);
        }
      });
      window.__settlementProbe.observe(document.getElementById('root'), {childList: true, subtree: true});
      if (!window.__filmListener) {
        window.__filmListener = true;
        addEventListener('transitionend', event => {
          if (event.propertyName === 'width' && event.target.matches('.l1-settlement .management-satisfaction-track > span')) window.__settlementAudit.barEnd = performance.now();
        }, true);
        addEventListener('message', event => {
          if (event.source !== document.querySelector('iframe')?.contentWindow || event.data?.channel !== 'test-film-probe') return;
          window.__filmAudit.samples.push(event.data.sample);
          window.__filmAudit.issues.push(...event.data.issues);
        });
      }
    }''')
    started = time.monotonic()
    observe.click()
    expect(page.locator('.score-paper')).to_have_count(0)
    expect(page.locator('.workbench-heading')).to_be_visible()
    expect(page.locator('.stepper')).to_be_visible()
    expect(page.locator('.stepper [aria-current="step"]')).to_contain_text('Observe')
    nav_box = page.locator('.stepper').bounding_box()
    film_box = page.locator('.settlement-cinematic').bounding_box()
    assert film_box['y'] >= nav_box['y'] + nav_box['height'] - 1
    expect(page.locator('.l1-settlement')).to_have_count(0)
    frame = page.frame_locator('iframe')
    expect(frame.locator('.l1-film')).to_have_attribute('data-metric', cinematic_id, timeout=15000)
    expect(frame.locator('.l1-film')).to_have_attribute('data-phase', 'branch')
    duration = float(frame.locator('.settlement-film').get_attribute('data-duration'))
    assert 25.7 <= duration <= 27.1, (id, duration)
    durations[id] = duration
    frame.locator('.settlement-film').evaluate(PROBE)
    return frame, started


# Observation only: samples the actual rendered frames, without changing playback.
PROBE = r"""film => {
  let priorKey = '';
  const poses = new Map();
  let priorPhase = null;
  let priorCover = 0;
  const sample = () => {
    const root = film.querySelector('.l1-film');
    if (!root) return;
    const phase = root.dataset.phase;
    const source = Number(root.dataset.sourceSeconds);
    const issues = [];
    const cover = Number(getComputedStyle(root.querySelector('.l1-scene-cover')).opacity);
    // Under frame drops, a fully covered last old frame also protects the cut.
    if (priorPhase && phase !== priorPhase && cover < .99 && priorCover < .99) issues.push(`Uncovered scene swap ${priorPhase} -> ${phase}, source ${source}, cover ${priorCover} -> ${cover}`);
    priorPhase = phase;
    priorCover = cover;
    if (root.querySelector('.l1-dialogue-shade, .l1-office-thought-shade, .l1-scene-shading, .l1-office .vignette')) issues.push('Removed subtitle shadow layer returned');
    const shots = root.querySelectorAll('.l1-scene');
    if (shots.length !== 1) issues.push('Overlapping scene layers: ' + shots.length);
    if (shots[0] && getComputedStyle(shots[0]).opacity !== '1') issues.push('Scene dissolve at ' + source);
    if (root.querySelector('.l1-office-memory, .l1-office-concepts')) issues.push('Removed montage/memory mounted at ' + source);
    if (phase === 'office' && root.querySelector('.l1-branch-world, .l1-common-plate')) issues.push('Alex reappeared in the office at ' + source);
    if (film.querySelector('button, [role="slider"], [role="progressbar"]')) issues.push('Player controls became visible');
    const camera = phase === 'branch' ? root.querySelector('.l1-branch-world > div:first-child > div:first-child') : root.querySelector('.office-camera');
    const pose = camera ? [getComputedStyle(camera).scale, getComputedStyle(camera).translate].join('|') : null;
    if (pose) {
      if (poses.has(phase) && poses.get(phase) !== pose) issues.push('Camera moved within ' + phase + ': ' + pose);
      poses.set(phase, pose);
    }
    const caption = root.querySelector('.l1-spoken [role="status"], .l1-office > [role="status"]')?.textContent ?? '';
    const key = [phase, caption, Math.floor(source * 4), Math.round(cover * 10)].join('|');
    if (key !== priorKey || issues.length) {
      priorKey = key;
      parent.postMessage({channel: 'test-film-probe', sample: {phase, source, caption, pose, cover}, issues}, '*');
    }
  };
  new MutationObserver(sample).observe(film, {subtree: true, childList: true, attributes: true, characterData: true});
  sample();
}"""

branch_tail = {
    'peer': ['Did you really discuss their ideas?', 'I met every response criterion.'],
    'prep': ['What was the main idea in the reading?', 'Uh... I finished the checklist.'],
    'part': ['Can you explain why?', 'I just wanted to participate.'],
    'focus': ['What did you discover?', 'I... kept the page open.'],
    'discuss': ['What new idea came out of the discussion?', 'I followed the discussion checklist.'],
    'reflect': ['What actually changed your mind?', 'That’s the format on the rubric.'],
}
thoughts = ['The numbers look great... but something still feels wrong.', 'Maybe one metric is too narrow.', 'What if we measured more than one?']


def watch_movie(page, frame, metric, started, capture=False):
    if capture:
        # Hover/click/space must not reveal controls or accidentally pause the movie.
        frame.locator('.settlement-film').hover()
        frame.locator('.settlement-film').click()
        page.keyboard.press('Space')
        expect(frame.locator('button, [role="slider"], [role="progressbar"]')).to_have_count(0)
        expect(frame.locator('.l1-office-result')).to_be_visible(timeout=40000)
        expect(frame.locator('.l1-office-result')).to_contain_text(metric[2])
        assert frame.locator('.l1-office img').evaluate_all('images => images.length > 0 && images.every(image => image.complete && image.naturalWidth > 0)')
        screenshot(page, 'level1-settlement-preview-film.png')
    expect(page.get_by_role('heading', name='What changed?', exact=True)).to_be_visible(timeout=50000)
    elapsed = time.monotonic() - started
    assert elapsed >= durations[metric[0]] - .5
    audit = page.evaluate('window.__filmAudit')
    if audit['issues']: diagnostics.append(audit)
    assert not audit['issues'], audit['issues']
    phases = list(dict.fromkeys(sample['phase'] for sample in audit['samples']))
    assert phases == ['branch', 'common', 'office'], phases
    assert audit['samples'][-1]['cover'] >= .99, audit['samples'][-1]
    captions = [sample['caption'] for sample in audit['samples'] if sample['cover'] < .01]
    for text in [metric[-1], *branch_tail[metric[0]], common, *thoughts]:
        assert text in captions, (metric[0], text, captions)
    assert captions.index(thoughts[0]) < captions.index(thoughts[1]) < captions.index(thoughts[2])
    for phase, expected in [('branch', '1.025|0% 0%'), ('office', '2.65|62.275% -1.325%')]:
        values = {sample['pose'] for sample in audit['samples'] if sample['phase'] == phase and sample['pose']}
        assert values == {expected}, (phase, values)
    playback[metric[0]] = {'realTimeSeconds': round(elapsed, 2), 'displayedDurationSeconds': durations[metric[0]],
                           'clockAccelerated': False, 'observedFrames': len(audit['samples']), 'issues': []}


def check_settlement(page, metric):
    id, _, label, before, after, behaviour, _ = metric
    settlement = page.locator('.l1-settlement')
    expect(settlement).to_be_visible()
    expect(settlement.locator('.perspective')).to_have_count(2)
    expect(settlement.locator('.perspective-heading h3')).to_have_text(['Management’s view', 'Students'])
    expect(settlement.locator('.l1-settlement-metric h2')).to_have_text(label)
    expect(settlement.locator('.management-satisfaction-label')).to_have_text('Satisfaction')
    expect(settlement.locator('.management-satisfaction-state')).to_have_text('Satisfied')
    expect(settlement.get_by_role('progressbar', name='Management satisfaction')).to_have_attribute('aria-valuenow', '44')
    expect(settlement.locator('.management-satisfaction-evidence')).to_have_text(f'Reported score {after} · target met')
    expect(settlement.locator('.student-behaviour')).to_have_text(behaviour)
    expect(settlement).to_have_attribute('data-stage', 'observed')
    page.wait_for_function('window.__settlementAudit.samples.some(sample => sample.student)')
    audit = page.evaluate('window.__settlementAudit')
    samples = audit['samples']
    assert any(sample['waiting'] and not sample['student'] for sample in samples), samples
    assert all(not sample['student'] for sample in samples if sample['replay'] != 'complete'), samples
    assert abs(samples[-1]['width'] - .44) < .005, samples[-1]
    reduced = page.evaluate('matchMedia("(prefers-reduced-motion: reduce)").matches')
    if not reduced:
        assert any(.14 < sample['width'] < .42 for sample in samples), samples
        assert audit['barEnd'] is not None
        firstStudent = next(sample['time'] for sample in samples if sample['student'])
        assert firstStudent - audit['barEnd'] >= 200, (firstStudent, audit['barEnd'])
    expect(settlement.locator('.settlement-student-visual')).to_have_attribute('data-metric', id)
    expect(settlement.locator('.observation-outside')).to_have_count(0)
    words = settlement.locator('.student-behaviour').bounding_box()
    picture = settlement.locator('.settlement-student-visual').bounding_box()
    assert words['x'] + words['width'] <= picture['x'], (words, picture)
    expect(settlement.locator('.learning-risk')).to_have_text('Learning at risk')
    expect(settlement.locator('.management-attention')).to_have_count(0)
    expect(page.locator('.dialogue-strip, .alex-bubble, .score-paper, .classroom-observation, .observation-recap')).to_have_count(0)
    expect(page.locator('.stepper li > span:last-child')).to_have_text(['Choose', 'Predict', 'Evaluate', 'Observe'])
    expect(page.locator('.stepper li.done')).to_have_count(4)
    expect(settlement.get_by_text('Measured result', exact=True)).to_have_count(0)
    expect(settlement.get_by_text('Classroom result', exact=True)).to_have_count(0)
    # Desktop cards balance each other; mobile stacks them inside the workbench.
    cards = settlement.locator('.perspective')
    first, second = cards.nth(0).bounding_box(), cards.nth(1).bounding_box()
    if page.viewport_size['width'] > 650:
        assert abs(first['y'] - second['y']) <= 1
        assert abs(first['height'] - second['height']) <= 1
    else:
        assert second['y'] >= first['y'] + first['height']
    details = settlement.locator('details')
    assert details.get_attribute('open') is None
    details.locator('summary').click()
    expect(details.locator('blockquote')).to_have_text(prediction)
    # Results describe the selected metric, without rating the player's free text.
    assert not settlement.locator('[data-prediction-score], .prediction-score').count()
    assert not any(term in details.inner_text().lower() for term in ('correct', 'incorrect', 'points', 'score'))
    expect(page.get_by_role('button', name='Replay animation', exact=True)).to_have_count(0)
    expect(page.get_by_role('button', name='Try another metric', exact=True)).to_be_enabled()
    no_horizontal_overflow(page)


def screenshot(page, name):
    path = out / name
    page.screenshot(path=str(path), full_page=True)
    screenshots.append(str(path.relative_to(root)))


failure = None
try:
    assert hashlib.sha256(archive.read_bytes()).hexdigest() == manifest['zipSha256']
    with ZipFile(archive) as bundle:
        assert bundle.testzip() is None
        files = {name: bundle.read(name) for name in bundle.namelist()}
    assert set(files) == set(manifest['entries'])
    for name, digest in manifest['entries'].items():
        assert hashlib.sha256(files[name]).hexdigest() == digest, name
    with ZipFile(root / 'play/Level1-play.zip') as original:
        assert original.testzip() is None
        assert files['Current-Level1.html'] == original.read('Level1.html')
    record('Archive CRC, ZIP hash and every entry hash match; Current-Level1.html is byte-identical to the original Level1-play.zip')

    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
        context = browser.new_context(viewport={'width': 1366, 'height': 1000}, reduced_motion='no-preference')
        context.set_offline(True)

        def serve(route):
            url = urlsplit(route.request.url)
            name = unquote(url.path.lstrip('/'))
            if url.netloc == 'level1-settlement.test' and name in files:
                route.fulfill(status=200, content_type='text/html' if name.endswith('.html') else 'text/plain', body=files[name])
            else:
                external_requests.append(route.request.url)
                route.abort()

        context.route('**/*', serve)
        page = context.new_page()
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.goto(origin + '/START-HERE.html', wait_until='networkidle')
        expect(page.locator('a[href="Level1-settlement.html"]')).to_be_visible()
        expect(page.locator('a[href="Current-Level1.html"]')).to_be_visible()
        no_horizontal_overflow(page)
        page.locator('a[href="Level1-settlement.html"]').click()
        page.get_by_role('button', name='Skip guide', exact=True).click()
        record('The offline launcher opens the actual new HTML and its six-choice Level 1 form')

        page.set_viewport_size({'width': 390, 'height': 900})
        page.emulate_media(reduced_motion='reduce')
        frame, started = begin(page, metrics[0])
        watch_movie(page, frame, metrics[0], started)
        check_settlement(page, metrics[0])
        record('Reduced motion completes the recap sequence without waiting for a missing width transition event; fixed shots and complete readable dialogue remain')

        page.emulate_media(reduced_motion='no-preference')
        page.set_viewport_size({'width': 1366, 'height': 1000})
        page.get_by_role('button', name='Try another metric', exact=True).click()

        # Every ending uses actual normal-speed playback; there are no seek controls.
        for index, metric in enumerate(metrics):
            if index:
                page.get_by_role('button', name='Try another metric', exact=True).click()
            frame, started = begin(page, metric)
            watch_movie(page, frame, metric, started, capture=index == 0)
            check_settlement(page, metric)
            if index == 0:
                screenshot(page, 'level1-settlement-preview-desktop.png')
            record(metric[0] + ': normal-speed full branch/common/office, every authored line, single opaque shots, fixed cameras, covered scene swaps without subtitle shading, no memory/montage/controls/replay; actual bar rise finishes before the matching illustrated student outcome')

        page.set_viewport_size({'width': 390, 'height': 900})
        no_horizontal_overflow(page)
        screenshot(page, 'level1-settlement-preview-mobile.png')
        page.get_by_role('button', name='Try another metric', exact=True).click()
        no_horizontal_overflow(page)
        frame, started = begin(page, metrics[0])
        no_horizontal_overflow(page)
        assert frame.locator('html').evaluate('element => element.scrollWidth <= innerWidth')
        watch_movie(page, frame, metrics[0], started)
        check_settlement(page, metrics[0])
        no_horizontal_overflow(page)
        record('At 390px the choice form, automatic movie and two-card settlement fit without horizontal overflow; Try another resets all six choices')

        page.goto(origin + '/START-HERE.html', wait_until='networkidle')
        no_horizontal_overflow(page)
        page.locator('a[href="Current-Level1.html"]').click()
        page.get_by_role('button', name='Skip guide', exact=True).click()
        expect(page.get_by_role('heading', name='What will you measure?', exact=True)).to_be_visible()
        expect(page.get_by_test_id('metric-prep')).to_be_visible()
        expect(page.locator('.l1-settlement-preview, .l1-settlement, iframe')).to_have_count(0)
        record('The launcher also fits 390px and opens the unchanged original HTML at its original metric-choice screen')
        assert not errors, errors
        assert not external_requests, external_requests
        record('The actual archive runs offline with zero external requests and zero browser runtime errors')
        context.close()
        browser.close()
except BaseException as error:
    failure = str(error)
    raise
finally:
    result = {'passed': len(checks), 'checks': checks, 'runtimeErrors': errors,
              'externalRequests': external_requests, 'archive': manifest['archive'],
              'zipSha256': manifest['zipSha256'], 'branchDurationsSeconds': durations,
              'realTimePlayback': playback, 'screenshots': screenshots,
              'failureDiagnostics': diagnostics, 'failure': failure}
    (out / 'level1-settlement-preview-results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
