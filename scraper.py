# -*- coding: utf-8 -*-
import re
import os
import csv
import sys
import time
import json
import logging
import traceback
import urllib.request

from typing import List, Union
from datetime import datetime

from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from components.models import CSVRequiredFields, Information, Benefits, Ingredients, Uses, Product, NormalizedProduct
from components.utils import get_logger, get_address, get_browser, double_br_join, wait_for_element, wait_for_all_elements, hover_over
from components.data import CSVHEADER, INFORMATION, BENEFITS, INGREDIENTS, USES


# TODO: Better organize this global mess
# Most efective way to get current script location
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

logname = os.path.join(__location__, rf"logs\SCRAPER_{datetime.now().strftime('%d%m%Y_%H%M%S')}.log")
log: logging.Logger = logging.getLogger()

# Buffers
SUBCATEGORIES_BUFF: List[str] = []
PRODUCTS_BUFF: List[str] = []

# Constants
CLEAR_CSV_FLAG = True
GENERATED_CSV_FILE = os.path.join(__location__, "generated", "Produtos doterra - Produtos.csv")
CONTEXT_CATEGORIES: List[str] = ["Cuidado Pessoal", "Suplementos"]
TIMEOUT = 2
MOUSE_SCROLL_DELAY = 1


def validate_dict(dict_: Union[Product, NormalizedProduct, Information, Benefits, Ingredients, Uses, dict]) -> bool:
    """
    Recursiverly going in nested dicts to validate no field was empty
    """
    for val in dict_.values():
        if not val:
            raise ValueError
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
        "Resumo": normalized_product["short_description"],
        "DescriÃ§Ã£o": normalized_product["long_description"],
        "PreÃ§o (imposto incluÃ­do)": normalized_product["retail_price"],
        "PreÃ§o de custo (atacado)": normalized_product["discount_price"],
        "Peso": normalized_product["weight"]
    }

    # Clever logic to clean CSV file in case its the first time this function is called
    if CLEAR_CSV_FLAG:
        mode = 'w'
    else:
        mode = 'a'

    # Writing to new CSV file
    with open(GENERATED_CSV_FILE, mode=mode, encoding="utf-8", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=CSVHEADER, delimiter=";")
        if mode == 'w':
            writer.writeheader() 
        writer.writerow(csv_fields)
        CLEAR_CSV_FLAG = False
        
    log.info(F"Product successfully written to {GENERATED_CSV_FILE}.") 
    return True


def download_all_images(browser: WebDriver, product_name: str) -> bool:
    """
    Get and download all images from product webpage
    """
    log.info(f"Downloading images for product '{product_name}'...")
    
    # Getting images
    images: List[WebElement] = wait_for_all_elements(browser, By.XPATH, "//img")
    product_images_dir = os.path.join(__location__, r"generated\images", re.sub(r"[<>:\"/\\|\?\*]", r" ", product_name))

    # Creating directory with name of product only if it doesnt already exists
    try:
        os.mkdir(product_images_dir)
    except FileExistsError:
        pass

    for image in images:
        image_src = image.get_attribute("src")

        if not image_src:
            # BUG: I have no clue why images come without source nor name text nor nothing 
            log.warning(f"Couldnt download image '{image.accessible_name}'.")
            continue
        elif re.findall(r"\.svg\s*$", image_src):
            # Ignore image in case it ends with .svg
            log.info(f"Ignored image: '{image_src}'")
            continue

        # Get string containing the text that comes after last slash of image_src
        try:
            regexed = re.findall(r"\/([^\/]*)$", image_src)[0]
        except IndexError:
            log.warning(f"Couldn't create local file name for '{image_src}'")
            continue

        # FIXME: improve this logic cause images may be overriden!!
        image_name = os.path.join(product_images_dir, regexed)
        if os.path.isfile(image_name):
            log.info(f"Images already existed: '{image_name}'")
            continue
        
        urllib.request.urlretrieve(image_src, image_name)

    return True
    

