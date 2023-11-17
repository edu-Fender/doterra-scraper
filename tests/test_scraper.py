# -*- coding: utf-8 -*-
import logging
import os
import os
import sys
import csv
import timeit
import pytest

from typing import List, Tuple, Union
from logging import handlers
from unittest import mock
from datetime import datetime
from unittest.mock import patch

from selenium.webdriver.edge.webdriver import WebDriver

import scraper
from components.utils import get_browser, get_address, get_logger, kill_edge
from components.models import NormalizedProduct, Product
from tests.test_data import PRODUCTS_URLS, VALID_PRODUCT, VALID_FORMAT_EMPTY_FIELDS_PRODUCT, INVALID_FORMAT_PRODUCT, VALID_NORMALIZED_PRODUCT, VALID_FORMAT_EMPTY_FIELD_NORMALIZED_PRODUCT, INVALID_FORMAT_NORMALIZED_PRODUCT


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


@mock.patch("scraper.log.handlers", pytest.handlers)
@pytest.mark.parametrize("id, product", [
    (0, VALID_PRODUCT),
    (1, VALID_FORMAT_EMPTY_FIELDS_PRODUCT),
    (2, INVALID_FORMAT_PRODUCT)
])
def test_validate_dict(id: int, product: Product):
    """
    Testing validate_product
    """
    if id == 0:
        assert scraper.validate_dict(product)
    if id == 1:
        with pytest.raises(ValueError):
            scraper.validate_dict(product)
    if id == 2:
        with pytest.raises(ValueError):
            scraper.validate_dict(product)


@mock.patch("scraper.log.handlers", pytest.handlers)
@pytest.mark.parametrize("dict_", [
    (VALID_PRODUCT)
])
def test_validate_dict_teimeit(dict_: Product):
    """
    Testing timeit validate_product
    """
    def test1():
        def helper(dict_: Union[Product, NormalizedProduct, dict]):
            for val in dict_.values():
                if not val:
                    raise ValueError("Product dict had empty fields.")
                if isinstance(val, dict):
                    helper(val)
    
    def test2():
        def helper(val):
            if not val:
                raise ValueError("Product dict had empty fields.")
            if isinstance(val, dict):
                helper(val)

        [helper(i) for i in dict_.values()]
    
    x = timeit.timeit(test1, number=1000)
    y = timeit.timeit(test2, number=1000)
    pass


@mock.patch("scraper.log.handlers", pytest.handlers)
@pytest.mark.parametrize("normalized_product", [
    (VALID_NORMALIZED_PRODUCT),
    (VALID_FORMAT_EMPTY_FIELD_NORMALIZED_PRODUCT),
    (INVALID_FORMAT_NORMALIZED_PRODUCT)
])
def test_write_csv(normalized_product: NormalizedProduct):
    """
    Testing write_csv
    """
    test_generated_csv_file = os.path.join(__location__, "TEST - Produtos doterra - Produtos.csv")

    with mock.patch("scraper.GENERATED_CSV_FILE", test_generated_csv_file):
        scraper.write_csv(normalized_product)
        
        # Asserting the generated CSV file has at least two lines (header and content)
        with open(test_generated_csv_file, mode='r', encoding="utf-8") as f:
            reader = csv.reader(f)
            lines = list(reader)
            assert len(lines) >= 2


@mock.patch("scraper.log.handlers", pytest.handlers)
@pytest.mark.parametrize("product_page_url", [
    ("https://shop.doterra.com/PT/pt_PT/shop/correctx/")
])
def test_download_product_images(browser: WebDriver, product_page_url):
    """
    Testing download_product_images
    """
    browser.get(product_page_url)
    product_name = "Pomada Essencial Correct-X™"
    images = scraper.download_all_images(browser, product_name)
    
    # Asserting images were correctly downloaded
    for i in images:
        assert os.path.isfile(i)


@mock.patch("scraper.log.handlers", pytest.handlers)
@pytest.mark.depends(on=['test_validate_dict'])
@pytest.mark.parametrize("product", [
    (VALID_PRODUCT)
])
def test_normalize_product(product: Product):
    """
    Testing normalize_product
    """
    normalized_product = scraper.normalize_product(product)
    assert scraper.validate_dict(normalized_product)


