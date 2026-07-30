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


def create_postgres_tables():
    with psycopg2.connect(POSTGRES_URL) as conn:
        with conn.cursor() as cur:
            # Execute the SQL commands from the schema.sql file
            with open("postgres/schema.sql", "r") as f:
                sql_commands = f.read()
                cur.execute(sql_commands)
                conn.commit()

            # Validate the creation of the tables by querying the information_schema
            cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
            tables = cur.fetchall()

            print("Tables created in the PostgreSQL database:")
            for table in tables:
                print(table[0])


def create_mysql_tables():
    with cpy.connect(**MYSQL_CREDENTIALS) as cnx:
        with cnx.cursor() as cur:
            # Execute the SQL commands from the schema.sql file
            with open("mysql/schema.sql", "r") as f:
                sql_commands = f.read()
                for response in cur.execute(sql_commands, multi=True):
                    pass
                cnx.commit()

            # Validate the creation of the tables by querying the information_schema
            cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = %s;", (MYSQL_CREDENTIALS['database'],))
            tables = cur.fetchall()

            print("Tables created in the MySQL database:")
            for table in tables:
                print(table[0])