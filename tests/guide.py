"""Browser checks for the short guide and accurate score-label placement."""
import argparse
import json
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

parser = argparse.ArgumentParser()
parser.add_argument('--file')
parser.add_argument('--url', default='http://127.0.0.1:5173/')
args = parser.parse_args()
artifact = Path(args.file).resolve().read_bytes() if args.file else None
url = 'https://level-one.test/' if args.file else args.url
output = Path(__file__).resolve().parents[1] / 'test-results'
checks = []
errors = []

def record(name):
    checks.append(name)
    print('PASS', name, flush=True)

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--no-sandbox'])
    for width, height in [(1366, 768), (960, 720), (390, 844), (320, 640)]:
        context = browser.new_context(viewport={'width': width, 'height': height}, reduced_motion='reduce')
        if artifact:
            context.set_offline(True)
            context.route('https://level-one.test/**', lambda r: r.fulfill(status=200, content_type='text/html', body=artifact))
        page = context.new_page()
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.goto(url, wait_until='networkidle')
        guide = page.get_by_role('dialog', name='Workbench guide')
        expect(guide).to_be_visible()
        expect(page.get_by_role('button', name='Next', exact=True)).to_be_focused()
        for _ in range(4):
            page.keyboard.press('Tab')
            assert page.evaluate('document.activeElement.closest(".workbench-guide") !== null')
        for index, title in enumerate(['Your decisions', 'Management’s view', 'The students’ view', 'The conversation']):
            expect(guide.get_by_role('heading', name=title, exact=True)).to_be_visible()
            card = page.locator('.guide-card').bounding_box()
            spot = page.locator('.guide-spotlight').bounding_box()
            assert card['x'] >= 0 and card['y'] >= 0
            assert card['x'] + card['width'] <= width + 1
            assert card['y'] + card['height'] <= height + 1
            assert spot['width'] > 30 and spot['height'] > 30
            if index == 2 and width in (1366, 390):
                page.screenshot(path=str(output / f'guide-{width}.png'), full_page=True)
            if index == 3:
                page.wait_for_timeout(800)
                assert page.locator('.maya-bubble p').count() == 0, 'Guide must pause new dialogue'
                page.get_by_role('button', name='Start Level 1').click()
            else:
                page.get_by_role('button', name='Next', exact=True).click()
        expect(guide).to_have_count(0)
        page.locator('.dialogue-strip').scroll_into_view_if_needed()
        expect(page.locator('.maya-bubble p')).to_have_text('Where should I start?')
        record(f'{width}px: four anchored guide steps fit, trap keyboard focus, and pause dialogue')

        page.reload(wait_until='networkidle')
        expect(guide).to_be_visible()
        page.get_by_role('button', name='Skip guide').click()
        page.get_by_test_id('metric-part').click()
        page.get_by_role('button', name='Guide', exact=True).click()
        expect(guide).to_be_visible()
        page.keyboard.press('Escape')
        expect(guide).to_have_count(0)
        expect(page.get_by_role('button', name='Guide', exact=True)).to_be_focused()
        expect(page.get_by_test_id('metric-part')).to_have_attribute('aria-pressed', 'true')
        record(f'{width}px: guide returns for every new page and preserves in-page choices when reopened')

        page.get_by_role('button', name='Make a prediction').click()
        page.get_by_label('What do you expect students to do?').fill('Students will develop ideas.')
        page.get_by_role('button', name='Run evaluation').click()
        expect(page.get_by_role('button', name='Observe the class')).to_be_enabled(timeout=10000)
        label = page.locator('.target-label').bounding_box()
        line = page.locator('.score-track > i').bounding_box()
        assert abs((label['x'] + label['width'] / 2) - (line['x'] + line['width'] / 2)) <= 1
        assert label['y'] >= line['y'] + line['height']
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        if width == 1366:
            page.screenshot(path=str(output / 'target-aligned.png'), full_page=True)
        page.get_by_role('button', name='Guide', exact=True).click()
        page.get_by_role('button', name='Skip guide').click()
        expect(page.locator('.after-score')).to_contain_text('85')
        record(f'{width}px: Target 70 sits under its real marker; reopening guide retains the evaluation')
        context.close()

    assert not errors, errors
    browser.close()

name = 'guide-offline-results.json' if args.file else 'guide-results.json'
(output / name).write_text(json.dumps({'passed': len(checks), 'checks': checks, 'runtime_errors': errors}, indent=2))
print(f'{len(checks)} guide and alignment checks passed.')