@mock.patch("scraper.log.handlers", pytest.handlers)
@pytest.mark.parametrize("product_page_url", PRODUCTS_URLS)
def test_parse_information(browser: WebDriver, handlers: Tuple[logging.StreamHandler, logging.FileHandler], product_page_url: str):    
    """
    Testing parse product general information
    """
    browser.get(product_page_url)
    assert scraper.validate_dict(scraper.parse_information(browser))


@mock.patch("scraper.log.handlers", pytest.handlers)
@pytest.mark.parametrize("product_page_url", PRODUCTS_URLS)
def test_parse_benefits(browser: WebDriver, product_page_url: str):    
    """
    Testing parse_product
    """
    browser.get(product_page_url)
    assert scraper.validate_dict(scraper.parse_benefits(browser))
    


@mock.patch("scraper.log.handlers", pytest.handlers)# @mock.patch("scraper.log.handlers[1].mode", get_logger(os.path.join(__location__, r"TEST_SCRAPER.log"), mode='a'))
@pytest.mark.parametrize("product_page_url", PRODUCTS_URLS)
def test_parse_ingredients(browser: WebDriver, product_page_url: str):    
    """
    Testing parse_product
    """
    browser.get(product_page_url)
    assert scraper.validate_dict(scraper.parse_ingredients(browser))


@mock.patch("scraper.log.handlers", pytest.handlers)
@pytest.mark.parametrize("product_page_url", PRODUCTS_URLS)
def test_parse_uses(browser: WebDriver, product_page_url: str):    
    """
    Testing parse product uses
    """
    browser.get(product_page_url)
    assert scraper.validate_dict(scraper.parse_uses(browser))
    

@mock.patch("scraper.log.handlers", pytest.handlers)
@pytest.mark.depends(on=['test_validate_dict'])
@pytest.mark.parametrize("product_page_url", [
    ("https://shop.doterra.com/PT/pt_PT/shop/correctx/")
])    
def test_parse_product(browser: WebDriver, product_page_url):    
    """
    Testing parse_product
    """
    browser.get(product_page_url)
    assert scraper.parse_product(browser) 


@mock.patch("scraper.log.handlers", pytest.handlers)
@pytest.mark.depends(on=[
    test_parse_product,
    test_normalize_product,
    test_download_product_images,
    test_write_csv
])
@pytest.mark.parametrize("product_page_url", PRODUCTS_URLS)    
def test_process_product_page(browser: WebDriver, product_page_url: str):    
    """
    Testing parse_product
    """
    browser.get(product_page_url)
    assert scraper.parse_product(browser)


@mock.patch("scraper.log.handlers", pytest.handlers)
@pytest.mark.parametrize("products_page_url, subcategory_address_list", [
    # Page with lots of product that need to be scrolled down to load the product
    (
        "https://shop.doterra.com/PT/pt_PT/shop/specialised-supplements", 
        ['Cuidado Pessoal', 'Suplementos Especializados']
    )
])
def test_process_subcategory_page(browser: WebDriver, products_page_url: str, subcategory_address_list: List[str]):
    """
    Testing process of subcategory page / product page 

    Apllies mocking patch of process_product_page and selenium.webdriver.remote.webelement.WebElement.click
    so these functions wont interfer with test of process_subcategory_page function 
    """

    with patch("scraper.parse_product", autospec=True), \
            patch("selenium.webdriver.remote.webelement.WebElement.click", autospec=True):
        
        browser.get(products_page_url)
        subcategory_address = get_address(subcategory_address_list)

    assert scraper.process_subcategory_page(browser, subcategory_address)


@mock.patch("scraper.log.handlers", pytest.handlers)
@pytest.mark.parametrize("website_url", [
    ("https://shop.doterra.com/PT/pt_PT/shop/home/")

])
def test_handle_hover_menu(browser: WebDriver, website_url: str):
    """
    Testing handle_hover_menu
    
    Applies mocking patch of process_subcategory_page 
    so it wont interfer with test of handle_hover_menu function
    """
    with patch("process_subcategory_page", autospec=True) as mocked_process_subcategory_page:
        mocked_process_subcategory_page.return_value = True
        
        browser.get(website_url)
    assert scraper.handle_hover_menu(browser)

def test_main():
    """
    Testing main
    """
    with mock.patch("scraper.CONTEXT_PRODUCTS", ["Creme Hidratante", "Loção Solar Mineral Rosto + Corpo dōTERRA™ sun"]):
        assert scraper.main()