# -*- coding: utf-8 -*-
import os
import sys

from components.models import Information, Benefits, Ingredients, Uses, CSVHeader

INFORMATION: Information = {
    "product_name": {
        # "xpath": '//*[@id="ProductSpotlightSection"]/div[1]/div/div/div[1]/h3/span',
        "css_selector": ".spotlight__head-title",
        "text": ""
    },
    "description": {
        # "xpath": '//*[@id="ProductSpotlightSection"]/div[1]/div/div/div[1]/div[1]/p/span',
        "css_selector": ".spotlight__head-copy",
        "text": ""
    },
    "dimensions": {
        # "xpath": '//*[@id="ProductSpotlightSection"]/div[1]/div/div/div[3]/div/div[2]/div[1]/div/div[2]/span',
        "css_selector": ".loyalty-order__row .loyalty-order__row-item-data--bold",
        "text": ""
    },
    "item_id": {
        # "xpath": '//*[@id="ProductSpotlightSection"]/div[1]/div/div/div[3]/div/div[2]/div[2]/div/div[2]',
        "css_selector": ".loyalty-order__row .loyalty-order__row-item-data--bold",
        "text": ""
    },
    "retail_price": {
        # "xpath": '//*[@id="ProductSpotlightSection"]/div[1]/div/div/div[3]/div/div[3]/div[1]/div/div[2]',
        "css_selector": ".loyalty-order__row--wholesale .loyalty-order__row-item .loyalty-order__row-item-data",
        "text": ""
    },
    "discount_price": {
        # "xpath": '//*[@id="ProductSpotlightSection"]/div[1]/div/div/div[3]/div/div[3]/div[1]/div/div[2]',
        "css_selector": ".loyalty-order__row-item-data-wicon",
        "text": ""
    }
}

BENEFITS: Benefits = {
    "benefits_title": {
        # "xpath": '//*[@id="ProductSpotlightSection"]/div[3]/div[2]/div/div/h3/span',
        "css_selector": ".spotlight__foot-block-title",
        "css_selector_sec": ".product-whats-inside--alt .product-whats-inside__info-list-item-title",
        "text": ""
    },
    "benefits": {
        # "xpath": '//*[@id="ProductSpotlightSection"]/div[3]/div[2]/div/div/div/ul',
        "css_selector": 'ul.spotlight__list-custom.custom-list',
        "text": [""]
    }
}

INGREDIENTS: Ingredients = {
    "ingredients_title": {
        # "xpath": '//*[@id="WhatsInsideSection"]/div/div[2]/div/h3/span',
        "css_selector": ".product-whats-inside__footer-title",
        "css_selector_sec": ".product-whats-inside__title",
        "text": ""
    },
    "ingredients": {
        # "xpath": '//*[@id="WhatsInsideSection"]/div/div[2]/div/div/p/span',
        "css_selector": ".product-whats-inside__footer-content, .product-whats-inside__footer-content p",
        "text": ""
    }
}

USES: Uses = {
    "uses_title": {
        "css_selector": "h3.product-uses__block-title",
        "text": ""
    },
    "uses": {
        "css_selector": 'div.product-uses__block-list',
        "text": [""]
    },
    "instructions_title": {
        "css_selector": "h3.product-uses__block-title",
        "text": ""
    },
    "instructions": {
        "css_selector": "div.product-uses__directions-for-use-copy",
        "text": ""
    },
    "cautions_title": {
        "css_selector": "h3.product-uses__block-title",
        "text": ""
    },
    "cautions": {
        "css_selector": "div.product-uses__cautions-body",
        "text": ""
    }
}

CSVHEADER: CSVHeader = [
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
]