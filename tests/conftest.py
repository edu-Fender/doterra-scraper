import os
import sys

import pytest

from typing import List, TypeVar

from selenium.webdriver.edge.webdriver import WebDriver

from scraper import accept_bloody_cookie
from components.utils import get_browser
from components.models import NormalizedProduct, Product

# Get parent directory location
__parentpath__ = os.path.realpath(os.path.abspath('.'))


def validate_nested_dicts(_dict):
    """
    Recursiverly going nested on dicts of dicts to validate no field is empty
    """
    for value in _dict.values():
        if isinstance(value, dict):
            validate_nested_dicts(value)
        if not value:
            return False
    return True
        
@pytest.fixture()
def browser() -> WebDriver:
    """
    Get the Selenium WebDriver object
    """
    
    driver_path = os.path.join(__parentpath__, r"components\msedgedriver.exe")
    driver_options = [
        # "--user-data-dir=C:\\Users\\anewe\\AppData\\Local\\Microsoft\\Edge\\User Data",
        # "--headless",
        "--inprivate",
        "--start-maximized",
        "--disable-extensions",
        "--remote-debugging-port=9222"
    ]

    timeout = 10
    browser = get_browser(driver_path, driver_options, timeout)
    browser.get("https://shop.doterra.com/PT/pt_PT")
    browser = accept_bloody_cookie(browser)

    return browser

# T  = TypeVar("T", bound=List[Product]) 
T = List[Product]

