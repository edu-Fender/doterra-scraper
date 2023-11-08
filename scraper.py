import re
import os
import time
import json
import asyncio
import traceback
import typing
import urllib.request

from typing import Dict, List, TypedDict, Union
from datetime import datetime
from numpy import cast

from selenium import webdriver  # selenium 4.8.3
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from sympy import Product

from components.models import Information, Benefits, Ingredients, Uses, Product
from components.utils import accept_bloody_cookie,  hover_over, kill_edge, log, wait_for_element


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Browser options
OPTIONS = [
    # "--user-data-dir=C:\\Users\\anewe\\AppData\\Local\\Microsoft\\Edge\\User Data",
    "--headless",
    "--inprivate",
    "--start-maximized",
    "--disable-extensions",
    "--remote-debugging-port=9222"
]

# URL doTERRA website
URL = "https://shop.doterra.com/PT/pt_PT/shop/home/"

# Delay do scroll do mouse em segundo
SCROLL_PAUSE_DELAY = 1.0

# Categorias que estao sendo processadas
CONTEXT_CATEGORIES = ["Cuidado Pessoal", "MetaPWR™", "Suplementos"]

# Buffer das categorias que ja foram abertas
OPENED_SUBCATEGORIES = []

LOGFILE = f"./logs/LOG_{datetime.now().strftime('%d%m%Y%H%M%S')}.txt"


def get_browser(options: List[str]) -> WebDriver:
    """
    Will get then return the Selenium driver
    """
    log(f"Getting browser object with custom options: {json.dumps(options, indent=4)}", logfile=LOGFILE)
    
    edge_options = Options()
    for i in options:
        edge_options.add_argument(i)
    
    service = Service(os.path.join(__location__, "components/msedgedriver.exe"))
    browser = webdriver.Edge(service=service, options=edge_options)

    return browser

def get_all_images(browser: WebDriver):
    """
    Get and download all images from webpage
    """
    pass

def parse_product_uses(browser: WebDriver):
    """
    Parse the product utilization information
    """ 
    log(f"Parsing product utilization information from product webpage: {browser.current_url}", logfile=LOGFILE)

    utilization_box: Uses = {
        "uses_title": {
            "type": "span",
            "field_name": "product_uses_title",
            "text": ""
        },
        "uses": {
            "type": "ul",
            "class_name": "custom-list",
            "text": ""
        },
        "instructions_title": {
            "type": "span",
            "field_name": "product_uses_directions_title",
            "text": ""
        },
        "instructions": {
            "type": "span",
            "field_name": "product_uses_directions_text1",
            "text": ""
        },
        "cautions_title": {
            "type": "span",
            "class_name": "product_uses_cautions_title",
            "text": ""
        },
        "cautions": {
            "type": "span",
            "class_name": "product_uses_cautions_text",
            "text": ""
        },
    }
        
def parse_product_ingredients(browser: WebDriver):
    """
    Parse the product ingredients information
    """
    log(f"Parsing ingredients information from product webpage: {browser.current_url}", logfile=LOGFILE)

    ingredients_box: Ingredients = {
        "ingredients_title": {
            "type": "h3",
            "class_name": "product-whats-inside__footer-title",
            "text": ""
        },
        "ingredients": {
            "type": "div",
            "class_name": "product-whats-inside__footer-content",
            "text": ""
        }
    }


def parse_product_benefits(browser: WebDriver):
    """
    Parse the product benefits information
    """
    log(f"Parsing benefits information from product webpage: {browser.current_url}", logfile=LOGFILE)

    benefits_box: Benefits = {
        "benefits_title": {
            "type": "h3",
            "class_name": "spotlight__foot-block-title",
            "text": ""
        },
        "benefits": {
            "type": "ul",
            "class_name": "spotlight__list-custom custom-list",
            "text": ""
        }
    }
        
def parse_product_information(browser: WebDriver):
    """
    Parse the product main information
    """
    log(f"Parsing main information from product webpage: {browser.current_url}", logfile=LOGFILE)
    # product_name_xpath  = '//*[@id="ProductSpotlightSection"]/div[1]/div/div/div[1]/h3[1]/span'
    # product_info_div_xpath = '//*[@id="ProductSpotlightSection"]/div/div/div/div[3]/div'

    information_box: Information = {
        "product_name": {
            "type": "h3",
            "class_name": "spotlight__head-title",
            "text": ""
        },
        "description": {
            "type": "div",
            "class_name": "spotlight__head-copy",
            "text": ""
        },
        "dimensions": {
            "type": "div",
            "class_name": "loyalty-order__row loyalty-order__row--size",
            "text": ""
        },
        "item_id": {
            "type": "div",
            "class_name": "loyalty-order__row loyalty-order__row--item",
            "text": ""
        },
        "retail_price": {
            "type": "div",
            "class_name": "loyalty-order__row loyalty-order__row--wholesale",
            "text": ""
        },
        "discount_price": {
            "type": "span",
            "class_name": "loyalty-order__row loyalty-order__row--retail",
            "text": ""
        },
        "images": []
    }

    for element_name, element_dict in information_box.items():
        field_names = element_dict.keys()
        
        if "class_name" in field_names:
            # element = browser.find_element(By.CLASS_NAME, element_dict["class_name"])
            element = wait_for_element(browser, By.XPATH, element_dict["class_name"])
        
        elif "field_name" in field_names:
            element = browser.find_element(By.NAME, element_dict["field_name"])
        elif "xpath" in field_names:
            element = browser.find_element(By.XPATH, element_dict["xpath_name"])
        else:
            log("Error: hit a never type.", logfile=LOGFILE)
            return False

        information_box[element_name]["text"] = element.text
    
    return

