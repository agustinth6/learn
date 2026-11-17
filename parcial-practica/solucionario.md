# Solucionario — Práctica de parcial

> Usar después de intentar el enunciado completo. Primero comparar resultados; recién después mirar el código.

---

## Parte 1 — Estructura

```sql
CREATE DATABASE idiomas;
USE idiomas;

CREATE TABLE profesores (
    id_profesor     INT PRIMARY KEY AUTO_INCREMENT,
    nombre          VARCHAR(50)  NOT NULL,
    email           VARCHAR(100) NOT NULL UNIQUE,
    idioma_nativo   VARCHAR(30),
    activo          ENUM('si','no') DEFAULT 'si'
);

CREATE TABLE cursos (
    id_curso        INT PRIMARY KEY AUTO_INCREMENT,
    nombre_curso    VARCHAR(60)  NOT NULL,
    nivel           VARCHAR(20)  NOT NULL,
    duracion_meses  INT          NOT NULL,
    precio          DECIMAL(10,2) NOT NULL,
    id_profesor     INT,
    CONSTRAINT fk_cursos_profesores
        FOREIGN KEY (id_profesor) REFERENCES profesores(id_profesor)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE inscripciones (
    id_inscripcion    INT PRIMARY KEY AUTO_INCREMENT,
    id_curso          INT,
    alumno            VARCHAR(60) NOT NULL,
    fecha_inscripcion DATE        NOT NULL,
    estado            ENUM('activo','finalizado','abandonó') DEFAULT 'activo',
    CONSTRAINT fk_inscripciones_cursos
        FOREIGN KEY (id_curso) REFERENCES cursos(id_curso)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
```

**Puntos que se miran:** `DECIMAL(10,2)` (no `FLOAT`), `ENUM` con las opciones exactas, `DEFAULT` separado de `NOT NULL`, la FK con nombre y los dos `CASCADE`, y la coma entre columnas salvo antes de la constraint.

### Carga de datos

```sql
INSERT INTO profesores (nombre, email, idioma_nativo, activo) VALUES
('Lucía Ferreyra', 'lucia@idiomas.com', 'inglés',   'si'),
('Marco Rossi',   'marco@idiomas.com', 'italiano', 'si'),
('Sofía Duarte',  'sofia@idiomas.com', 'portugués','no');

INSERT INTO cursos (nombre_curso, nivel, duracion_meses, precio, id_profesor) VALUES
('Inglés general',   'básico',      4, 25000.00, 1),
('Inglés conversación','intermedio',6, 38000.00, 1),
('Italiano general', 'básico',      4, 24000.00, 2),
('Portugués general','avanzado',    8, 42000.00, 3);

INSERT INTO inscripciones (id_curso, alumno, fecha_inscripcion, estado) VALUES
(1, 'Ana Pérez',    '2025-03-04', 'activo'),
(1, 'Luis Gómez',   '2025-03-05', 'finalizado'),
(2, 'Ana Pérez',    '2025-04-01', 'activo'),
(3, 'Carla Núñez',  '2025-04-12', 'abandonó'),
(4, 'Diego Salas',  '2025-05-02', 'activo');
```

> No hace falta poner los IDs: al ser `AUTO_INCREMENT` se generan solos **en el orden de inserción** (1, 2, 3…). Por eso `id_profesor = 1` es Lucía.

### Pruebas de restricciones

```sql
-- Debe fallar: el email ya existe  →  ERROR 1062 (23000): Duplicate entry 'lucia@idiomas.com' for key 'email'
INSERT INTO profesores (nombre, email, idioma_nativo)
VALUES ('Otro Profe', 'lucia@idiomas.com', 'francés');

-- Debe fallar: el curso 99 no existe  →  ERROR 1452 (23000): Cannot add or update a child row: a foreign key constraint fails
INSERT INTO inscripciones (id_curso, alumno, fecha_inscripcion)
VALUES (99, 'Nadie', '2025-06-01');
```

---

## Parte 2 — Consultas sobre `biblioteca`

### 2.1 Consultas simples

```sql
-- 1
SELECT titulo, anio_publicacion
FROM libros
WHERE anio_publicacion > 1970
ORDER BY anio_publicacion DESC;

-- 2  (NULL no se compara con =, se compara con IS NULL)
SELECT lector, fecha_prestamo, id_libro
FROM prestamos
WHERE fecha_devolucion IS NULL;

-- 3
SELECT titulo, genero
FROM libros
WHERE genero IN ('fantasía', 'ficción');

-- 4
SELECT titulo
FROM libros
WHERE titulo LIKE '%la%';

-- 5
SELECT nombre, nacionalidad
FROM autores
WHERE nacionalidad = 'argentina';
```

**Errores típicos acá:** `WHERE fecha_devolucion = NULL` (no devuelve nada, siempre falso); usar `OR` mal paréntesis cuando se combina con `AND`; escribir `'fantasia'` sin acento cuando los datos tienen `'fantasía'`.

### 2.2 Agregación

