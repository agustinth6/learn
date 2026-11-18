-- ============================================================
--  FIX: ERROR 1452 al insertar en `alquileres`
--  Causa: los id_pelicula reales NO son 1..6 (el AUTO_INCREMENT
--  no se reinicia tras un INSERT fallido), así que (1,1,...)
--  apunta a una película que no existe.
-- ============================================================

-- 1) DIAGNÓSTICO: ver los IDs reales
SELECT id_pelicula, titulo, id_actor FROM peliculas;
SELECT id_cliente, nombre, apellido FROM clientes;

-- ============================================================
--  OPCIÓN A — la correcta para el parcial: IDs limpios 1..6
--  (se puede porque alquileres está vacío)
-- ============================================================

-- 1.0 Si el DELETE tira ERROR 1175 (safe update mode de Workbench):
SET SQL_SAFE_UPDATES = 0;

-- 1.1 vaciar alquileres (sin WHERE borra todas las filas, no la tabla)
DELETE FROM alquileres;
-- alternativa que además reinicia el contador:
-- TRUNCATE TABLE alquileres;

-- 1.2 borrar películas y reiniciar el contador
DELETE FROM peliculas;
ALTER TABLE peliculas AUTO_INCREMENT = 1;

-- 1.3 reinsertar las 6 películas → ahora sí quedan 1..6
INSERT INTO peliculas (titulo, genero, anio_estreno, id_actor) VALUES
('Titanic',     'Romance',         1997, 1),
('Inception',   'Ciencia Ficción', 2010, 1),
('Matrix',      'Acción',          2003, 2),
('John Wick',   'Acción',          2019, 2),
('La La Land',  'Musical',         2016, 3),
('Cruella',     'Comedia',         2021, 3);

-- 1.4 verificar que quedaron 1..6 ANTES de insertar alquileres
SELECT id_pelicula, titulo FROM peliculas ORDER BY id_pelicula;

-- 1.5 ahora sí
INSERT INTO alquileres (id_pelicula, id_cliente, fecha_alquiler, dias_alquilada) VALUES
(1, 1, '2025-01-02', 5),
(2, 1, '2025-02-10', 3),
(3, 2, '2025-01-15', 7),
(4, 3, '2025-03-01', 2),
(5, 4, '2025-03-10', 4),
(6, 5, '2025-04-05', 6),
(3, 6, '2025-04-12', 3),
(2, 7, '2025-02-22', 5),
(1, 8, '2025-03-14', 2),
(4, 5, '2025-05-05', 4),
(5, 2, '2025-05-10', 6),
(6, 1, '2025-06-01', 7);

-- ============================================================
--  OPCIÓN B — sin tocar los IDs: insertar buscando por título
--  Cada fila se arma con una subconsulta, así no importa
--  qué número tiene cada película.
-- ============================================================

-- INSERT INTO alquileres (id_pelicula, id_cliente, fecha_alquiler, dias_alquilada)
-- SELECT p.id_pelicula, c.id_cliente, '2025-01-02', 5
-- FROM peliculas p, clientes c
-- WHERE p.titulo = 'Titanic' AND c.nombre = 'Laura' AND c.apellido = 'Gómez';
--
-- ... y así con cada uno de los 12 alquileres.

-- ============================================================
--  VERIFICACIÓN FINAL
-- ============================================================
SELECT COUNT(*) AS alquileres_cargados FROM alquileres;   -- debe dar 12

SELECT al.id_alquiler, p.titulo, c.nombre, c.apellido, al.fecha_alquiler, al.dias_alquilada
FROM alquileres al
INNER JOIN peliculas p ON al.id_pelicula = p.id_pelicula
INNER JOIN clientes  c ON al.id_cliente  = c.id_cliente
ORDER BY al.id_alquiler;
