# -*- coding: utf-8 -*-
import logging
import os
import sys

from typing import List, Tuple
from datetime import datetime
from unittest import mock

import pytest

from selenium.webdriver.edge.webdriver import WebDriver

# os.getcwd()
from components.utils import get_browser, get_logger


# Get absolute path of the project root
__rootpath__ = os.path.realpath(os.path.abspath('.'))
TIMEOUT = 2


@pytest.fixture(scope="session")
def browser() -> WebDriver:
    """
    Get the Selenium WebDriver object
    """
    driver_path = os.path.join(__rootpath__, r"components\msedgedriver.exe")
    driver_options = [
        # "--user-data-dir=C:\\Users\\anewe\\AppData\\Local\\Microsoft\\Edge\\User Data",
        # "--headless",
        # "--inprivate",
        "--start-maximized",
        "--disable-extensions",
        "--remote-debugging-port=9222"
    ]
    browser = get_browser(driver_path, driver_options, TIMEOUT)

    return browser


@pytest.hookimpl
def pytest_sessionstart():
    """
    Run before tests start
    """
    # logfile = os.path.join(__rootpath__, "logs", fr"TEST_SCRAPER_{datetime.now().strftime('%d%m%Y_%H%M%S')}.log")
    logfile = os.path.join(__rootpath__, "logs", fr"TEST_SCRAPER.log") # HACK
    log = get_logger(logfile)

    # Creating/overriding the output CSV that will be used for tests 
    generated_csv_file = os.path.join(__rootpath__, "generated", "TEST - Produtos doterra - Produtos.csv")
    with open(generated_csv_file, 'w'):
        pass

    # Global variable
    pytest.log = log # type: ignore
    pytest.generated_csv_file = generated_csv_file # type: ignore


@pytest.hookimpl
def pytest_sessionfinish(session, exitstatus):
    """
    Executes once all tests are finished
    """
    cmds = [
        "taskkill /im msedge.exe /t /f",
        "taskkill /im msedgedriver.exe /t /f",
        "taskkill /im microsoftwebdriver.exe /t /f",
        "taskkill /im msedgewebview2.exe /t /f"
    ]
        
    for cmd in cmds:
        logging.debug(f"Sending command: {cmd}")
        os.system(cmd)
