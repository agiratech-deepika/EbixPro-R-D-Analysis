from controllers.database_controller import DatabaseController

class ProductModel:
    def __init__(self):
        self.db = DatabaseController()

    def get_product_by_url(self, url):
        return self.db.fetch_one("SELECT * FROM products WHERE given_url = %s", (url,))

    def insert_product(self, data):
        query = """
        INSERT INTO products (given_url, product_name, description, source, image_url, video_url, image_path, video_path)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
        """
        self.db.execute_query(query, (
            data['given_url'], data['product_name'], data['description'], data['source'],
            data['image_url'], data['video_url'], data['image_path'], data['video_path']
        ))

    def close(self):
        self.db.close()
