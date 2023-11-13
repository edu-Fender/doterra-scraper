import os
import pytest

from typing import List
from unittest.mock import patch

from selenium.webdriver.edge.webdriver import WebDriver

import scraper 

from tests.conftest import validate_nested_dicts
from components.utils import kill_edge
from components.models import NormalizedProduct, Product

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def test_write_csv(normalized_products: List[NormalizedProduct]):
    """
    Testing write_csv
    """
    for product in normalized_products:
        assert scraper.write_csv(product)

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

def test_normalize_product(products: List[Product]):
    """
    Testing normalize_product
    """
    for product in products:
        normalized_product = scraper.normalize_product(product)
        assert validate_nested_dicts(normalized_product)

def test_validate_product(products: List[Product]):
    """
    Testing validate_product
    """
    for product in products:
        assert scraper.validate_product(product)

@pytest.mark.parametrize("product_page_url", [
    ("https://shop.doterra.com/PT/pt_PT/shop/correctx/")

])
@kill_edge    
def test_parse_product_text(browser: WebDriver, product_page_url):    
    """
    Testing parse_product_text
    """
    browser.get(product_page_url)
    product = scraper.parse_product_text(browser) 
    assert validate_nested_dicts(product)

@pytest.mark.parametrize("product_page_url", [
    ("https://shop.doterra.com/PT/pt_PT/shop/correctx/")

])
@kill_edge    
def test_process_product_page(browser: WebDriver, product_page_url):    
    """
    Testing process_product_page
    """
    browser.get(product_page_url)
    assert scraper.process_product_page(browser) 

@kill_edge
@pytest.mark.parametrize("products_page_url", [
    # Pagina que tem muitos produtos que so sao carregados ao fazer scrolldown com o mouse
    ("https://shop.doterra.com/PT/pt_PT/shop/essential-skin-care-brand")
])
def test_handle_subcategory_page(browser: WebDriver, products_page_url: str):
    """
    Testando as páginas de subcategorias
    """
    browser.get(products_page_url)

    # Mocking scraper.process_product_page function to return nothing
    # Mocking is so cool!
    with patch("scraper.process_product_page", autospec=True) as mocked_process_product_page, patch("selenium.webdriver.remote.webelement.WebElement.click", autospec=True) as mocked_webelement_click:
        mocked_process_product_page.return_value = True
        mocked_webelement_click.return_value = True
        
        subcategory_address = r' -> '.join(['Cuidado Pessoal', 'Cuidado da Pele Essencial'])
        assert scraper.handle_subcategory_page(browser, subcategory_address)

@kill_edge
@pytest.mark.parametrize("website_url", [
    ("https://shop.doterra.com/PT/pt_PT/shop/home/")

])
def test_handle_hover_menu(browser: WebDriver, website_url: str):
    """
    Testing handle_hover_menu
    """
    # Mocking handle_subcategory_page to return True so it dosn't interfer with handle_hover_menu function test
    with patch("scraper.handle_subcategory_page", autospec=True) as mocked_handle_subcategory_page:
        mocked_handle_subcategory_page.return_value = True
        browser.get(website_url)
        assert scraper.handle_hover_menu(browser)

# @kill_edge
def test_main():
    """
    Testing main
    """
    assert scraper.main()