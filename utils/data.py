import os
import random
from datetime import datetime, timedelta
import numpy as np


# seed fixed for reproducibility
rng = np.random.default_rng(seed=23)

OUTPUT_DIR = "data"
ROWS = 100000
OMI_BASE = 8000000

# default values for no third-party libraries
PAISES = [
    "Panama", "Liberia", "Islas Marshall", "Hong Kong", "Singapur", "Malta", "Bahamas", 
    "China", "Grecia", "Japon", "Alemania", "Estados Unidos", "Noruega", "Dinamarca", 
    "Reino Unido", "Espana", "Colombia", "Chile", "Brasil", "Mexico", "Peru", "Ecuador"
]

ESTADOS_VIAJE = ["Programado", "En Transito", "Completado", "Cancelado", "Retrasado"]

DESCRIPCIONES_MERCANCIA = [
    "Contenedor con productos electronicos", "Carga de granel de trigo", "Productos textiles y confecciones",
    "Maquinaria industrial pesada", "Piezas de repuesto automotrices", "Productos quimicos no peligrosos",
    "Frutas y alimentos refrigerados", "Cafe de exportacion", "Acero laminado en bobinas", "Materiales de construccion"
]


def crear_navieras():
    filename = os.path.join(OUTPUT_DIR, "naviera.csv")
    with open(filename, "w", encoding="utf-8") as f:
        f.write("nombre,pais_registro,certificacion_solas,certificacion_ism\n")
        for i in range(1, ROWS + 1):
            nombre = f"Naviera_{i:06d}"
            pais = random.choice(PAISES)
            solas = random.choice([True, False])
            ism = random.choice([True, False])
            f.write(f"{nombre},{pais},{solas},{ism}\n")
    print(f"Creado: {filename} ({ROWS:,} filas)")



def crear_buques():
    filename = os.path.join(OUTPUT_DIR, "buque.csv")    
        
    with open(filename, "w", encoding="utf-8") as f:
        f.write("numero_omi,nombre,bandera,anio_construccion,capacidad_teu,eslora,manga,calado_maximo,nombre_naviera\n")
        for i in range(1, ROWS + 1):
            numero_omi = OMI_BASE + i
            nombre = f"Buque_{i:06d}"
            # fix: numpy random generator
            bandera = random.choice(PAISES)
            anio_construccion = random.randint(1980, 2025)
            capacidad_teu = random.randint(500, 24000)
            eslora = round(random.uniform(50.0, 400.0), 2)
            manga = round(random.uniform(10.0, 60.0), 2)
            calado_maximo = round(random.uniform(5.0, 20.0), 2)
            
            # foreign key to Naviera
            naviera_id = random.randint(1, ROWS)
            nombre_naviera = f"Naviera_{naviera_id:06d}"
            
            f.write(f"{numero_omi},{nombre},{bandera},{anio_construccion},{capacidad_teu},{eslora},{manga},{calado_maximo},{nombre_naviera}\n")
    print(f"Creado: {filename} ({ROWS:,} filas)")


def crear_viajes():
    filename = os.path.join(OUTPUT_DIR, "viaje.csv")
    
    # base date for generating random dates in YYYY-MM-DD format
    base_date = datetime(2020, 1, 1)

    with open(filename, "w", encoding="utf-8") as f:
        f.write("codigo,fecha_estimada_salida,fecha_estimada_llegada,estado,consumo_combustible,buque_numero_omi\n")
        for i in range(1, ROWS + 1):
            codigo = f"V{i:06d}"
            
            # Garantizar que fecha_llegada >= fecha_salida
            dias_salida = random.randint(0, 3000)
            duracion_dias = random.randint(2, 90)
            fecha_salida = base_date + timedelta(days=dias_salida)
            fecha_llegada = fecha_salida + timedelta(days=duracion_dias)
            
            estado = random.choice(ESTADOS_VIAJE)
            consumo_combustible = round(random.uniform(10.0, 20000.0), 2)
            
            # FK a Buque existente
            buque_id = random.randint(1, ROWS)
            buque_numero_omi = OMI_BASE + buque_id
            
            f.write(f"{codigo},{fecha_salida.strftime('%Y-%m-%d')},{fecha_llegada.strftime('%Y-%m-%d')},{estado},{consumo_combustible},{buque_numero_omi}\n")
    print(f"Creado: {filename} ({ROWS:,} filas)")


def crear_mercancias():
    filename = os.path.join(OUTPUT_DIR, "mercancia.csv")
    with open(filename, "w", encoding="utf-8") as f:
        f.write("codigo,descripcion,peso_bruto,volumen,pais_origen,codigo_viaje\n")
        for i in range(1, ROWS + 1):
            codigo = f"M{i:06d}"
            descripcion = random.choice(DESCRIPCIONES_MERCANCIA)
            peso_bruto = round(random.uniform(100.0, 50000.0), 2)
            volumen = round(random.uniform(1.0, 200.0), 2)
            pais_origen = random.choice(PAISES)
            
            # FK a Viaje existente
            viaje_id = random.randint(1, ROWS)
            codigo_viaje = f"V{viaje_id:06d}"
            
            f.write(f"{codigo},{descripcion},{peso_bruto},{volumen},{pais_origen},{codigo_viaje}\n")
    print(f"Creado: {filename} ({ROWS:,} filas)")