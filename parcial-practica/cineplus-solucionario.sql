-- ============================================================
--  SOLUCIONARIO — Modelo Segundo Parcial CinePlus
--  Sintaxis MySQL (Workbench). Datos verificados con las
--  12 filas de alquileres del enunciado.
-- ============================================================

-- ============================================================
--  EJERCICIO 1 y 2 — Base de datos y DDL
-- ============================================================

CREATE DATABASE cineplus;
USE cineplus;

CREATE TABLE actores (
    id_actor     INT PRIMARY KEY AUTO_INCREMENT,
    nombre       VARCHAR(100) NOT NULL,
    nacionalidad VARCHAR(100) NOT NULL
);

CREATE TABLE peliculas (
    id_pelicula  INT PRIMARY KEY AUTO_INCREMENT,
    titulo       VARCHAR(100) NOT NULL UNIQUE,
    genero       VARCHAR(50)  NOT NULL,     -- ver nota: UNIQUE en el PDF es un error
    anio_estreno INT          NOT NULL,
    id_actor     INT          NOT NULL,
    CONSTRAINT fk_peliculas_actores
        FOREIGN KEY (id_actor) REFERENCES actores(id_actor)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE clientes (
    id_cliente INT PRIMARY KEY AUTO_INCREMENT,
    nombre     VARCHAR(100) NOT NULL,
    apellido   VARCHAR(100) NOT NULL,
    ciudad     VARCHAR(100) NOT NULL
);

CREATE TABLE alquileres (
    id_alquiler     INT  PRIMARY KEY AUTO_INCREMENT,
    id_pelicula     INT  NOT NULL,
    id_cliente      INT  NOT NULL,
    fecha_alquiler  DATE NOT NULL,
    dias_alquilada  INT  NOT NULL,
    CONSTRAINT fk_alquileres_peliculas
        FOREIGN KEY (id_pelicula) REFERENCES peliculas(id_pelicula)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_alquileres_clientes
        FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- ============================================================
--  EJERCICIO 3 — DML
--  (los INSERT son los del enunciado, en este orden: el orden
--   importa porque los IDs referenciados son 1,2,3...)
-- ============================================================

INSERT INTO actores (nombre, nacionalidad) VALUES
('Leonardo DiCaprio', 'Estadounidense'),
('Keanu Reeves',      'Canadiense'),
('Emma Stone',        'Estadounidense');

INSERT INTO peliculas (titulo, genero, anio_estreno, id_actor) VALUES
('Titanic',     'Romance',         1997, 1),
('Inception',   'Ciencia Ficción', 2010, 1),
('Matrix',      'Acción',          2003, 2),
('John Wick',   'Acción',          2019, 2),
('La La Land',  'Musical',         2016, 3),
('Cruella',     'Comedia',         2021, 3);

INSERT INTO clientes (nombre, apellido, ciudad) VALUES
('Laura',    'Gómez',     'Buenos Aires'),
('Carlos',   'Pérez',     'Rosario'),
('Ana',      'Martínez',  'Córdoba'),
('Lucía',    'Fernández', 'Mendoza'),
('Santiago', 'Ramos',     'Salta'),
('María',    'López',     'Tucumán'),
('Pedro',    'García',    'La Plata'),
('Sofía',    'Ruiz',      'Mar del Plata');

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
--  CONSULTAS SIMPLES
-- ============================================================

-- 1. Todas las películas  → 6 filas
SELECT * FROM peliculas;

-- 2. Actores ordenados por nombre  → Emma, Keanu, Leonardo
SELECT * FROM actores
ORDER BY nombre ASC;

-- 3. Estrenadas después de 2018  → John Wick (2019), Cruella (2021)
SELECT * FROM peliculas
WHERE anio_estreno > 2018;

-- 4. Alquileres de Laura Gómez
--    Opción A (la más directa): buscando por id
SELECT * FROM alquileres
WHERE id_cliente = 1;

--    Opción B (más robusta, y la que espera el profe): por nombre y apellido
SELECT a.*
FROM alquileres a
INNER JOIN clientes c ON a.id_cliente = c.id_cliente
WHERE c.nombre = 'Laura' AND c.apellido = 'Gómez';
-- → 3 filas: (1, Laura, '2025-01-02'), (2, '2025-02-10'), (6, '2025-06-01')

-- 5. Género Acción o Comedia  → Matrix, John Wick, Cruella
SELECT * FROM peliculas
WHERE genero IN ('Acción', 'Comedia');

--    Equivalente con OR:
SELECT * FROM peliculas
WHERE genero = 'Acción' OR genero = 'Comedia';

-- ============================================================
--  ALTER / UPDATE / DELETE
-- ============================================================

-- 6.
ALTER TABLE clientes ADD COLUMN email VARCHAR(100);

-- 7. (el enunciado da 1999; el año real de Matrix es 1999, el INSERT dice 2003)
UPDATE peliculas
SET anio_estreno = 1999
WHERE titulo = 'Matrix';

-- 8. Alquiler puntual por id (ejemplo: el 12)
DELETE FROM alquileres
WHERE id_alquiler = 12;

-- 9. CHANGE: nombre viejo, nombre nuevo y tipo, SIN coma en el medio
ALTER TABLE clientes
CHANGE ciudad localidad VARCHAR(100);

--    Alternativa (MySQL 8+), más explícita:
-- ALTER TABLE clientes RENAME COLUMN ciudad TO localidad;

-- ============================================================
--  JOIN
-- ============================================================

-- 10. Cliente + película + actor principal  → 12 filas
SELECT c.nombre, c.apellido, p.titulo, ac.nombre AS actor_principal
FROM alquileres al
INNER JOIN clientes  c  ON al.id_cliente  = c.id_cliente
INNER JOIN peliculas p  ON al.id_pelicula = p.id_pelicula
INNER JOIN actores   ac ON p.id_actor     = ac.id_actor;

-- 11. Todas las películas con su actor  → 6 filas
SELECT p.titulo, ac.nombre AS actor_principal
FROM peliculas p
INNER JOIN actores ac ON p.id_actor = ac.id_actor;

-- 12. Clientes que alquilaron películas de Leonardo DiCaprio
--     → Laura Gómez, Pedro García, Sofía Ruiz
SELECT DISTINCT c.nombre, c.apellido
FROM clientes c
INNER JOIN alquileres al ON c.id_cliente  = al.id_cliente
INNER JOIN peliculas  p  ON al.id_pelicula = p.id_pelicula
INNER JOIN actores    ac ON p.id_actor     = ac.id_actor
WHERE ac.nombre = 'Leonardo DiCaprio';

-- ============================================================
--  GROUP BY
-- ============================================================

-- 13. Películas por género  → Acción 2, y 1 de cada uno de los otros 4
SELECT genero, COUNT(*) AS cantidad_peliculas
FROM peliculas
GROUP BY genero;

-- 14. Promedio de días de alquiler por cliente  → 8 filas
SELECT c.nombre, c.apellido,
       AVG(al.dias_alquilada) AS promedio_dias
FROM clientes c
INNER JOIN alquileres al ON c.id_cliente = al.id_cliente
GROUP BY c.id_cliente, c.nombre, c.apellido;

--    Con redondeo y ordenado, más presentable:
SELECT c.nombre, c.apellido,
       ROUND(AVG(al.dias_alquilada), 2) AS promedio_dias
FROM clientes c
INNER JOIN alquileres al ON c.id_cliente = al.id_cliente
GROUP BY c.id_cliente, c.nombre, c.apellido
ORDER BY promedio_dias DESC;

-- 15. Cuántas veces fue alquilada cada película
--     Todas fueron alquiladas 2 veces con estos datos.
SELECT p.titulo, COUNT(al.id_alquiler) AS veces_alquilada
FROM peliculas p
INNER JOIN alquileres al ON p.id_pelicula = al.id_pelicula
GROUP BY p.id_pelicula, p.titulo
ORDER BY veces_alquilada DESC;

--    Variante "incluye las películas nunca alquiladas (con 0)":
SELECT p.titulo, COUNT(al.id_alquiler) AS veces_alquilada
FROM peliculas p
LEFT JOIN alquileres al ON p.id_pelicula = al.id_pelicula
GROUP BY p.id_pelicula, p.titulo;

-- ============================================================
--  VISTA
-- ============================================================

-- 16.
CREATE VIEW vista_alquileres_detalle AS
SELECT c.nombre AS cliente, c.apellido, p.titulo AS pelicula
FROM alquileres al
INNER JOIN clientes  c ON al.id_cliente  = c.id_cliente
INNER JOIN peliculas p ON al.id_pelicula = p.id_pelicula;

SELECT * FROM vista_alquileres_detalle;

-- ============================================================
--  VERDADERO O FALSO
-- ============================================================
-- 1. V  — GROUP BY agrupa valores iguales y permite COUNT, AVG, SUM, MIN, MAX.
-- 2. F  — UPDATE modifica filas existentes; para insertar es INSERT.
-- 3. V  — DELETE FROM ... WHERE borra las filas que cumplen la condición.
--         (Sin WHERE borra TODAS, pero sigue siendo DELETE de filas, no de la tabla.)
-- 4. F  — eso es FULL OUTER JOIN. INNER JOIN solo devuelve las coincidencias.
-- 5. V  — la FK relaciona con la PK de la tabla padre y garantiza integridad referencial.
-- 6. V  — en muchos a muchos la tabla intermedia es obligatoria (acá: alquileres).

-- ============================================================
--  MÚLTIPLE CHOICE
-- ============================================================
-- 1. c)  Es la única que agrupa por cliente y cuenta los alquileres de ese cliente.
--        La a) cuenta todos los alquileres, no por cliente; la b) cuenta clientes.
-- 2. b)  ALTER TABLE ... ADD COLUMN.
-- 3. c)  Borra la fila de Matrix.
-- 4. c)  UPDATE.

