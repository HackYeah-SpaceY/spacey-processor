from openai import OpenAI
import random
import json

from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
import asyncio
from typing import Optional, Dict, Type, List
from bs4 import BeautifulSoup
import re

def CleanData(text: str) -> str:
    cleaned_text = re.sub(r'\n{3,}', '\n\n', text)
    return cleaned_text 

async def GetFullHTML(URL: str) -> Optional[str]:

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False,args=["--start-maximised"], no_viewport=True)
        try:
            page = await browser.new_page()
            await page.goto(URL, timeout=10000)
            data = await page.content()
            return data
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
            return CleanData(plain_text)
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
            
            return div_strings
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()

class ChefClient:
    def __init__(self, client, url):
        self.functions = []
        self.client = client

        function_defs = [
            {
                "function": self.fetch_website,
                "description": "Fetches the website with the provided url. Provides the plain text and also available actionable elements",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "url of the website",
                        }
                    },
                    "required": ["name"],
                    "additionalProperties": False,
                },
                "return_type": "string",
            }
        ]


        for function_def in function_defs:
            self.functions.append(
                {
                    "type": "function",
                    "function": {
                        "name": function_def["function"].__name__,
                        "description": function_def["description"],
                        "parameters": function_def["parameters"],
                        "return_type": function_def["return_type"],
                    }
                }
            )
        
        self.messages = [
            {"role": "system", "content": "You\'re an assistant that has an ability to interact with websites"},
            {"role": "system", "content": f"Please fetch the website: {url}"}
        ]

    def fetch_website(self, url: str) -> tuple[str, List[str]]:
        loop = asyncio.get_event_loop()
        actionables = loop.run_until_complete(Locate(url))
        plain_text = loop.run_until_complete(GetPlainTextFromHTML(url))

        return plain_text, actionables 
    
    def handle_function(self, function):
        if function.name == "fetch_website":
            print(json.loads(function.arguments)['url'])
            res = self.fetch_website(**json.loads(function.arguments))
            print (res)
            return res

        return None
    
    def query(self):
        return self.client.chat.completions.create(
            messages=self.messages,
            model="gpt-3.5-turbo",
            tools=self.functions,
        )

br = False

url = input("Website url: ")

openai_client = OpenAI()
client = ChefClient(openai_client, url)

while not br:
    user_input = input("> ")
    
    if user_input.lower() == "exit":
        break

    client.messages.append({"role": "user", "content": user_input})

    chat_completion = client.query()
    
    client.messages.append(chat_completion.choices[0].message)

    tool_calls = chat_completion.choices[0].message.tool_calls
    if (tool_calls is not None):
        for i in range(len(tool_calls)):
            function = tool_calls[i].function

            client.messages.append({
                "role": "tool",
                "content": json.dumps(client.handle_function(function)),
                "tool_call_id": tool_calls[i].id
            })

        chat_completion = client.query()

        client.messages.append(chat_completion.choices[0].message)
        print(chat_completion.choices[0].message.content)
    else:
        print(chat_completion.choices[0].message.content)

