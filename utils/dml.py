import os
import time
from dotenv import load_dotenv
import psycopg2
import mysql.connector as cpy
import polars as pl



load_dotenv()


POSTGRES_CREDENTIALS = {
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT"),
    "database": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD")  
}

POSTGRES_URL = f"postgresql://{POSTGRES_CREDENTIALS['user']}:{POSTGRES_CREDENTIALS['password']}@{POSTGRES_CREDENTIALS['host']}:{POSTGRES_CREDENTIALS['port']}/{POSTGRES_CREDENTIALS['database']}"

MYSQL_CREDENTIALS = {
    "host": os.getenv("MYSQL_HOST"),
    "port": int(os.getenv("MYSQL_PORT")),
    "database": os.getenv("MYSQL_DB"),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD")  
}

MYSQL_URL = f"mysql://{MYSQL_CREDENTIALS['user']}:{MYSQL_CREDENTIALS['password']}@{MYSQL_CREDENTIALS['host']}:{MYSQL_CREDENTIALS['port']}/{MYSQL_CREDENTIALS['database']}"

TABLES = ["mercancia", "viaje", "buque", "naviera"]
DB_URLS = {
    "postgres": POSTGRES_URL,
    "mysql": MYSQL_URL
}


def select_all_database(name_database):
    result = {}
    for table in TABLES:
        result[table] = pl.read_database_uri(
            query=f"SELECT * FROM {table};",
            uri=DB_URLS[name_database],
            engine="connectorx"
        )
    return result
    
    
def query_mysql(name_query):
    with cpy.connect(**MYSQL_CREDENTIALS) as cnx:
        with cnx.cursor() as cur:
            with open(f"mysql/{name_query}.sql", "r") as f:
                sql_query = f.read()
                start_time = time.perf_counter()
                cur.execute(sql_query)
                result = cur.fetchall()
                elapsed_time = time.perf_counter() - start_time
    return result, elapsed_time


def query_postgres(name_query):
    with psycopg2.connect(POSTGRES_URL) as conn:
        with conn.cursor() as cur:
            with open(f"postgres/{name_query}.sql", "r") as f:
                sql_query = f.read()
                start_time = time.perf_counter()
                cur.execute(sql_query)
                result = cur.fetchall()
                elapsed_time = time.perf_counter() - start_time
    return result, elapsed_time