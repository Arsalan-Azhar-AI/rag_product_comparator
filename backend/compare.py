import re

def extract_price(text):
    match = re.search(r"Rs[ .]*([\d,]+)", text)
    if match:
        return int(match.group(1).replace(",", ""))
    return None

def extract_title(text):
    lines = text.strip().split("\n")
    for line in lines:
        if len(line.split()) >= 2 and len(line) < 100:
            return line.strip()
    return "Unknown Product"

def extract_features(text):
    lines = text.strip().split("\n")
    features = [line.strip() for line in lines if any(keyword in line.lower() for keyword in ["battery", "bluetooth", "noise", "wireless", "mic", "type"])]
    return ", ".join(features) if features else "Not found"

def get_product_info(text):
    return {
        "title": extract_title(text),
        "price": extract_price(text),
        "features": extract_features(text)
    }

def compare_products(text1, text2):
    product1 = get_product_info(text1)
    product2 = get_product_info(text2)

    result = [
    f"Product 1: {product1['title']} (Rs. {product1['price']})",
    f"Features: {product1['features']}",
    "",
    f"Product 2: {product2['title']} (Rs. {product2['price']})",
    f"Features: {product2['features']}",
    ""
    ]

    if product1['price'] and product2['price']:
        if product1['price'] < product2['price']:
            result.append("\u2705 Product 1 is cheaper.")
        elif product2['price'] < product1['price']:
            result.append("\u2705 Product 2 is cheaper.")
        else:
            result.append("\ud83d\udcb8 Both products have the same price.")
    else:
        result.append("\u26a0\ufe0f Could not extract prices accurately.")

    return "\n".join(result)



