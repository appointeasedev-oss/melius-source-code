import asyncio
from playwright.async_api import async_playwright

class MeliusBrowser:
    def __init__(self):
        self.browser = None
        self.page = None

    async def start(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
        self.page = await self.browser.new_page()

    async def navigate(self, url):
        if not self.page:
            await self.start()
        await self.page.goto(url)
        return await self.page.title()

    async def get_content(self):
        if self.page:
            return await self.page.content()
        return ""

    async def close(self):
        if self.browser:
            await self.browser.close()
            await self.playwright.stop()
