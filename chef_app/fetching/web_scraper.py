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
            main_list=[]
            input_elements = soup.find_all('input')
            input_strings = [str(input_element) for input_element in input_elements]
            for index,input_string in enumerate(input_strings):
                main_list.append({
                    "index":index,
                    "input_string":input_string
                })

            return main_list
        except Exception as e:
            return f"Error: {e}"

    async def LocateInputWith3Divs(self) -> Optional[List[str]]:
        try:
            html_content = await self.playwright_manager.get_page_content()
            soup = BeautifulSoup(html_content, 'html.parser')

            inputs = soup.find_all('input')
            main_list = []

            for index,input_element in enumerate(inputs):
                current_div = input_element
                divs_above = []
                for _ in range(3):
                    current_div = current_div.find_parent()
                    if current_div is None:
                        break
                    divs_above.append(current_div.text)
                if current_div is not None:
                    main_list.append({
                        "index":index,
                        "InputDivs":divs_above
                    })
            
            return main_list
        except Exception as e:
            return f"Error: {e}"

    async def LocateButtonWith1Divs(self) -> Optional[List[str]]:

        try:
            html_content = await self.playwright_manager.get_page_content()
            soup = BeautifulSoup(html_content, 'html.parser')

            buttons = soup.find_all('button')
            main_list= []

            for index,button_element in enumerate(buttons):
                current_div = button_element
                divs_above = []
                for _ in range(1):
                    current_div = current_div.find_parent('div')
                    if current_div is None:
                        break
                    divs_above.append(current_div)
                main_list.append({
                    "index":index,
                    "ButtonDivs":divs_above
                })

            return main_list
        except Exception as e:
            return f"Error: {e}"

    async def LocateButton(self) -> Optional[List[str]]:
        try:
            html_content = await self.playwright_manager.get_page_content()
            soup = BeautifulSoup(html_content, 'html.parser')
            main_list=[]
            buttons = soup.find_all('button')
            button_strings = [str(button) for button in buttons]
            for index,button_string in enumerate(button_strings):
                main_list.append({
                    "index":index,
                    "button":button_string
                })
            return main_list
        except Exception as e:
            return f"Error: {e}"

    async def LocateHrefs(self) -> Optional[List[dict]]:
        try:
            html_content = await self.playwright_manager.get_page_content()
            soup = BeautifulSoup(html_content, 'html.parser')

            a_elements = soup.find_all('a', href=True)  
            divs_above_list = []

            for index,a_element in enumerate(a_elements):
                href = a_element["href"]
                if "https" in href:  
                    divs_above_list.append({
                        "index": index,  
                        "href": href,
                        #
                    })

            return divs_above_list  #
        except Exception as e:
            return f"Error: {e}"