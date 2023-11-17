import os

from typing import Any, List, NamedTuple, Optional, Sequence, Tuple, Dict, Literal, TypeVar, Union, TypedDict, Annotated
from typing_extensions import NotRequired


############################## Product Base Classes ##############################
class HTMLElement(TypedDict):
    css_selector: str
    css_selector_sec: NotRequired[str]
    text: Union[str, List[str]]

############################## Product Actual Clases ##############################
class Information(TypedDict):
    product_name: HTMLElement
    description: HTMLElement
    dimensions: HTMLElement
    item_id: HTMLElement
    retail_price: HTMLElement
    discount_price: HTMLElement

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

############################## Others ##############################
class NormalizedProduct(TypedDict):
    product_name: str
    item_id: str 
    retail_price: str
    discount_price: str
    description: str

CSVHeader = List[Literal[
    "ID do produto",
    "ReferÃªncia",
    "Ativo (0 = NÃ£o, 1 = Sim)",
    "Nome",
    "EAN13",
    "UPC",
    "ISBN",
    "MPN",
    "Visibilidade",
    "DoenÃ§a",
    "Mostrar condiÃ§Ã£o (0 = NÃ£o, 1 = Sim)",
    "Pacote (0 = NÃ£o, 1 = Sim)",
    "Resumo",
    "DescriÃ§Ã£o",
    "Marcas (x,y,z...)",
    "DisponÃ­vel para pedido (0 = NÃ£o, 1 = Sim)",
    "Data de disponibilidade",
    "Mostrar preÃ§o (0 = NÃ£o, 1 = Sim)",
    "Data de criaÃ§Ã£o",
    "DisponÃ­vel apenas online (0 = NÃ£o, 1 = Sim)",
    "Ã‰ Produto Virtual (0 = NÃ£o, 1 = Sim)",
    "URL do arquivo virtual",
    "Nome exibido do arquivo virtual",
    "NÃºmero de downloads permitidos",
    "Data de expiraÃ§Ã£o do download",
    "NÃºmero de dias acessÃ­veis",
    "Tipo de quantidade do pacote",
    "PreÃ§o (excluindo impostos)",
    "PreÃ§o (imposto incluÃ­do)",
    "PreÃ§o de custo (atacado)",
    "Emblema de Venda (0 = NÃ£o, 1 = Sim)",
    "GestÃ£o de Prioridades",
    "Nome da regra fiscal",
    "Ecotaxa",
    "Unidade",
    "Unit Price",
    "MetatÃ­tulo",
    "Meta-palavras-chave",
    "Meta DescriÃ§Ã£o",
    "URL reescrito",
    "Tipo de redirecionamento",
    "ID de redirecionamento de destino",
    "Nome de redirecionamento de destino",
    "ID de categoria padrÃ£o",
    "Nome da categoria padrÃ£o",
    "IDs de categoria (x,y,z...)",
    "Nomes de categoria (x,y,z...)",
    "Marca",
    "IDs de produtos relacionados (x,y,z...)",
    "Nomes de produtos relacionados (x,y,z...)",
    "Nomes de produtos no pacote (x,y,z...)",
    "Quantidades do produto no pacote (x,y,z...)",
    "Nomes das operadoras (x,y,z...)",
    "Largura",
    "Altura",
    "Profundidade",
    "Peso",
    "Prazo de entrega de produtos em estoque",
    "Prazo de entrega de produtos fora de estoque",
    "Taxas de envio adicionais",
    "Prazo de entrega",
    "Quantidade vendida",
    "NÃºmero de vendas",
    "Quantidade",
    "Quantidade mÃ­nima",
    "LocalizaÃ§Ã£o",
    "Baixo nÃ­vel de estoque",
    "Alerta de estoque baixo (0 = NÃ£o, 1 = Sim)",
    "Etiqueta Quando em Estoque",
    "Etiqueta quando o pedido em espera Ã© permitido",
    "AÃ§Ã£o quando fora de estoque",
    "ArmazÃ©ns (ReferÃªncia:Nome:LocalizaÃ§Ã£o) (x,y,z...)",
    "Desconto de quantidade (0 = NÃ£o, 1 = Sim)",
    "URL da imagem de capa",
    "URLs de imagem (x,y,z...)",
    "Textos alternativos da imagem (x,y,z...)",
    "Features (Name~Value~Custom) (x,y,z...)",
    "Ã‰ personalizÃ¡vel (0 = NÃ£o, 1 = Sim)",
    "Campos de personalizaÃ§Ã£o (RÃ³tulo:Tipo:ObrigatÃ³rio) (x,y,z...)",
    "Arquivos carregÃ¡veis (0 = NÃ£o, 1 = Sim)",
    "Campos de texto (0 = NÃ£o, 1 = Sim)",
    "Tem Anexos (0 = NÃ£o, 1 = Sim)",
    "URLs de anexos (x,y,z...)",
    "Nomes de anexos (x,y,z...)",
    "DescriÃ§Ãµes de anexos (x,y,z...)",
    "Nome do fornecedor padrÃ£o",
    "ReferÃªncia de fornecedor padrÃ£o",
    "Nomes de Fornecedores (x,y,z...)",
    "ReferÃªncias de Fornecedores (x,y,z...)",
    "PreÃ§os do Fornecedor (x,y,z...)",
    "CÃ³digos ISO da moeda do fornecedor (x,y,z...)"
]]

CSVRequiredFields = TypedDict('CSVRequiredFields', {
    "ID do produto": str,
    "Nome": str,
    "DescriÃ§Ã£o": str,
    "PreÃ§o (imposto incluÃ­do)": str,
    "PreÃ§o de custo (atacado)": str
})