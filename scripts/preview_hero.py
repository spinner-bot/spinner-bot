"""Capture reproducible English, Chinese, and reduced-motion hero previews.

Requires playwright and a locally installed Chromium browser:
    python scripts/preview_hero.py
"""

from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
PREVIEW = ROOT / "docs" / "design" / "hero-preview.html"
OUT = ROOT / "docs" / "design" / "previews"


def capture(page, filename: str, delay_ms: int = 0) -> None:
    page.goto(PREVIEW.as_uri())
    page.locator("img").wait_for(state="visible")
    if delay_ms:
        page.wait_for_timeout(delay_ms)
    page.locator("img").screenshot(path=str(OUT / filename))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            normal = browser.new_context(viewport={"width": 1200, "height": 440}, device_scale_factor=1)
            page = normal.new_page()
            capture(page, "hero-en.png", 300)
            capture(page, "hero-zh.png", 6500)
            normal.close()

            reduced = browser.new_context(
                viewport={"width": 1200, "height": 440},
                device_scale_factor=1,
                reduced_motion="reduce",
            )
            capture(reduced.new_page(), "hero-reduced-motion.png", 300)
            reduced.close()
        finally:
            browser.close()


if __name__ == "__main__":
    main()