-- ============================================================
--  NOTAS QUE VALEN PUNTOS
-- ============================================================
-- (*) ERROR 1072 "Key column 'id_actor' doesn't exist in table" al crear
--     peliculas = te olvidaste de DECLARAR la columna id_actor. La FK no crea
--     la columna: solo la marca como foránea, y tiene que existir antes en la
--     misma tabla. La columna va en la lista de columnas, la FK al final.
--
-- (*) UNIQUE en peliculas.genero es un error del modelo: como hay dos
--     películas "Acción" (Matrix y John Wick), el INSERT falla con
--     ERROR 1062 Duplicate entry 'Acción'. Si el profe insiste en el UNIQUE,
--     hay que cambiar los géneros a valores distintos. Lo correcto es sacarlo
--     (o poner UNIQUE en una tabla generos aparte).
--
-- (*) peliculas.genero y clientes.ciudad son NOT NULL: nada de NULL ahí.
--
-- (*) Los IDs se generan por AUTO_INCREMENT en el orden de inserción:
--     actores 1=DiCaprio, 2=Reeves, 3=Stone; películas 1..6; clientes 1..8.
--     Si se saltea un INSERT o se corre dos veces, todo deja de coincidir.
--
-- (*) El promedio da números con coma (6.5, 3.0...). En MySQL AVG devuelve
--     DECIMAL y se ve bien; en otros motores conviene ROUND(x, 2).
--
-- (*) Claves: no usar mayúsculas no descuenta, pero el orden de las cláusulas
--     sí importa: SELECT → FROM → JOIN/ON → WHERE → GROUP BY → HAVING → ORDER BY.

