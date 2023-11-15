import os
import decorator
import sys
import json
import logging
import urllib.request

from typing import Dict, List, Union
from pathlib import Path

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


# Most efective way to get currerent script location
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Get parent directory location
__parentpath__ = os.path.realpath(os.path.abspath('.'))

# Standard timeout
TIMEOUT: float = 5


######################################## General Helpers ########################################
def get_logger(logpath: Union[str, Path]) -> logging.Logger:
    """
    Getting logger
    Why is logging so frustrating??
    """
    fmt = "%(asctime)s - %(levelname)s: %(message)s"
    datefmt = "%d-%m-%Y %H:%M:%S"

    log = logging.getLogger(__name__)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setStream(sys.stdout)
    stream_handler.setLevel(logging.INFO)

    file_handler = logging.FileHandler(logpath, mode='w', encoding='utf-8')
    file_handler.setFormatter(logging.Formatter(fmt=fmt, datefmt=datefmt))
    file_handler.setLevel(logging.INFO)

    log.addHandler(stream_handler)
    log.addHandler(file_handler)
    log.setLevel(logging.INFO)

    return log


def join_strings(strings: List[str]):
    """
    Join incoming strings
    """
    sep = ' -> '
    joined = sep.join(strings)

    return joined


######################################## Selenium Helpers ########################################
def get_browser(driver_path, options: List[str], timeout: float = TIMEOUT, zoom: float = 100) -> WebDriver:
    """
    Will get then return the Selenium driver
    """
    logging.info(f"Getting browser object with custom options: {json.dumps(options, indent=4)}")
    
    edge_options = Options()
    for i in options:
        edge_options.add_argument(i)
    
    service = Service(driver_path)
    browser = webdriver.Edge(service=service, options=edge_options)
    browser.implicitly_wait(timeout)

    # Very important, setting zoom
    browser.execute_script(f"document.body.style.zoom='{zoom}%';")

    return browser


def hover_over(browser: WebDriver, xpath_or_webelement: Union[str, WebElement], timeout: float = 5, verbose: bool = False) -> bool:
    """
    Hover mouse pointer over HTML element
    """
    # Introducing: Type Guards
    if isinstance(xpath_or_webelement, str):
        webelement: WebElement = wait_for_element(browser, By.XPATH, xpath_or_webelement, timeout=timeout)
    elif isinstance(xpath_or_webelement, WebElement):
        webelement = xpath_or_webelement
    else:
        raise SystemExit("Hit a never type.")

    logging.info(f"Hovering over element {webelement.text}") if verbose else None
    hover = ActionChains(browser).move_to_element(webelement)
    hover.perform()

    return True
 

def wait_for_element(browser: Union[WebDriver, WebElement], by_what: str, direction: str, timeout: float = 5):
    """
    Helper function to wait for visibility of element located then grab it
    Note that 'browser' could be a WebDriver or a WebElement as both of then has find_element attribute
    """
    element = WebDriverWait(browser, timeout).until(
        EC.visibility_of_element_located ((
            by_what, direction)))
    
    return element


def wait_for_all_elements(browser: Union[WebDriver, WebElement], by_what: str, direction: str, timeout: float = 5) -> List[WebElement]:
    """
    Helper function to wait for visibility of all elements located then grab it
    Note that 'browser' could be a WebDriver or a WebElement as both of then has find_elements attribute
    """
    # Waiting until all images loaded
    WebDriverWait(browser, timeout).until(
        EC.presence_of_all_elements_located ((
            by_what, direction)))
    
    # Getting images
    elements: List[WebElement] = browser.find_elements(by_what, direction)

    return elements


def accept_bloody_cookie(browser: WebDriver) -> WebDriver:
    """
    Accept bloody cookie
    """
    try:
        logging.info("Accepting bloody cookie...")
        accept_cookie_btn_xpath = '//*[@id="truste-consent-button"]'
        WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located ((
                By.XPATH, accept_cookie_btn_xpath))).click()
        
        return browser
    
    # For some reason Python sadly wont catch TimeoutException
    except:
        raise SystemExit("Error, couldn't accept bloody cookie.")


######################################## Decorator Helpers ########################################
def kill_edge(func):
    """
    Decorator that will terminate Edge processes with each code execution.
    This is necessary because if there is an Edge process alive when Edge is opened by Selenium, Selenium will not work correctly
    """
    def wrapper(func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        finally:
            cmds = [
                "taskkill /im msedge.exe /t /f",
                "taskkill /im msedgedriver.exe /t /f",
                "taskkill /im microsoftwebdriver.exe /t /f"
            ]
                
            for cmd in cmds:
                logging.debug(f"Sending command: {cmd}")
                os.system(cmd)
        
    return decorator.decorator(wrapper, func)
