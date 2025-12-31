from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout


def fetch_html_js(url: str, timeout: int = 45000) -> str:
    """
    Robust JS fetcher for large / JS-heavy pages.
    """
    with sync_playwright() as p:
        #Launch browser
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-gpu", "--no-sandbox", "--disable-dev-shm-usage"],
        )

        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/120 Safari/537.36"
            )
        )

        # Open new page
        page = context.new_page()

        try:
            # Load DOM (do NOT wait for networkidle)
            page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=timeout,
            )

            # Give JS a moment to render
            page.wait_for_timeout(3000)

            # Scroll to trigger lazy-loaded sponsors
            page.evaluate("""
                async () => {
                    for (let i = 0; i < 10; i++) {
                        window.scrollBy(0, document.body.scrollHeight);
                        await new Promise(r => setTimeout(r, 1000));
                    }
                }
            """)

            # Final small wait
            page.wait_for_timeout(2000)

            html = page.content()

        except PlaywrightTimeout:
            # Even if timeout happens, try to salvage HTML
            html = page.content()

        finally:
            browser.close()
            print(f"Fetched URL with JS rendering.")

        return html