import re
from bs4 import BeautifulSoup
from download import get_pages

def extract_product_info(html):
    soup = BeautifulSoup(html, "html.parser")
    products = soup.find_all("div", class_="entry-product")
    product_info = []
    for product in products:
        product_dict = {}
        product_dict["product_name"] = product.find("h3").text.strip() or "Unknown"
        product_dict["product_url"] = product.find("a")["href"] or "Unknown"
        product_price = product.find("span", class_="price").text.strip() or "Unknown"
        prices = re.findall(r"\$(\d+(?:\.\d+)?)", product_price)
        if len(prices) == 2:
            price1 = float(prices[0]) if prices[0] != "Unknown" else 9999
            price2 = float(prices[1]) if prices[1] != "Unknown" else 9999
            product_dict["product_price"] = min(price1, price2)
        elif len(prices) == 1:
            product_dict["product_price"] = float(prices[0]) if prices[0] != "Unknown" else 9999
        else:
            product_dict["product_price"] = 9999
        product_info.append(product_dict)
    return product_info


def get_products():
    products = []
    pages = get_pages("https://iriedirect.com/irie-direct")
    for page in pages:
        product_info = extract_product_info(page)
        products.extend(product_info)
        if __name__ == "__main__":
            for product_dict in product_info:
                print(f"Product Name: {product_dict['product_name']}")
                print(f"Product URL: {product_dict['product_url']}")
                print(f"Product Price: ${product_dict['product_price']:.2f}")
                print("---")
    return products


if __name__ == "__main__":
    p = get_products()
