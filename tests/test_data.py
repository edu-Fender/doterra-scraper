# -*- coding: utf-8 -*-
from components.models import NormalizedProduct, Product

PRODUCTS_URLS = [
    "https://shop.doterra.com/PT/pt_PT/shop/daily-nutrient-pack/",
    "https://shop.doterra.com/PT/pt_PT/shop/hydrating-cream/",
    "https://shop.doterra.com/PT/pt_PT/shop/doterra-sun-face-body-mineral-sunscreen-lotion/",
    "https://shop.doterra.com/PT/pt_PT/shop/moisturising-bath-bar/",
    "https://shop.doterra.com/PT/pt_PT/shop/doterra-hd-clear-foaming-face-wash/"
    "https://shop.doterra.com/PT/pt_PT/shop/doterra-daily-conditioner/",
    "https://shop.doterra.com/PT/pt_PT/shop/verage-skin-care-collection/",
    "https://shop.doterra.com/PT/pt_PT/shop/deep-blue-rub-samples/",
    "https://shop.doterra.com/PT/pt_PT/shop/metapwr-beadlets/",
    "https://shop.doterra.com/PT/pt_PT/shop/alpha-crs-plus/",
    "https://shop.doterra.com/PT/pt_PT/shop/deep-blue-polyphenol-complex/",
    "https://shop.doterra.com/PT/pt_PT/shop/phytoestrogen-essential-complex/",
    "https://shop.doterra.com/PT/pt_PT/shop/zengest-softgels/",
    "https://shop.doterra.com/PT/pt_PT/shop/metapwr-beadlets/"
]


VALID_PRODUCT: Product = { 
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
}

VALID_FORMAT_EMPTY_FIELDS_PRODUCT: Product = {
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
            "text":  "" # Empty
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
}

INVALID_FORMAT_PRODUCT: Product = {
    "bvbb'": { # type: ignore
        "product_name": {
            "xpath": "//*[@id=\"ProductSpotlightSection\"]/div[1]/div/div/div[1]/h3/span",
            "text": "'Pomada Essencial Correct-X\u2122'"
        },
        "description": {
            "xpath": "//*[@id=\"ProductSpotlightSection\"]/div[1]/div/div/div[1]/div[1]/p/span",
            "text": "'A pomada Correct-X \u00e9 uma pomada natural e polivalente que ajuda a acalmar e manter a pele limpa enquanto recupera de um desconforto. A pomada Correct-X cria uma barreira de hidrata\u00e7\u00e3o para ajudar a proteger a pele enquanto os \u00f3leos essenciais de Frankincense, Helicriso (Perp\u00e9tua das Areias), \u00c1rvore do Ch\u00e1, Cedro e Lavanda acalmam e purificam. Esta pomada sem petr\u00f3leo nem conservantes \u00e9 rapidamente absorvida e \u00e9 suave e n\u00e3o irritante, sendo ideal para peles sens\u00edveis.'"
        },
        "liklnlk": {
            "xpath": "//*[@id=\"ProductSpotlightSection\"]/div[1]/div/div/div[3]/div/div[2]/div[1]/div/div[2]/span",
            "text": "'15 ml'"
        },
        "item_id": {
            "xpath": "//*[@id=\"ProductSpotlightSection\"]/div[1]/div/div/div[3]/div/div[2]/div[2]/div/div[2]",
            "text": "'60213438'"
        },
        "jhjh": {
            "xpath": "//*[@id=\"ProductSpotlightSection\"]/div[1]/div/div/div[3]/div/div[3]/div[1]/div/div[2]",
            "text": "'\u20ac20.67'"
        },
        "discount_kjjbbkprice": {
            "xpath": "//*[@id=\"ProductSpotlightSection\"]/div[1]/div/div/div[3]/div/div[3]/div[1]/div/div[2]",
            "text": "'\u20ac20.67'"
        }
    }
} 

