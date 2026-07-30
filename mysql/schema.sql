CREATE TABLE IF NOT EXISTS naviera (
    nombre VARCHAR(20) NOT NULL,
    pais_registro VARCHAR(20) NOT NULL,
    certificacion_solas BOOLEAN NOT NULL,
    certificacion_ism BOOLEAN NOT NULL,
    CONSTRAINT PK_NAVIERA PRIMARY KEY (nombre)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS buque (
    numero_omi INT UNSIGNED NOT NULL,
    nombre VARCHAR(20) NOT NULL,
    bandera VARCHAR(20) NOT NULL,
    anio_construccion SMALLINT UNSIGNED NOT NULL,
    capacidad_teu INT UNSIGNED NOT NULL,
    eslora SMALLINT UNSIGNED NOT NULL,
    manga SMALLINT UNSIGNED NOT NULL,
    calado_maximo SMALLINT UNSIGNED NOT NULL,
    nombre_naviera VARCHAR(20) NOT NULL,
    CONSTRAINT PK_BUQUE PRIMARY KEY (numero_omi),
    CONSTRAINT FK_BUQUE_NAVIERA FOREIGN KEY (nombre_naviera) 
        REFERENCES NAVIERA (nombre) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT CK_BUQUE_ANIO CHECK (anio_construccion >= 1800),
    CONSTRAINT CK_BUQUE_TEU CHECK (capacidad_teu >= 0),
    CONSTRAINT CK_BUQUE_ESLORA CHECK (eslora > 0),
    CONSTRAINT CK_BUQUE_MANGA CHECK (manga > 0),
    CONSTRAINT CK_BUQUE_CALADO CHECK (calado_maximo > 0)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS viaje (
    codigo CHAR(10) NOT NULL,
    fecha_estimada_salida DATE NOT NULL,
    fecha_estimada_llegada DATE NOT NULL,
    estado VARCHAR(20) NOT NULL,
    consumo_combustible INT UNSIGNED NOT NULL,
    buque_numero_omi INT UNSIGNED NOT NULL,
    CONSTRAINT PK_VIAJE PRIMARY KEY (codigo),
    CONSTRAINT FK_VIAJE_BUQUE FOREIGN KEY (buque_numero_omi) 
        REFERENCES BUQUE (numero_omi) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT CK_VIAJE_FECHAS CHECK (fecha_estimada_llegada >= fecha_estimada_salida),
    CONSTRAINT CK_VIAJE_CONSUMO CHECK (consumo_combustible >= 0)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS mercancia (
    codigo CHAR(10) NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    peso_bruto INT UNSIGNED NOT NULL,
    volumen INT UNSIGNED NOT NULL,
    pais_origen VARCHAR(20) NOT NULL,
    codigo_viaje CHAR(10) NOT NULL,
    CONSTRAINT PK_MERCANCIA PRIMARY KEY (codigo),
    CONSTRAINT FK_MERCANCIA_VIAJE FOREIGN KEY (codigo_viaje) 
        REFERENCES VIAJE (codigo) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT CK_MERCANCIA_PESO CHECK (peso_bruto > 0),
    CONSTRAINT CK_MERCANCIA_VOLUMEN CHECK (volumen > 0)
) ENGINE=InnoDB;