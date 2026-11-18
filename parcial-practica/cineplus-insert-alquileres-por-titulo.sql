-- ============================================================
--  INSERT de alquileres que NO depende de los IDs
--  Sirve aunque las películas sean 7..12 o cualquier otro número.
--  Busca cada película por título y cada cliente por nombre+apellido.
--  Probado: inserta 12 filas con IDs desplazados.
-- ============================================================

-- 0) Ver el estado real antes de tocar nada
SELECT id_pelicula, titulo FROM peliculas ORDER BY id_pelicula;
SELECT id_cliente, nombre, apellido FROM clientes ORDER BY id_cliente;
SELECT COUNT(*) AS alquileres_actuales FROM alquileres;

-- 1) Vaciar alquileres si quedó algo (si tira ERROR 1175, correr la línea de abajo)
SET SQL_SAFE_UPDATES = 0;
DELETE FROM alquileres;

-- 2) Insertar los 12 alquileres resolviendo los IDs por nombre
INSERT INTO alquileres (id_pelicula, id_cliente, fecha_alquiler, dias_alquilada)
SELECT p.id_pelicula, c.id_cliente, d.fecha, d.dias
FROM (
    SELECT 'Titanic'     AS titulo, 'Laura'    AS nombre, 'Gómez'     AS apellido, '2025-01-02' AS fecha, 5 AS dias
    UNION ALL SELECT 'Inception',   'Laura',    'Gómez',     '2025-02-10', 3
    UNION ALL SELECT 'Matrix',      'Carlos',   'Pérez',     '2025-01-15', 7
    UNION ALL SELECT 'John Wick',   'Ana',      'Martínez',  '2025-03-01', 2
    UNION ALL SELECT 'La La Land',  'Lucía',    'Fernández', '2025-03-10', 4
    UNION ALL SELECT 'Cruella',     'Santiago', 'Ramos',     '2025-04-05', 6
    UNION ALL SELECT 'Matrix',      'María',    'López',     '2025-04-12', 3
    UNION ALL SELECT 'Inception',   'Pedro',    'García',    '2025-02-22', 5
    UNION ALL SELECT 'Titanic',     'Sofía',    'Ruiz',      '2025-03-14', 2
    UNION ALL SELECT 'John Wick',   'Santiago', 'Ramos',     '2025-05-05', 4
    UNION ALL SELECT 'La La Land',  'Carlos',   'Pérez',     '2025-05-10', 6
    UNION ALL SELECT 'Cruella',     'Laura',    'Gómez',     '2025-06-01', 7
) d
JOIN peliculas p ON p.titulo = d.titulo
JOIN clientes  c ON c.nombre = d.nombre AND c.apellido = d.apellido;

-- 3) Verificar: tiene que dar 12
SELECT COUNT(*) AS alquileres_cargados FROM alquileres;

-- 4) Ver el detalle legible
SELECT al.id_alquiler, p.titulo, c.nombre, c.apellido, al.fecha_alquiler, al.dias_alquilada
FROM alquileres al
INNER JOIN peliculas p ON al.id_pelicula = p.id_pelicula
INNER JOIN clientes  c ON al.id_cliente  = c.id_cliente
ORDER BY al.id_alquiler;

-- ------------------------------------------------------------
--  Si el paso 2 devuelve MENOS de 12 filas, algún título o
--  nombre no coincide exactamente (acentos, mayúsculas, espacios).
--  Diagnóstico:
--
--  SELECT titulo FROM peliculas WHERE titulo LIKE '%wick%';
--  SELECT nombre, apellido FROM clientes WHERE nombre LIKE '%sof%';
-- ------------------------------------------------------------
