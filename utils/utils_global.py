from typing import Union
from loguru import logger
from selenium.webdriver import Remote
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.utils_decorator import handle_find_element_exceptions


def wait_for_element_to_load(driver: Remote, selector: str, address: str, timeout=10):
    logger.info(f"Waiting for element to load | timeout {timeout}s")
    wait = WebDriverWait(driver=driver, timeout=timeout)
    wait.until(EC.presence_of_element_located((selector, address)))
    return True


@handle_find_element_exceptions
def findelement(driver: Remote, path: Union[By, str], value: str, variable : str):
    text = driver.find_element(path,value).text
    return text


@handle_find_element_exceptions
def findelement_getattribute(driver: Remote, path: Union[By, str], value: str, attri: str, variable : str):
    text = driver.find_element(path,value).get_attribute(attri)
    return text