def normalizer(text: str) -> str:
    """
    Join strs and lists of strs together applying some regex also  
    """
    # Removes leading and trailing spaces/single-quotes/double-quotes
    exp = r"^([\s\'\"]*)|([\s\'\"]*)$"

    regexed = re.sub(exp, r"", text)

    # Removing leading and trailing line breaks
    regexed = re.sub(r"^(\n+)|(\n+)$", r"", regexed)

    # Escaping the '\n' so they wont mess the CSV up
    regexed = re.sub(r"\n", r"\\n", regexed)

    return regexed


def parse_information(browser: WebDriver) -> Information:
    """
    Parse general information from product webpage
    """
    log.info(f"Parsing general information from product webpage: {browser.current_url}")
    information: Information = INFORMATION

    for INFORMATION_key in information.keys():
        INFORMATION_item: dict = information[INFORMATION_key]

        locator = INFORMATION_item["css_selector"]
        text = ''
        
        if INFORMATION_key in ["dimensions", "item_id"]:
            # Dimensions and item_id share the same css_selector
            elements: List[WebElement] = wait_for_all_elements(browser, By.CSS_SELECTOR, locator, TIMEOUT)
            
            for element in elements:
                # Dimensions is the one which has only numbers
                if re.match(r"\d{6,}", element.text) and INFORMATION_key == "item_id":
                    text = element.text
                elif not re.match(r"\d{6,}", element.text) and INFORMATION_key == "dimensions":
                    text = element.text
                    
        else:
            element: WebElement = wait_for_element(browser, By.CSS_SELECTOR, locator, TIMEOUT)
            text = element.text

        if not text:
            log.warning(f"Element '{INFORMATION_key}' from selector '{locator}' was empty.")
            information[INFORMATION_key]["text"] = ''
            continue

        # Normalizing and assigning
        text = normalizer(text)
        information[INFORMATION_key]["text"] = text
    
    log.info(f"Parsed product information: {json.dumps(information, indent=4)}")
    return information


def parse_benefits(browser: WebDriver) -> Benefits:
    """
    Parse benefits information from product webpage
    """
    log.info(f"Parsing benefits from product webpage: {browser.current_url}")
    benefits: Benefits = BENEFITS

    for BENEFITS_key in benefits.keys():
        BENEFITS_item: dict = benefits[BENEFITS_key]
    
        locator = BENEFITS_item["css_selector"]
        try:
            element: WebElement = wait_for_element(browser, By.CSS_SELECTOR, locator, TIMEOUT)
        except TimeoutException:
            log.warning(f"Product had no benefits section.")
            benefits[BENEFITS_key]["text"] = ''
            continue
            
        # Trying to parse element's text from secondary selector if text from primary locator was empty (that could happen)
        text = element.text
        if text:
            # Benefits could actually be a ul
            if element.tag_name == "ul":
                lis = wait_for_all_elements(element, By.XPATH, "./li")
                text = '\n'.join(li.text for li in lis if li.text)
        else:
            log.warning(f"Element '{BENEFITS_key}' from selector selector '{locator}' was empty.")

        # Normalizing and assigning
        text = normalizer(text)
        benefits[BENEFITS_key]["text"] = text

    log.info(f"Parsed product benefits: {json.dumps(benefits, indent=4)}")
    return benefits


