import scrape
import mariadb
from time import sleep

SLEEP_MINUTES = (60*60)

def main():
    # Get the product information from scrape.py
    product_list = scrape.get_products()

    # Connect to the database
    db = mariadb.ProductDatabase()

    # Insert each product into the database
    db.sync_products(product_list)

if __name__ == '__main__':
    while True:
        main()
        sleep(SLEEP_MINUTES)
