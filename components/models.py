import os

from typing import Union, TypedDict, Annotated

class Product(TypedDict):
    name: str
    reference_id: str
    retail_price: float
    discount_price: float
    short_description: str
    description: Annotated[str, 'Os principais benefícios, ingredientes, utilização, indicações de uso e precauções pode colocar tudo no mesmo campo de "descrição"']
    images: Union[str, os.PathLike]