VALID_NORMALIZED_PRODUCT: NormalizedProduct = {
    "product_name": "Pomada Essencial Correct-X\u2122",
    "item_id": "60213438",
    "retail_price": "\u20ac20.67",
    "discount_price": "\u20ac20.67",
    "description": "Principais Benef\u00edcios\\rO Frankincense, o Helicriso (Perp\u00e9tua das Areias), a \u00c1rvore do Ch\u00e1, o Cedro e a Lavanda podem acalmar e purificar a pele\\rO Bisabolol \u00e9 conhecido pelos seus efeitos calmantes e pela sua capacidade de promover uma pele de aspeto saud\u00e1vel\\r\u00c0 semelhan\u00e7a dos \u00f3leos naturais presentes na pele, a Jojoba promove uma hidrata\u00e7\u00e3o ideal, ajudando a melhorar a textura da pele\\rO extrato de Casca de Phellodendron Amurense \u00e9 utilizado para hidratar a pele\\rLista completa de ingredientes\\rExtrato de Cevada (Hordeum distichon), Extrato de S\u00e2ndalo (Santalum album), Extrato de Casca de Phellodendron Amurense, Estearato de Glicerol, Acacia Decurrens/Jojoba/Cera de Semente de Girassol/Poligliceril-3 \u00c9steres, Capr\u00edlico/Triglic\u00e9rido Capr\u00edlico, Miristato de Glicerol, Palmitato de Glicerol, Ricinoleato de Glicerol, \u00d3leo de Madeira de Cedro (Juniperus virginiana), \u00d3leo de Lavanda (Lavandula angustifolia), \u00d3leo de Folha de \u00c1rvore do Ch\u00e1 (Melaleuca alternifolia), Extrato de Physalis Angulata, \u00d3leo de Semente de Noz Inca (Plukenetia volubilis), \u00d3leo de Frankincense (Boswellia Carterii), \u00d3leo de Flor de Helicriso (Perp\u00e9tua das Areias) (Helichrysum italicum), \u00d3leo de Fruto de Rosa Canina, Extrato de Raiz de Gengibre (Zingiber officinale), \u00d3leo de Palmeira (Elaeis Guineensis), \u00d3leo de Semente de Algod\u00e3o (Gossypium Herbaceum), Extrato de Bidens Pilosa, Bisabolol, \u00d3leo de Semente Linha\u00e7a (Linum Usitatissimum), \u00c1cido Linoleico, Fosfol\u00edpidos, Eicosanedioato de Glicerol, Ester\u00f3is de Soja (Glycine Soja), Palmitato de Dextrina, Glicirrizinato de Estearilo\\rUtiliza\u00e7\u00f5es\\rIntegre a Pomada Essencial Correct-X na sua rotina de beleza matinal e noturna\\rAplique na pele seca para limpar, purificar e hidratar a pele com as suas propriedades calmantes\\rUtilize a f\u00f3rmula da pomada Correct-X nas zonas afetadas para proporcionar al\u00edvio \u00e0 pele quando ocorrem irrita\u00e7\u00f5es\\rMantenha um frasco da pomada \u00e0 m\u00e3o, na mala de viagem, para uma utiliza\u00e7\u00e3o f\u00e1cil e pr\u00e1tica\\rIndica\u00e7\u00f5es de Uso\\rAplique nas zonas afetadas conforme necess\u00e1rio.\\rPrecau\u00e7\u00f5es\\rApenas para utiliza\u00e7\u00e3o externa. Evite o contacto direto com os olhos. Em caso de irrita\u00e7\u00e3o, interrompa a utiliza\u00e7\u00e3o."
}

VALID_FORMAT_EMPTY_FIELD_NORMALIZED_PRODUCT: NormalizedProduct = {
    "product_name": "Pomada Essencial Correct-X\u2122",
    "item_id": "60213438",
    "retail_price": "\u20ac20.67",
    "discount_price": "\u20ac20.67",
    "description": ""
}

INVALID_FORMAT_NORMALIZED_PRODUCT: NormalizedProduct = {
    "product_name": "Pomada Essencial Correct-X\u2122",
    "item_id": "60213438",
    "retail_price": "\u20ac20.67",
    "discount_price": "\u20ac20.67",
    "HBBHKJKJBB": "BLAH BLAH BLAH"
}