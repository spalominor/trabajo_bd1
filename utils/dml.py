import os
from dotenv import load_dotenv
import psycopg2
import mysql.connector as cpy



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


# per default, the select all is in the MySQL database
# TODO: add a parameter to select the database (MySQL or PostgreSQL)
# generics functions with params
def select_all_mysql():
    with cpy.connect(**MYSQL_CREDENTIALS) as cnx:
        with cnx.cursor() as cur:
            cur.execute("SELECT * FROM mercancia;")
            mercancia_rows = cur.fetchall()
            
            cur.execute("SELECT * FROM viaje;")
            viaje_rows = cur.fetchall()
            
            cur.execute("SELECT * FROM buque;")
            buque_rows = cur.fetchall()
            
            cur.execute("SELECT * FROM naviera;")
            naviera_rows = cur.fetchall()
    
    return {
        "mercancia": mercancia_rows,
        "viaje": viaje_rows,
        "buque": buque_rows,
        "naviera": naviera_rows
    }
    
    
def select_all_postgres():
    with psycopg2.connect(POSTGRES_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM mercancia;")
            mercancia_rows = cur.fetchall()
            
            cur.execute("SELECT * FROM viaje;")
            viaje_rows = cur.fetchall()
            
            cur.execute("SELECT * FROM buque;")
            buque_rows = cur.fetchall()
            
            cur.execute("SELECT * FROM naviera;")
            naviera_rows = cur.fetchall()
    
    return {
        "mercancia": mercancia_rows,
        "viaje": viaje_rows,
        "buque": buque_rows,
        "naviera": naviera_rows
    }
    
    
def query_1_mysql():
    with cpy.connect(**MYSQL_CREDENTIALS) as cnx:
        with cnx.cursor() as cur:
            with open("mysql/query_1.sql", "r") as f:
                sql_query = f.read()
                cur.execute(sql_query)
                result = cur.fetchall()
    return result


def query_2_mysql():
    with cpy.connect(**MYSQL_CREDENTIALS) as cnx:
        with cnx.cursor() as cur:
            with open("mysql/query_2.sql", "r") as f:
                sql_query = f.read()
                cur.execute(sql_query)
                result = cur.fetchall()
    return result


def query_1_postgres():
    with psycopg2.connect(POSTGRES_URL) as conn:
        with conn.cursor() as cur:
            with open("postgres/query_1.sql", "r") as f:
                sql_query = f.read()
                cur.execute(sql_query)
                result = cur.fetchall()
    return result


def query_2_postgres():
    with psycopg2.connect(POSTGRES_URL) as conn:
        with conn.cursor() as cur:
            with open("postgres/query_2.sql", "r") as f:
                sql_query = f.read()
                cur.execute(sql_query)
                result = cur.fetchall()
    return result