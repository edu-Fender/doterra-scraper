# -*- coding: latin-1 -*-
import re
import os
import csv
import time
import json
import logging
import traceback
import urllib.request

from typing import List, TypeVar, Union, Sequence

from selenium.webdriver.common.by import By
from selenium.webdriver.edge.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from components.models import Information, Benefits, Ingredients, Uses, Product, NormalizedProduct
from components.utils import accept_bloody_cookie, get_browser, get_logger, hover_over, join_strings, wait_for_element, wait_for_all_elements, kill_edge
from components.data import INFORMATION, BENEFITS, INGREDIENTS, UTILIZATION

# Most efective way to get current script location
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


# Buffers
SUBCATEGORIES_BUFF: List[str] = []
PRODUCTS_BUFF: List[str] = []

# Constants
TIMEOUT = 5
SCROLL_PAUSE_DELAY = 2.0
GENERATED_CSV_FILE = os.path.join(__location__, "generated", "Produtos doterra - Produtos.csv")
CONTEXT_CATEGORIES = ["Cuidado Pessoal", "MetaPWR™", "Suplementos"]


# Getting log object
log = get_logger(os.path.join(__location__, fr"logs\SCRAPER.log"))

def write_csv(normalized_product: NormalizedProduct):
    """
    Write CSV with product information
    """
    header: Union[Sequence[str], None]
    required_fields = [    
        "Nome",
        "DescriÃ§Ã£o",
        "PreÃ§o (imposto incluÃ­do)",
        "PreÃ§o de custo (atacado)",
        "ReferÃªncia"
    ]
    
    # Parsing CSV template file
    template_csv = os.path.join(__location__, "templates", "Produtos doterra - Produtos.csv")
    with open(template_csv, mode='r', encoding="latin-1") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        
        # Validating header
        if not header or any(i not in header for i in required_fields):
            logging.error(f"Couldn't parse header from CSV: {template_csv}.")
            raise SystemExit

        logging.info(f"Parsed header from CSV '{template_csv}': {json.dumps(header, indent=4)}")
    
    # Writing to new CSV file
    with open(GENERATED_CSV_FILE, mode='a+', encoding="latin-1") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerow({
            "Nome": normalized_product["product_name"],
            "ReferÃªncia": normalized_product["item_id"],
            "PreÃ§o (imposto incluÃ­do)": normalized_product["retail_price"],
            "PreÃ§o de custo (atacado)": normalized_product["discount_price"],
            "DescriÃ§Ã£o": normalized_product["description"]
        })
 
    return

def download_all_images(browser: WebDriver, product_name: str) -> List[str]:
    """
    Get and download all images from product webpage
    """
    logging.info(f"Downloading images for product {product_name}...")
    
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

        # Ignore image in case it ends with .svg
        if re.findall(r"\.svg\s*$", image_src):
            ignored_images.append(image_src)
            continue

        # Get string containing the text that comes after last slash of image_src
        try:
            regexed = re.findall(r"\/([^\/]*)$", image_src)[0]
        except IndexError:
            log.warning(f"Couldn't match regex pattern for {image_src}")
            continue

        image_name = os.path.join(product_images_dir, regexed)

        # Downloading image
        path, _ = urllib.request.urlretrieve(image_src, image_name)
        
        if not path:
            logging.warning(f"Image [{image_src}] couldn't be downloaded.")

        downloaded_images.append(path)    

    logging.info(f"Succesfully downloaded the images: {json.dumps(downloaded_images, indent=4)}")
    logging.info(f"Ingnored images: {json.dumps(ignored_images, indent=4)}")

    return downloaded_images



def normalize_product(product: Product) -> NormalizedProduct:
    """
    Normalize product and fields according to clients specifications of generated CSV
    """
    def normalizer(text: Union[str, List[str]], title: str = ''):
        """
        Join strs and lists of strs in single strings applying some regex also  
        """
        # Removing leading and trailing spaces/single-quotes/double-quotes of title
        exp = r"^([\s\'\"]*)|([\s\'\"]*)$"
        regexed = ""
        
        if title:
            regexed += re.sub(exp, r"", title)
            regexed += '\n'

        if isinstance(text, str):
            # Removing leading and trailing spaces/single-quotes/double-quotes of text
            regexed += re.sub(exp, r"", text)
        elif isinstance(text, list):
            # Joining all itens of list of strings on a single string
            regexed += ''.join('\n' + re.sub(exp, r"", i) for i in text)
        else:
            log.error("Hit a never type.")
            raise TypeError("Hit a never type.")

        return regexed

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

    log.info(f"Normalized product to: \n{json.dumps(normalized_product, indent=4)}")

    return normalized_product

def validate_product(product: Union[dict, Product]) -> bool:
    """
    Recursiverly going nested on dicts of dicts to validate no field is empty
    """
    for value in product.values():
        if isinstance(value, dict):
            validate_product(value)
        if not value:
            log.error(f"Product dictionary has empty fields.")
            raise ValueError
    
    return True

