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
                "description": "Fetches the website with the provided url. Provides the clickable buttons, fillable inputs, links and plain text.",
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
                "description": "Clicks the button with the provided index. Returns the clickable buttons, fillable inputs, links and plain text on the new page.",
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
            },
            {
                "function": self.go_to_link,
                "description": "Navigates to the link. The assistant should only navigate to the links on the page. Returns the clickable buttons, fillable inputs, links and plain text on the new page.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "link url",
                        }
                    },
                    "required": ["url"],
                    "additionalProperties": False,
                },
                "return_type": "string",
            },
            {
                "function": self.fill_input,
                "description": "Fills the input with the provided value. Returns the clickable buttons, fillable inputs, links and plain text.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "input_idx": {
                            "type": "integer",
                            "description": "index of the input",
                        },
                        "value": {
                            "type": "string",
                            "description": "value to fill in the input",
                        }
                    },
                    "required": ["input_idx", "value"],
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
            {"role": "system", "content": "You\'re an assistant that has an ability to interact with websites based on your functions. You can fetch the website and click buttons on it. Please be concise and don\'t provide too much information at once."},
            {"role": "system", "content": f"Please fetch the website: {url}"}
        ]

    async def __aenter__(self):
        self.manager = await PlaywrightManager(self.url).__aenter__()
        self.scraper = WebScraper(self.manager)
        self.interaction_handler = InteractionHandler(self.manager)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.manager.__aexit__(exc_type, exc_val, exc_tb)

    async def fetch_website(self) -> tuple[str, str, str, str]:
        try:
            buttons = await self.scraper.LocateButton()
            inputs = await self.scraper.LocateInput()
            links = await self.scraper.LocateHrefs()
            plain_text = await self.scraper.GetPlainTextFromHTML()

            return buttons, inputs, links, plain_text
        except Exception as e:
            return f"Error: {e}"
        
    async def click_button(self, idx: int) -> tuple[str, str, str, str]:
        try:
            buttons = await self.scraper.LocateButton()

            if idx >= len(buttons):
                return "Error: Invalid index"

            await self.interaction_handler.click_button(buttons[idx]['button'])

            buttons = await self.scraper.LocateButton()
            inputs = await self.scraper.LocateInput()
            links = await self.scraper.LocateHrefs()
            plain_text = await self.scraper.GetPlainTextFromHTML()

            return buttons, inputs, links, plain_text
        except Exception as e:
            return f"Error: {e}"
    
    async def go_to_link(self, url: str) -> tuple[str, str, str, str]:
        try:
            await self.interaction_handler.open_href(url)

            buttons = await self.scraper.LocateButton()
            inputs = await self.scraper.LocateInput()
            links = await self.scraper.LocateHrefs()
            plain_text = await self.scraper.GetPlainTextFromHTML()

            return buttons, inputs, links, plain_text
        except Exception as e:
            return f"Error: {e}"
        
    async def fill_input(self, input_idx: int, value: str) -> tuple[str, str, str, str]:
        try:
            inputs = await self.scraper.LocateInput()
            print(inputs)

            if input_idx >= len(inputs):
                return "Error: Invalid index"

            await self.interaction_handler.fill_input(inputs[input_idx]['input_string'], value)

            buttons = await self.scraper.LocateButton()
            inputs = await self.scraper.LocateInput()
            links = await self.scraper.LocateHrefs()
            plain_text = await self.scraper.GetPlainTextFromHTML()

            return buttons, inputs, links, plain_text
        except Exception as e:
            return f"Error: {e}"
    
    async def handle_function(self, function):
        if function.name == "fetch_website":
            # print(json.loads(function.arguments)['url'])
            print (f"Agent with chat id {self.url} is fetching website with url {json.loads(function.arguments)['url']}")
            res = await self.fetch_website()
            return res
        elif function.name == "click_button":
            print(f"Agent with chat id {self.url} is clicking button with index {json.loads(function.arguments)['idx']} on page with url {self.url}")
            # print(json.loads(function.arguments)['idx'])
            res = await self.click_button(json.loads(function.arguments)['idx'])
            return res
        elif function.name == "go_to_link":
            print(f"Agent with chat id {self.url} is going to link with url {json.loads(function.arguments)['url']} on page with url {self.url}")
            # print(json.loads(function.arguments)['idx'])
            res = await self.go_to_link(json.loads(function.arguments)['url'])
            return res
        elif function.name == "fill_input":
            print(f"Agent with chat id {self.url} is filling input with index {json.loads(function.arguments)['input_idx']} with value {json.loads(function.arguments)['value']} on page with url {self.url}")
            # print(json.loads(function.arguments)['idx'])
            res = await self.fill_input(json.loads(function.arguments)['input_idx'], json.loads(function.arguments)['value'])
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