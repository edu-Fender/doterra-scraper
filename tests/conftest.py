import os
import sys

import pytest

from selenium.webdriver.edge.webdriver import WebDriver

# Little dirty trick
sys.path.append("..")
from scraper import accept_bloody_cookie, get_browser, main


OPTIONS = [
    # "--user-data-dir=C:\\Users\\anewe\\AppData\\Local\\Microsoft\\Edge\\User Data",
    "--headless",
    "--inprivate",
    "--start-maximized",
    "--disable-extensions",
    "--remote-debugging-port=9222"
]

@pytest.fixture()
def browser() -> WebDriver:
    browser = get_browser(OPTIONS)
    browser.implicitly_wait(30)  # Timeout

    url = "https://shop.doterra.com/PT/pt_PT"
    browser.get(url)

    try:
        browser = accept_bloody_cookie(browser)
    except:
        pass

    return browser