@pytest.fixture()
def products() -> T:
    """
    Mocked Product type dictionaries
    """
    products: T = [{
        "information": {
            "product_name": {
                "xpath": "//*[@id=\"ProductSpotlightSection\"]/div[1]/div/div/div[1]/h3/span",
                "text": "'Pomada Essencial Correct-X\u2122'"
            },
            "description": {
                "xpath": "//*[@id=\"ProductSpotlightSection\"]/div[1]/div/div/div[1]/div[1]/p/span",
                "text": "'A pomada Correct-X \u00e9 uma pomada natural e polivalente que ajuda a acalmar e manter a pele limpa enquanto recupera de um desconforto. A pomada Correct-X cria uma barreira de hidrata\u00e7\u00e3o para ajudar a proteger a pele enquanto os \u00f3leos essenciais de Frankincense, Helicriso (Perp\u00e9tua das Areias), \u00c1rvore do Ch\u00e1, Cedro e Lavanda acalmam e purificam. Esta pomada sem petr\u00f3leo nem conservantes \u00e9 rapidamente absorvida e \u00e9 suave e n\u00e3o irritante, sendo ideal para peles sens\u00edveis.'"
            },
            "dimensions": {
                "xpath": "//*[@id=\"ProductSpotlightSection\"]/div[1]/div/div/div[3]/div/div[2]/div[1]/div/div[2]/span",
                "text": "'15 ml'"
            },
            "item_id": {
                "xpath": "//*[@id=\"ProductSpotlightSection\"]/div[1]/div/div/div[3]/div/div[2]/div[2]/div/div[2]",
                "text": "'60213438'"
            },
            "retail_price": {
                "xpath": "//*[@id=\"ProductSpotlightSection\"]/div[1]/div/div/div[3]/div/div[3]/div[1]/div/div[2]",
                "text": "'\u20ac20.67'"
            },
            "discount_price": {
                "xpath": "//*[@id=\"ProductSpotlightSection\"]/div[1]/div/div/div[3]/div/div[3]/div[1]/div/div[2]",
                "text": "'\u20ac20.67'"
            }
        },
        "benefits": {
            "benefits_title": {
                "xpath": "//*[@id=\"ProductSpotlightSection\"]/div[3]/div[2]/div/div/h3/span",
                "text": "'Principais Benef\u00edcios'"
            },
            "benefits": {
                "xpath": "//*[@id=\"ProductSpotlightSection\"]/div[3]/div[2]/div/div/div/ul",
                "text": [
                    "'O Frankincense, o Helicriso (Perp\u00e9tua das Areias), a \u00c1rvore do Ch\u00e1, o Cedro e a Lavanda podem acalmar e purificar a pele'\n",
                    "'O Bisabolol \u00e9 conhecido pelos seus efeitos calmantes e pela sua capacidade de promover uma pele de aspeto saud\u00e1vel'\n",
                    "'\u00c0 semelhan\u00e7a dos \u00f3leos naturais presentes na pele, a Jojoba promove uma hidrata\u00e7\u00e3o ideal, ajudando a melhorar a textura da pele'\n",
                    "'O extrato de Casca de Phellodendron Amurense \u00e9 utilizado para hidratar a pele'\n"
                ]
            }
        },
        "ingredients": {
            "ingredients_title": {
                "xpath": "//*[@id=\"WhatsInsideSection\"]/div/div[2]/div/h3/span",
                "text": "'Lista completa de ingredientes'"
            },
            "ingredients": {
                "xpath": "//*[@id=\"WhatsInsideSection\"]/div/div[2]/div/div/p/span",
                "text": "'Extrato de Cevada (Hordeum distichon), Extrato de S\u00e2ndalo (Santalum album), Extrato de Casca de Phellodendron Amurense, Estearato de Glicerol, Acacia Decurrens/Jojoba/Cera de Semente de Girassol/Poligliceril-3 \u00c9steres, Capr\u00edlico/Triglic\u00e9rido Capr\u00edlico, Miristato de Glicerol, Palmitato de Glicerol, Ricinoleato de Glicerol, \u00d3leo de Madeira de Cedro (Juniperus virginiana), \u00d3leo de Lavanda (Lavandula angustifolia), \u00d3leo de Folha de \u00c1rvore do Ch\u00e1 (Melaleuca alternifolia), Extrato de Physalis Angulata, \u00d3leo de Semente de Noz Inca (Plukenetia volubilis), \u00d3leo de Frankincense (Boswellia Carterii), \u00d3leo de Flor de Helicriso (Perp\u00e9tua das Areias) (Helichrysum italicum), \u00d3leo de Fruto de Rosa Canina, Extrato de Raiz de Gengibre (Zingiber officinale), \u00d3leo de Palmeira (Elaeis Guineensis), \u00d3leo de Semente de Algod\u00e3o (Gossypium Herbaceum), Extrato de Bidens Pilosa, Bisabolol, \u00d3leo de Semente Linha\u00e7a (Linum Usitatissimum), \u00c1cido Linoleico, Fosfol\u00edpidos, Eicosanedioato de Glicerol, Ester\u00f3is de Soja (Glycine Soja), Palmitato de Dextrina, Glicirrizinato de Estearilo'"
            }
        },
        "uses": {
            "uses_title": {
                "xpath": "//*[@id=\"ProductUsesSection\"]/div[1]/div/div[2]/h3[1]/span",
                "text": "'Utiliza\u00e7\u00f5es'"
            },
            "uses": {
                "xpath": "//*[@id=\"ProductUsesSection\"]/div[1]/div/div[2]/div[1]/ul",
                "text": [
                    "'Integre a Pomada Essencial Correct-X na sua rotina de beleza matinal e noturna'\n",
                    "'Aplique na pele seca para limpar, purificar e hidratar a pele com as suas propriedades calmantes'\n",
                    "'Utilize a f\u00f3rmula da pomada Correct-X nas zonas afetadas para proporcionar al\u00edvio \u00e0 pele quando ocorrem irrita\u00e7\u00f5es'\n",
                    "'Mantenha um frasco da pomada \u00e0 m\u00e3o, na mala de viagem, para uma utiliza\u00e7\u00e3o f\u00e1cil e pr\u00e1tica'\n"
                ]
            },
            "instructions_title": {
                "xpath": "//*[@id=\"ProductUsesSection\"]/div[1]/div/div[2]/h3[2]/span",
                "text": "'Indica\u00e7\u00f5es de Uso'"
            },
            "instructions": {
                "xpath": "//*[@id=\"ProductUsesSection\"]/div[1]/div/div[2]/div[2]/div/div[2]/span",
                "text": "'Aplique nas zonas afetadas conforme necess\u00e1rio.'"
            },
            "cautions_title": {
                "xpath": "//*[@id=\"ProductUsesSection\"]/div[1]/div/div[2]/div[3]/h3/span",
                "text": "'Precau\u00e7\u00f5es'"
            },
            "cautions": {
                "xpath": "//*[@id=\"ProductUsesSection\"]/div[1]/div/div[2]/div[3]/div/p/span",
                "text": "'Apenas para utiliza\u00e7\u00e3o externa. Evite o contacto direto com os olhos. Em caso de irrita\u00e7\u00e3o, interrompa a utiliza\u00e7\u00e3o.'"
            }
        }
    }]

    return products

# T  = TypeVar("T", bound=List[Product]) 
T = List[NormalizedProduct]

@pytest.fixture()
def normalized_products() -> T:
    normalized_products: T = {}
    return normalized_products