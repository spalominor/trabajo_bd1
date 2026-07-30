import os
from datetime import datetime, timedelta
import numpy as np


# seed fixed for reproducibility
rng = np.random.default_rng(seed=23)

OUTPUT_DIR = "data"
ROWS = 100
OMI_BASE = 9000000

os.makedirs(OUTPUT_DIR, exist_ok=True)

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


def create_navieras():
    filename = os.path.join(OUTPUT_DIR, "naviera.csv")
    
    # pregenerate all the random values
    paises_random = rng.choice(PAISES, size=ROWS)
    solas_random = rng.choice([True, False], size=ROWS, p=[0.8, 0.2])
    ism_random = rng.choice([True, False], size=ROWS, p=[0.8, 0.2])
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write("nombre,pais_registro,certificacion_solas,certificacion_ism\n")
        for i in range(ROWS):
            nombre = f"Naviera_{i:06d}"
            pais = paises_random[i]
            solas = solas_random[i]
            ism = ism_random[i]
            f.write(f"{nombre},{pais},{solas},{ism}\n")
    print(f"Creado: {filename} ({ROWS:,} filas)")


def create_buques():
    filename = os.path.join(OUTPUT_DIR, "buque.csv")    
    
    # pregenerate all the random values
    banderas_random = rng.choice(PAISES, size=ROWS)
    anios_random = rng.integers(1980, 2026, size=ROWS)
    capacidades_random = rng.integers(500, 24001, size=ROWS)
    esloras_random = rng.integers(50, 400, size=ROWS)
    mangas_random = rng.integers(10, 60, size=ROWS)
    calados_random = rng.integers(5, 20, size=ROWS)
    navieras_fk_random = rng.integers(0, ROWS, size=ROWS)
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write("numero_omi,nombre,bandera,anio_construccion,capacidad_teu,eslora,manga,calado_maximo,nombre_naviera\n")
        for i in range(ROWS):
            numero_omi = OMI_BASE + i
            nombre = f"Buque_{i:06d}"
            bandera = banderas_random[i]
            anio_construccion = anios_random[i]
            capacidad_teu = capacidades_random[i]
            eslora = esloras_random[i]
            manga = mangas_random[i]
            calado_maximo = calados_random[i]
            
            # foreign key to Naviera
            naviera_id = navieras_fk_random[i]
            nombre_naviera = f"Naviera_{naviera_id:06d}"
            
            f.write(f"{numero_omi},{nombre},{bandera},{anio_construccion},{capacidad_teu},{eslora},{manga},{calado_maximo},{nombre_naviera}\n")
    print(f"Creado: {filename} ({ROWS:,} filas)")


def create_viajes():
    filename = os.path.join(OUTPUT_DIR, "viaje.csv")
    
    # pregenerate all the random values
    dias_salida_random = rng.integers(0, 3000, size=ROWS)
    duracion_dias_random = rng.integers(2, 91, size=ROWS)
    estados_random = rng.choice(ESTADOS_VIAJE, size=ROWS)
    consumos_combustible_random = rng.integers(1000, 20000, size=ROWS)
    buques_fk_random = rng.integers(0, ROWS, size=ROWS)
    
    # base date for generating random dates in YYYY-MM-DD format
    base_date = datetime(2020, 1, 1)

    with open(filename, "w", encoding="utf-8") as f:
        f.write("codigo,fecha_estimada_salida,fecha_estimada_llegada,estado,consumo_combustible,buque_numero_omi\n")
        for i in range(ROWS):
            codigo = f"V{i:09d}"
            
            # Garantizar que fecha_llegada >= fecha_salida
            dias_salida = int(dias_salida_random[i])
            duracion_dias = int(duracion_dias_random[i])
            fecha_salida = base_date + timedelta(days=dias_salida)
            fecha_llegada = fecha_salida + timedelta(days=duracion_dias)
            
            estado = estados_random[i]
            consumo_combustible = consumos_combustible_random[i]
            
            # FK to a Buque existing
            buque_id = buques_fk_random[i]
            buque_numero_omi = OMI_BASE + buque_id
            
            f.write(f"{codigo},{fecha_salida.strftime('%Y-%m-%d')},{fecha_llegada.strftime('%Y-%m-%d')},{estado},{consumo_combustible},{buque_numero_omi}\n")
    print(f"Creado: {filename} ({ROWS:,} filas)")


def create_mercancias():
    filename = os.path.join(OUTPUT_DIR, "mercancia.csv")
    
    # pregenerate all the random values
    descripciones_random = rng.choice(DESCRIPCIONES_MERCANCIA, size=ROWS)
    pesos_random = rng.integers(100.0, 50000.0, size=ROWS)
    volumenes_random = rng.integers(1.0, 200.0, size=ROWS)
    paises_random = rng.choice(PAISES, size=ROWS)
    viajes_fk_random = rng.integers(0, ROWS, size=ROWS)
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write("codigo,descripcion,peso_bruto,volumen,pais_origen,codigo_viaje\n")
        for i in range(ROWS):
            codigo = f"M{i:09d}"
            descripcion = descripciones_random[i]
            peso_bruto = pesos_random[i]
            volumen = volumenes_random[i]
            pais_origen = paises_random[i]
            
            # FK to a Viaje existing
            viaje_id = viajes_fk_random[i]
            codigo_viaje = f"V{viaje_id:09d}"
            
            f.write(f"{codigo},{descripcion},{peso_bruto},{volumen},{pais_origen},{codigo_viaje}\n")
    print(f"Creado: {filename} ({ROWS:,} filas)")