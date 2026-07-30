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
print(POSTGRES_URL)

MYSQL_CREDENTIALS = {
    "host": os.getenv("MYSQL_HOST"),
    "port": int(os.getenv("MYSQL_PORT")),
    "database": os.getenv("MYSQL_DB"),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD")  
}