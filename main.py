from collections import defaultdict
from utils import data, ddl, dml, pythonic_queries



"""
TEST_DATABASES = ["postgres", "mysql"]
TEST_ROWS = [1, 10, 100]
TEST_QUERIES = ["query_1", "query_2"]
TEST_TRIES = 3
"""
TEST_DATABASES = ["postgres", "mysql"]
TEST_ROWS = [1000, 10000, 100000]
TEST_QUERIES = ["query_1", "query_2"]
TEST_TRIES = 3


# step 1: database creation
def schema_creation():
    ddl.create_postgres_tables()
    ddl.create_mysql_tables()


def benchmark():
    # initialize dicts for results
    insertion_results = defaultdict(list)
    sql_query_results = defaultdict(list)
    polars_query_results = defaultdict(list)
    
    # step 1 and 2
    schema_creation()
    
    # for each number of rows
    for db_name in TEST_DATABASES:
        for number_rows in TEST_ROWS:
            data.create_all_data(number_rows)
            for attempt in range(TEST_TRIES):
                ddl.reset_db(db_name)
                
                # fase ii: data insertion
                insertion_time = dml.insert_data(db_name, number_rows)
                insertion_results[(db_name, number_rows)].append(insertion_time)
                
                # fase iii: sql queries execution
                for query in TEST_QUERIES:
                    result, sql_time = dml.query(db_name, query)
                    sql_query_results[(db_name, number_rows, query)].append(sql_time)
                    
                # fase iv: pythonic queries execution
                tables, elapsed_time = dml.select_all_database(db_name)
                for query in TEST_QUERIES:
                    result, polars_time = pythonic_queries.polars_query(tables, query)
                    total_time = elapsed_time + polars_time
                    polars_query_results[(db_name, number_rows, query)].append(total_time)
    
    return insertion_results, sql_query_results, polars_query_results


# step 6: print all the results
def print_results():
    # obtain the results from the benchmark function
    insertion_results, sql_query_results, polars_query_results = benchmark()
    
    print("\n" + "=" * 50)
    print(" 1. RESULTADOS DE INSERCIÓN DE DATOS")
    print("=" * 50)
    for (db, size), times in insertion_results.items():
        avg_time = sum(times) / len(times)
        print(f"[{db.upper()}] Filas: {size:<7} | Tiempos: {times} | Promedio: {avg_time:.4f}s")

    print("\n" + "=" * 50)
    print(" 2. RESULTADOS DE CONSULTAS SQL NATIVAS")
    print("=" * 50)
    for (db, size, query), times in sql_query_results.items():
        avg_time = sum(times) / len(times)
        print(f"[{db.upper()}] Filas: {size:<7} | Query: {query} | Tiempos: {times} | Promedio: {avg_time:.4f}s")

    print("\n" + "=" * 50)
    print(" 3. RESULTADOS DE CONSULTAS CON POLARS")
    print("=" * 50)
    for (db, size, query), times in polars_query_results.items():
        avg_time = sum(times) / len(times)
        print(f"[{db.upper()}] Filas: {size:<7} | Query: {query} | Tiempos: {times} | Promedio: {avg_time:.4f}s")
        

if __name__ == "__main__":
    print_results()