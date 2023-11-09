import os
import decorator
import sys
import json
import logging
import urllib.request

from datetime import datetime
from typing import Dict, List, TypedDict, Union

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


'''def log(*args, console=True, logfile=None) -> None:
    """
    Print message to logfile.txt and console depending on input
    """
    args = str(*args)
    if args:
        if console:
            print(args)
        if logfile:
            with open(logfile, 'a+') as f:
                now = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
                f.write(f"{now} {args}\n")
'''
# def download_image(browser: WebDriver, xpath: str, product_name: str) -> str:
#     """
#     Helper to make download of images easier
#     """
#     element = browser.find_element(
#         By.XPATH,
#         xpath
#     )

#     img_src = element.get_attribute("src")
#     path, _ = urllib.request.urlretrieve(img_src, os.path.join(os.path.join(__parentpath__, "images"),  product_name + ".png"))

#     return path

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
    
    # For some reason sadly Python wont catch TimeoutException in this case
    except:
        logging.error("Error, couldn't accept bloody cookie")
        raise SystemExit

def hover_over(browser: WebDriver, xpath_or_webelement: Union[str, WebElement] = "") -> bool:
    """
    Hover mouse pointer over HTML element
    """
    # Introducing: Type Guards
    if isinstance(xpath_or_webelement, str):
        webelement: WebElement = WebDriverWait(browser, 5).until(
            EC.visibility_of_element_located ((
                By.XPATH, xpath_or_webelement)))
        logging.info(f"Hovering over element on XPATH {xpath_or_webelement}")

    elif isinstance(xpath_or_webelement, WebElement):
        webelement = xpath_or_webelement
        logging.info(f"Hovering over element {xpath_or_webelement.tag_name}")

    else:
        raise NotImplementedError(f"Error: Hit a never type.")

    hover = ActionChains(browser).move_to_element(webelement)
    hover.perform()

    return True
 
def wait_for_element(browser: WebDriver, by_what: str, direction: str, timeout: int = 5):
    """
    Helper function to wait for visibility of element located
    """
    element = WebDriverWait(browser, timeout).until(
        EC.visibility_of_element_located ((
            by_what, direction)))
    
    return element

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
