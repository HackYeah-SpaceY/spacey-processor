from bs4 import BeautifulSoup
import re
from typing import Optional, List
from fetching.playwright_manager import PlaywrightManager

def CleanData(text: str) -> str:
    cleaned_text = re.sub(r'\n{3,}', '\n\n', text)
    return cleaned_text

class WebScraper:
    def __init__(self, playwright_manager: PlaywrightManager):
        self.playwright_manager = playwright_manager

    async def GetFullHTML(self) -> Optional[str]:
        try:
            return await self.playwright_manager.get_page_content()
        except Exception as e:
            return f"Error: {e}"

    async def GetPlainTextFromHTML(self) -> Optional[str]:
        try:
            data = await self.playwright_manager.get_page_content()
            soup = BeautifulSoup(data, 'html.parser')
            plain_text = soup.get_text(separator="\n")
            return CleanData(plain_text)
        except Exception as e:
            return f"Error: {e}"

    async def LocateInput(self) -> Optional[List[str]]:
        try:
            html_content = await self.playwright_manager.get_page_content()
            soup = BeautifulSoup(html_content, 'html.parser')
            
            input_elements = soup.find_all('input')
            input_strings = [str(input_element) for input_element in input_elements]
            return input_strings
        except Exception as e:
            return f"Error: {e}"

    async def LocateInputWith5Divs(self) -> Optional[List[str]]:
        try:
            html_content = await self.playwright_manager.get_page_content()
            soup = BeautifulSoup(html_content, 'html.parser')

            inputs = soup.find_all('input')
            divs_above_list = []

            for input_element in inputs:
                current_div = input_element
                divs_above = []
                for _ in range(5):
                    current_div = current_div.find_parent('div')
                    if current_div is None:
                        break
                    divs_above.append(current_div)
                divs_above_list.append(divs_above)
            
            return divs_above_list
        except Exception as e:
            return f"Error: {e}"

    async def LocateButtonWith1Divs(self) -> Optional[List[str]]:

        try:
            html_content = await self.playwright_manager.get_page_content()
            soup = BeautifulSoup(html_content, 'html.parser')

            buttons = soup.find_all('button')
            divs_above_list = []

            for button_element in buttons:
                current_div = button_element
                divs_above = []
                for _ in range(1):
                    current_div = current_div.find_parent('div')
                    if current_div is None:
                        break
                    divs_above.append(current_div)
                divs_above_list.append(divs_above)

            return divs_above_list
        except Exception as e:
            return f"Error: {e}"

    async def LocateButton(self) -> Optional[List[str]]:
        try:
            html_content = await self.playwright_manager.get_page_content()
            soup = BeautifulSoup(html_content, 'html.parser')

            buttons = soup.find_all('button')
            button_strings = [str(button) for button in buttons]
            return button_strings
        except Exception as e:
            return f"Error: {e}"