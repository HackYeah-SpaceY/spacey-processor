from playwright.async_api import Page
from fetching.playwright_manager import PlaywrightManager
from typing import Optional, List
from bs4 import BeautifulSoup
import asyncio
import re

def generate_css_selector(element_string):
    tag_name_match = re.match(r'^<(\w+)', element_string)
    if not tag_name_match:
        raise ValueError("Nie znaleziono tagu w podanym stringu.")
    tag_name = tag_name_match.group(1)
    attributes_string = re.sub(r'^<\w+|\s*\/?>$', '', element_string)
    attributes = re.findall(r'([\w-]+)="(.*?)"', attributes_string)
    selectors = [f'[{name}="{value}"]' for name, value in attributes]
    full_selector = f'{tag_name}{"".join(selectors)}'

    return full_selector

import re

def generate_css_selector_button(element_string):
    tag_name_match = re.match(r'^<(\w+)', element_string)
    if not tag_name_match:
        raise ValueError("Nie znaleziono tagu w podanym stringu.")
    tag_name = tag_name_match.group(1)
    tag_content = re.search(r'^<[^>]+>', element_string)
    if not tag_content:
        raise ValueError("Nie można znaleźć zamknięcia tagu.")
    attributes_string = tag_content.group(0)
    attributes = re.findall(r'([\w-]+)="(.*?)"', attributes_string)
    selectors = [f'[{name}="{value}"]' for name, value in attributes]
    
    full_selector = f'{tag_name}{"".join(selectors)}'
    
    return full_selector


class InteractionHandler:
    def __init__(self, playwright_manager: PlaywrightManager):
        self.playwright_manager = playwright_manager

    async def click_button(self, element: str) -> None:
        try:
            selector=generate_css_selector_button(str(element))
            page = await self.playwright_manager.get_page()
            buttons = await page.query_selector_all(selector)
            for button in buttons:
                try: 
                    if await button.is_visible():
                        await button.scroll_into_view_if_needed()
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
            selector=generate_css_selector(str(element))
            page = await self.playwright_manager.get_page()
            await page.locator(selector).scroll_into_view_if_needed()
            await page.locator(selector).fill(value=value)
        except Exception as e:
            return("Error ",e)
    async def open_href(self, element: str) -> None:
        try:
            page = await self.playwright_manager.get_page()
            await page.goto(element)
        except Exception as e:
            return("Error ", e)
        
    async def scroll_down(self) -> None:
        try:
            page = await self.playwright_manager.get_page()
            print(page.viewport_size)
            # await page.mouse.wheel(0, 700)
            await page.evaluate(f"window.scrollBy(0, {page.viewport_size['height']/2})")
        except Exception as e:
            return("Error ", e)