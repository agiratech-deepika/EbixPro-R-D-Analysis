import psycopg2
from psycopg2.extras import DictCursor
from config import DATABASE_URL

class DatabaseController:
    def __init__(self):
        self.conn = psycopg2.connect(DATABASE_URL)
        self.cursor = self.conn.cursor(cursor_factory=DictCursor)

    def execute_query(self, query, params=None):
        """Executes INSERT/UPDATE queries"""
        self.cursor.execute(query, params)
        self.conn.commit()

    def fetch_one(self, query, params=None):
        """Fetches a single row"""
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def fetch_all(self, query, params=None):
        """Fetches all rows"""
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()
