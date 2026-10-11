"""Capture the timeline at README desktop and mobile widths."""

from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "design" / "timeline-preview.html"
PREVIEWS = ROOT / "docs" / "design" / "previews"


def main() -> None:
    PREVIEWS.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            page = browser.new_page(viewport={"width": 1248, "height": 900}, device_scale_factor=1)
            page.goto(PAGE.as_uri())
            page.locator("picture img").screenshot(path=str(PREVIEWS / "timeline-desktop-v2.png"))
            page.set_viewport_size({"width": 390, "height": 900})
            page.locator("picture img").screenshot(path=str(PREVIEWS / "timeline-mobile-v2.png"))
        finally:
            browser.close()


if __name__ == "__main__":
    main()
