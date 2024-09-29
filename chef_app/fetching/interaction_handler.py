from playwright.async_api import Page
from fetching.playwright_manager import PlaywrightManager
from typing import Optional, List
from bs4 import BeautifulSoup
import asyncio
import re


class InteractionHandler:
    def __init__(self, playwright_manager: PlaywrightManager):
        self.playwright_manager = playwright_manager

    async def click_button(self, element: str) -> None:
        try:
            pattern = r'<button[^>]*\bclass="([^"]+)"'
            match = re.search(pattern, str(element))
            classes = match.group(1).split('"')[0].split()
            selector = f"button.{'.'.join(classes)}"
            page = await self.playwright_manager.get_page()
            buttons = await page.query_selector_all(selector)
            for button in buttons:
                try: 
                    if await button.is_visible():
                        await button.click(force=True)
                        await asyncio.sleep(3)
                        return 
                except Exception as e:
                    print(f"Nie udało się kliknąć przycisku: {e}")
                    continue 
        except Exception as e:
            return("Error ",e)
    async def fill_input(self, element: str, value: str) -> None:
        try:
            pattern = r'<input[^>]*\bclass="([^"]+)"'
            # pattern = element
            match = re.search(pattern, str(element))
            classes = match.group(1).split('"')[0].split()
            selector = f"input.{'.'.join(classes)}"
            

            page = await self.playwright_manager.get_page()
            await page.locator(selector).fill(value=value)
        except Exception as e:
            return("Error ",e)
    async def open_href(self, element: str) -> None:
        try:
            page = await self.playwright_manager.get_page()
            await page.goto(element)
        except Exception as e:
            return("Error ", e)