import mysql.connector

class ProductDatabase:
    HOST = "192.168.86.6"
    PORT = 3306
    USERNAME = "dc_test"
    PASSWORD = "dc_test"
    DB_NAME = "dc_test"

    def __init__(self):
        self.conn = mysql.connector.connect(
            host=self.HOST,
            port=self.PORT,
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
        for name, url, price in products:
            self.insert_product(name, url, price)
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

if __name__ == "__main__":
    db = ProductDatabase()
