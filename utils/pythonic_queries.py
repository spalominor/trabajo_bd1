import time
import polars as pl
import dml



def query_1_polars(name_database):
    # initialize the timer
    start_time = time.perf_counter()
    
    # obtain the tables
    tables =dml.select_all_database(name_database)
    
    naviera = tables["naviera"]
    buque = tables["buque"]
    viaje = tables["viaje"]
    
    result = (
        naviera
        .join(buque, left_on="nombre", right_on="nombre_naviera", suffix="_buque")
        .join(viaje, left_on="numero_omi", right_on="buque_numero_omi", suffix="_viaje")
        .select([
            pl.col("nombre"),
            pl.col("nombre_buque"),
            pl.col("codigo"),
            pl.col("estado"),
            pl.col("fecha_estimada_salida")
        ])
    )
    
    elapsed_time = time.perf_counter() - start_time
    
    return result, elapsed_time


def query_2_polars(name_database):
    # initialize the timer
    start_time = time.perf_counter()
    
    # obtain the tables
    tables = dml.select_all_database(name_database)
    
    naviera = tables["naviera"]
    buque = tables["buque"]
    viaje = tables["viaje"]
    
    result = (
        naviera
        .join(buque, left_on="nombre", right_on="nombre_naviera", suffix="_buque")
        .join(viaje, left_on="numero_omi", right_on="buque_numero_omi", suffix="_viaje")
        .group_by(["nombre", "bandera"])
        .agg(pl.col("codigo").count().alias("total_viajes"))
        .sort("total_viajes", descending=True)
        .rename({"nombre": "nombre_naviera"})
    )
    
    elapsed_time = time.perf_counter() - start_time
    
    return result, elapsed_time