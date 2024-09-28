import asyncio
from playwright_manager import PlaywrightManager
from web_scraper import WebScraper

async def main():
    url = "https://www.uber.com/pl/pl/"
    async with PlaywrightManager(url) as playwright_manager:
        scraper = WebScraper(playwright_manager)
        #print(await scraper.GetPlainTextFromHTML(), "\n")
        #print(await scraper.LocateInput(), "\n")
        #print(await scraper.LocateInputWith5Divs(), "\n")
        print(await scraper.LocateButton(), "\n")
        #print(await scraper.LocateButtonWith3Divs(), "\n")
    

if __name__ == "__main__":
    asyncio.run(main())