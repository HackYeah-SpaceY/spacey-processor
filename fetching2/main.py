import asyncio
from playwright_manager import PlaywrightManager
from web_scraper import WebScraper
from interaction_handler import InteractionHandler

async def main():
    url = "https://hackyeah.pl/"
    async with PlaywrightManager(url) as playwright_manager:
        scraper = WebScraper(playwright_manager)
        interaction = InteractionHandler(playwright_manager)
        #print(await scraper.GetPlainTextFromHTML(), "\n")
        #print(await scraper.LocateInput(), "\n")
        #print(await scraper.LocateInputWith5Divs(), "\n")
        print(await scraper.LocateButton(), "\n")
        #test= await scraper.LocateButtonWith1Divs()
        #print(await scraper.LocateInput())
        #print(await scraper.LocateHrefsWith1Divs())
        #test=await scraper.LocateInput()
        #print(test)button_xpath = result_list[index_to_extract]["button_xpath"]
        #print(await interaction.click_button(element=test[15]["button_xpath"]))

if __name__ == "__main__":
    asyncio.run(main())