def parse_product_text(browser: WebDriver) -> Product:
    """
    Parse all product information and images from individual product page
    """
    # Cool Generics action
    T = TypeVar('T', Information, Benefits, Ingredients, Uses)

    def parser(browser: WebDriver, elements_box: T) -> T:
        """
        Help parsing the product page
        """
        logging.info(f"Entered the parser helper for...")

        for element_name in elements_box.keys():
            element_dict: dict = elements_box[element_name]
            element: WebElement = wait_for_element(browser, By.XPATH, element_dict["xpath"], TIMEOUT)

            if element.tag_name == "ul":
                lis = element.find_elements(By.XPATH, "./li")
                element_text_list = [li.text + '\n' for li in lis]
                elements_box[element_name]["text"] = element_text_list
            else:
                elements_box[element_name]["text"] = element.text
        
        logging.info(f"Parsed product: {json.dumps(elements_box, indent=4)}")

        return elements_box

    # Parsing information
    logging.info(f"Parsing information from product webpage: {browser.current_url}")
    
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

    # Recursiverly nested. Sounds cool huh?
    validate_product(product)

    return product

def process_product_page(browser: WebDriver) -> bool:
    """
    Process the product page
    """
    # Sorry, is it Python or C?
    try:
        # Parsing products
        parsed_product: Product = parse_product_text(browser)

        # Normalizing products
        normalized_product: NormalizedProduct = normalize_product(parsed_product)

        # Downloading images
        download_all_images(browser, normalized_product["product_name"])

        # Writing CSV
        write_csv(normalized_product)

        return True
    
    except SystemExit:
        raise SystemExit

def handle_subcategory_page(browser: WebDriver, subcategory_address: str) -> bool:
    """
    Handle all the products present on products page / subcategory page
    """
    logging.info(f"Processing products page '{subcategory_address}'...")
    products: List[WebElement]

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
            log.info(f"Found {len(products)} total products on the '{subcategory_address}' page.")
            break

        log.info(f"Scrolled {new_scroll_height - last_scroll_height} pixels down to last visible product.")

    # ============================== Clicking products ==============================
    # The most important loop you'll see today
    for product in products:
        product_name = product.text
        product_address = join_strings([subcategory_address, product_name])        

        if product_address not in PRODUCTS_BUFF:
            try:
                # Getting to product page
                product.click()
                process_product_page(browser)
                PRODUCTS_BUFF.append(product_address)
                log.info(f"PRODUCTS_BUFF: {json.dumps(PRODUCTS_BUFF, indent=4)}")

            except Exception:
                log.warning(f"Unhandled exception while trying to parse product '{product.text}': {traceback.format_exc}")
                log.warning(f"Continuing to next product...")
                continue

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

    # ===================================== Hovering mouse over the context categoriies =====================================
    categories_div_xpath = '//*[@id="header"]/div[4]/div/div/div/div[2]/nav/ul/li[1]/div/div/div/div/div/div[2]/div/ul'
    categories_div: WebElement = wait_for_element(browser, By.XPATH, categories_div_xpath)
    categories_lis: List[WebElement] = wait_for_all_elements(categories_div, By.XPATH, "./li") # "lis" stands for "List ItemS" 

    for category_li in categories_lis:
        category_name = category_li.text

        if category_name in CONTEXT_CATEGORIES:
            hover_over(browser, category_li, verbose=verbose)
            subcategories_lis: list[WebElement] = category_li.find_elements(By.XPATH, "./ul/li")

            for subcategory_li in subcategories_lis:
                subcategory_name = subcategory_li.text
                
                # ===================================== Hovering mouse over all the subcategories of given category =====================================
                if subcategory_li.text:
                    subcategory_address = join_strings([category_name, subcategory_name]) 
                
                    if not subcategory_address in SUBCATEGORIES_BUFF:
                        # Parsing the given product page
                        subcategory_li.click()
                        handle_subcategory_page(browser, subcategory_address)
                        SUBCATEGORIES_BUFF.append(subcategory_address)
                        log.info(f"Added value to SUBCATEGORIES_BUFF: {json.dumps(SUBCATEGORIES_BUFF, indent=4)}")

                        # A little bit of recursion
                        handle_hover_menu(browser)
    
    log.info(f"{SUBCATEGORIES_BUFF} subcategories parsed.")
    return True

@kill_edge
def main() -> bool:
    """
    Another main function
    """
    logging.info("Starting the scraper...")

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

        # Cleaning generated output csv file
        with open(GENERATED_CSV_FILE, "w"):
            pass
        
        # Starting the fun
        handle_hover_menu(browser)

        return True
    
    except SystemExit:
        log.info("Finishing application...")
        raise SystemExit
    except Exception:
        logging.critical(f"Unhandled error: {traceback.format_exc()}")
        raise SystemExit


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
