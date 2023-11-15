# -*- coding: utf-8 -*-
import os
import os
import sys
import csv
import timeit
from unittest import mock
import pytest

from typing import List, Union
from unittest.mock import patch

from selenium.webdriver.edge.webdriver import WebDriver

import scraper

from components.utils import join_strings, kill_edge
from components.models import NormalizedProduct, Product
from tests.test_data import VALID_PRODUCT, VALID_FORMAT_EMPTY_FIELDS_PRODUCT, INVALID_FORMAT_PRODUCT, VALID_NORMALIZED_PRODUCT, VALID_FORMAT_EMPTY_FIELD_NORMALIZED_PRODUCT, INVALID_FORMAT_NORMALIZED_PRODUCT


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


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


@pytest.mark.parametrize("product_page_url", [
    ("https://shop.doterra.com/PT/pt_PT/shop/correctx/")
])
@kill_edge
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


@pytest.mark.depends(on=['test_validate_dict'])
@pytest.mark.parametrize("product_page_url", [
    ("https://shop.doterra.com/PT/pt_PT/shop/correctx/")
])
@kill_edge    
def test_parse_product(browser: WebDriver, product_page_url):    
    """
    Testing parse_product
    """
    browser.get(product_page_url)
    assert scraper.parse_product(browser) 


@pytest.mark.depends(on=[
    test_parse_product,
    test_normalize_product,
    test_download_product_images,
    test_write_csv
])
@pytest.mark.parametrize("product_page_urls", [
    ([
        "https://shop.doterra.com/PT/pt_PT/shop/correctx/",
        "https://shop.doterra.com/PT/pt_PT/shop/daily-nutrient-pack/",
        "https://shop.doterra.com/PT/pt_PT/shop/hydrating-cream/",
        "https://shop.doterra.com/PT/pt_PT/shop/doterra-sun-face-body-mineral-sunscreen-lotion/",
        "https://shop.doterra.com/PT/pt_PT/shop/metapwr-beadlets/"
])])
@kill_edge    
def test_process_product_page(browser: WebDriver, product_page_urls: List[str]):    
    """
    Testing parse_product
    """
    for i in product_page_urls:
        browser.get(i)
        assert scraper.process_product_page(browser)

    return


@kill_edge
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
        subcategory_address = join_strings(subcategory_address_list)

    assert scraper.process_subcategory_page(browser, subcategory_address)


@kill_edge
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


@kill_edge
def test_main():
    """
    Testing main
    """
    assert scraper.main()