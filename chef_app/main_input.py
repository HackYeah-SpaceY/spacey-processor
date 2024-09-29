from openai import OpenAI
import random
import json

from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
import asyncio
from chef_client import ChefClient

br = False

url = input("Website url: ")

openai_client = OpenAI()

async def main():
    async with ChefClient(openai_client, url) as client:
        while not br:
            user_input = input("> ")
            
            if user_input.lower() == "exit":
                break

            client.messages.append({"role": "user", "content": user_input})

            chat_completion = await client.query()
            
            client.messages.append(chat_completion.choices[0].message)

            tool_calls = chat_completion.choices[0].message.tool_calls
            # print(chat_completion)
            # print(tool_calls)
            while (tool_calls is not None):
                for i in range(len(tool_calls)):
                    function = tool_calls[i].function

                    client.messages.append({
                        "role": "tool",
                        "content": json.dumps(await client.handle_function(function)),
                        "tool_call_id": tool_calls[i].id
                    })
                    # print(client.messages)

                chat_completion = await client.query()
                tool_calls = chat_completion.choices[0].message.tool_calls

                print("WOO!")
                # print(client.messages)

                client.messages.append(chat_completion.choices[0].message)
                print(chat_completion.choices[0].message.content)
            else:
                print(chat_completion.choices[0].message.content)

if __name__ == "__main__":
    asyncio.run(main())