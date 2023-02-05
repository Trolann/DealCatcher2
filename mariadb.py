import mysql.connector
import os

class ProductDatabase:
    def __init__(self):
        # load the environment variables from the db.env file
        #with open('db.env') as f:
        #    for line in f:
        #        key, value = line.strip().split('=', 1)
        #        os.environ[key] = value

        # access the environment variables
        self.HOST = os.getenv("HOST")
        self.PORT = os.getenv("PORT")
        self.USERNAME = os.getenv("USERNAME")
        self.PASSWORD = os.getenv("PASSWORD")
        self.DB_NAME = os.getenv("DB_NAME")

        self.conn = mysql.connector.connect(
            host=self.HOST,
            port=int(self.PORT),
            user=self.USERNAME,
            password=self.PASSWORD,
            database=self.DB_NAME
        )
        self.cursor = self.conn.cursor()
        self.create_deals_table()
        self.create_new_deals_table()

    def create_deals_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS deals (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                url VARCHAR(255) NOT NULL,
                price FLOAT NOT NULL
            )
        """)

    def create_new_deals_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS new_deals (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                url VARCHAR(255) NOT NULL,
                price FLOAT NOT NULL
            )
        """)

    def insert_product(self, name, url, price):
        self.cursor.execute("""
            INSERT INTO deals (name, url, price)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE name=VALUES(name), url=VALUES(url), price=VALUES(price)
        """, (name, url, price))
        self.cursor.execute("""
            INSERT INTO new_deals (name, url, price)
            VALUES (%s, %s, %s)
        """, (name, url, price))

    def update_product(self, name, url, price):
        self.cursor.execute("""
            UPDATE deals
            SET name=%s, url=%s, price=%s
            WHERE name=%s
        """, (name, url, price, name))

    def remove_product(self, name):
        self.cursor.execute("""
            DELETE FROM deals WHERE name=%s
        """, (name,))

    def get_product(self, name):
        self.cursor.execute("""
            SELECT * FROM deals WHERE name=%s
        """, (name,))
        return self.cursor.fetchone()

    def get_all_products(self):
        self.cursor.execute("""
            SELECT * FROM deals
        """)
        return self.cursor.fetchall()

    def add_products(self, products):
        for product in products:
            name = product["product_name"]
            url = product["product_url"]
            price = product["product_price"]
            try:
                self.insert_product(name, url, price)
            except mysql.connector.errors.DataError as e:
                print(name, url, price)
                print(e)
        self.conn.commit()

    def sync_products(self, website_products):
        # Get all products from the database
        db_products = self.get_all_products()
        db_product_names = [product[1] for product in db_products]

        # Iterate through all products on the website
        for website_product in website_products:
            product_name = website_product["product_name"]
            product_url = website_product["product_url"]
            product_price = website_product["product_price"]

            # Check if the product is in the database
            if product_name in db_product_names:
                # Get the product from the database
                db_product = self.get_product(product_name)
                # Compare the prices
                if db_product[3] != product_price:
                    # Update the price if there's a difference
                    self.update_product(product_name, product_url, product_price)
                # Remove the product name from the list of product names in the database
                db_product_names.remove(product_name)
            else:
                # Insert the new product into the database
                self.insert_product(product_name, product_url, product_price)

        # Remove any products that are in the database but not on the website
        for remaining_product_name in db_product_names:
            self.remove_product(remaining_product_name)

        self.conn.commit()


    def close(self):
        self.cursor.close()
        self.conn.close()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

if __name__ == "__main__":
    db = ProductDatabase()
    while True:
        continue
