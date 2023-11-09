import re
import os
import csv
import time
import json
import typing
import asyncio
import logging
import traceback
import urllib.request

from typing import Dict, List, TypeVar, TypedDict, Union
from datetime import datetime
from numpy import cast, product

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from sympy import Product

from components.models import Information, Benefits, Ingredients, Uses, Product
from components.utils import accept_bloody_cookie, hover_over, wait_for_element, kill_edge


# Most efective way to get currerent script location
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Browser options
OPTIONS = [
    # "--user-data-dir=C:\\Users\\anewe\\AppData\\Local\\Microsoft\\Edge\\User Data",
    # "--headless",
    "--inprivate",
    "--start-maximized",
    "--disable-extensions",
    "--remote-debugging-port=9222"
]

# URL doTERRA website
URL = "https://shop.doterra.com/PT/pt_PT/shop/home/"

# Mouse scroll delay in seconds
SCROLL_PAUSE_DELAY = 2.0

# Categorias que estao sendo processadas
CONTEXT_CATEGORIES = ["Cuidado Pessoal", "MetaPWR™", "Suplementos"]

# Buffer das categorias que ja foram abertas
OPENED_SUBCATEGORIES = []

# Timeout
TIMEOUT = 5

log = logging.getLogger("scraper")
logging.basicConfig(
    filename=f"./logs/SCRAPER_{datetime.now().strftime('%d-%m-%Y_%H.%M.%S')}.log", 
    filemode='w+',
    format="%(asctime)s - %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
    encoding='utf-8', 
    level=logging.INFO
)

def get_browser(options: List[str]) -> WebDriver:
    """
    Will get then return the Selenium driver
    """
    log.info(f"Getting browser object with custom options: {json.dumps(options, indent=4)}")
    
    edge_options = Options()
    for i in options:
        edge_options.add_argument(i)
    
    service = Service(os.path.join(__location__, "components/msedgedriver.exe"))
    browser = webdriver.Edge(service=service, options=edge_options)
    browser.implicitly_wait(TIMEOUT)  # Timeout

    return browser


def write_csv(product: Product):
    """
    Write CSV with product information
    """
    template_csv = os.path.join(__location__, "Produtos doterra - Produtos.csv")
    csv_reader = csv.reader(template_csv)

# Introducing: Generics
T = TypeVar('T', Information, Benefits, Ingredients, Uses)

def parser_helper(browser: WebDriver, box: T) -> T:
    """
    Help parsing the pages
    """
    log.info(f"Entered the parser helper...")

    for element_name in box.keys():
        element_dict = box[element_name]
        element_dict_keys = element_dict.keys()

        if "class_name" in element_dict_keys:
            element = wait_for_element(browser, By.CLASS_NAME, element_dict["class_name"], TIMEOUT)
        elif "field_name" in element_dict_keys:
            element = wait_for_element(browser, By.NAME, element_dict["field_name"], TIMEOUT)
        elif "xpath" in element_dict_keys:
            element = wait_for_element(browser, By.XPATH, element_dict["xpath"], TIMEOUT)
        else:
            log.error("Error: hit a never type.")
            raise SystemExit
        
        if element.tag_name == "ul":
            lis = element.find_elements(By.XPATH, "./li")
            # repr will convert unicoded chars into their nice printable versions
            string = [repr(li.text) + '\n' for li in lis]            
            box[element_name]["text"] = string
        else:
            box[element_name]["text"] = repr(element.text)
    
    log.info(f"Parsed product: {json.dumps(box, indent=4)}")

    return box

def parse_product_images(browser: WebDriver) -> List[WebElement]:
    """
    Get and download all images from product webpage
    """
    images: List[WebElement] = browser.find_elements(By.CSS_SELECTOR, "img")
    return images

def parse_product_uses(browser: WebDriver):
    """
    Parse the product utilization information
    """ 
    log.info(f"Parsing product utilization information from product webpage: {browser.current_url}")

    utilization_box: Uses = {
        "uses_title": {
            "xpath": '//*[@id="ProductUsesSection"]/div[1]/div/div[2]/h3[1]/span',
            "text": ""
        },
        "uses": {
            "xpath": '//*[@id="ProductUsesSection"]/div[1]/div/div[2]/div[1]/ul',
            "text": ""
        },
        "instructions_title": {
            "xpath": '//*[@id="ProductUsesSection"]/div[1]/div/div[2]/h3[2]/span',
            "text": ""
        },
        "instructions": {
            "xpath": '//*[@id="ProductUsesSection"]/div[1]/div/div[2]/div[2]/div/div[2]/span',
            "text": ""
        },
        "cautions_title": {
            "xpath": '//*[@id="ProductUsesSection"]/div[1]/div/div[2]/div[3]/h3/span',
            "text": ""
        },
        "cautions": {
            "xpath": '//*[@id="ProductUsesSection"]/div[1]/div/div[2]/div[3]/div/p/span',
            "text": ""
        },
    }

    new_utilization_box = parser_helper(browser, utilization_box)
    return new_utilization_box

