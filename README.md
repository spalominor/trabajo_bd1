# Benchmark de Rendimiento: PostgreSQL vs. MySQL con Python & Polars

Este proyecto realiza un análisis comparativo de rendimiento entre PostgreSQL y MySQL ejecutados sobre contenedores Podman. Evalúa los tiempos de inserción masiva a distintas escalas ($1, 10, 100$ y $100.000$ filas) utilizando comandos nativos (`COPY FROM STDIN` y `LOAD DATA LOCAL INFILE`), así como la latencia de respuesta en consultas SQL nativas comparadas contra un motor de procesamiento en memoria con Polars.

---

## 🛠️ Requisitos Previos

Asegúrate de contar con lo siguiente instalado en tu sistema:
* **Python 3.10+**
* **Podman** y **Podman Compose** (o Docker / Docker Compose)
* **Git**

---

## 🚀 Replicación del Proyecto Paso a Paso

### 1. Clonar el repositorio
```bash
git clone https://github.com/spalominor/trabajo_bd1.git
cd trabajo_bd1

# Crear el entorno virtual
python3 -m venv .venv

# Activar el entorno virtual (Linux/Mac)
source .venv/bin/activate

# Actualizar pip e instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# Copiar el archivo .env (si deseas puedes ajustar usuarios, puertos o contraseñas)
cp .env.example .env

# Levantar los servicios de PostgreSQL y MySQL (podman ó docker)
podman-compose up -d

# Ejecutar el benchmark
python3 main.py
```