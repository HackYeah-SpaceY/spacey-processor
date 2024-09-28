from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
import asyncio
from typing import Optional, Dict, Type, List
from bs4 import BeautifulSoup
import re

def CleanData(text: str) -> str:
    cleaned_text = re.sub(r'\n{3,}', '\n\n', text)
    return cleaned_text

async def SaveDataToFile(data: str):
   
    async with asyncio.Lock():  
        with open("Test.txt", "a", encoding="utf-8") as file:
            file.write(data + "\n")  

async def GetFullHTML(URL: str) -> Optional[str]:

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False,args=["--start-maximised"], no_viewport=True)
        try:
            page = await browser.new_page()
            await page.goto(URL, timeout=10000)
            data = await page.content()
            await SaveDataToFile(data) 
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()

async def GetPlainTextFromHTML(URL: str) -> Optional[str]:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        try:
            page = await browser.new_page()
            await page.goto(URL, timeout=10000)
            data = await page.content()
            soup = BeautifulSoup(data, 'html.parser')
            plain_text = soup.get_text(separator="\n")
            print(CleanData(plain_text))
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()
async def Locate(URL: str) -> Optional[str]:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False,args=["--start-maximised"])
        try:
            page = await browser.new_page()
            await page.goto(URL, timeout=10000)
            html_content = await page.content()
            soup = BeautifulSoup(html_content, 'html.parser')
            
            divs_with_input = soup.find_all('input')
            
            div_strings = [str(div) for div in divs_with_input]
            
            for div in div_strings:
                print(div)
                print(' ') 
            print(div_strings)
            await asyncio.sleep(10)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()
if __name__=="__main__":
       loop = asyncio.get_event_loop()
       loop.run_until_complete(Locate("https://www.uber.com/pl/pl/"))