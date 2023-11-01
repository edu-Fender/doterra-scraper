import re
import os
import time
import json
import urllib.request
import traceback

from typing import Dict
from datetime import datetime


import selenium

from selenium import webdriver  # selenium 4.8.3
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC

trace = True

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def log(*args, console=True) -> None:
    """
    Print message to logfile.txt and console depending on input
    """
    global trace

    args = str(*args)
    if args:
        if console:
            print(args)
        if trace:
            with open("logfile.txt", 'a') as f:
                now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(f"{now} {args}\n")

    return


def format_text(text: str):
    """
    Limpando textos que vem de elements HTML
    """
    # Removendo qubras de linhas e tabs
    text = re.sub(r"\n|\t", "", text)

    # Removendo espaços caso venham no começo ou final da string
    text = re.sub(r"^\s+|\s+$", "", text)

    return text


def get_value_from_label(browser: webdriver, xpath: str) -> str:
    """
    Função helper para facilitar o acesso aos valores dos elementos HTML tipo label
    """
    element = browser.find_element(
        By.XPATH,
        xpath
    )
    text = element.get_attribute("textContent")
    text = format_text(text)

    return format_text(text)


def get_value_from_textbox(browser: webdriver, xpath: str) -> str:
    """
    Função helper para facilitar o acesso aos valores dos elementos HTML tipo textbox
    """
    element = browser.find_element(
        By.XPATH,
        xpath
    )

    text = element.get_attribute("value")
    text = format_text(text)

    return text

def download_image(browser: webdriver, xpath: str, product_name: str) -> str:
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

def validate_product(product: dict) -> bool:
    """
    Validando product
    """
    error_flag = False

    # Para cada par chave-valor no dicionario product
    for key, value in product.items():
        # Se valor da chave é um dicionario
        if type(product[key]) is dict:
            # Checando cada valor no dicionario
            for inner_value in product[key].values():
                if not inner_value:
                    error_flag = True

        # Se valor da chave é uma string
        else:
            if not value:
                error_flag = True

    if error_flag:
        log("Product contem campos mandatórios vazios.")
        log(json.dumps(product, indent=4))
        return False

    return True

def parse_product(browser: webdriver) -> dict:
    """
    Parsea product
    """
    product_div_xpath =         "/html/body/div[1]/div[1]/div/div/section[2]/div"
    product_image_xpath =       "/html/body/div[1]/div[1]/div/div/section[2]/div/div[2]/div[1]/img"
    product_name_xpath =        "/html/body/div[1]/div[1]/div/div/section[2]/div/div[2]/div[2]/div[1]/h2"
    product_description_xpath = "/html/body/div[1]/div[1]/div/div/section[2]/div/div[2]/div[2]/div[1]/div/p"

    product_price_div_xpath =       "/html/body/div[1]/div[1]/div/div/section[2]/div/div[2]/div[2]/div[4]"
    product_retail_price_xpath =    "/html/body/div[1]/div[1]/div/div/section[2]/div/div[2]/div[2]/div[4]/div[1]/div/span"
    product_wholesale_price_xpath = "/html/body/div[1]/div[1]/div/div/section[2]/div/div[2]/div[2]/div[4]/div[2]/div/span"

    product: Dict[str, str] = {
        "name": "",
        "description": "",
        "image": "",
        "price": {
            "retail": "",
            "wholesale": ""
        }
    }


    # Recuperando o nome do produto
    product["name"] = get_value_from_label(browser, product_name_xpath)

    # Baixando imagem do produto
    product["image"] = download_image(browser, product_image_xpath, product["name"])

    # Recuperando descrição do produto
    product["description"] = get_value_from_label(browser, product_description_xpath)

    # Recuperando preço do produto
    product["price"]["retail"] = get_value_from_label(browser, product_retail_price_xpath)

    # Recuperando preço do produto
    product["price"]["wholesale"] = get_value_from_label(browser, product_wholesale_price_xpath)

    # Validando product
    if not validate_product(product):
        return False

    log(f"Parse da product bem sucedido. Product: {json.dumps(product, indent=4)}")
    return product

def get_products(product_first_pos, total_products):
    products = {}
    product_index = 1

    try:
        edge_options = Options()
        # edge_options.add_argument("--headless")
        edge_options.add_argument("--start-maximized")
        edge_options.add_argument("--remote-debugging-port=9222")
        edge_options.add_argument("--disable-extensions")
        # Ao indicar esse parametro, o driver será capaz de recuperar os cookies e seções abertas no navegador
        # edge_options.add_argument("user-data-dir=C:\\Users\\anewe\\AppData\\Local\\Microsoft\\Edge\\User Data")

        log("Inicializando instancia...")
        service = Service(os.path.join(__location__, "msedgedriver.exe"))
        browser = webdriver.Edge(service=service, options=edge_options)
        browser.implicitly_wait(30)  # Timeout

        url = "https://www.doterra.com/US/en/pl/most-popular-oils"
        browser.get(url)

        # Clicando nas products
        for product_pos in range(product_first_pos, total_products):

            # Localizando image product
            product_image_xpath = f"/html/body/div[1]/div[1]/div/div[2]/div/div[2]/div[2]/div[{product_pos}]/div/a"
            product_description_xpath = "/html/body/div[1]/div[1]/div/div/section[2]/div/div[2]/div[2]/div[1]/div/p"

            # Clicando na imagem dp produto
            product_button = WebDriverWait(browser, 5).until(
                EC.presence_of_element_located((
                    By.XPATH, product_image_xpath)))

            log(f"Clincando no produto: {product_index}")
            product_button.click()

            # Garantindo que a janela da product ja foi aberta
            WebDriverWait(browser, 5).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    product_description_xpath
                )))

            log(f"Produto {product_index} aberto com sucesso. Colhendo descrição do produto...")

            # Iniciando o parse da product
            product = parse_product(browser)
            if not product:
                return False

            # Adicionando product ao dicionário de products
            new_key = product["team_a"] + '|' + product["team_b"]
            products[new_key] = product

            # Fechando janela da product
            close_button_xpath = "/html/body/app/div[1]/div/div[1]/div/div/div[2]/div/div[3]/button"
            browser.find_element(By.XPATH, close_button_xpath).click()

            product_pos += 1
            product_index += 1
            time.sleep(2)

        # with open("logfile.txt", 'w') as f:
        #     s = json.dumps(products, indent=4)
        #     f.write(s)

        browser.quit()

        return True

    except ZeroDivisionError:
        pass
    except Exception:
        log(f"Erro inesperado ao processar product {product_index}. Verificar logfile.txt para mais informações.")
        log(traceback.format_exc(), console=False)
        return False
    finally:
        log("Terminando script...")
        # Terminando os processos do Edge a cada execução do código.
        # Isso é necessário pois se quando o Edge for aberto pelo Seleniumm haja algum processo Edge vivo, o Selenium não funciona corretamente
        cmd = 'taskkill /im msedge.exe /t /f'
        log(f"Enviando comando: {cmd}")
        os.system(cmd)


def main():
    # Cleaning logfile.txt
    with open("logfile.txt", 'w'):
        pass

    # Pode mudar constantemente
    product_first_pos = 1
    total_product = 100

    products = get_products(product_first_pos, total_product)
    if not products:
        return False


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
