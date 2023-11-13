from components.models import Information, Benefits, Ingredients, Uses

INFORMATION: Information = {
    "product_name": {
        "xpath": '//*[@id="ProductSpotlightSection"]/div[1]/div/div/div[1]/h3/span',
        "text": ""
    },
    "description": {
        "xpath": '//*[@id="ProductSpotlightSection"]/div[1]/div/div/div[1]/div[1]/p/span',
        "text": ""
    },
    "dimensions": {
        "xpath": '//*[@id="ProductSpotlightSection"]/div[1]/div/div/div[3]/div/div[2]/div[1]/div/div[2]/span',
        "text": ""
    },
    "item_id": {
        "xpath": '//*[@id="ProductSpotlightSection"]/div[1]/div/div/div[3]/div/div[2]/div[2]/div/div[2]',
        "text": ""
    },
    "retail_price": {
        "xpath": '//*[@id="ProductSpotlightSection"]/div[1]/div/div/div[3]/div/div[3]/div[1]/div/div[2]',
        "text": ""
    },
    "discount_price": {
        "xpath": '//*[@id="ProductSpotlightSection"]/div[1]/div/div/div[3]/div/div[3]/div[1]/div/div[2]',
        "text": ""
    }
}

BENEFITS: Benefits = {
    "benefits_title": {
        "xpath": '//*[@id="ProductSpotlightSection"]/div[3]/div[2]/div/div/h3/span',
        "text": ""
    },
    "benefits": {
        "xpath": '//*[@id="ProductSpotlightSection"]/div[3]/div[2]/div/div/div/ul',
        "text": [""]
    }
}

INGREDIENTS: Ingredients = {
    "ingredients_title": {
        "xpath": '//*[@id="WhatsInsideSection"]/div/div[2]/div/h3/span',
        "text": ""
    },
    "ingredients": {
        "xpath": '//*[@id="WhatsInsideSection"]/div/div[2]/div/div/p/span',
        "text": ""
    }
}

UTILIZATION: Uses = {
    "uses_title": {
        "xpath": '//*[@id="ProductUsesSection"]/div[1]/div/div[2]/h3[1]/span',
        "text": ""
    },
    "uses": {
        "xpath": '//*[@id="ProductUsesSection"]/div[1]/div/div[2]/div[1]/ul',
        "text": [""]
    },
    "instructions_title": {
        "xpath": '//*[@id="ProductUsesSection"]/div[1]/div/div[2]/h3[2]/span',
        "text": ""
    },
    "instructions": {
        "xpath": '//*[@id="ProductUsesSection"]/div[1]/div/div[2]/div[2]/div/div[2]/span',
        "text": ""
    },
    "cautions_title": {
        "xpath": '//*[@id="ProductUsesSection"]/div[1]/div/div[2]/div[3]/h3/span',
        "text": ""
    },
    "cautions": {
        "xpath": '//*[@id="ProductUsesSection"]/div[1]/div/div[2]/div[3]/div/p/span',
        "text": ""
    }
}
