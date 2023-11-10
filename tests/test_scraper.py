import os
import pytest
from selenium.webdriver.edge.webdriver import WebDriver

import scraper 
from components.utils import kill_edge


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

@kill_edge
def test_download_product_images(browser: WebDriver):
    url = "https://shop.doterra.com/PT/pt_PT/shop/correctx/"
    browser.get(url)
    product_name = "Pomada Essencial Correct-X™"
    result = scraper.download_product_images(browser, product_name)
    assert result

@kill_edge
def test_parse_product_information(browser: WebDriver):    
    url = "https://shop.doterra.com/PT/pt_PT/shop/correctx/"
    browser.get(url)
    result = scraper.parse_product_information(browser)
    assert result

# @kill_edge
def test_parse_product_benefits(browser: WebDriver):    
    url = "https://shop.doterra.com/PT/pt_PT/shop/correctx/"
    browser.get(url)
    result = scraper.parse_product_benefits(browser) 

# @kill_edge
def test_parse_product_ingredients(browser: WebDriver):    
    url = "https://shop.doterra.com/PT/pt_PT/shop/correctx/"
    browser.get(url)
    result = scraper.parse_product_ingredients(browser) 

# @kill_edge
def test_parse_product_uses(browser: WebDriver):    
    url = "https://shop.doterra.com/PT/pt_PT/shop/correctx/"
    browser.get(url)
    result = scraper.parse_product_uses(browser)

# @kill_edge
def test_parse_product_images(browser: WebDriver):    
    url = "https://shop.doterra.com/PT/pt_PT/shop/correctx/"
    browser.get(url)
    result = scraper.parse_product_images(browser) 

# @kill_edge    
def test_parse_product(browser: WebDriver):    
    url = "https://shop.doterra.com/PT/pt_PT/shop/correctx/"
    browser.get(url)
    result = scraper.parse_product(browser) 
    
# @kill_edge
@pytest.mark.parametrize("url", [
    # Pagina que tem muitos produtos que so sao carregados ao fazer scrolldown com o mouse
    ("https://shop.doterra.com/PT/pt_PT/shop/roll-on-essentials")

])
def test_process_subcategory_page(browser: WebDriver, url: str):
    """
    Testando as páginas de subcategorias
    """
    browser.get(url)
    assert scraper.process_products_page(browser)

# @kill_edge
@pytest.mark.parametrize("url", [
    ("https://shop.doterra.com/PT/pt_PT/shop/home/")

])
def test_handle_hover_menu(browser: WebDriver, url: str):
    browser.get(url)
    assert scraper.handle_hover_menu(browser)

# @kill_edge
def test_main():
    assert scraper.main()