-- ============================================================
--  EJERCICIO 17 (EXTRA) — Borrado en cadena manual en CinePlus
--  No está en el PDF, pero el profe lo toma. Mismo patrón que
--  la base biblioteca, adaptado a 3 niveles.
-- ============================================================

-- Consigna: eliminar al actor "Keanu Reeves" (id_actor = 2),
-- todas sus películas (Matrix, John Wick) y todos los alquileres
-- de esas películas.

-- 0) Ver qué se va a borrar ANTES (siempre)
SELECT id_pelicula, titulo FROM peliculas WHERE id_actor = 2;
SELECT * FROM alquileres
WHERE id_pelicula IN (SELECT id_pelicula FROM peliculas WHERE id_actor = 2);

-- 1) PRIMERO los nietos: alquileres de esas películas
DELETE FROM alquileres
WHERE id_pelicula IN (SELECT id_pelicula FROM peliculas WHERE id_actor = 2);

-- 2) DESPUÉS los hijos: las películas del actor
DELETE FROM peliculas
WHERE id_actor = 2;

-- 3) AL FINAL el padre: el actor
DELETE FROM actores
WHERE id_actor = 2;

-- 4) Verificación: quedan 2 actores, 4 películas y 8 alquileres
SELECT * FROM actores;
SELECT id_pelicula, titulo FROM peliculas;

-- ------------------------------------------------------------
--  POR QUÉ ESE ORDEN (lo que se pregunta en el parcial):
--  Si borrás el actor primero, MySQL tira
--  ERROR 1451 Cannot delete or update a parent row:
--  a foreign key constraint fails (peliculas, FOREIGN KEY (id_actor)...)
--  porque todavía hay películas que lo referencian. Siempre se va
--  de la punta de la cadena hacia la raíz: nietos → hijos → padre.
-- ------------------------------------------------------------

-- VARIANTE con JOIN (más compacta, misma lógica):
-- DELETE al FROM alquileres al
-- INNER JOIN peliculas p ON al.id_pelicula = p.id_pelicula
-- WHERE p.id_actor = 2;

-- NOTA: si la FK se declaró con ON DELETE CASCADE, este borrado
-- manual NO hace falta: basta con
--   DELETE FROM actores WHERE id_actor = 2;
-- y MySQL arrastra películas y alquileres solo. El borrado manual
-- se pide justamente cuando NO hay cascade.

-- NOTA 2: los IDs borrados no se reutilizan; el AUTO_INCREMENT sigue.
