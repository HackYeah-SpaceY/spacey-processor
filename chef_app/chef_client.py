from typing import Optional, Dict, Type, List
from bs4 import BeautifulSoup
import re

from fetching.interaction_handler import InteractionHandler
from fetching.web_scraper import WebScraper
from fetching.playwright_manager import PlaywrightManager
import json

class ChefClient:
    def __init__(self, client, url):
        self.functions = []
        self.client = client
        self.url = url

        function_defs = [
            {
                "function": self.fetch_website,
                "description": "Fetches the website with the provided url. Provides the plain text and also available buttons and fillable inputs.",
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
            },
            {
                "function": self.click_button,
                "description": "Clicks the button with the provided index. Returns the new page plain text and available buttons and fillable inputs.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "idx": {
                            "type": "integer",
                            "description": "index of the button",
                        }
                    },
                    "required": ["idx"],
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
            {"role": "system", "content": "You\'re an assistant that has an ability to interact with websites based on your functions. You can fetch the website and click buttons on it. If there are some obvious buttons that could be clicked (like \"start now\") - do it immediately and without asking the user."},
            {"role": "system", "content": f"Please fetch the website: {url}"}
        ]

    async def __aenter__(self):
        self.manager = await PlaywrightManager(self.url).__aenter__()
        self.scraper = WebScraper(self.manager)
        self.interaction_handler = InteractionHandler(self.manager)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.manager.__aexit__(exc_type, exc_val, exc_tb)

    async def fetch_website(self) -> tuple[str, List[str], List[str]]:
        try:
            buttons = await self.scraper.LocateButton()
            inputs = await self.scraper.LocateInput()
            plain_text = await self.scraper.GetPlainTextFromHTML()

            return buttons, inputs, plain_text
        except Exception as e:
            return f"Error: {e}"
        
    async def click_button(self, idx: int) -> tuple[str, List[str], List[str]]:
        try:
            buttons = await self.scraper.LocateButton()

            if idx >= len(buttons):
                return "Error: Invalid index"

            await self.interaction_handler.click_button(buttons[idx]['button'])

            buttons = await self.scraper.LocateButton()
            inputs = await self.scraper.LocateInput()
            plain_text = await self.scraper.GetPlainTextFromHTML()

            return buttons, inputs, plain_text
        except Exception as e:
            return f"Error: {e}"
    
    async def handle_function(self, function):
        if function.name == "fetch_website":
            # print(json.loads(function.arguments)['url'])
            print (f"Agent with chat id {self.url} is fetching website with url {json.loads(function.arguments)['url']}")
            res = await self.fetch_website()
            # print (res)
            return res
        elif function.name == "click_button":
            print(f"Agent with chat id {self.url} is clicking button with index {json.loads(function.arguments)['idx']} on page with url {self.url}")
            # print(json.loads(function.arguments)['idx'])
            res = await self.click_button(json.loads(function.arguments)['idx'])
            return res

        return None
    
    async def query(self):
        return self.client.chat.completions.create(
            messages=self.messages,
            model="gpt-4o-mini",
            tools=self.functions,
        )
    
    async def save_screenshot(self):
        await self.manager.save_screenshot()