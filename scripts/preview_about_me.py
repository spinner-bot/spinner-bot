"""Capture desktop and narrow-screen previews of the bilingual About Me card."""

from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "design" / "about-me-preview.html"
PREVIEW_DIR = ROOT / "docs" / "design" / "previews"


def main() -> None:
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            page = browser.new_page(viewport={"width": 1280, "height": 560}, device_scale_factor=1)
            page.goto(PAGE.as_uri())
            page.locator("img").screenshot(path=str(PREVIEW_DIR / "about-me-v2.png"))
            page.set_viewport_size({"width": 390, "height": 780})
            page.locator("img").screenshot(path=str(PREVIEW_DIR / "about-me-mobile-v2.png"))
        finally:
            browser.close()


if __name__ == "__main__":
    main()
