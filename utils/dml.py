import os
import io
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
    "password": os.getenv("MYSQL_PASSWORD"),
    "allow_local_infile": True
}

MYSQL_URL = f"mysql://{MYSQL_CREDENTIALS['user']}:{MYSQL_CREDENTIALS['password']}@{MYSQL_CREDENTIALS['host']}:{MYSQL_CREDENTIALS['port']}/{MYSQL_CREDENTIALS['database']}"

TABLES = ["naviera", "buque", "viaje", "mercancia"]
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


def insert_data_postgres(number_rows):
    # insert n rows from csv file into postgres database
    with psycopg2.connect(POSTGRES_URL) as conn:
        with conn.cursor() as cur:
            start_time = time.perf_counter()
            
            for table in TABLES:
                csv_filepath = f"data/{table}.csv"
                
                buffer = io.StringIO()
                with open(csv_filepath, "r", encoding="utf-8") as f:
                    for idx, line in enumerate(f):
                        if idx > number_rows:
                            break
                        buffer.write(line)
                buffer.seek(0)
                
                sql_copy = f"""
                    COPY {table} 
                    FROM STDIN 
                    WITH (FORMAT CSV, HEADER true, DELIMITER ',');
                """
                cur.copy_expert(sql_copy, buffer)
            
            conn.commit()
            elapsed_time = time.perf_counter() - start_time
            print(f"Inserted {number_rows} rows into Postgres in {elapsed_time:.4f} seconds.")
    return elapsed_time


def insert_data_mysql(number_rows):
    with cpy.connect(**MYSQL_CREDENTIALS) as cnx:
        with cnx.cursor() as cur:
            start_time = time.perf_counter()
            
            for table in TABLES:
                csv_filepath = f"data/{table}.csv"
                    
                sql_load = f"""
                    LOAD DATA LOCAL INFILE '{csv_filepath}'
                    INTO TABLE {table}
                    FIELDS TERMINATED BY ','
                    OPTIONALLY ENCLOSED BY '"'
                    LINES TERMINATED BY '\n'
                    IGNORE 1 LINES
                    LIMIT {number_rows};
                """
                cur.execute(sql_load)

            cnx.commit()
            elapsed_time = time.perf_counter() - start_time
            print(f"Inserted {number_rows} rows into MySQL in {elapsed_time:.4f} seconds.")
    return elapsed_time


def insert_data(name_database, number_rows):
    if name_database == "postgres":
        print(f"Inserting {number_rows} rows into Postgres...")
        return insert_data_postgres(number_rows)
    elif name_database == "mysql":
        print(f"Inserting {number_rows} rows into MySQL...")
        return insert_data_mysql(number_rows)
    

def query(name_database, name_query):
    if name_database == "postgres":
        return query_postgres(name_query)
    elif name_database == "mysql":
        return query_mysql(name_query)