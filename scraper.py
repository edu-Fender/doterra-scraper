# -*- coding: utf-8 -*-
import re
import os
import csv
import sys
import time
import json
import logging
import timeit
import traceback
import urllib.request

from typing import List, TypeVar, Union, Sequence
from numpy import product

from selenium.webdriver.common.by import By
from selenium.webdriver.edge.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from components.models import CSVRequiredFields, Information, Benefits, Ingredients, Uses, Product, NormalizedProduct
from components.utils import get_logger, get_browser, wait_for_element, wait_for_all_elements, hover_over, accept_bloody_cookie, join_strings, kill_edge
from components.data import CSVHEADER, INFORMATION, BENEFITS, INGREDIENTS, UTILIZATION


# Most efective way to get current script location
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Getting logger
log = get_logger(os.path.join(__location__, r"logs\SCRAPER.log"))

# Buffers
SUBCATEGORIES_BUFF: List[str] = []
PRODUCTS_BUFF: List[str] = []

# Constants
TIMEOUT = 5
SCROLL_PAUSE_DELAY = 2.0
GENERATED_CSV_FILE = os.path.join(__location__, "generated", "Produtos doterra - Produtos.csv")
CLEAR_CSV_FLAG = True
CONTEXT_CATEGORIES = ["Cuidado Pessoal", "MetaPWR™", "Suplementos"]


def validate_dict(dict_: Union[Product, NormalizedProduct, dict]) -> bool:
    """
    Recursiverly going in nested dicts to validate no field is empty
    """
    for val in dict_.values():
        if not val:
            raise ValueError("Product dict had empty fields.")
        if isinstance(val, dict):
            validate_dict(val)

    return True


def write_csv(normalized_product: NormalizedProduct) -> bool:
    """
    Write CSV with product information
    """
    global CLEAR_CSV_FLAG
    
    log.info("Writing product to CSV...")

    csv_fields: CSVRequiredFields = {
        "ID do produto": normalized_product["item_id"],
        "Nome": normalized_product["product_name"],
        "DescriÃ§Ã£o": normalized_product["description"],
        "PreÃ§o (imposto incluÃ­do)": normalized_product["retail_price"],
        "PreÃ§o de custo (atacado)": normalized_product["discount_price"]
    }

    # Clever logic to clean CSV file in case its the first time this function is called
    if CLEAR_CSV_FLAG:
        with open(GENERATED_CSV_FILE, 'w'):
            CLEAR_CSV_FLAG = False

    # Writing to new CSV file
    with open(GENERATED_CSV_FILE, mode='w', encoding="utf-8", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=CSVHEADER, delimiter=";")
        writer.writeheader()
        writer.writerow(csv_fields)
 
    return True


def download_all_images(browser: WebDriver, product_name: str) -> List[str]:
    """
    Get and download all images from product webpage
    """
    log.info(f"Downloading images for product {product_name}...")
    
    # Getting images
    images: List[WebElement] = wait_for_all_elements(browser, By.XPATH, "//img")
    product_images_dir = os.path.join(__location__, r"generated\images", product_name)

    # Creating directory with name of product only if it doesnt already exists
    try:
        os.mkdir(product_images_dir)
    except FileExistsError:
        pass

    downloaded_images = []
    ignored_images = []
    for image in images:
        image_src = image.get_attribute("src")

        if not image_src:
            log.warning(f"Couldn't download image {image_src}.")
            continue 
        elif re.findall(r"\.svg\s*$", image_src):
            # Ignore image in case it ends with .svg
            ignored_images.append(image_src)
            continue

        # Get string containing the text that comes after last slash of image_src
        try:
            regexed = re.findall(r"\/([^\/]*)$", image_src)[0]
        except IndexError:
            log.warning(f"Couldn't match regex pattern for {image_src}")
            continue
        
        image_name = os.path.join(product_images_dir, regexed)
        
        # If image already exists with same name
        if os.path.isfile(image_name):
            for i in range(1000):
                image_name += str(i)
                if not os.path.isfile(image_name):
                    break
            else:
                raise SystemExit("Tried 1000 different names for image but somehow they were all taken.")

        # Downloading image
        path, _ = urllib.request.urlretrieve(image_src, image_name)
        if not path:
            log.warning(f"Image [{image_src}] couldn't be downloaded.")
            continue

        downloaded_images.append(path)    

    log.info(f"Succesfully downloaded images: {json.dumps(downloaded_images, indent=4)}")
    log.info(f"Ingnored images: {json.dumps(ignored_images, indent=4)}")

    return downloaded_images
    

