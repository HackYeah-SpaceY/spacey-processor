import asyncio
from playwright_manager import PlaywrightManager
from web_scraper import WebScraper
from interaction_handler import InteractionHandler

async def main():
    url = "https://forms.office.com/Pages/ResponsePage.aspx?id=RPtf1l4zWE-SbVhBA9Thf-bNYiMYeDJDuCrFOHn09odUMVBCQlpLUVNZQVVQMDBLTE84VlZTOE9ZSS4u"
    async with PlaywrightManager(url) as playwright_manager:
        scraper = WebScraper(playwright_manager)
        interaction = InteractionHandler(playwright_manager)
        #print(await scraper.GetPlainTextFromHTML(), "\n")
       # print(await scraper.LocateInput(), "\n")
        #print(await scraper.LocateInputWith3Divs(), "\n")
        #print(await scraper.LocateButton(), "\n")
        #print(await scraper.LocateButtonWith1Divs())
        #print(await scraper.LocateHrefs())

        buttons=await scraper.LocateButton()
        print(buttons)
        print(buttons[3]["button"])
        print(await interaction.click_button(element=buttons[3]["button"]))

        # buttons=await scraper.LocateButtonWith1Divs()
        # print(buttons[0]["ButtonDivs"])
        # print(await interaction.click_button(element=buttons[0]["ButtonDivs"]))


        inputy=await scraper.LocateInput()
        print(inputy)
        print(inputy[0]["input_string"])
        print(await interaction.fill_input(element=inputy[0]["input_string"],value="Witam"))


        # inputydiv=await scraper.LocateInputWith3Divs()
        # print(inputydiv)
        # print(inputydiv[0]["InputDivs"])
        # print(await interaction.fill_input(element=inputydiv[0]["InputDivs"],value="Witam"))

        # links=await scraper.LocateHrefs()
        # print(links[0]["href"])
        # print(await interaction.open_href(element=links[0]["href"]))
        
        await asyncio.sleep(30)

if __name__ == "__main__":
    asyncio.run(main())