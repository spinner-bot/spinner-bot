"""Capture desktop, mobile, and reduced-motion invitation previews."""

from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "design" / "connect-preview.html"
PREVIEWS = ROOT / "docs" / "design" / "previews"


def main() -> None:
    PREVIEWS.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            page = browser.new_page(viewport={"width": 1248, "height": 900}, device_scale_factor=1)
            page.goto(PAGE.as_uri())
            page.locator("picture img").screenshot(path=str(PREVIEWS / "connect-desktop-v1.png"))
            page.set_viewport_size({"width": 390, "height": 900})
            page.locator("picture img").screenshot(path=str(PREVIEWS / "connect-mobile-v1.png"))
            page.wait_for_timeout(1500)
            page.locator("picture img").screenshot(path=str(PREVIEWS / "connect-mobile-motion-v1.png"))
            reduced_context = browser.new_context(viewport={"width": 390, "height": 900}, reduced_motion="reduce")
            reduced = reduced_context.new_page()
            reduced.goto(PAGE.as_uri())
            reduced.locator("picture img").screenshot(path=str(PREVIEWS / "connect-reduced-motion-v1.png"))
            reduced_context.close()
        finally:
            browser.close()


if __name__ == "__main__":
    main()