def normalize_product(product: Product) -> NormalizedProduct:
    """
    Normalize product and fields according to clients specifications of generated CSV
    """
    def normalizer(text: Union[str, List[str]], title: str = ''):
        """
        Join strs and lists of strs together applying some regex also  
        """
        # Removes leading and trailing spaces/single-quotes/double-quotes
        exp = r"^([\s\'\"]*)|([\s\'\"]*)$"
        regexed = ""
        
        if title:
            regexed += re.sub(exp, r"", title) + '\n'

        if isinstance(text, str):
            regexed += re.sub(exp, r"", text)
        elif isinstance(text, list):
            # Joining all itens of list in a single string
            regexed += '\n'.join(re.sub(exp, r"", i) for i in text)
        else:
            raise SyntaxError("Hit a never type.")
        
        # Removing leading and trailing line breaks
        regexed = re.sub(r"^(\n+)|(\n+)$", r"", regexed)

        # Escaping the '\n' so they wont mess the CSV up
        regexed = re.sub(r"\n", r"\\n", regexed)

        return regexed

    # TODO: improve this logic please its too ugly
    benefits = normalizer(
        product["benefits"]["benefits"]["text"], 
        title=product["benefits"]["benefits_title"]["text"]
    )
    ingredients = normalizer(
        product["ingredients"]["ingredients"]["text"], 
        title=product["ingredients"]["ingredients_title"]["text"]
    )
    uses_uses = normalizer(
        product["uses"]["uses"]["text"], 
        title=product["uses"]["uses_title"]["text"]
    )
    uses_instructions = normalizer(
        product["uses"]["instructions"]["text"], 
        title=product["uses"]["instructions_title"]["text"]
    )
    uses_cautions = normalizer(
        product["uses"]["cautions"]["text"], 
        title=product["uses"]["cautions_title"]["text"]
    )

    normalized_product: NormalizedProduct = {
        "product_name": normalizer(product["information"]["product_name"]["text"]),
        "item_id": normalizer(product["information"]["item_id"]["text"]),
        "retail_price": normalizer(product["information"]["retail_price"]["text"]),
        "discount_price": normalizer(product["information"]["discount_price"]["text"]),
        "description": normalizer([benefits, ingredients, uses_uses, uses_instructions, uses_cautions])
    }

    validate_dict(normalized_product)
    log.info(f"Normalized product: {json.dumps(normalized_product, indent=4)}")

    return normalized_product


def parse_product(browser: WebDriver) -> Product:
    """
    Parses text from product
    """
    # Cool Generics action
    T = TypeVar('T', Information, Benefits, Ingredients, Uses)

    def parser(browser: WebDriver, elements_box: T) -> T:
        """
        Help parsing the information from product webelements
        """
        for element_name in elements_box.keys():
            element_dict: dict = elements_box[element_name]
            element: WebElement = wait_for_element(browser, By.XPATH, element_dict["xpath"], TIMEOUT)

            if element.tag_name == "ul":
                lis = element.find_elements(By.XPATH, "./li")
                element_text_list = [li.text + '\n' for li in lis]
                elements_box[element_name]["text"] = element_text_list
            else:
                elements_box[element_name]["text"] = element.text
        
        return elements_box

    log.info(f"Parsing information from product webpage: {browser.current_url}")
    
    information_box: Information = parser(browser, INFORMATION)
    benefits_box: Benefits = parser(browser, BENEFITS)
    ingredients_box: Ingredients = parser(browser, INGREDIENTS)
    uses_box: Uses = parser(browser, UTILIZATION)

    # Assemblying the Megazord
    product: Product = { 
        "information": information_box,
        "benefits": benefits_box,
        "ingredients": ingredients_box,
        "uses": uses_box
    }

    # Validating Product dict
    validate_dict(product)

    log.info(f"Parsed product: {json.dumps(product, indent=4)}")
    return product


def process_product_page(browser: WebDriver) -> bool:
    """
    Parse all product information and images from individual product page
    """
    # Parsing product
    product: Product = parse_product(browser)

    # Normalizing products
    normalized_product: NormalizedProduct = normalize_product(product)

    # Downloading images
    download_all_images(browser, normalized_product["product_name"])

    # Writing CSV
    write_csv(normalized_product)

    # Sorry, is it Python or C?
    return True