def parse_ingredients(browser: WebDriver) -> Ingredients:
    """
    Parse ingredients information from product webpage
    """
    log.info(f"Parsing ingredients from product webpage: {browser.current_url}")
    ingredients: Ingredients = INGREDIENTS

    for INGREDIENTS_key in ingredients.keys():
        INGREDIENTS_item: dict = ingredients[INGREDIENTS_key]
    
        locator = INGREDIENTS_item["css_selector"]
        try:
            element: WebElement = wait_for_element(browser, By.CSS_SELECTOR, locator, TIMEOUT)
        except TimeoutException:
            log.warning(f"Product had no ingredients section.")
            ingredients[INGREDIENTS_key]["text"] = ''
            continue

        text = element.text
        if not text:
            log.warning(f"Element '{INGREDIENTS_key}' from selector '{locator}' was empty, attempting to find element with secondary locator...")
            locator = INGREDIENTS_item["css_selector_sec"]            
            
            if INGREDIENTS_key == "ingredients_title":
                element: WebElement = wait_for_element(browser, By.CSS_SELECTOR, locator, TIMEOUT)
                text = element.text

            elif INGREDIENTS_key == "ingredients":
                locator = INGREDIENTS_item["css_selector_sec"]
                whatsinside_div = wait_for_element(browser, By.CSS_SELECTOR, locator, TIMEOUT)
                text = whatsinside_div.text
            else:
                raise SystemExit("Hit a never type")

        if not text:
            logging.warning(f"Element '{INGREDIENTS_key}' was empty.")

        # Normalizing and assigning
        text = normalizer(text)
        ingredients[INGREDIENTS_key]["text"] = text

    log.info(f"Parsed product ingredients: {json.dumps(ingredients, indent=4)}")
    return ingredients


def parse_uses(browser: WebDriver) -> Uses:
    """
    Parse uses from product webpage
    """
    log.info(f"Parsing uses from product webpage: {browser.current_url}")
    uses: Uses = USES
    text = ''

    for USES_key in uses.keys():
        USES_item: dict = uses[USES_key]

        locator = USES_item["css_selector"]

        # These three elements share the same css_selector
        if USES_key in ["uses_title", "instructions_title", "cautions_title"]:
            try:
                elements: List[WebElement] = wait_for_all_elements(browser, By.CSS_SELECTOR, locator, TIMEOUT)
            except TimeoutException:
                log.warning(f"Product had no uses section.")
                uses[USES_key]["text"] = ''
                continue

            # The loop will iterate through the element with given css_selector and find the right ones with regex patterns
            for element in elements:
                if re.match(r"Utilizações", element.text) and USES_key == "uses_title":
                    text = element.text
                elif re.match(r"Indicações de Uso", element.text) and USES_key == "instructions_title":
                    text = element.text
                elif re.match(r"Precauções", element.text) and USES_key == "cautions_title":
                    text = element.text

        elif USES_key in ["uses", "instructions", "cautions"]:
            try:
                element: WebElement = wait_for_element(browser, By.CSS_SELECTOR, locator, TIMEOUT)
            except TimeoutException:
                log.warning(f"Timed out while waiting for element '{locator}' of '{USES_key}'")
                return USES
            
            # Uses could actually be a ul or a simple string
            if element.tag_name == "ul":
                lis = element.find_elements(By.XPATH, "./li")
                text = '\n'.join(li.text for li in lis)
            else:
                text = element.text
        
        else:
            raise SystemExit("Hit a never type")

        if not text:
            log.warning(f"Element '{USES_key}' was empty.")

        # Normalizing and assigning
        text = normalizer(text)
        uses[USES_key]["text"] = text

    log.info(f"Parsed product uses: {json.dumps(uses, indent=4)}")
    return uses


