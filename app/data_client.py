# import sqlite3
from sqlite3 import Error
import psycopg2
# import csv
from abc import ABC, abstractmethod


class DataClient(ABC):
    @abstractmethod
    def get_connection(self):
        pass

    @abstractmethod
    def create_table(self, conn, sql_request):
        pass

    @abstractmethod
    def get_items(self, conn, sql_request):
        pass

    @abstractmethod
    def insert(self, conn, sql_request):
        pass

    def run_test(self):
        conn = self.get_connection()
        self.create_table(conn, """
            CREATE TABLE IF NOT EXISTS mebel
            (
                id serial PRIMARY KEY, 
                link text, 
                price integer, 
                description text
            )
        """)
        items = self.get_items(conn, "SELECT * FROM mebel WHERE price >= 50 and price <= 1000")
        self.insert(conn, "INSERT INTO mebel (link, price, description) VALUES ('https://link.com', '850', 'description')")
        for item in items:
            print(item)

        conn.close()


class PostgresClient(DataClient):
    USER = "nervokey"
    PASSWORD = "postgres"
    HOST = "localhost"
    PORT = "5432"

    def get_connection(self):
        try:
            connection = psycopg2.connect(
                user=self.USER,
                password=self.PASSWORD,
                host=self.HOST,
                port=self.PORT,
                dbname='postgres'
            )
            return connection
        except Error:
            print(f"Error: {Error}")

    def create_table(self, conn, sql_request):
        """
            CREATE TABLE IF NOT EXISTS mebel
            (
                id serial PRIMARY KEY,
                link text,
                price integer,
                description text
            )
        """

        cursor = conn.cursor()
        cursor.execute(sql_request)
        conn.commit()

    def get_items(self, conn, sql_request):
        """f'SELECT * FROM mebel WHERE price >= {price_from} and price <= {price_to}'"""
        cursor = conn.cursor()
        cursor.execute(sql_request)
        return cursor.fetchone()

    def insert(self, conn, sql_request):
        """INSERT INTO mebel (link, price, description) VALUES ('{link}', '{price}', '{description}')"""
        cursor = conn.cursor()
        cursor.execute(sql_request)
        conn.commit()


# data_client = PostgresClient()
# data_client = Sqlite3Client()
# data_client.run_test()
