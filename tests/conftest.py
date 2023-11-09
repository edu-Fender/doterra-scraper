import os
import sys

import pytest

from selenium.webdriver.edge.webdriver import WebDriver

from scraper import accept_bloody_cookie, get_browser
from components.utils import kill_edge


OPTIONS = [
    # "--user-data-dir=C:\\Users\\anewe\\AppData\\Local\\Microsoft\\Edge\\User Data",
    # "--headless",
    # "--inprivate",
    "--start-maximized",
    "--disable-extensions",
    "--remote-debugging-port=9222"
]

@pytest.fixture()
def browser() -> WebDriver:
    """
    Get Selenium WebBrowser object
    """
    browser = get_browser(OPTIONS)

    url = "https://shop.doterra.com/PT/pt_PT"
    browser.get(url)

    browser = accept_bloody_cookie(browser)

    return browser