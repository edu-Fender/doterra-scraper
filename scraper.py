import re
import os
import time
import json
import urllib.request
import traceback

from typing import Dict, List
from datetime import datetime


import selenium

from selenium import webdriver  # selenium 4.8.3
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException
from components.utils import log

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

processed_subcategories = []
context_categories = ["Cuidado Pessoal", "MetaPWR™", "Suplementos"]
# expected = ["Ofertas Sazonais"]


def download_image(browser: WebDriver, xpath: str, product_name: str) -> str:
    """
    Função helper para facilitar o download de imagens
    """
    element = browser.find_element(
        By.XPATH,
        xpath
    )

    img_src = element.get_attribute("src")
    path, _ = urllib.request.urlretrieve(img_src, os.path.join(os.path.join(__location__, "images"),  product_name + ".png"))

    return path

def hover_over(browser: WebDriver, xpath: str) -> None:
    """
    Hover over HTML element
    """
    # comprar_btn_xpath = '//*[@id="offcanvas-menu"]/div[4]/div/div/ul/li[1]/a' # That is when btn in inside burguer menu
    element: WebElement = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((
            By.XPATH, xpath)))

    log(f'Passando o mouse no botão: [{element.text}]')
    hover = ActionChains(browser).move_to_element(element)
    hover.perform()
 

def handle_hover_menu(browser: WebDriver):
    """
    Handles interaction with hover type menu to get the categories, then the subcategories, then the products
    """

    try:
        # ===================================== Aceitando a merda do cookie =====================================
        accept_cookie_btn_xpath = '//*[@id="truste-consent-button"]'
        try:
            if not processed_subcategories:
                WebDriverWait(browser, 1).until(
                    EC.presence_of_element_located((
                        By.XPATH, accept_cookie_btn_xpath))).click()
        except TimeoutException:
            pass

        # ===================================== Passando o mouse no botão "comprar" =====================================
        comprar_btn_xpath = '//*[@id="header"]/div[4]/div/div/div/div[2]/nav/ul/li[1]/a/span'
        hover_over(browser, comprar_btn_xpath)

        # ===================================== Passando o mouse nas diferentes categorias =====================================
        categories_div_xpath = '//*[@id="header"]/div[4]/div/div/div/div[2]/nav/ul/li[1]/div/div/div/div/div/div[2]/div/ul'
        categories_div: WebElement = browser.find_element(By.XPATH, categories_div_xpath)

        categories_lis: List[WebElement] = categories_div.find_elements(By.XPATH, "./li")

        for category_li in categories_lis:
            if category_li.text in context_categories:
                log(f'Passando o mouse no botão {category_li.text}')
                hover = ActionChains(browser).move_to_element(category_li)
                hover.perform()

                subcategories_ul_xpath = '//*[@id="header"]/div[4]/div/div/div/div[2]/nav/ul/li[1]/div/div/div/div/div/div[2]/div/ul/li[3]/ul'
                subcategories_lis: list[WebElement] = category_li.find_elements(By.XPATH, "./ul/li")

                for subcategory_li in subcategories_lis:
                    if subcategory_li.text:
                        subcategory_full_name = category_li.text + "." + subcategory_li.text
                        if not subcategory_full_name in processed_subcategories:
                            processed_subcategories.append(subcategory_full_name)
                            subcategory_li.click()
                            # chama a funcao pra parsear os produtos na pagina

                            # Aplicando recursao
                            handle_hover_menu(browser)
                    else:
                        # Se o li nao tem texto, e porque esta vazio
                        continue

        browser.quit()

        return True

    except ZeroDivisionError:
        pass

def get_browser() -> WebDriver:
    """
    Will get then return the Selenium driver
    """
    edge_options = Options()
    # edge_options.add_argument("--headless")
    # edge_options.add_argument("--inprivate")
    edge_options.add_argument("--start-maximized")
    edge_options.add_argument("--disable-extensions")
    edge_options.add_argument("--remote-debugging-port=9222")
    
    # Ao indicar esse parametro, o driver será capaz de recuperar os cookies e seções abertas no navegador
    # edge_options.add_argument("user-data-dir=C:\\Users\\anewe\\AppData\\Local\\Microsoft\\Edge\\User Data")

    service = Service(os.path.join(__location__, "components/msedgedriver.exe"))
    browser = webdriver.Edge(service=service, options=edge_options)

    return browser
    
def main():
    """
    Another main function
    """
    try:
        # Cleaning logfile.txt
        with open("logfile.txt", 'w'):
            pass
        
        log("Inicializando instancia...")
        browser = get_browser()
        browser.implicitly_wait(30)  # Timeout

        # OBS: necessário entrar no VPN de portugal porque o Edge redireciona pro site BR que é diferente
        url = "https://shop.doterra.com/PT/pt_PT/shop/home/"
        browser.get(url)
        handle_hover_menu(browser)

        return True
    
    except ZeroDivisionError:
        pass
    except Exception:
        log(f"Erro inesperado: {traceback.format_exc()}")
        return False
    finally:
        log("Terminando script...")
        # Terminando os processos do Edge a cada execução do código.
        # Isso é necessário pois se quando o Edge for aberto pelo Seleniumm haja algum processo Edge vivo, o Selenium não funciona corretamente
        cmd = 'taskkill /im msedge.exe /t /f'
        log(f"Enviando comando: {cmd}")
        os.system(cmd)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
