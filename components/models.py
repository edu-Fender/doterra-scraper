import os
from tkinter import X

from typing import List, Dict, Union, TypedDict, Annotated
from typing_extensions import NotRequired


############################## Base Classes ##############################
class HTMLElement(TypedDict):
    type: str
    text: str
    
class HTMLElementFromClassName(HTMLElement):
    class_name: str

class HTMLElementFromFieldName(HTMLElement):
    field_name: str

class HTMLElementFromXpath(HTMLElement):
    xpath: str

# Type alias
HTMLElement = Union[HTMLElementFromXpath, HTMLElementFromClassName, HTMLElementFromFieldName]

############################## Actual Clases ##############################
class Information(TypedDict):
    product_name: HTMLElement
    description: HTMLElement
    dimensions: HTMLElement
    item_id: HTMLElement
    retail_price: HTMLElement
    discount_price: HTMLElement
    images: List[HTMLElement]

class Benefits(TypedDict):
    benefits_title: HTMLElement
    benefits: HTMLElement

class Ingredients(TypedDict):
    ingredients_title: HTMLElement
    ingredients: HTMLElement

class Uses(TypedDict):
    uses_title: HTMLElement
    uses: HTMLElement
    instructions_title: HTMLElement
    instructions: HTMLElement
    cautions_title: HTMLElement
    cautions: HTMLElement

# The Megazord
class Product(TypedDict):
    information: Information
    benefits: Benefits
    ingredients: Ingredients
    uses: Uses