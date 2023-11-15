import os
import sys

from typing import List

import pytest

from selenium.webdriver.edge.webdriver import WebDriver

# os.getcwd()
from components.utils import accept_bloody_cookie, get_browser

# Get parent directory location
__parentpath__ = os.path.realpath(os.path.abspath('.'))

TIMEOUT = 5
        
@pytest.fixture()
def browser() -> WebDriver:
    """
    Get the Selenium WebDriver object
    """
    driver_path = os.path.join(__parentpath__, r"components\msedgedriver.exe")
    driver_options = [
        # "--user-data-dir=C:\\Users\\anewe\\AppData\\Local\\Microsoft\\Edge\\User Data",
        # "--headless",
        # "--inprivate",
        "--start-maximized",
        "--disable-extensions",
        "--remote-debugging-port=9222"
    ]

    browser = get_browser(driver_path, driver_options, TIMEOUT, zoom=70)
    browser.implicitly_wait(TIMEOUT)

    # OBS: necessery to be connected to Portugal's VPN
    url = "https://shop.doterra.com/PT/pt_PT/shop/home/"
    browser.get(url)
    browser = accept_bloody_cookie(browser)

    return browser
