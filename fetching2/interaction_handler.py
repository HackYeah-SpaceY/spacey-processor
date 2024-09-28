from playwright.async_api import Page
from playwright_manager import PlaywrightManager
from typing import Optional, List
from bs4 import BeautifulSoup
class InteractionHandler:
    def __init__(self, playwright_manager: PlaywrightManager):
        self.playwright_manager = playwright_manager

    async def click_button(self, element: str) -> None:
        page = await self.playwright_manager.get_page()
        await page.locator(element).click()

    async def fill_input(self, element: str, value: str) -> None:
        try:
            page = await self.playwright_manager.get_page()
            data = await page.content()
            soup = BeautifulSoup(data, 'html.parser')
            target_element = soup.find(element)
            components = []
            child = target_element if target_element.name else target_element.parent
            for parent in child.parents:
                siblings = parent.find_all(child.name, recursive=False)
                if len(siblings) > 1:
                    index = next(i for i, sibling in enumerate(siblings, 1) if sibling is child)
                    components.append(f'{child.name}[{index}]')
                else:
                    components.append(child.name)
                child = parent
            components.reverse()

            return None
        except Exception as e:
            return e

    async def get_text(self, selector: str) -> str:
        page = await self.playwright_manager.get_page()
        return await page.inner_text(selector)

    async def get_attribute(self, selector: str, attribute: str) -> Optional[str]:
        page = await self.playwright_manager.get_page()
        element = await page.query_selector(selector)
        if element:
            return await element.get_attribute(attribute)
        return None

    async def wait_for_selector(self, selector: str, timeout: int = 5000) -> None:
        page = await self.playwright_manager.get_page()
        await page.wait_for_selector(selector, timeout=timeout)

    async def get_elements(self, selector: str) -> List[dict]:
        page = await self.playwright_manager.get_page()
        elements = await page.query_selector_all(selector)
        return [{"text": await el.inner_text(), "html": await el.inner_html()} for el in elements]
### Do przetestowaniass 