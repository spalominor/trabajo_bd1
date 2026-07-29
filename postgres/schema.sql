CREATE TABLE NAVIERA (
    nombre VARCHAR(100) NOT NULL,
    pais_registro VARCHAR(100) NOT NULL,
    certificacion_solas BOOLEAN NOT NULL,
    certificacion_ism BOOLEAN NOT NULL,
    CONSTRAINT PK_NAVIERA PRIMARY KEY (nombre)
);

CREATE TABLE BUQUE (
    numero_omi INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    bandera VARCHAR(100) NOT NULL,
    anio_construccion INT NOT NULL,
    capacidad_teu INT NOT NULL,
    eslora NUMERIC(6, 2) NOT NULL,
    manga NUMERIC(6, 2) NOT NULL,
    calado_maximo NUMERIC(6, 2) NOT NULL,
    nombre_naviera VARCHAR(100) NOT NULL,
    CONSTRAINT PK_BUQUE PRIMARY KEY (numero_omi),
    CONSTRAINT FK_BUQUE_NAVIERA FOREIGN KEY (nombre_naviera) 
        REFERENCES NAVIERA (nombre) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT CK_BUQUE_ANIO CHECK (anio_construccion >= 1800),
    CONSTRAINT CK_BUQUE_TEU CHECK (capacidad_teu >= 0),
    CONSTRAINT CK_BUQUE_ESLORA CHECK (eslora > 0),
    CONSTRAINT CK_BUQUE_MANGA CHECK (manga > 0),
    CONSTRAINT CK_BUQUE_CALADO CHECK (calado_maximo > 0)
);

CREATE TABLE VIAJE (
    codigo VARCHAR(50) NOT NULL,
    fecha_estimada_salida TIMESTAMP NOT NULL,
    fecha_estimada_llegada TIMESTAMP NOT NULL,
    estado VARCHAR(30) NOT NULL,
    consumo_combustible NUMERIC(10, 2) NOT NULL,
    buque_numero_omi INT NOT NULL,
    CONSTRAINT PK_VIAJE PRIMARY KEY (codigo),
    CONSTRAINT FK_VIAJE_BUQUE FOREIGN KEY (buque_numero_omi) 
        REFERENCES BUQUE (numero_omi) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT CK_VIAJE_FECHAS CHECK (fecha_estimada_llegada >= fecha_estimada_salida),
    CONSTRAINT CK_VIAJE_CONSUMO CHECK (consumo_combustible >= 0)
);

CREATE TABLE MERCANCIA (
    codigo VARCHAR(50) NOT NULL,
    descripcion TEXT NOT NULL,
    peso_bruto NUMERIC(10, 2) NOT NULL,
    volumen NUMERIC(10, 2) NOT NULL,
    pais_origen VARCHAR(100) NOT NULL,
    codigo_viaje VARCHAR(50) NOT NULL,
    CONSTRAINT PK_MERCANCIA PRIMARY KEY (codigo),
    CONSTRAINT FK_MERCANCIA_VIAJE FOREIGN KEY (codigo_viaje) 
        REFERENCES VIAJE (codigo) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT CK_MERCANCIA_PESO CHECK (peso_bruto > 0),
    CONSTRAINT CK_MERCANCIA_VOLUMEN CHECK (volumen > 0)
);