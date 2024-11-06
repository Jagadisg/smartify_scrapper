import asyncio
from loguru import logger
from selenium.webdriver import Remote

from utils.utils_climatetech import ClimateTech
from utils.utils_driver import initialise_selenium_driver


def lambda_handler(event, context):
    """
    AWS lamdba handler
    """
    
    result = asyncio.run(main())
    return {
        "statusCode": 200,
        "body": result
    }
    
    
async def main():
    driver = initialise_selenium_driver()
    if not isinstance(driver, Remote):
        logger.error("Driver could not be initialised")
        return None
    
    climate_scraper = ClimateTech(driver=driver,website_link="https://www.climatetechlist.com/jobs")
    
    result = await climate_scraper.run_scraper()
    logger.info(result)
            