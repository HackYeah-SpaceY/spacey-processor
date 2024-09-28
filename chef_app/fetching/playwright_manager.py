from playwright.async_api import async_playwright, Browser, Page
import asyncio
class PlaywrightManager:
    def __init__(self, url: str):
        self.url = url
        self.playwright = None
        self.browser = None
        self.page = None

    async def __aenter__(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
        self.page = await self.browser.new_page()
        await self.page.goto(self.url, timeout=10000)
        await asyncio.sleep(3)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return

    async def close(self):
        await self.page.close()
        await self.browser.close()
        await self.playwright.stop()

    async def get_page_content(self) -> str:
        return await self.page.content()

    async def get_page(self) -> Page:
        return self.page
    
    async def save_screenshot(self):
        await self.page.screenshot(path="screenshot.jpg")
        