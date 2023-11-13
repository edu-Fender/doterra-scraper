import os
from tkinter import X

from typing import Any, List, NamedTuple, Optional, Sequence, Tuple, Dict, Literal, TypeVar, Union, TypedDict, Annotated
from typing_extensions import NotRequired
from dataclasses import dataclass

############################## Product Base Classes ##############################
class HTMLElement(TypedDict):
    xpath: str
    
class HTMLNormalElement(HTMLElement):
    text: str

class HTMLBulletedElement(HTMLElement):
    text: List[str]

############################## Product Actual Clases ##############################
class Information(TypedDict):
    product_name: HTMLNormalElement
    description: HTMLNormalElement
    dimensions: HTMLNormalElement
    item_id: HTMLNormalElement
    retail_price: HTMLNormalElement
    discount_price: HTMLNormalElement

class Benefits(TypedDict):
    benefits_title: HTMLNormalElement
    benefits: HTMLBulletedElement

class Ingredients(TypedDict):
    ingredients_title: HTMLNormalElement
    ingredients: HTMLNormalElement

class Uses(TypedDict):
    uses_title: HTMLNormalElement
    uses: HTMLBulletedElement
    instructions_title: HTMLNormalElement
    instructions: HTMLNormalElement
    cautions_title: HTMLNormalElement
    cautions: HTMLNormalElement
    
# The Megazord
class Product(TypedDict):
    information: Information
    benefits: Benefits
    ingredients: Ingredients
    uses: Uses

############################## Others ##############################
class NormalizedProduct(TypedDict):
    product_name: str
    item_id: str 
    retail_price: str
    discount_price: str
    description: str