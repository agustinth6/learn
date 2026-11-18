# Modelo de Segundo Parcial — CinePlus

> Transcripción ordenada del PDF de cátedra. El enunciado original está en
> `MODELO DE SEGUNDO PARCIAL BD CINEPLUS.pdf`; esto es lo mismo, listo para trabajar.

## Enunciado

CinePlus gestiona un sistema de alquiler de películas online.

- Cada **cliente** puede alquilar distintas **películas**, y cada película puede ser alquilada por varios clientes → **muchos a muchos**.
- Cada **película** pertenece a **un** actor principal, y un actor puede participar en varias películas → **uno a muchos**.
- `alquileres` actúa como **tabla intermedia** que resuelve el muchos a muchos entre clientes y películas.

Datos a registrar: actores (nombre, nacionalidad), películas (título, género, año de estreno, actor principal), clientes (nombre, apellido, localidad) y alquileres (fecha y cantidad de días).

## Tablas

### `actores`

| Atributo | Tipo | Restricciones |
|---|---|---|
| `id_actor` | INT | PK, AUTO_INCREMENT |
| `nombre` | VARCHAR(100) | NOT NULL |
| `nacionalidad` | VARCHAR(100) | NOT NULL |

### `peliculas`

| Atributo | Tipo | Restricciones |
|---|---|---|
| `id_pelicula` | INT | PK, AUTO_INCREMENT |
| `titulo` | VARCHAR(100) | NOT NULL, UNIQUE |
| `genero` | VARCHAR(50) | NOT NULL, UNIQUE |
| `anio_estreno` | INT | NOT NULL |
| `id_actor` | INT | FK → `actores.id_actor`, NOT NULL |

### `clientes`

| Atributo | Tipo | Restricciones |
|---|---|---|
| `id_cliente` | INT | PK, AUTO_INCREMENT |
| `nombre` | VARCHAR(100) | NOT NULL |
| `apellido` | VARCHAR(100) | NOT NULL |
| `ciudad` | VARCHAR(100) | NOT NULL |

### `alquileres`

| Atributo | Tipo | Restricciones |
|---|---|---|
| `id_alquiler` | INT | PK, AUTO_INCREMENT |
| `id_pelicula` | INT | FK → `peliculas.id_pelicula`, NOT NULL |
| `id_cliente` | INT | FK → `clientes.id_cliente`, NOT NULL |
| `fecha_alquiler` | DATE | NOT NULL |
| `dias_alquilada` | INT | NOT NULL |

## Datos a insertar

```sql
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
```

## Instrucciones

1. Crear la base de datos `cineplus`.
2. Crear las 4 tablas con sus PK y FK (DDL).
3. Insertar los datos: 3 actores, 6 películas, 8 clientes, 12 alquileres.

## Consultas

### Simples
1. Mostrar todas las películas registradas.
2. Listar los actores ordenados por nombre.
3. Mostrar las películas estrenadas después del año 2018.
4. Mostrar los alquileres realizados por el cliente "Laura Gómez".
5. Mostrar las películas de género "Acción" o "Comedia".

### ALTER / UPDATE / DELETE
6. Agregar una columna `email` a la tabla `clientes`.
7. Actualizar el año de estreno de la película "Matrix" a 1999.
8. Eliminar un alquiler específico por su id.
9. Cambiar el nombre de la columna `ciudad` en `clientes` a `localidad`.

### JOIN
10. Mostrar el nombre del cliente, el título de la película y el actor principal.
11. Mostrar todas las películas con su actor.
12. Mostrar los clientes que alquilaron películas del actor "Leonardo DiCaprio".

### GROUP BY
13. Mostrar cuántas películas hay de cada género.
14. Promedio de días que cada cliente alquila las películas.
15. Cuántas veces fue alquilada cada película.

### Vista
16. Crear una vista `vista_alquileres_detalle` que muestre el nombre del cliente y la película alquilada.

## Verdadero o Falso

1. La cláusula `GROUP BY` se utiliza para agrupar registros con valores iguales y aplicar funciones de agregación como `COUNT` o `AVG`.
2. El comando `UPDATE` sirve para insertar nuevos registros en una tabla.
3. La sentencia `DELETE FROM` borra filas específicas según una condición.
4. `INNER JOIN` muestra todos los registros de ambas tablas, coincidan o no.
5. `FOREIGN KEY` se usa para relacionar tablas y garantizar integridad referencial.
6. En una relación muchos a muchos siempre se necesita una tabla intermedia.

## Múltiple choice

**1. ¿Cuál de las siguientes consultas muestra cuántas películas alquiló cada cliente?**

- a) `SELECT COUNT(*) FROM alquileres;`
- b) `SELECT nombre, COUNT(*) FROM clientes;`
- c) `SELECT c.nombre, COUNT(al.id_alquiler) FROM clientes c JOIN alquileres al ON c.id_cliente = al.id_cliente GROUP BY c.nombre;`
- d) `SELECT * FROM alquileres WHERE fecha_alquiler IS NOT NULL;`

**2. ¿Cuál instrucción agrega una nueva columna a una tabla existente?**

- a) `ADD COLUMN clientes email VARCHAR(100);`
- b) `ALTER TABLE clientes ADD COLUMN email VARCHAR(100);`
- c) `UPDATE TABLE clientes email VARCHAR(100);`
- d) `CREATE COLUMN email VARCHAR(100);`

**3. ¿Qué hace `DELETE FROM peliculas WHERE titulo = 'Matrix';`?**

- a) Borra la base de datos completa.
- b) Actualiza el registro de Matrix.
- c) Borra la película "Matrix" de la tabla.
- d) Cambia el nombre de la película.

**4. ¿Qué comando se usa para modificar datos existentes?**

- a) `INSERT`　b) `ALTER`　c) `UPDATE`　d) `SELECT`
