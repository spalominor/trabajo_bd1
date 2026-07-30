from utils import data, ddl, dml, pythonic_queries, summarize



# step 1: database creation
def schema_creation():
    ddl.create_postgres_tables()
    ddl.create_mysql_tables()
    
    
# step 2: data creation. only one time for the 100.000 rows
def artificial_data_creation():
    data.create_navieras()
    data.create_buques()
    data.create_viajes()
    data.create_mercancias()
    

# step 3: data insertion
def data_insertion():
    TEST_ROWS = [1000, 10000, 100000]
    TRIES = 3
    
    # postgres
    results_postgres = {}
    for number_rows in TEST_ROWS:
        for _ in range(TRIES):
            results_postgres[number_rows] = []
            ddl.drop_postgres_tables()
            ddl.create_postgres_tables()
            elapsed_time = dml.insert_data_postgres(number_rows)
            results_postgres[number_rows].append(elapsed_time)
            
    # mysql
    results_mysql = {}
    for number_rows in TEST_ROWS:
        for _ in range(TRIES):
            results_mysql[number_rows] = []
            ddl.drop_mysql_tables()
            ddl.create_mysql_tables()
            elapsed_time = dml.insert_data_mysql(number_rows)
            results_mysql[number_rows].append(elapsed_time)
            
    return results_postgres, results_mysql
            

# step 4: sql queries execution
def sql_queries_execution():
    TEST_QUERIES = ["query1", "query2"]
    TRIES = 3
    
    # postgres
    results_postgres = {}
    for query in TEST_QUERIES:
        for _ in range(TRIES):
            results_postgres[query] = []
            result, elapsed_time = dml.query_postgres(query)
            results_postgres[query].append(elapsed_time)
            
    # mysql
    results_mysql = {}
    for query in TEST_QUERIES:
        for _ in range(TRIES):
            results_mysql[query] = []
            result, elapsed_time = dml.query_mysql(query)
            results_mysql[query].append(elapsed_time)
            
    return results_postgres, results_mysql
            

# step 5: pythonic queries execution
def pythonic_queries_execution():
    TEST_DATABASES = ["postgres", "mysql"]
    TEST_QUERIES = ["query1", "query2"]
    TRIES = 3
    
    # postgres
    results = {}
    for database in TEST_DATABASES:
        for query in TEST_QUERIES:
            for _ in range(TRIES):
                results[(database, query)] = []
                if query == "query1":
                    result, elapsed_time = pythonic_queries.query_1_polars(database)
                elif query == "query2":
                    result, elapsed_time = pythonic_queries.query_2_polars(database)
                results[(database, query)].append(elapsed_time)
    
    return results
    

# step 6: print all the results
def print_results():
    # fase ii: data insertion
    results_postgres_2, results_mysql_2 = data_insertion()
    
    # fase iii: sql queries execution
    results_postgres_3, results_mysql_3 = sql_queries_execution()
    
    # fase iv: pythonic queries execution
    results_4 = pythonic_queries_execution()
