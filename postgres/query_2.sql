SELECT N.nombre AS naviera, B.bandera AS bandera, count(V.codigo) AS total_viajes
FROM NAVIERA N
JOIN BUQUE B ON N.nombre = B.nombre_naviera
JOIN VIAJE V ON B.numero_omi = V.buque_numero_omi
GROUP BY N.nombre, B.bandera
ORDER BY count(V.codigo) DESC;