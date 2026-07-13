import asyncio
from playwright.async_api import async_playwright

class BrowserOperator:
    async def execute(self, action: str, url: str = None, selector: str = None, text: str = None):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            result = ""
            try:
                if action == "navigate" and url:
                    await page.goto(url)
                    result = f"Navigated to {url}"
                elif action == "click" and selector:
                    await page.click(selector)
                    result = f"Clicked {selector}"
                elif action == "type" and selector and text:
                    await page.fill(selector, text)
                    result = f"Typed '{text}' into {selector}"
                elif action == "screenshot":
                    path = "web_screenshot.png"
                    await page.screenshot(path=path)
                    result = f"Screenshot saved to {path}"

                # Capture state
                title = await page.title()
                result += f" | Current Title: {title}"
            except Exception as e:
                result = f"Browser error: {e}"
            finally:
                await browser.close()
            return result

    def run_sync(self, *args, **kwargs):
        """Wrapper to run the async execute method in a synchronous context."""
        return asyncio.run(self.execute(*args, **kwargs))
