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
    "database": os.getenv("MYSQL_DATABASE"),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "allow_local_infile": True
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
            cur.execute(f"USE {MYSQL_CREDENTIALS['database']};")
            # Execute the SQL commands from the schema.sql file
            with open("mysql/schema.sql", "r") as f:
                sql_commands = f.read()
                
            statements = sql_commands.split(';')
            for statement in statements:
                if statement.strip():
                    cur.execute(statement)
                    
            cnx.commit()

            # Validate the creation of the tables by querying the information_schema
            cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = %s;", (MYSQL_CREDENTIALS['database'],))
            tables = cur.fetchall()

            print("Tables created in the MySQL database:")
            for table in tables:
                print(table[0])
                

def drop_postgres_tables():
    with psycopg2.connect(POSTGRES_URL) as conn:
        with conn.cursor() as cur:
            # Drop the tables in reverse order to avoid foreign key constraint issues
            cur.execute("DROP TABLE IF EXISTS MERCANCIA, VIAJE, BUQUE, NAVIERA CASCADE;")
            conn.commit()
            print("Tables dropped in the PostgreSQL database.")


def drop_mysql_tables():
    with cpy.connect(**MYSQL_CREDENTIALS) as cnx:
        with cnx.cursor() as cur:
            # Drop the tables in reverse order to avoid foreign key constraint issues
            cur.execute("DROP TABLE IF EXISTS MERCANCIA, VIAJE, BUQUE, NAVIERA;")
            cnx.commit()
            print("Tables dropped in the MySQL database.")
            

def reset_db(name_database):
    if name_database == "postgres":
        drop_postgres_tables()
        create_postgres_tables()
    elif name_database == "mysql":
        drop_mysql_tables()
        create_mysql_tables()    