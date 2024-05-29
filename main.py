from loguru import logger
from selenium.webdriver import Remote

from utils.utils_climatetech import ClimateTech
from utils.utils_driver import initialise_selenium_driver


def main():
    driver = initialise_selenium_driver()
    if not isinstance(driver, Remote):
        logger.error("Driver could not be initialised")
        return None
    
    company_data = ClimateTech(driver=driver,website_link="https://www.climatetechlist.com/jobs")
    logger.info(company_data)
    
main()