def parse_product(browser: WebDriver):
    """
    Parse all product information and images from product page
    """
    log(f"Parsing information from product webpage: {browser.current_url}", logfile=LOGFILE)
    parse_product_information(browser)

def process_subcategory_products_page(browser: WebDriver):
    """
    Handle all the products present on subcategory products page
    """
    log("", logfile=LOGFILE)
    # ============================== Scrolando para baixo para carregar os produtos ============================== 
    # Get scroll height
    original_height = browser.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_DELAY)

        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script("return document.body.scrollHeight")

        if original_height == new_height:
            break

    # ============================== Clicando nos produtos ==============================
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    products_div_xpath = '//*[@id="categoryitemgrid"]'
    products_div: WebElement = browser.find_element(By.XPATH, products_div_xpath)
    products: List[WebElement] = products_div.find_elements(By.XPATH, "./div/a")
    
    # TODO: criar logica async para parsear a pagina de produtos
    for product in products:
        product.click()
        parse_product(browser)

def handle_hover_menu(browser: WebDriver):
    """
    Handles interaction with hover type menu to get the categories, then the subcategories, then the products
    """
    try:
        log("Handling hover menu 'COMPRAR'", logfile=LOGFILE)
        # ===================================== Passando o mouse no botão "comprar" =====================================
        comprar_btn_xpath = '//*[@id="header"]/div[4]/div/div/div/div[2]/nav/ul/li[1]/a/span'
        hover_over(browser, comprar_btn_xpath)

        # ===================================== Passando o mouse nas diferentes categorias =====================================
        categories_div_xpath = '//*[@id="header"]/div[4]/div/div/div/div[2]/nav/ul/li[1]/div/div/div/div/div/div[2]/div/ul'
        categories_div: WebElement = browser.find_element(By.XPATH, categories_div_xpath)
        
        # "lis" stands for: "li" -> HTML element li (List Item); "s" -> plural of li
        categories_lis: List[WebElement] = categories_div.find_elements(By.XPATH, "./li")

        for category_li in categories_lis:
            if category_li.text in CONTEXT_CATEGORIES:
                hover_over(browser, category_li)
                # subcategories_ul_xpath = '//*[@id="header"]/div[4]/div/div/div/div[2]/nav/ul/li[1]/div/div/div/div/div/div[2]/div/ul/li[3]/ul'
                subcategories_lis: list[WebElement] = category_li.find_elements(By.XPATH, "./ul/li")

                for subcategory_li in subcategories_lis:
                    # ===================================== Passando o mouse nas subcategorias de cada categorias =====================================
                    if subcategory_li.text:
                        subcategory_full_name = category_li.text + "." + subcategory_li.text
                        
                        # TODO: implementar logica async (provavelmente) para processar a pagina da subcategoria de produtos
                        if not subcategory_full_name in OPENED_SUBCATEGORIES:
                            OPENED_SUBCATEGORIES.append(subcategory_full_name)
                            subcategory_li.click()

                            # Chama a funcao pra parsear a pagina da subcategoria atual
                            process_subcategory_products_page(browser)

                            # Aplicando recursao
                            handle_hover_menu(browser)
                    else:
                        # Se o li nao tem texto, e porque esta vazio
                        continue

    except ZeroDivisionError:
        pass
    
def main():
    """
    Another main function
    """
    try:
        log("Starting script...", logfile=LOGFILE)
        
        log("Inicializando instancia...", logfile=LOGFILE)
        browser = get_browser(OPTIONS)
        browser.implicitly_wait(30)  # Timeout

        # OBS: necessário entrar no VPN de portugal porque o Edge redireciona pro site BR que é diferente
        browser.get(URL)
        browser = accept_bloody_cookie(browser)
        handle_hover_menu(browser)

        return True
    
    except ZeroDivisionError:
        pass
    except Exception:
        log(f"Unexpected error: {traceback.format_exc()}", logfile=LOGFILE)
        return False
    finally:
        log("Finishing execution...", logfile=LOGFILE)
        kill_edge()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
