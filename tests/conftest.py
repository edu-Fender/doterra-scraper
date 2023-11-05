import os
import sys

import pytest

from selenium.webdriver.edge.webdriver import WebDriver

sys.path.append("..") # Little dirty trick
from scraper import accept_bloody_cookie, get_browser, main


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

@pytest.fixture()
def browser() -> WebDriver:
    browser = get_browser()
    browser.implicitly_wait(30)  # Timeout

    url = "https://shop.doterra.com/PT/pt_PT"
    browser.get(url)

    try:
        browser = accept_bloody_cookie(browser)
    except:
        pass

    return browser