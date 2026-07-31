from playwright.sync_api import sync_playwright


def get_page_content(url: str) -> str:
    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        print("Opening page...")

        page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=30000
        )

        print("Page loaded!")

        html = page.content()

        browser.close()

        return html