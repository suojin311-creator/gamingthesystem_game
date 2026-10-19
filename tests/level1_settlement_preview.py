"""Exercise the exact independent settlement ZIP offline through its real controls."""
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
    started = time.monotonic()
    page.get_by_role('button', name='Run evaluation', exact=True).click()
    expect(page.locator('.score-paper')).to_have_count(0)
    expect(page.locator('.l1-settlement')).to_have_count(0)
    frame = page.frame_locator('iframe')
    expect(frame.locator('.l1-film')).to_have_attribute('data-metric', cinematic_id, timeout=15000)
    expect(frame.locator('.l1-film')).to_have_attribute('data-phase', 'branch')
    duration = float(frame.locator('.settlement-film').get_attribute('data-duration'))
    assert 25.3 <= duration <= 26.7, (id, duration)
    durations[id] = duration
    return frame, started


def seek(frame, fraction):
    """Use the visible Remotion player controls; never change application state."""
    pause = frame.get_by_role('button', name='Pause video', exact=True)
    if pause.count():
        pause.click()
    expect(frame.get_by_role('button', name='Play video', exact=True)).to_be_visible()
    progress = frame.locator('div[style*="touch-action: none"]').first
    bounds = progress.bounding_box()
    assert bounds and bounds['width'] > 0, bounds
    progress.click(position={'x': bounds['width'] * fraction, 'y': 6})


def finish_from_controls(page, frame):
    seek(frame, .97)
    frame.get_by_role('button', name='Play video', exact=True).click()
    expect(page.get_by_role('heading', name='What changed?', exact=True)).to_be_visible(timeout=8000)


def check_settlement(page, metric):
    id, _, label, before, after, behaviour, _ = metric
    settlement = page.locator('.l1-settlement')
    expect(settlement).to_be_visible()
    expect(settlement.locator('.l1-settlement-card')).to_have_count(2)
    expect(settlement.locator('.l1-settlement-metric h2')).to_have_text(label)
    expect(settlement.locator('.l1-settlement-score')).to_have_text([str(before), str(after)])
    expect(settlement.locator('.l1-settlement-target')).to_have_text('Target 70 met')
    expect(settlement.locator('.l1-settlement-score-note')).to_have_text('Illustrative score')
    expect(settlement.locator('.l1-settlement-behaviour')).to_have_text(behaviour)
    expect(page.locator('.dialogue-strip, .alex-bubble, .perspectives, .score-paper')).to_have_count(0)
    details = settlement.locator('details')
    assert details.get_attribute('open') is None
    details.locator('summary').click()
    expect(details.locator('blockquote')).to_have_text(prediction)
    # Results describe the selected metric, without rating the player's free text.
    assert not settlement.locator('[data-prediction-score], .prediction-score').count()
    assert not any(term in details.inner_text().lower() for term in ('correct', 'incorrect', 'points', 'score'))
    expect(page.get_by_role('button', name='Replay animation', exact=True)).to_be_enabled()
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

        # One full, normal-motion, real-time run: no clock installation or seeking.
        frame, started = begin(page, metrics[0])
        observe_text(page, frame, metrics[0][-1])
        assert frame.locator('.l1-film img').evaluate_all('images => images.length > 0 && images.every(image => image.complete && image.naturalWidth > 0)')
        expect(frame.locator('.l1-film')).to_have_attribute('data-phase', 'common', timeout=15000)
        observe_text(page, frame, common)
        expect(frame.locator('.l1-film')).to_have_attribute('data-phase', 'office', timeout=10000)
        expect(frame.locator('.l1-office-result')).to_contain_text(metrics[0][2], timeout=8000)
        observe_text(page, frame, 'The numbers look great... but something still feels wrong.', timeout=8000)
        observe_text(page, frame, 'Maybe one metric is too narrow.')
        observe_text(page, frame, 'What if we measured more than one?')
        expect(page.get_by_role('heading', name='What changed?', exact=True)).to_be_visible(timeout=8000)
        elapsed = time.monotonic() - started
        assert elapsed >= durations['peer'] - .5, (elapsed, durations['peer'])
        playback = {'metric': 'peer', 'realTimeSeconds': round(elapsed, 2), 'displayedDurationSeconds': durations['peer'], 'clockAccelerated': False}
        check_settlement(page, metrics[0])
        screenshot(page, 'level1-settlement-preview-desktop.png')
        record('Peer response plays branch → common → office with both thoughts and the final bridge in real time, then opens the correct dialogue-free settlement (' + str(round(elapsed, 2)) + ' seconds)')

        page.get_by_role('button', name='Replay animation', exact=True).click()
        replay = page.frame_locator('iframe')
        expect(replay.locator('.l1-film')).to_have_attribute('data-metric', metrics[0][1], timeout=15000)
        expect(replay.locator('.l1-film')).to_have_attribute('data-phase', 'branch')
        expect(page.locator('.l1-settlement')).to_have_count(0)
        finish_from_controls(page, replay)
        check_settlement(page, metrics[0])
        record('Replay starts the same branch in a fresh iframe and returns to the same result without legacy review UI')

        for metric in metrics[1:]:
            page.get_by_role('button', name='Try another metric', exact=True).click()
            frame, _ = begin(page, metric)
            seek(frame, .10)
            expect(frame.locator('.l1-film')).to_contain_text(metric[-1])
            assert frame.locator('.l1-film img').evaluate_all('images => images.length > 0 && images.every(image => image.complete && image.naturalWidth > 0)')
            seek(frame, .40)
            expect(frame.locator('.l1-film')).to_have_attribute('data-phase', 'common')
            expect(frame.locator('.l1-film')).to_contain_text(common)
            seek(frame, .60)
            expect(frame.locator('.l1-film')).to_have_attribute('data-phase', 'office')
            expect(frame.locator('.l1-office-result')).to_contain_text(metric[2])
            seek(frame, .72)
            observe_text(page, frame, 'The numbers look great... but something still feels wrong.')
            seek(frame, .85)
            observe_text(page, frame, 'Maybe one metric is too narrow.')
            seek(frame, .94)
            observe_text(page, frame, 'What if we measured more than one?')
            finish_from_controls(page, frame)
            check_settlement(page, metric)
            record(metric[0] + ': correct branch, common/office, scores, behaviour and unscored verbatim prediction through real player controls')

        page.set_viewport_size({'width': 390, 'height': 900})
        no_horizontal_overflow(page)
        screenshot(page, 'level1-settlement-preview-mobile.png')
        page.get_by_role('button', name='Try another metric', exact=True).click()
        no_horizontal_overflow(page)
        frame, _ = begin(page, metrics[0])
        no_horizontal_overflow(page)
        assert frame.locator('html').evaluate('element => element.scrollWidth <= innerWidth')
        finish_from_controls(page, frame)
        check_settlement(page, metrics[0])
        no_horizontal_overflow(page)
        record('At 390px the choice form, iframe and two-card settlement fit without horizontal overflow; Try another resets all six choices')

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