def parse_product_ingredients(browser: WebDriver):
    """
    Parse the product ingredients information
    """
    log.info(f"Parsing ingredients information from product webpage: {browser.current_url}")

    ingredients_box: Ingredients = {
        "ingredients_title": {
            "xpath": '//*[@id="WhatsInsideSection"]/div/div[2]/div/h3/span',
            "text": ""
        },
        "ingredients": {
            "xpath": '//*[@id="WhatsInsideSection"]/div/div[2]/div/div/p/span',
            "text": ""
        }
    }

    new_ingredients_box = parser_helper(browser, ingredients_box)
    return new_ingredients_box

def parse_product_benefits(browser: WebDriver):
    """
    Parse the product benefits information
    """

    benefits_box: Benefits = {
        "benefits_title": {
            "xpath": '//*[@id="ProductSpotlightSection"]/div[3]/div[2]/div/div/h3/span',
            "text": ""
        },
        "benefits": {
            "xpath": '//*[@id="ProductSpotlightSection"]/div[3]/div[2]/div/div/div/ul',
            "text": ""
        }
    }

    new_benefits_box = parser_helper(browser, benefits_box)
    return new_benefits_box
        
def parse_product_information(browser: WebDriver):
    """
    Parse the product main information
    """
    log.info(f"Parsing main information from product webpage: {browser.current_url}")

    information_box: Information = {
        "product_name": {
            "xpath": '//*[@id="ProductSpotlightSection"]/div[1]/div/div/div[1]/h3/span',
            "text": ""
        },
        "description": {
            "xpath": '//*[@id="ProductSpotlightSection"]/div[1]/div/div/div[1]/div[1]/p/span',
            "text": ""
        },
        "dimensions": {
            "xpath": '//*[@id="ProductSpotlightSection"]/div[1]/div/div/div[3]/div/div[2]/div[1]/div/div[2]/span',
            "text": ""
        },
        "item_id": {
            "xpath": '//*[@id="ProductSpotlightSection"]/div[1]/div/div/div[3]/div/div[2]/div[2]/div/div[2]',
            "text": ""
        },
        "retail_price": {
            "xpath": '//*[@id="ProductSpotlightSection"]/div[1]/div/div/div[3]/div/div[3]/div[1]/div/div[2]',
            "text": ""
        },
        "discount_price": {
            "xpath": '//*[@id="ProductSpotlightSection"]/div[1]/div/div/div[3]/div/div[3]/div[1]/div/div[2]',
            "text": ""
        }
    }

    new_information_box = parser_helper(browser, information_box)
    return new_information_box
    
def parse_product(browser: WebDriver) -> Product:
    """
    Parse all product information and images from product page
    """
    log.info(f"Parsing information from product webpage: {browser.current_url}")
    
    utilization_box = parse_product_information(browser)
    ingredients_box = parse_product_benefits(browser)
    benefits_box = parse_product_ingredients(browser)
    information_box = parse_product_uses(browser)
    images = parse_product_images(browser)

    product: Product = { 
        "information": utilization_box,
        "benefits": ingredients_box,
        "ingredients": benefits_box,
        "uses": information_box,
        "images": images
    }

    return product

def process_products_page(browser: WebDriver):
    """
    Handle all the products present on subcategory products page
    """
    log.info("Processing products page...")
    
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
        log.info("Handling hover menu 'COMPRAR'")
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
                            process_products_page(browser)

                            # Aplicando recursao
                            handle_hover_menu(browser)
                    else:
                        # Se o li nao tem texto, e porque esta vazio
                        continue

    except ZeroDivisionError:
        pass
    
@kill_edge
def main():
    """
    Another main function
    """
    log.info("Starting script...")

    try:
        browser = get_browser(OPTIONS)
        browser.implicitly_wait(30)  # Timeout

        # OBS: necessário entrar no VPN de portugal porque o Edge redireciona pro site BR que é diferente
        browser.get(URL)
        browser = accept_bloody_cookie(browser)
        handle_hover_menu(browser)

        return True
    
    except ZeroDivisionError:
        pass
    except SystemExit:
        raise SystemExit
    except Exception:
        log.error(f"Unexpected error: {traceback.format_exc()}")
        return False

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
