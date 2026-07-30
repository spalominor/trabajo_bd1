from utils import data, ddl, dml, pythonic_queries 



# step 1: database creation
def fase_1():
    ddl.create_postgres_tables()
    ddl.create_mysql_tables()

# data creation
data.crear_navieras()
data.crear_buques()
data.crear_viajes()
data.crear_mercancias()

# data insertion

# data selection