def process_subcategory_page(browser: WebDriver, subcategory_address: str) -> bool:
    """
    Handle all the products present on products page / subcategory page
    """
    log.info(f"Processing products page '{subcategory_address}'...")
    products: List[WebElement] = []

    products_div_xpath = '//*[@id="categoryitemgrid"]'
    products_div: WebElement = wait_for_element(browser, By.XPATH, products_div_xpath)
    
    # ============================== Scrolling down to last visible product to load the products ============================== 
    while True:
        products: List[WebElement] = wait_for_all_elements(products_div, By.XPATH, "./div/a")

        last_product: WebElement = products[-1]
        last_scroll_height = browser.execute_script("return document.body.scrollHeight")

        # Javascript expression to scroll to a particular element
        # arguments[0] refers to the first argument that is later passed
        # in to execute_script method
        browser.execute_script("arguments[0].scrollIntoView();", last_product)   

        # Wait to load page
        time.sleep(SCROLL_PAUSE_DELAY)

        # Calculate new scroll height and compare with original scroll height
        new_scroll_height = browser.execute_script("return document.body.scrollHeight")
        if last_scroll_height == new_scroll_height:
            log.info(f"Found {len(products)} products on page '{subcategory_address}'.")
            break

        log.info(f"Scrolled {new_scroll_height - last_scroll_height} pixels down to last visible product.")

    # ============================== Clicking products ==============================
    # The most important loop you'll see today
    for count, product in enumerate(products, start=1):
        product_name = product.accessible_name
        product_address = join_strings([subcategory_address, product_name])        

        if product_address not in PRODUCTS_BUFF:
            log.info(f"Clicking product {count}. '{product_address}'...")
            
            try:
                # Getting to product page
                product.click()
                process_product_page(browser)
                PRODUCTS_BUFF.append(product_address)

            except SystemExit:
                log.critical(f"Critical error: {traceback.format_exc}")
                log.info(f"Exiting...")
                sys.exit()
            except Exception:
                log.warning(f"Coudn't parse product '{product_address}' due to unexpected error: {traceback.format_exc}")
                log.info(f"Continuing to next product...")
                continue
    
    log.info(f"{len(PRODUCTS_BUFF)} products parsed.")
    log.info(f"PRODUCTS_BUFF: {json.dumps(PRODUCTS_BUFF, indent=4)}")

    return True


def handle_hover_menu(browser: WebDriver) -> bool:
    """
    Handles interaction with hover type menu to get the categories, then the subcategories, then click it 
    """
    # Verbose will only be allowed for first execution of the function
    # Remember that the function applies recursion
    if not SUBCATEGORIES_BUFF:
        verbose = True
        log.info("Handling hover menu...")
    else:
        verbose = True
        log.info("Entered recursion...")

    # ===================================== Hovering mouse over "comprar" button =====================================
    comprar_btn_xpath = '//*[@id="header"]/div[4]/div/div/div/div[2]/nav/ul/li[1]/a/span'
    hover_over(browser, comprar_btn_xpath, verbose=verbose)

    # ===================================== Hovering mouse over the context categories =====================================
    categories_div_xpath = '//*[@id="header"]/div[4]/div/div/div/div[2]/nav/ul/li[1]/div/div/div/div/div/div[2]/div/ul'
    categories_div: WebElement = wait_for_element(browser, By.XPATH, categories_div_xpath)
    categories_lis: List[WebElement] = wait_for_all_elements(categories_div, By.XPATH, "./li") # "lis" stands for "List ItemS" 

    for category_li in categories_lis:
        category_name = category_li.text

        if category_name in CONTEXT_CATEGORIES:
            hover_over(browser, category_li, verbose=verbose)
            subcategories_lis: list[WebElement] = category_li.find_elements(By.XPATH, "./ul/li")

            # ===================================== Hovering mouse over all subcategories for given category =====================================
            for subcategory_li in subcategories_lis:
                subcategory_name = subcategory_li.text
                
                if subcategory_li.text:
                    subcategory_address = join_strings([category_name, subcategory_name]) 
                
                    if not subcategory_address in SUBCATEGORIES_BUFF:
                        # Parsing the given product page
                        subcategory_li.click()
                        process_subcategory_page(browser, subcategory_address)
                        SUBCATEGORIES_BUFF.append(subcategory_address)
                        log.info(f"Added value to SUBCATEGORIES_BUFF: {json.dumps(SUBCATEGORIES_BUFF, indent=4)}")

                        # A little bit of recursion
                        handle_hover_menu(browser)
    
    log.info(f"{len(SUBCATEGORIES_BUFF)} subcategories parsed.")
    return True


@kill_edge
def main() -> bool:
    """
    Another main function
    """
    log.info("Starting the scraper...")

    try:
        driver_path = os.path.join(__location__, r"components\msedgedriver.exe")
        driver_options = [
            # "--user-data-dir=C:\\Users\\anewe\\AppData\\Local\\Microsoft\\Edge\\User Data",
            # "--headless",
            "--inprivate",
            "--start-maximized",
            "--disable-extensions",
            "--remote-debugging-port=9222"
        ]

        browser = get_browser(driver_path, driver_options, TIMEOUT, zoom=70)
        browser.implicitly_wait(TIMEOUT)

        # OBS: necessery to be connected to Portugal's VPN
        url = "https://shop.doterra.com/PT/pt_PT/shop/home/"
        browser.get(url)
        browser = accept_bloody_cookie(browser)

        # Starting the fun
        handle_hover_menu(browser)

        return True
    
    except SystemExit:
        log.info("Finishing application...")
        raise SystemExit
    except Exception:
        log.critical(f"Unhandled error: {traceback.format_exc()}")
        raise SystemExit


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
