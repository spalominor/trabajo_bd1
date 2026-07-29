import os
from dotenv import load_dotenv
import psycopg2
import _mysql_connector


load_dotenv()

# postgres table creation
POSTGRES_CREDENTIALS = {
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT"),
    "database": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD")  
}
POSTGRES_URL = f"postgresql://{POSTGRES_CREDENTIALS['user']}:{POSTGRES_CREDENTIALS['password']}@{POSTGRES_CREDENTIALS['host']}:{POSTGRES_CREDENTIALS['port']}/{POSTGRES_CREDENTIALS['database']}"
print(POSTGRES_URL)


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

            print("Tables created in the database:")
            for table in tables:
                print(table[0])

            # Eliminate the tables to clean up the database
            cur.execute(
                """
                DROP TABLE IF EXISTS NAVIERA, BUQUE, VIAJE, MERCANCIA CASCADE;"""
            )
            conn.commit()

create_postgres_tables()