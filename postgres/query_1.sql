SELECT N.nombre, B.nombre, V.codigo, V.estado, V.fecha_estimada_salida
FROM NAVIERA N
JOIN BUQUE B ON N.nombre = B.nombre_naviera
JOIN VIAJE V ON B.numero_omi = V.buque_numero_omi;