def parse_product(browser: WebDriver, count: int) -> bool:
    """
    Parse all product information and images from individual product page
    """
    log.info(f"Parsing product {count}: '{browser.current_url}'...")

    # Parsing product
    information_box: Information = parse_information(browser)
    benefits_box: Benefits = parse_benefits(browser)
    ingredients_box: Ingredients = parse_ingredients(browser)
    uses_box: Uses = parse_uses(browser)

    # Assemblying the Megazord
    product: Product = { 
        "information": information_box,
        "benefits": benefits_box,
        "ingredients": ingredients_box,
        "uses": uses_box
    }
    
    log.info(f"Normalizing product {count}: '{browser.current_url}'...")

    # TODO: improve this logic please its too ugly
    benefits = double_br_join(product["benefits"]["benefits_title"]["text"], product["benefits"]["benefits"]["text"])
    ingredients = double_br_join(product["ingredients"]["ingredients_title"]["text"], product["ingredients"]["ingredients"]["text"])
    uses_uses = double_br_join(product["uses"]["uses_title"]["text"], product["uses"]["uses"]["text"])
    uses_instructions = double_br_join(product["uses"]["instructions_title"]["text"], product["uses"]["instructions"]["text"])
    uses_cautions = double_br_join(product["uses"]["cautions_title"]["text"], product["uses"]["cautions"]["text"])

    normalized_product: NormalizedProduct = {
        "product_name": product["information"]["product_name"]["text"],
        "item_id": product["information"]["item_id"]["text"],
        "short_description": product["information"]["description"]["text"],
        "long_description": double_br_join(benefits, ingredients, uses_uses, uses_instructions, uses_cautions),
        "retail_price": product["information"]["retail_price"]["text"],
        "discount_price": product["information"]["discount_price"]["text"],
        "weight": product["information"]["dimensions"]["text"]
    }

    log.info(f"Normalized product: {json.dumps(normalized_product, indent=4)}")

    # # Validating Product dict
    # validate_dict(product)

    # Downloading images
    download_all_images(browser, normalized_product["product_name"])

    # Writing CSV
    write_csv(normalized_product)

    return True


def process_subcategory_page(browser: WebDriver, subcategory_address: str) -> bool:
    """
    Handle all the products present on products page / subcategory page
    """
    log.info(f"Processing products page '{subcategory_address}'...")
    
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
        time.sleep(MOUSE_SCROLL_DELAY)

        # Calculate new scroll height and compare with original scroll height
        new_scroll_height = browser.execute_script("return document.body.scrollHeight")
        if last_scroll_height == new_scroll_height:
            log.info(f"Found {len(products)} products on page '{subcategory_address}'.")
            break
        else:
            log.info(f"Scrolled {new_scroll_height - last_scroll_height} pixels down to last visible product.")
    
    # ============================== Clicking products ==============================
    # The backbone of the app
    for count, product in enumerate(products, start=1):
        product_name = product.accessible_name
        product_address = get_address([subcategory_address, product_name])
            
        if product_address not in PRODUCTS_BUFF:
            log.info(f"Clicking product {count}. '{product_address}'...")
            
            # try:
            # Getting to product page
            product.click()
            parse_product(browser, count)
            PRODUCTS_BUFF.append(product_address)
            log.info(f"Added value to PRODUCTS_BUFF: '{product_address}'")
            
            if product == products[-1]:
                # Calling handle_hover_menu to go to next subcategory page if product is indeed the last product of page
                log.info(f"Added value to PRODUCTS_BUFF: {json.dumps(PRODUCTS_BUFF, indent=4)}")
                handle_hover_menu(browser)
            else: 
                # Going back to subcategory page and applying recursion if product is not the last product of page
                browser.execute_script("window.history.go(-1)")
                process_subcategory_page(browser, subcategory_address)

            # except Exception:
            #     log.warning(f"Coudn't parse product '{product_address}' due to unexpected error: {traceback.format_exc}")
            #     log.info(f"Continuing to next product...")
            #     continue

    log.info(f"{len(PRODUCTS_BUFF)} products parsed.")
    log.info(f"PRODUCTS_BUFF: {json.dumps(PRODUCTS_BUFF, indent=4)}")

    return True


