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
TIMEOUT = 5


# def pytest_namespace():
#     """
#     Global variables shared between all test files
#     """
#     return {
#         "TIMEOUT": 5,
#         "logfile": os.path.join(__rootpath__, "logs", fr"TEST_SCRAPER_{datetime.now().strftime('%Y%d%m_%H%M%S')}.log")
#     }

def pytest_configure():
    """
    Run before tests start
    """
    date = datetime.now().strftime('%Y%d%m_%H%M%S')
    logfile = os.path.join(__rootpath__, "logs", fr"TEST_SCRAPER_{date}.log")

    fmt = "%(asctime)s - %(levelname)s: %(message)s"
    datefmt = "%d-%m-%Y %H:%M:%S"

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setStream(sys.stdout)

    file_handler = logging.FileHandler(logfile, mode="w", encoding='utf-8')
    file_handler.setFormatter(logging.Formatter(fmt=fmt, datefmt=datefmt))

    # Global variable
    pytest.handlers = (stream_handler, file_handler)

def pytest_sessionfinish(session, exitstatus):
    """
    Executes once all tests are finished
    """
    cmds = [
        "taskkill /im msedge.exe /t /f",
        "taskkill /im msedgedriver.exe /t /f",
        "taskkill /im microsoftwebdriver.exe /t /f"
    ]
        
    for cmd in cmds:
        logging.debug(f"Sending command: {cmd}")
        os.system(cmd)


@pytest.fixture(scope="session")
def handlers() -> Tuple[logging.StreamHandler, logging.FileHandler]:
    """
    Return logging hundlers for logging of tests
    """
    date = datetime.now().strftime('%Y%d%m_%H%M%S')
    logfile = os.path.join(__rootpath__, "logs", fr"TEST_SCRAPER_{date}.log")

    fmt = "%(asctime)s - %(levelname)s: %(message)s"
    datefmt = "%d-%m-%Y %H:%M:%S"

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setStream(sys.stdout)

    file_handler = logging.FileHandler(logfile, mode="w", encoding='utf-8')
    file_handler.setFormatter(logging.Formatter(fmt=fmt, datefmt=datefmt))

    return stream_handler, file_handler 


@pytest.fixture(scope="session", autouse=True)
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
    browser = get_browser(driver_path, driver_options, TIMEOUT, zoom=70)

    return browser


# def pytest_sessionstart(session):
#     """
#     Called after the Session object has been created and
#     before performing collection and entering the run test loop.
#     """
#     driver_path = os.path.join(__rootpath__, r"components\msedgedriver.exe")
#     driver_options = [
#         # "--user-data-dir=C:\\Users\\anewe\\AppData\\Local\\Microsoft\\Edge\\User Data",
#         # "--headless",
#         # "--inprivate",
#         "--start-maximized",
#         "--disable-extensions",
#         "--remote-debugging-port=9222"
#     ]
#     browser = get_browser(driver_path, driver_options, TIMEOUT, zoom=70)

#     return browser