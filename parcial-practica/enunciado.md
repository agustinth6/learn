# Práctica de parcial — Administración y Gestión de Bases de Datos

**Modalidad:** individual, sin apuntes (salvo el DER impreso en la parte 2).
**Tiempo sugerido:** 100 minutos (40 para la parte 1, 60 para la parte 2).
**Entrega:** un script `.sql` por parte, en el orden de las consignas.

> Reglas de la cátedra que aplican acá:
> - No usar mayúsculas en las palabras reservadas **no descuenta**.
> - El **tipo de JOIN** que hay que usar está indicado en cada consigna.
> - `FULL JOIN` no se toma.
> - Las consultas tienen que **ejecutar sin error** y devolver exactamente lo pedido (columnas y filas).

---

## Parte 1 — Crear la estructura y cargar datos (40 min)

Una escuela de idiomas quiere informatizar su oferta de cursos. Se pide crear la base de datos
`idiomas` con las siguientes tablas.

### 1.1 Tabla `profesores`

| Atributo | Tipo | Restricciones |
|---|---|---|
| `id_profesor` | entero | PK, autoincremental |
| `nombre` | texto hasta 50 | NOT NULL |
| `email` | texto hasta 100 | NOT NULL, UNIQUE |
| `idioma_nativo` | texto hasta 30 | — |
| `activo` | opción entre `'si'` y `'no'` | valor por defecto `'si'` |

### 1.2 Tabla `cursos`

| Atributo | Tipo | Restricciones |
|---|---|---|
| `id_curso` | entero | PK, autoincremental |
| `nombre_curso` | texto hasta 60 | NOT NULL |
| `nivel` | texto hasta 20 | NOT NULL |
| `duracion_meses` | entero | NOT NULL |
| `precio` | decimal con 2 decimales | NOT NULL |
| `id_profesor` | entero | FK a `profesores(id_profesor)` |

La FK debe definirse con nombre propio (`fk_cursos_profesores`) y con **borrado y actualización en cascada**.

### 1.3 Tabla `inscripciones`

| Atributo | Tipo | Restricciones |
|---|---|---|
| `id_inscripcion` | entero | PK, autoincremental |
| `id_curso` | entero | FK a `cursos(id_curso)` |
| `alumno` | texto hasta 60 | NOT NULL |
| `fecha_inscripcion` | fecha | NOT NULL |
| `estado` | opción entre `'activo'`, `'finalizado'`, `'abandonó'` | por defecto `'activo'` |

### 1.4 Carga de datos

Insertar **3 profesores**, **4 cursos** y **5 inscripciones** inventadas por vos. Cada curso debe
quedar asociado a un profesor existente y cada inscripción a un curso existente.

### 1.5 Pruebas de que las restricciones funcionan

Escribir (y ejecutar) **dos** `INSERT` que deban fallar, uno por cada caso, y anotar al lado con un
comentario `--` el error que devuelve MySQL:

1. Un profesor con un `email` ya cargado.
2. Una inscripción con un `id_curso` que no existe.

---

## Parte 2 — Consultas sobre la base `biblioteca` (60 min)

Base de la cátedra (el DER se entrega impreso):

```
autores(id_autor, nombre, nacionalidad)
libros(id_libro, titulo, genero, anio_publicacion, id_autor)
prestamos(id_prestamo, id_libro, lector, fecha_prestamo, fecha_devolucion)
```

- `libros.id_autor` es FK hacia `autores.id_autor`.
- `prestamos.id_libro` es FK hacia `libros.id_libro`.
- `fecha_devolucion` queda en `NULL` mientras el libro no se devolvió.

Resolver con **una sola consulta** por consigna, salvo donde se indica.

### 2.1 Consultas simples

1. Mostrar `titulo` y `anio_publicacion` de los libros publicados **después de 1970**, ordenados del más nuevo al más viejo.
2. Mostrar `lector`, `fecha_prestamo` e `id_libro` de los préstamos que **todavía no fueron devueltos**.
3. Mostrar `titulo` y `genero` de los libros cuyo género sea **`'fantasía'` o `'ficción'`**, usando `IN`.
4. Mostrar todos los libros cuyo título **contenga** la palabra `'la'`, sin importar mayúsculas ni lo que venga antes o después.
5. Listar los autores de **nacionalidad argentina**, mostrando `nombre` y `nacionalidad`.

### 2.2 Agregación y agrupamiento

6. Contar cuántos libros hay en total.
7. Mostrar la cantidad de libros **por género**, ordenada de mayor a menor cantidad.
8. Mostrar el **promedio de `anio_publicacion`** de todos los libros, redondeado a 2 decimales y con el alias `promedio_anio`.
9. Mostrar cuántos préstamos tiene cada libro (`titulo` y cantidad), incluyendo solamente los libros que tengan **más de 1 préstamo**.

### 2.3 JOIN

10. Mostrar `titulo` y `nombre del autor` de todos los libros, usando **INNER JOIN**.
11. Mostrar `titulo`, `lector` y `fecha_prestamo` de los préstamos **no devueltos**, con el título del libro (dos tablas, **INNER JOIN**).
12. Mostrar `titulo`, `lector` y `nombre del autor` de los préstamos no devueltos (**INNER JOIN de tres tablas**).
13. Mostrar `nombre` de los autores que **no tienen ningún libro** cargado, usando **LEFT JOIN**.

### 2.4 Modificación de datos y estructura

14. Agregar a `autores` la columna `anio_nacimiento` de tipo `INT`.
15. Cambiar el año de publicación de `'Rayuela'` a `1964`.
16. Renombrar la columna `nombre_lector` de `prestamos` a `lector`, manteniendo el tipo `VARCHAR(50)`.

### 2.5 Borrado en cadena (a mano)

17. Borrar al autor con `id_autor = 3` junto con **todos** sus libros y **todos** los préstamos de esos libros. Escribir las sentencias **en el orden correcto** y justificar en un comentario por qué ese es el orden.

### 2.6 Vista

18. Crear una vista `vista_prestamos_pendientes` que muestre `titulo`, `lector` y `fecha_prestamo` de los préstamos no devueltos. Después consultarla.
19. Explicar en un comentario qué hay que hacer si se quiere **modificar** esa vista (por ejemplo, agregarle una columna) y por qué.

---

## Criterios de corrección (orientativos)

| Punto | Qué se mira |
|---|---|
| 1.1 – 1.3 | tipos correctos, PK, FK con nombre, `CASCADE`, `UNIQUE`, `DEFAULT`, `ENUM` |
| 1.4 | que los IDs referenciados existan |
| 1.5 | que el error sea el esperado (duplicado / FK inexistente) |
| 2.1 – 2.3 | sintaxis, cláusula correcta (`WHERE` vs `HAVING`), JOIN pedido, `NULL` bien tratado |
| 2.4 | `ALTER TABLE … ADD`, `UPDATE … SET … WHERE`, `CHANGE` **sin coma** |
| 2.5 | orden hijo → padre y justificación |
| 2.6 | `CREATE VIEW` y la necesidad de `DROP VIEW` previo |