def handle_hover_menu(browser: WebDriver) -> bool:
    """
    Handles interaction with hover type menu to get the categories, then the subcategories, then click it 
    """
    log.info("Handling hover menu...")

    # ===================================== Hovering mouse over "comprar" button =====================================
    comprar_btn_xpath = '//*[@id="header"]/div[4]/div/div/div/div[2]/nav/ul/li[1]/a/span'
    hover_over(browser, comprar_btn_xpath)

    # ===================================== Hovering mouse over the categories =====================================
    categories_div_xpath = '//*[@id="header"]/div[4]/div/div/div/div[2]/nav/ul/li[1]/div/div/div/div/div/div[2]/div/ul'
    categories_div: WebElement = wait_for_element(browser, By.XPATH, categories_div_xpath)
    categories_lis: List[WebElement] = wait_for_all_elements(categories_div, By.XPATH, "./li") # "lis" stands for "List ItemS" 

    for category_li in categories_lis:
        # FIXME: For some reason code is breaking on category 'Difusores'
        try:
            category_name = category_li.text
        except StaleElementReferenceException:
            log.error("StaleElementReferenceException bug, shutting down the application...")
            return True

        if category_name in CONTEXT_CATEGORIES:
            # ===================================== Hovering mouse over all subcategories for given category =====================================
            hover_over(browser, category_li)
            subcategories_lis: list[WebElement] = category_li.find_elements(By.XPATH, "./ul/li")

            # If category has no subcategories click the category instead
            if not category_name in SUBCATEGORIES_BUFF:
                if not any(i.text for i in subcategories_lis):
                    category_li.click()
                    process_subcategory_page(browser, category_name)
                    SUBCATEGORIES_BUFF.append(category_name)
                    log.info(f"Added value to SUBCATEGORIES_BUFF: {json.dumps(SUBCATEGORIES_BUFF, indent=4)}")

                    # A little bit of recursion
                    handle_hover_menu(browser)
                    break
                
            for subcategory_li in subcategories_lis:
                subcategory_name = subcategory_li.text
                
                if subcategory_li.text:
                    subcategory_address = get_address([category_name, subcategory_name]) 
                
                    if not subcategory_address in SUBCATEGORIES_BUFF:
                        # Parsing the given product page
                        subcategory_li.click()
                        process_subcategory_page(browser, subcategory_address)
                        SUBCATEGORIES_BUFF.append(subcategory_address)
                        log.info(f"Added value to SUBCATEGORIES_BUFF: '{subcategory_address}'")

                        # A little bit of recursion
                        handle_hover_menu(browser)
    
    log.info(f"{len(SUBCATEGORIES_BUFF)} subcategories parsed.")
    log.info(f"SUBCATEGORIES_BUFF: {json.dumps(SUBCATEGORIES_BUFF, indent=4)}")

    return True


def main() -> bool:
    """
    Another main function
    """
    log.info("Starting the scraper...")
    constants = {
        "CONTEXT_CATEGORIES": CONTEXT_CATEGORIES,
        "TIMEOUT": TIMEOUT,
        "CLEAR_CSV_FLAG": CLEAR_CSV_FLAG,
        "GENERATED_CSV_FILE": GENERATED_CSV_FILE
    }
    log.info(f"Params: {json.dumps(constants, indent=4)}")

    try:
        driver_path = os.path.join(__location__, r"components\msedgedriver.exe")
        driver_options = [
            # "--user-data-dir=C:\\Users\\anewe\\AppData\\Local\\Microsoft\\Edge\\User Data",
            # "--headless",
            # "--inprivate",
            "--start-maximized",
            "--disable-extensions",
            "--remote-debugging-port=9222"
        ]
        browser = get_browser(driver_path, driver_options, TIMEOUT)
        
        # Starting the fun
        handle_hover_menu(browser)

        return True
    
    except Exception:
        log.critical(f"Unhandled error: \n{traceback.format_exc()}")
        sys.exit()
    finally:
        cmds = [
            "taskkill /im msedge.exe /t /f",
            "taskkill /im msedgedriver.exe /t /f",
            "taskkill /im microsoftwebdriver.exe /t /f",
            "taskkill /im msedgewebview2.exe /t /f"
        ]
            
        for cmd in cmds:
            logging.debug(f"Sending command: {cmd}")
            os.system(cmd)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    log = get_logger(logname)
    main()