```sql
-- 6
SELECT COUNT(*) AS total_libros FROM libros;

-- 7
SELECT genero, COUNT(*) AS cantidad
FROM libros
GROUP BY genero
ORDER BY cantidad DESC;

-- 8
SELECT ROUND(AVG(anio_publicacion), 2) AS promedio_anio FROM libros;

-- 9  (filtrar grupos, no filas: por eso HAVING)
SELECT l.titulo, COUNT(p.id_prestamo) AS cantidad_prestamos
FROM libros l
INNER JOIN prestamos p ON l.id_libro = p.id_libro
GROUP BY l.id_libro, l.titulo
HAVING COUNT(p.id_prestamo) > 1;
```

En el 9, `WHERE COUNT(...) > 1` da error: `COUNT` es una función de agregación y se filtra con `HAVING`. Además conviene agrupar por `l.id_libro` (la PK) y no solo por `titulo`, para que dos libros con el mismo título no se mezclen.

### 2.3 JOIN

```sql
-- 10
SELECT l.titulo, a.nombre AS autor
FROM libros l
INNER JOIN autores a ON l.id_autor = a.id_autor;

-- 11
SELECT l.titulo, p.lector, p.fecha_prestamo
FROM prestamos p
INNER JOIN libros l ON p.id_libro = l.id_libro
WHERE p.fecha_devolucion IS NULL;

-- 12
SELECT l.titulo, p.lector, a.nombre AS autor
FROM prestamos p
INNER JOIN libros  l ON p.id_libro  = l.id_libro
INNER JOIN autores a ON l.id_autor  = a.id_autor
WHERE p.fecha_devolucion IS NULL;

-- 13
SELECT a.nombre
FROM autores a
LEFT JOIN libros l ON a.id_autor = l.id_autor
WHERE l.id_libro IS NULL;
```

En el 13 el `LEFT JOIN` deja las filas del autor aunque no tenga libros; las que no matchean quedan con las columnas de `libros` en `NULL`, y eso es justamente lo que se filtra. Si con los datos cargados **todos** los autores tienen libros, el resultado es una tabla vacía: eso también es una respuesta correcta.

En el 12 el orden importa: primero se une `prestamos` con `libros` (que es la relación directa), y después `libros` con `autores`. Si se arranca por `autores` también funciona, pero hay que encadenar las tres igual.

### 2.4 Modificación

```sql
-- 14
ALTER TABLE autores ADD COLUMN anio_nacimiento INT;

-- 15  (UPDATE siempre con WHERE: sin él se actualizan todas las filas)
UPDATE libros
SET anio_publicacion = 1964
WHERE titulo = 'Rayuela';

-- 16  (CHANGE lleva el nombre viejo, el nuevo y el tipo, SIN coma en el medio)
ALTER TABLE prestamos
CHANGE nombre_lector lector VARCHAR(50);
```

Ojo con el 16: la coma entre `nombre_lector` y `lector` es un error de sintaxis; el `CHANGE` va todo seguido. Y si otra consulta o vista usaba `nombre_lector`, deja de funcionar hasta que se la actualice.

### 2.5 Borrado en cadena manual

```sql
-- 1) primero los hijos de los hijos
DELETE FROM prestamos
WHERE id_libro IN (SELECT id_libro FROM libros WHERE id_autor = 3);

-- 2) después los hijos
DELETE FROM libros WHERE id_autor = 3;

-- 3) al final el padre
DELETE FROM autores WHERE id_autor = 3;
```

**Por qué ese orden:** la FK `prestamos.id_libro → libros.id_libro` y `libros.id_autor → autores.id_autor` impiden borrar una fila que todavía tiene hijos ("cannot delete or update a parent row"). Hay que ir de la punta de la cadena hacia la raíz: nietos → hijos → padre. Si al borrar el autor todavía quedaran libros suyos, el borrado falla, y borrar los préstamos después no arregla nada.

También sirve sin subconsulta, buscando primero los libros del autor a mano:

```sql
SELECT id_libro FROM libros WHERE id_autor = 3;   -- paso previo
DELETE FROM prestamos WHERE id_libro IN (3, 12);  -- los IDs que devolvió
```

> Los IDs borrados **no se reutilizan**: el `AUTO_INCREMENT` sigue avanzando.

### 2.6 Vista

```sql
CREATE VIEW vista_prestamos_pendientes AS
SELECT l.titulo, p.lector, p.fecha_prestamo
FROM prestamos p
INNER JOIN libros l ON p.id_libro = l.id_libro
WHERE p.fecha_devolucion IS NULL;

SELECT * FROM vista_prestamos_pendientes;
```

Para **modificar** una vista existente no existe un `ALTER VIEW` cómodo: hay que borrarla y volver a crearla.

```sql
DROP VIEW vista_prestamos_pendientes;
-- y después el CREATE VIEW ... con la columna nueva
```

---

## Autoevaluación rápida

| Si te pasó esto | Repasar |
|---|---|
| `= NULL` en vez de `IS NULL` | 6.3 (y 2.4 para NULL) y 6.4 (`LIKE`) |
| `WHERE COUNT(*)` | 10.1 / 10.3 (`WHERE` filas vs `HAVING` grupos) |
| olvidaste el `FROM` en `DELETE` | 8.4 |
| coma dentro del `CHANGE` | 8.3 |
| borraste el padre primero | 8.5 (borrado manual en cadena) |
| `INNER JOIN` donde pedían `LEFT` | 9.4 / 9.5 |
| `UPDATE` sin `WHERE` | 8.1 y 8.2 |
