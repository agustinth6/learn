# Administración y Gestión de Bases de Datos — Resumen de estudio

**Contenido:** clases del 30/09, 06/10, 07/10, 13/10, 14/10, 21/10, 27/10, 28/10, **03/11** y 04/11.
**Eje del material:** SQL en MySQL Workbench — desde los tipos de datos y las restricciones hasta las consultas con `JOIN`, `GROUP BY`/`HAVING` y vistas.

> **Nota sobre las fuentes:** de la clase del **31/11** había llegado primero un PDF con una transcripción en otro idioma, sin contenido de la materia. Ese archivo se reemplazó por la versión en español, que **sí está incorporada** en este resumen (práctica de `JOIN` y borrado manual sobre la base **biblioteca**).

---

## Índice

1. [Mapa general de la materia](#1-mapa-general-de-la-materia)
2. [Tipos de datos en SQL](#2-tipos-de-datos-en-sql)
3. [Constraints (restricciones)](#3-constraints-restricciones)
4. [DDL: crear la base de datos y las tablas](#4-ddl-crear-la-base-de-datos-y-las-tablas)
5. [DML: cargar datos con INSERT](#5-dml-cargar-datos-con-insert)
6. [Consultas simples (SELECT)](#6-consultas-simples-select)
7. [Funciones de agregación](#7-funciones-de-agregación)
8. [UPDATE, ALTER y DELETE: modificar datos vs. modificar estructura](#8-update-alter-y-delete-modificar-datos-vs-modificar-estructura)
9. [JOIN: combinar tablas](#9-join-combinar-tablas)
10. [GROUP BY y HAVING](#10-group-by-y-having)
11. [Caso práctico integrador: base biblioteca](#11-caso-práctico-integrador-base-de-datos-biblioteca)
12. [Vistas (VIEW)](#12-vistas-view)
13. [Buenas prácticas, errores típicos y consejos de la cátedra](#13-buenas-prácticas-errores-típicos-y-consejos-de-la-cátedra)
14. [Bases de datos usadas para practicar](#14-bases-de-datos-usadas-para-practicar)
15. [Cómo se evalúa (parcial)](#15-cómo-se-evalúa-parcial)
16. [Chuleta de sintaxis](#16-chuleta-de-sintaxis)

---

## 1. Mapa general de la materia

SQL se organiza en dos grandes bloques que se usan siempre en ese orden:

| Bloque | Nombre | Qué hace | Ejemplos de palabras reservadas |
|---|---|---|---|
| **DDL** | *Data Definition Language* | Define la **estructura**: base de datos, tablas, columnas, restricciones | `CREATE DATABASE`, `CREATE TABLE`, `ALTER TABLE`, `DROP` |
| **DML** | *Data Manipulation Language* | Trabaja con los **datos** dentro de esa estructura: cargar, consultar, actualizar, borrar | `INSERT`, `SELECT`, `UPDATE`, `DELETE` |

**Por qué importa la separación:** en el trabajo real se reciben dos archivos, `DDL` (estructura) y `DML` (datos y consultas). En la cursada y en el parcial se permite unificarlos en **un solo archivo**, pero el orden lógico se mantiene: primero la estructura, después los datos, después las consultas.

**Recorrido completo del cuatrimestre:**

```
Tipos de datos → Constraints → CREATE DATABASE / TABLE → INSERT
      → SELECT simples → funciones de agregación → UPDATE / ALTER / DELETE
      → JOIN (inner, left, right, full) → GROUP BY / HAVING → VIEWS
```

**Idea clave que atraviesa todo:** SQL es un **lenguaje de consultas**. Cada sentencia hace *una* cosa y hay que elegir la palabra reservada correcta; escribir algo parecido no alcanza (por ejemplo, `DELETE TAB` no existe: para borrar una tabla se usa `DROP`).

---

## 2. Tipos de datos en SQL

### 2.1 Texto: `CHAR` vs `VARCHAR`

| Tipo | Comportamiento | Ejemplo de uso |
|---|---|---|
| `CHAR(n)` | Ocupa **siempre** los `n` caracteres, aunque se usen menos (rellena con espacios) | Datos de longitud fija: `DNI CHAR(8)` |
| `VARCHAR(n)` | Es de **longitud variable**: si se declara 100 pero se guardan 8, ocupa solo 8 | Caso general de texto: nombres, mails, descripciones cortas |
| `TEXT` | Texto largo y sin límite definido | Descripciones generales |

- **En la práctica se usa más `VARCHAR`**, porque no desperdicia espacio.
- `CHAR` tiene sentido cuando se está **seguro** de que la longitud no cambia. El DNI es el ejemplo de la clase: siempre 8 dígitos, así que `CHAR(8)` es correcto.
- **Cuidado con los casos límite:** una libreta de enrolamiento tiene más dígitos que un DNI, así que un campo pensado solo para DNI podría no alcanzar. Hay que prever esos escenarios al dimensionar el campo.
- Los valores de texto **siempre van entre comillas simples** en las consultas y en los `INSERT`.

### 2.2 Números

| Tipo | Uso | Ejemplo |
|---|---|---|
| `INT` | Números enteros | edad, cantidad, IDs |
| `DECIMAL(10,2)` | Números con decimales exactos. **`10` = total de dígitos, `2` = dígitos después de la coma** | precios, salarios, totales |
| `FLOAT` | Valores flotantes, con más decimales y menos exactitud | medidas, cálculos científicos |

- `DECIMAL(10,2)` es la **convención** para dinero: 10 dígitos en total, 2 decimales (por ejemplo, `1250.50`).
- Los números **no** llevan comillas en las consultas.

### 2.3 Fechas y horas

- `DATE`: guarda **año, mes y día**, en el orden `AAAA-MM-DD` (por ejemplo `2025-03-15`).
- `MONTH()` y `YEAR()` permiten extraer el mes o el año de una fecha para filtrar o agrupar.
- Las fechas **van entre comillas** en las consultas, aunque parezcan números.
- Para trabajar con semanas existe también `WEEK()`.

### 2.4 Booleanos y listas de valores

- `BOOLEAN`: verdadero / falso.
- `ENUM('valor1','valor2', ...)`: cuando un atributo solo puede tomar **un conjunto fijo de valores**. Ejemplo de la clase: el estado de una inscripción con `ENUM('activo','completado','cancelado')`.
  - Cada valor posible va entre comillas simples, separado por comas, dentro del paréntesis.
  - Se puede combinar con `DEFAULT`: `DEFAULT 'activo'` completa el campo con `activo` si no se indica nada.

---

## 3. Constraints (restricciones)

**Definición:** las *constraints* son **reglas** que se le ponen a los atributos de una tabla al crearla, para que los datos se guarden correctamente y no se almacene «cualquier cosa». *Constraint = restricción.*

**Para qué sirven:**
- Evitar datos repetidos o incorrectos.
- Mantener las relaciones entre tablas.
- Obligar a que ciertos campos estén completos.

### 3.1 Tipos de constraint

| Constraint | Qué hace | Detalle importante |
|---|---|---|
| `PRIMARY KEY` (PK) | Identifica de forma **única** cada fila | **No se puede repetir y no admite nulos** |
| `FOREIGN KEY` (FK) | Relaciona una tabla con otra; solo admite valores que existan en la tabla padre | Se declara con `FOREIGN KEY (...) REFERENCES tabla(columna)` |
| `UNIQUE` | Evita valores repetidos en esa columna | **Sí admite nulos**, a diferencia de la PK |
| `NOT NULL` | No permite valores vacíos: el dato es obligatorio | Equivale a un campo obligatorio de un formulario |
| `CHECK` | Define una condición que el dato debe cumplir al cargarse | Existe y se menciona, pero **no se usa** en la cursada (ejemplo: «el precio debe ser mayor a cero») |
| `DEFAULT` | Define un valor por defecto si no se indica ninguno | Se autocompleta |
| `AUTO_INCREMENT` | El valor se genera solo, sumando 1 a cada registro nuevo | Se usa en las PK numéricas para no cargarlas a mano |

### 3.2 PK vs UNIQUE (diferencia que se pregunta)

- Ambas evitan repetir valores.
- La **PK** es mucho más restrictiva: **única + no nula**, y es *el* identificador de la fila.
- **UNIQUE** permite nulos: se puede tener una columna `email UNIQUE` y alguna fila sin mail.
- Ejemplo de la clase: `email VARCHAR(100) NOT NULL UNIQUE`. El `UNIQUE` acá deja asentado que un cliente no puede tener dos mails iguales; si se intenta, MySQL arroja error y no deja avanzar.

**Sobre `NOT NULL` y `UNIQUE` en la práctica:** `NOT NULL` es muy común, porque las empresas quieren juntar la mayor cantidad de información. `UNIQUE` se aplica solo a datos que realmente deben ser únicos (mail, DNI, usuario). `nombre` no debería ser `UNIQUE`: dos personas pueden llamarse igual.

### 3.3 Cómo se declaran (ejemplo completo)

```sql
CREATE TABLE estudiantes (
    id_estudiante   INT PRIMARY KEY AUTO_INCREMENT,
    nombre          VARCHAR(50)  NOT NULL,
    apellido        VARCHAR(50)  NOT NULL,
    fecha_nacimiento DATE,
    dni             CHAR(8)      UNIQUE,
    email           VARCHAR(100) NOT NULL UNIQUE
);
```

- Si a un atributo **no** se le pone `PRIMARY KEY`, MySQL lo trata como **un atributo común** y admite cualquier cosa (repetidos, nulos). Por eso la declaración de constraint es imprescindible.
- Las PK y FK de una tabla hija se ven como **atributos más** de esa tabla (por ejemplo `id_estudiante` dentro de `inscripciones`): son FK para la relación, pero también columnas que hay que cargar.

### 3.4 Borrado y actualización en cascada

`ON DELETE CASCADE` y `ON UPDATE CASCADE` se declaran dentro de la FK:

```sql
CONSTRAINT fk_inscripciones_estudiantes
    FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id_estudiante)
    ON DELETE CASCADE
    ON UPDATE CASCADE
```

- **`ON DELETE CASCADE`**: si se borra un registro de la **tabla padre**, se borran automáticamente todos los registros relacionados en las **tablas hijas**. Ejemplo: se borra un estudiante y desaparecen sus inscripciones y sus notas.
- **`ON UPDATE CASCADE`**: si se modifica el valor de la clave en el padre, se actualiza en las hijas.
- **¿Es obligatorio?** No. Es una **buena práctica muy usada**, pero hay empresas que no lo ponen. Si no está:
  - Hay que borrar **manualmente** en todas las tablas afectadas (padre e hijas). Si se borra solo en el padre, quedan **datos huérfanos** ocupando espacio y la base queda **inconsistente**; lo más probable es que además arroje error.
  - También puede ser intencional: cuando no se quiere borrar *todo* lo relacionado, sino elegir qué sí y qué no.
- Funciona igual en relaciones 1:N, no solo en tablas intermedias.
- Otras acciones de la FK que **existen pero no se usan**: `ON DELETE SET NULL` (deja el campo en `NULL` en la hija; requiere que la columna admita nulos) y `ON DELETE RESTRICT` (impide borrar si hay datos relacionados).

---

## 4. DDL: crear la base de datos y las tablas

### 4.1 Crear y seleccionar la base

```sql
CREATE DATABASE escuela;
USE escuela;
```

- `CREATE DATABASE` crea la base con el nombre indicado. `CREATE TABLE` **no** sirve para esto.
- `USE` le indica a SQL **con qué base de datos se va a trabajar**. Si no se ejecuta, las consultas fallan porque MySQL no sabe dónde buscar.
- Si se intenta crear una base que ya existe, da error. Ahí se puede usar `DROP DATABASE nombre;` y volver a empezar (ver 4.6).

### 4.2 Comentarios

- En SQL: **dos guiones y un espacio** → `-- esto es un comentario`. **Si falta el espacio, no funciona.**
- Es una buena costumbre comentar al lado de cada consulta qué hace, sobre todo al estudiar.

### 4.3 Orden de creación de tablas (regla de oro)

1. Primero las **tablas padre** (las que no dependen de nadie).
2. **Al final** la **tabla intermedia / hija**, la que contiene las claves foráneas.

**Motivo:** no se puede crear una tabla que hace referencia (`FOREIGN KEY`) a una tabla que todavía no existe. Si se intenta, MySQL no ejecuta la sentencia.

- Si más adelante se agregan tablas nuevas no relacionadas con la intermedia, se pueden crear **debajo** sin problema.
- La regla se justifica además por **convención y trabajo en equipo**: la base va a ser usada por otras personas, y el orden debe ser comprensible para cualquiera.

### 4.4 Convenciones de escritura

- Las **palabras reservadas van en MAYÚSCULA** (`CREATE`, `TABLE`, `SELECT`, `FROM`, `WHERE`…) y los nombres propios en minúscula.
- **No es obligatorio**: si no se respeta, el código igual se ejecuta. Se pierden las buenas prácticas, nada más.
- Los **nombres de tablas y atributos deben escribirse siempre igual**, sin acentos y sin errores de tipeo. Un acento de más o un guion bajo faltante produce errores difíciles de encontrar.
- Todo termina en **punto y coma** (`;`). Las comas separan atributos **salvo en el último**, que se cierra con paréntesis y punto y coma:

```sql
CREATE TABLE cursos (
    id_curso        INT PRIMARY KEY AUTO_INCREMENT,
    nombre_curso    VARCHAR(100) NOT NULL,
    fecha_inicio    DATE NOT NULL,
    fecha_fin       DATE NOT NULL,
    docente_titular VARCHAR(100) NOT NULL
);
```

- La **fonética** ayuda a entender las palabras reservadas: `ALTER` = alterar/modificar; `ADD` = agregar; `DROP` = soltar/eliminar; `CHANGE` = cambiar; `MODIFY` = modificar.

### 4.5 Ejemplo completo: tabla intermedia con dos FK

Tabla `inscripciones` que relaciona `estudiantes` y `cursos`:

```sql
CREATE TABLE inscripciones (
    id_inscripcion  INT PRIMARY KEY AUTO_INCREMENT,
    id_estudiante   INT NOT NULL,
    id_curso        INT NOT NULL,
    estado          ENUM('activo','completado','cancelado') DEFAULT 'activo',
    fecha_inscripcion DATE,
    CONSTRAINT fk_inscripciones_estudiantes
        FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id_estudiante)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_inscripciones_cursos
        FOREIGN KEY (id_curso) REFERENCES cursos(id_curso)
        ON DELETE CASCADE ON UPDATE CASCADE
);
```

Observaciones de la clase:
- `CONSTRAINT` lleva **un nombre representativo** (un alias de la relación), por ejemplo `fk_inscripciones_estudiantes`. Debe describir la relación; «cualquier cosa» no sirve.
- También es válido declarar la FK directamente sin `CONSTRAINT` (`id_cliente INT, FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)`). **Las dos formas funcionan**; lo importante es marcar que es una clave foránea.
- Si se usa `CONSTRAINT`, conviene poner el `ON DELETE CASCADE` **antes de la coma** que cierra esa restricción.

### 4.6 Sobre `DROP` (y por qué es peligroso)

- `DROP DATABASE tienda;` borra **todo**: estructura y datos. **No es una buena práctica tenerlo en un script de trabajo** («en un trabajo no lo vas a tener porque te matan»).
- Se conserva en los scripts de la cursada **solo con fines didácticos**, como último recurso: si hay un error que no se puede resolver después de buscar mucho, se borra la base y se vuelve a crear de cero.
- La recomendación concreta de la cátedra: **antes de borrar, leer el mensaje de error y buscar la causa**. Si tras un buen rato no se encuentra, ahí sí se dropea.
- Alternativa menos destructiva: `DROP TABLE nombre;` o `TRUNCATE` para vaciar una tabla.

### 4.7 Ejecución en MySQL Workbench

- Para ejecutar: seleccionar la línea o líneas y apretar el **rayito** (o `Ctrl + Enter`). Debe estar **seleccionado** lo que se quiere ejecutar.
- **Ejecutar de a una sentencia al principio** (tabla por tabla, insert por insert): si algo falla, es mucho más fácil identificar dónde está el error que ejecutando todo el bloque junto.
- Los mensajes de resultado y de error aparecen **abajo**. Un tilde/verde indica éxito; la X indica error, y abajo se lee el detalle.
- Usar el panel **Schemas** y el botón **refresh** para ver si la tabla se creó, y para revisar los nombres exactos de tablas y atributos sin tener que buscarlos en el código.
- Guardar los scripts en una **carpeta dedicada** (`script SQL`) y con nombres claros (`DDL_escuela.sql`, `DML_escuela.sql`). Si en el diálogo de guardado ya está seleccionado el tipo SQL, la extensión `.sql` se agrega sola.
- **Si no se guarda el archivo**, la base queda en «memoria» de la sesión: al volver a entrar hay que recrearla. Con `USE escuela;` alcanza si el script está guardado y la base existe.

---

## 5. DML: cargar datos con INSERT

### 5.1 Regla del orden

**Los datos se insertan en el mismo orden en que se crearon las tablas y en el mismo orden en que se declararon los atributos.**

- Si primero se creó `estudiantes`, se cargan primero los datos de `estudiantes`; después `cursos`; al final la intermedia.
- Si en la tabla se declaró `nombre, apellido, fecha_nacimiento, email`, en el `INSERT` van en ese orden. **Si se altera el orden, MySQL tira error** (o carga datos en columnas equivocadas).

### 5.2 Sintaxis

```sql
INSERT INTO estudiantes (nombre, apellido, fecha_nacimiento, email)
VALUES
    ('Lucía', 'Gómez', '2001-03-15', 'lucia.gomez@email.com'),
    ('Mateo', 'Fernández', '1999-11-02', 'mateo.fernandez@email.com');
```

- `INSERT INTO` (las dos palabras) + tabla + paréntesis con los atributos + `VALUES` + paréntesis con los valores.
- Entre registros va **coma**; el último termina en **punto y coma**.
- Comillas simples para **texto y fechas**; los **números van sin comillas**.

### 5.3 La PK no se carga

- **No se incluye la PK** en el `INSERT` cuando es `AUTO_INCREMENT`: la genera el sistema.
- Las **FK sí se cargan**, porque son datos de la tabla (por ejemplo `id_estudiante`, `id_curso` en `inscripciones`).

### 5.4 Cómo se leen los datos de una tabla intermedia

Ejemplo de `inscripciones`:

| id_inscripcion | id_estudiante | id_curso | estado | fecha_inscripcion |
|---|---|---|---|---|
| 1 | 1 (Lucía) | 1 | activo | 2025-03-10 |
| 2 | 1 (Lucía) | 2 | activo | 2025-03-12 |
| 3 | 2 (Mateo) | 1 | activo | 2025-03-15 |
| 4 | 2 (Mateo) | 4 | cancelado | 2025-03-22 |

- El **mismo `id_estudiante` aparece varias veces**: Lucía está en el curso 1 y en el curso 2. Eso es exactamente el objetivo de la tabla intermedia: **no repetir los datos del alumno** en la tabla de cursos, sino registrar la relación.
- `(1,1)`, `(2,1)`, `(1,2)`, `(2,4)` son pares alumno–curso, no un error de carga.

### 5.5 Carga masiva

- Con pocos registros se escribe a mano. Con muchos, lo habitual es que la empresa entregue los datos en **Excel** y se importen o se arme el `INSERT` a partir de ahí. También hay herramientas que automatizan la carga.
- Igual, en general las bases se construyen sobre una base sólida ya existente: no se cargan 10.000 registros de a uno.

---

## 6. Consultas simples (SELECT)

**Estructura básica:**

```sql
SELECT [qué columnas] FROM [tabla] WHERE [condición] ORDER BY [columna] [ASC|DESC];
```

- El `SELECT` va **primero**; `FROM` indica de dónde; `WHERE` filtra filas; `ORDER BY` ordena.
- Todo puede ir en una línea o en varias: es indistinto para MySQL. Se puede poner el `WHERE` debajo del `FROM` sin problema.

### 6.1 Traer todo o solo algunas columnas

```sql
SELECT * FROM estudiantes;                      -- todos los atributos
SELECT nombre, apellido FROM estudiantes;        -- solo las columnas pedidas
```

- El **asterisco (`*`)** significa «todos los atributos».
- Conviene traer **solo lo que pide el ejercicio**: no más, no menos (aunque traer un dato extra no invalida la consulta).

### 6.2 Ordenar

```sql
SELECT * FROM estudiantes ORDER BY apellido;            -- ascendente (por defecto)
SELECT * FROM estudiantes ORDER BY apellido DESC;       -- descendente
SELECT * FROM productos  ORDER BY precio DESC;
```

- Sin indicar nada, el orden es **ASC (ascendente)**: A→Z, menor→mayor.
- `DESC` invierte: Z→A, mayor→menor.
- `ORDER BY` puede ir en la misma línea o debajo.

### 6.3 Filtrar con WHERE

```sql
-- Nacidos después del 1/1/2000 (formato AAAA-MM-DD)
SELECT * FROM estudiantes
WHERE fecha_nacimiento > '2000-01-01';

-- Combinando condición y orden
SELECT nombre, apellido, fecha_nacimiento
FROM estudiantes
WHERE fecha_nacimiento > '2000-01-01'
ORDER BY fecha_nacimiento DESC;

-- Un registro específico
SELECT * FROM estudiantes WHERE id_estudiante = 1;

-- Dos condiciones a la vez
SELECT * FROM cursos
WHERE YEAR(fecha_inicio) = 2025 AND docente_titular LIKE '%Ramírez%';
```

- Solo se traen las filas que **cumplen** la condición.
- Varias condiciones se unen con `AND` / `OR`.
- Si la condición no coincide con ningún dato, **no da error**: devuelve la tabla vacía o con valores `NULL`.
- **Los strings se comparan exactamente como están cargados.** Si el dato dice `Pérez` con acento y se busca `Perez`, no lo encuentra. Lo mismo con mayúsculas/minúsculas y con comillas simples o dobles (aunque las dobles suelen ser más permisivas, lo seguro es usar una).

### 6.4 LIKE: búsquedas parciales

| Comodín | Significado | Ejemplo |
|---|---|---|
| `%` | Cualquier cantidad de caracteres (incluido ninguno) | `email LIKE '%@gmail.com'` |
| `_` | **Exactamente un** carácter | `nombre LIKE 'L____'` (L + 4 caracteres) |

```sql
-- Mails que terminan en @gmail.com
SELECT * FROM clientes WHERE email LIKE '%@gmail.com';

-- Nombres que empiezan con L y tienen 4 caracteres más (Lucía)
SELECT * FROM estudiantes WHERE nombre LIKE 'L____';

-- Nombres que contienen la palabra "sistemas"
SELECT * FROM cursos WHERE nombre_curso LIKE '%sistemas%';
```

- Se puede combinar `%` antes y después cuando la palabra puede estar en cualquier posición.
- Contar los guiones bajos es clave: si se pone uno solo, se pide «L + 1 carácter» y no aparece ningún resultado.

### 6.5 BETWEEN: rangos (extremos incluidos)

```sql
SELECT * FROM inscripciones
WHERE fecha_inscripcion BETWEEN '2025-03-01' AND '2025-03-31';

SELECT * FROM clientes WHERE edad BETWEEN 25 AND 35;
```

- **Incluye los dos extremos**: si existe un registro del 1/3 y otro del 31/3, ambos aparecen.
- Si no hay datos en el extremo exacto, simplemente muestra los que estén dentro del rango.
- Funciona con fechas y con números.

### 6.6 IN: listas de valores

```sql
-- Clientes llamados Juan o Ana
SELECT * FROM clientes WHERE nombre IN ('Juan','Ana');
```

- Es equivalente a `WHERE nombre = 'Juan' OR nombre = 'Ana'`, pero **más corto y prolijo**.
- Los valores van **siempre entre paréntesis**, separados por comas y entre comillas si son texto.
- Es preferible a encadenar muchos `OR`, porque en el `OR` hay que **repetir el nombre de la columna en cada condición** y es fácil olvidarlo (fuente habitual de errores).

### 6.7 DISTINCT: quitar repetidos

```sql
-- Años de inicio sin repetir
SELECT DISTINCT YEAR(fecha_inicio) FROM cursos;

-- Solo las edades que existen (una vez cada una)
SELECT DISTINCT edad FROM clientes;
```

- `DISTINCT` devuelve **un solo valor por cada valor distinto** encontrado.
- Sin `DISTINCT`, la misma fecha o edad aparece tantas veces como registros haya.
- **No confundir** con contar: `DISTINCT` **lista**; `COUNT` **cuenta**.

### 6.8 MONTH() y YEAR(): filtrar por mes o año

```sql
-- Cursos que empiezan en abril
SELECT * FROM cursos WHERE MONTH(fecha_inicio) = 4;

-- Ventas del año 2025
SELECT * FROM ventas WHERE YEAR(fecha_venta) = 2025;

-- Ventas de marzo
SELECT * FROM ventas WHERE MONTH(fecha_venta) = 3;
```

- En la base la fecha está como número (`2025-04-02`), **no** como texto «abril». Por eso se filtra con el número de mes.
- La función va pegada al paréntesis: `MONTH(fecha_inicio)`. Si se separa (`MONTH (fecha)`), MySQL tira error.
- La misma lógica sirve para `YEAR()`, `WEEK()`, `DAY()`.

---

## 7. Funciones de agregación

**Qué son:** funciones que hacen **operaciones matemáticas sobre un conjunto de filas** y devuelven **un solo valor** (o un valor por grupo, si se combinan con `GROUP BY`).

| Función | Qué hace | Acepta |
|---|---|---|
| `COUNT()` | Cuenta registros | Números, texto, `*` |
| `SUM()` | Suma valores | **Solo numéricos** |
| `AVG()` | Calcula el promedio | **Solo numéricos** |
| `MAX()` | Valor máximo | Números **o texto** |
| `MIN()` | Valor mínimo | Números **o texto** |

**Diferencia clave entre COUNT y SUM:** `COUNT` **cuenta filas** (puede contar un mail, un ID, un texto); `SUM` **suma valores numéricos**. No son intercambiables.

### 7.1 Ejemplos

```sql
-- Cantidad total de clientes
SELECT COUNT(*) AS cantidad_clientes FROM clientes;

-- Cantidad de mails distintos
SELECT COUNT(DISTINCT email) AS emails_distintos FROM clientes;

-- Promedio de edad
SELECT AVG(edad) AS edad_promedio FROM clientes;

-- Precio máximo y mínimo
SELECT MAX(precio) AS precio_maximo,
       MIN(precio) AS precio_minimo
FROM productos;

-- Total de personas que viajan (suma de todas las reservas)
SELECT SUM(cantidad_personas) AS total_personas FROM reservas;

-- Cantidad de ventas de un año específico
SELECT COUNT(*) AS total_ventas FROM ventas WHERE YEAR(fecha_venta) = 2025;
```

### 7.2 El alias (`AS`) es casi obligatorio

- Sin alias, la columna de resultado aparece con el nombre de la función (`COUNT(*)`), y quien lea la consulta (o quien la guarde para otro) no sabe qué se está contando.
- Con `AS cantidad_clientes` el resultado es autoexplicativo. **Es una buena práctica siempre.**
- En `MAX`/`MIN`/`AVG` el alias es especialmente importante porque el nombre de la columna **no aparece** en el resultado.
- `AS` es opcional: `COUNT(*) cantidad_clientes` también funciona. Pero se recomienda escribirlo.

### 7.3 Redondear promedios

```sql
SELECT genero, ROUND(AVG(anio_publicacion)) AS promedio_anio
FROM libros
GROUP BY genero;
```

- `ROUND()` envuelve la función de agregación → **doble paréntesis**: `ROUND(AVG(...))`.
- Devuelve el promedio sin decimales (o con los decimales indicados en un segundo argumento).

---

## 8. UPDATE, ALTER y DELETE: modificar datos vs. modificar estructura

Esta es una de las distinciones más importantes de la materia.

| Sentencia | Qué modifica | Nivel | Ejemplo |
|---|---|---|---|
| `UPDATE` | **Registros / datos** de una tabla | Dato | Cambiar el mail de un cliente |
| `ALTER TABLE` | **Estructura** de la tabla: columnas, tipos, nombres | Estructura | Agregar una columna `teléfono` |
| `DELETE` | **Borra registros** de una tabla | Dato | Borrar el estudiante con ID 2 |
| `DROP` | **Borra la estructura** completa (tabla, columna o base) | Estructura | Eliminar la tabla o la base |

**Regla mnemotécnica:** `UPDATE` = actualizar **datos**; `ALTER` = alterar la **tabla**; `DROP` = eliminar **estructura**; `DELETE` = eliminar **filas**.

### 8.1 UPDATE: modificar registros

```sql
UPDATE estudiantes
SET email = 'lucia.gomez2025@email.com'
WHERE id_estudiante = 1;
```

- `UPDATE` + tabla + `SET` + **el dato nuevo** + `WHERE` (qué registro).
- **En el `SET` va siempre el valor nuevo**, no el viejo. Copiar y pegar el dato anterior es un error frecuente.
- **El `WHERE` es imprescindible.** Sin `WHERE` se modifican **todas** las filas de la tabla.
- `UPDATE` **no muestra** el resultado: si el mensaje sale en verde, la operación se hizo, pero para **verificar** hay que hacer un `SELECT` después.

```sql
-- Cambiar varios campos a la vez
UPDATE estudiantes
SET nombre = 'Matías', apellido = 'Fernández López'
WHERE id_estudiante = 2;

-- Pasar todas las inscripciones activas a completado
UPDATE inscripciones
SET estado = 'completado'
WHERE estado = 'activo';

-- Cargar el dato de una columna recién creada
UPDATE estudiantes SET telefono = '11-5555-1234' WHERE id_estudiante = 2;
```

- **Buena práctica antes de un `UPDATE` masivo:** hacer un `SELECT` con el mismo `WHERE` para ver qué filas se van a ver afectadas.
- Las actualizaciones afectan las consultas posteriores: si se cambió una fecha de 2025 a 2026, esa venta ya no aparece al filtrar por 2025.

### 8.2 La línea que «desbloquea» las actualizaciones

```sql
SET SQL_SAFE_UPDATES = 0;
```

- MySQL tiene por defecto un **mecanismo de seguridad** (un «candado») que, después de varias modificaciones, empieza a rechazar `UPDATE`/`ALTER` y devuelve error aunque el código esté bien.
- Para evitarlo se ejecuta esta línea **antes** de empezar con las actualizaciones y las modificaciones de estructura. Luego se trabaja normalmente.
- **En el parcial se entrega esta línea incluida**, para no perder tiempo. Efecto práctico: funciona como un «reseteo» / permiso para seguir haciendo cambios.
- Si aparecen errores encadenados sin causa aparente, lo primero que hay que revisar es si falta esta línea.

### 8.3 ALTER TABLE: modificar la estructura

```sql
-- Agregar una columna (con su tipo de dato, como al crear la tabla)
ALTER TABLE estudiantes ADD telefono VARCHAR(20);

-- Agregar una columna numérica
ALTER TABLE productos ADD stock INT;
ALTER TABLE ventas ADD cantidad INT;
ALTER TABLE clientes ADD direccion VARCHAR(100);

-- Borrar una columna
ALTER TABLE estudiantes DROP COLUMN telefono;

-- Cambiar el nombre de una columna (nombre viejo y nuevo, separados por espacio)
ALTER TABLE cursos CHANGE nombre_curso titulo_curso VARCHAR(100);

-- Modificar el tipo o el tamaño de una columna
ALTER TABLE cursos MODIFY docente_titular VARCHAR(100);
ALTER TABLE clientes MODIFY nombre VARCHAR(100) NOT NULL;
ALTER TABLE productos MODIFY precio DECIMAL(12,2);
```

- Las palabras reservadas que acompañan a `ALTER` son: **`ADD`** (agregar), **`DROP`** (borrar columna), **`CHANGE`** (cambiar nombre), **`MODIFY`** (cambiar tipo/tamaño).
- `ADD` y `ADD COLUMN` funcionan igual; la palabra `COLUMN` es opcional.
- Al agregar una columna **hay que indicar el tipo de dato**, porque se está creando un atributo nuevo.
- La columna nueva queda con **`NULL`** en todos los registros existentes: se creó la estructura, pero no se cargaron datos. Para cargarlos se usa `UPDATE` (ver 8.1).
- `MODIFY` **no se ve** en un `SELECT`: no hay forma de comprobar a simple vista si el tamaño cambió, solo confiar en que se ejecutó sin error.
- Ampliar el tamaño de un campo permite después cargar datos más largos (por ejemplo, nombres de más de 50 caracteres).

### 8.4 DELETE: borrar registros

```sql
DELETE FROM estudiantes WHERE id_estudiante = 2;
```

- `DELETE FROM` + tabla + `WHERE`. Borra **solo las filas** que cumplen la condición.
- **La palabra `FROM` es obligatoria.** `DELETE préstamos` (sin `FROM`) no funciona: MySQL no sabe de dónde borrar.
- Si se borra el ID 2, la lista pasa del 1 al 3. **El número borrado no se reutiliza nunca**: si después se inserta un registro nuevo, ocupa la posición siguiente, no el hueco.
- **Sin `WHERE` se borran todas las filas** de la tabla (pero la tabla sigue existiendo).
- No existe `DELETE TAB` ni `SELECT DELETE FROM ...`: no son comandos válidos y MySQL devuelve error.
- En las empresas **muy poca gente tiene permiso para borrar datos**, porque es una operación riesgosa.

### 8.5 Borrado manual cuando NO hay `ON DELETE CASCADE`

**Procedimiento general: se borra de la tabla más «lejana» hacia la más «cercana»** — primero los registros que dependen de otros, y el registro principal al final. Si se intenta al revés, MySQL no lo permite porque el dato todavía está siendo referenciado.

Ejemplo con `clientes` → `ventas`:

```sql
-- 1) Ver qué hay
SELECT * FROM clientes WHERE id_cliente = 1;
SELECT * FROM ventas   WHERE id_cliente = 1;

-- 2) Borrar primero en las tablas hijas
DELETE FROM ventas   WHERE id_cliente = 1;

-- 3) Borrar en la tabla padre
DELETE FROM clientes WHERE id_cliente = 1;
```

**Ejemplo completo de la clase (base biblioteca): borrar al autor Julio Cortázar y todo lo asociado.**

La cadena de dependencias es: `autores` → `libros` → `prestamos`. Un autor tiene libros, y esos libros tienen préstamos. Para eliminar al autor hay que **ir de la punta de la cadena hacia atrás**:

```sql
-- 1) Ubicar al autor
SELECT * FROM autores;              -- Julio Cortázar = id_autor 3

-- 2) Ver qué libros y préstamos están asociados
SELECT * FROM libros WHERE id_autor = 3;              -- Rayuela (3) y Bestiario (12)
SELECT * FROM prestamos WHERE id_libro IN (3, 12);

-- 3) Borrar primero los préstamos de esos libros
DELETE FROM prestamos WHERE id_libro = 3;
DELETE FROM prestamos WHERE id_libro = 12;   -- o: WHERE id_libro IN (3, 12)

-- 4) Después los libros de ese autor
DELETE FROM libros WHERE id_autor = 3;

-- 5) Por último el autor
DELETE FROM autores WHERE id_autor = 3;
```

- **Paso a paso:** se verifica en cada etapa con un `SELECT` que el registro ya no está antes de pasar al siguiente nivel.
- **Para pensar el orden:** agarrar el **DER** impreso y preguntarse «tengo que borrar el libro del ID 4… ¿ese libro tiene préstamos? ¿cuántos? Los borro». Así, tabla por tabla, se va desarmando la cadena.
- En las empresas esto queda resuelto con `ON DELETE CASCADE`, pero **en el parcial probablemente la estructura no lo tenga**, justamente para practicar el borrado manual.
- «Pensalo como un JOIN»: el razonamiento para recorrer las tablas relacionadas es el mismo.
- Este borrado en varios pasos también es válido en relaciones 1:N, no solo con tablas intermedias.

---

## 9. JOIN: combinar tablas

### 9.1 Para qué sirven

Hasta este punto todas las consultas trabajaban con **una sola tabla**. Pero en una base real la información está repartida: los datos del estudiante en `estudiantes`, los del curso en `cursos`, y la relación entre ambos en `inscripciones`.

**JOIN = unir.** Sirve para **consultar información distribuida en varias tablas como si fuera una sola**.

**Ejemplo conceptual:** «¿En qué curso está Ana López?» → el nombre está en `estudiantes`, el curso en `cursos`, y el vínculo en `inscripciones`. Ninguna tabla sola responde la pregunta.

**Fundamento:** esto se deriva de la **normalización** y de la **atomicidad** vistas en la primera parte de la materia: cada tabla guarda solo los datos que le corresponden y tiene su PK. Por eso, para reconstruir la información completa, hay que **relacionar** las tablas por sus claves.

### 9.2 Cómo funciona: PK, FK y la cláusula ON

```sql
SELECT ...
FROM tabla_a
INNER JOIN tabla_b ON tabla_a.pk = tabla_b.fk;
```

- SQL sabe qué registros están relacionados **por una columna en común**: la **PK** de una tabla y la **FK** de la otra.
- **`ON` es la condición de unión**: indica *por dónde* se unen las tablas. **Sin `ON` no hay JOIN útil**: la consulta devuelve una combinación masiva sin sentido («trae cualquier cosa»).
- **`ON` ≠ `WHERE`**:
  - `ON` → **une** las tablas (qué registros se relacionan).
  - `WHERE` → **filtra** los registros del resultado, y va **al final**, después de todos los JOIN.
- Cuando se unen más de 2 tablas, **cada JOIN necesita su propio `ON`**.

### 9.3 Los cuatro tipos de JOIN

| Tipo | Devuelve | En el diagrama de Venn |
|---|---|---|
| `INNER JOIN` | **Solo las filas que coinciden** en ambas tablas | La intersección |
| `LEFT JOIN` | **Todas las filas de la tabla izquierda** + las coincidentes de la derecha; lo que falta se completa con `NULL` | Círculo izquierdo completo |
| `RIGHT JOIN` | **Todas las filas de la tabla derecha** + las coincidentes de la izquierda; lo que falta se completa con `NULL` | Círculo derecho completo |
| `FULL JOIN` | **Todas las filas de ambas tablas**, coincidan o no; los faltantes van con `NULL` | Ambos círculos completos |

**¿Qué es «tabla izquierda» y «tabla derecha»?**
- **Izquierda** = la que se escribe **después de `FROM`**.
- **Derecha** = la que se escribe **después de `JOIN`**.
- No tiene que ver con la posición en el diagrama (DER), sino con **el orden en que se escribe la consulta**. Esto es importante cuando hay 5 o 20 tablas.

### 9.4 INNER JOIN

Devuelve **solo lo que existe en las dos tablas**. Si un estudiante no tiene ninguna inscripción, **no aparece**; si una inscripción apunta a un estudiante que no existe, **tampoco aparece**.

**Ejemplo con datos (empleados / departamentos):**

| id_empleado | nombre |   | id_departamento | id_empleado | departamento |
|---|---|---|---|---|---|
| 1 | Ana |   | 1 | 1 | Ventas |
| 2 | Luis |   | 2 | 3 | Marketing |
| 3 | Marta |   | 3 | 4 | Finanzas |

`INNER JOIN` devuelve **Ana (Ventas)** y **Marta (Marketing)**.
**No** devuelve a Luis (no tiene departamento) ni al empleado 4 (no existe en la tabla de empleados).

**Ejemplo de la base escuela:**

```sql
-- Estudiantes inscriptos, con el curso y el estado
SELECT e.nombre, e.apellido, c.nombre_curso, i.estado
FROM inscripciones i
INNER JOIN estudiantes e ON i.id_estudiante = e.id_estudiante
INNER JOIN cursos      c ON i.id_curso      = c.id_curso;
```

- **Se recomienda partir de la tabla intermedia**: es la que contiene todas las FK y desde ahí se llega a las demás.
- El orden de los JOIN es **indistinto**: se puede unir primero con `estudiantes` o primero con `cursos`; el resultado es el mismo.
- `INNER JOIN` se puede abreviar como **`JOIN`**: MySQL lo interpreta igual. En cambio, `LEFT` y `RIGHT` **sí** hay que nombrarlos.

### 9.5 LEFT JOIN

Devuelve **todo lo de la tabla izquierda**, aunque no tenga pareja en la derecha. Las columnas de la derecha quedan en **`NULL`**.

```sql
-- Todos los estudiantes, estén o no inscriptos en algún curso
SELECT e.nombre, e.apellido, c.nombre_curso, i.estado
FROM estudiantes e
LEFT JOIN inscripciones i ON e.id_estudiante = i.id_estudiante
LEFT JOIN cursos        c ON i.id_curso      = c.id_curso;
```

- Ejemplo de la clase: se agregó un estudiante **Pedro** sin ninguna inscripción. Aparece en el resultado, con `nombre_curso` y `estado` en `NULL`.
- Se arranca **desde la tabla que se quiere priorizar**, no desde la intermedia.
- Todos los JOIN de esa consulta deben ser `LEFT` si se quiere conservar la prioridad hasta el final.
- **Equivalencia práctica:** un `LEFT JOIN` con la tabla priorizada después del `FROM` da el mismo resultado que un `RIGHT JOIN`. La elección es cuestión de comodidad; lo que no se puede es mezclar criterios sin pensar qué registro tiene que estar sí o sí.

**Ejemplo de la clase (base biblioteca):**

```sql
-- Libros que no tienen autor asignado
SELECT l.titulo, l.anio_publicacion
FROM libros l
LEFT JOIN autores a ON l.id_autor = a.id_autor
WHERE a.id_autor IS NULL;
```

**Para traer SOLO los que no tienen pareja** (los que «no compraron nunca»):

```sql
SELECT c.nombre, c.apellido, p.nombre_producto
FROM clientes c
LEFT JOIN ventas v    ON c.id_cliente = v.id_cliente
LEFT JOIN productos p ON v.id_producto = p.id_producto
WHERE v.id_cliente IS NULL;
```

- Se usa **`IS NULL`** (no `= NULL`): `= NULL` no funciona porque `NULL` no es un valor comparable.
- El filtro va sobre una columna de la tabla que **no** se prioriza: así quedan solo las filas donde no hubo coincidencia.

### 9.6 RIGHT JOIN

Es el **complemento del LEFT**: prioriza **todas las filas de la tabla derecha** y completa con `NULL` lo que falte de la izquierda.

```sql
-- Todos los cursos, tengan o no estudiantes inscriptos
SELECT e.nombre, e.apellido, c.nombre_curso, i.estado
FROM inscripciones i
RIGHT JOIN cursos       c ON i.id_curso      = c.id_curso
LEFT  JOIN estudiantes  e ON i.id_estudiante = e.id_estudiante;
```

- Mismo caso de ejemplo: se agregó un curso **Matemáticas** sin inscriptos. Aparece, con los datos del estudiante en `NULL`.
- También se puede resolver con un `LEFT JOIN` poniendo la tabla priorizada después del `FROM`; el resultado es equivalente (puede cambiar el orden de las filas).

**Caso combinado (ejercicio 8 del instituto) — por qué `RIGHT` y después `LEFT`:**

```sql
-- Todos los cursos, tengan o no estudiantes, con nombre y apellido y estado
SELECT c.nombre_curso, e.nombre, e.apellido, i.estado
FROM inscripciones i
RIGHT JOIN cursos      c ON i.id_curso      = c.id_curso
LEFT  JOIN estudiantes e ON i.id_estudiante = e.id_estudiante;
```

- El **`RIGHT JOIN` con `cursos`** conserva **todos los cursos**, aunque no tengan inscripciones. Es lo que pide la consigna.
- El **`LEFT JOIN` con `estudiantes`** conserva **el resultado del paso anterior** (incluidos los cursos sin inscriptos) y agrega nombre y apellido cuando hay coincidencia.
- **Si el segundo también fuera `RIGHT JOIN`**, se conservarían **todos los estudiantes**, incluidos los que no están inscriptos en ningún curso — y eso **no** es lo que pide el enunciado.
- **Regla general:** cada JOIN cumple una función distinta. Hay que preguntarse **qué registros sí o sí tienen que estar** en el resultado, y elegir `INNER`, `LEFT` o `RIGHT` en consecuencia.

### 9.7 FULL JOIN (existe, pero no en MySQL)

- Devuelve **todo**: lo que coincide y lo que no, completando con `NULL`.
- **MySQL no tiene `FULL JOIN`.** Se **simula con `UNION`**, uniendo un `LEFT` y un `RIGHT`:

```sql
SELECT e.nombre, e.apellido, c.nombre_curso, i.estado
FROM estudiantes e
LEFT JOIN inscripciones i ON e.id_estudiante = i.id_estudiante
LEFT JOIN cursos       c ON i.id_curso      = c.id_curso

UNION

SELECT e.nombre, e.apellido, c.nombre_curso, i.estado
FROM estudiantes e
RIGHT JOIN inscripciones i ON e.id_estudiante = i.id_estudiante
LEFT  JOIN cursos        c ON i.id_curso      = c.id_curso;
```

- Otras bases de datos sí lo tienen implementado; conviene saber que existe y cómo se simula.
- **No se toma en el parcial.**

### 9.8 Alias de tabla

```sql
SELECT e.nombre, e.apellido, c.nombre_curso
FROM estudiantes e
INNER JOIN inscripciones i ON e.id_estudiante = i.id_estudiante
INNER JOIN cursos c        ON i.id_curso      = c.id_curso;
```

- `e`, `i`, `c` son **alias de tabla**: abreviaturas para escribir menos.
- **Regla estricta:** si se pone un alias en el `SELECT`, hay que usarlo **en todos lados** (en el `FROM`, en los `ON` y en el `WHERE`). Si en el `FROM` se escribe el nombre completo pero en el `SELECT` el alias, **MySQL tira error**.
- **Alternativa:** usar siempre el **nombre completo de la tabla** (`estudiantes.nombre`). Es más largo pero más claro; las dos formas son válidas y una consulta con nombres completos está perfecta.
- Es una limitación/convención de SQL, no una regla de negocio.

### 9.9 Cómo pensar una consulta con JOIN (método de la cátedra)

1. **Leer la consigna y separar qué pide**: «mostrar el nombre del estudiante, el nombre del curso y el estado».
2. **Preguntarse en qué tabla está cada dato** → eso define qué tablas hay que unir.
3. **Escribir el `SELECT`** con esos atributos (con o sin alias, pero coherente).
4. **Elegir desde dónde arrancar**:
   - En un `INNER` → en general **la tabla intermedia**.
   - En un `LEFT`/`RIGHT` → la **tabla que se quiere priorizar**.
5. **Agregar los JOIN con sus `ON`**, uniendo **FK = PK**.
6. **Agregar el `WHERE`** (condiciones) **al final**, después de todos los JOIN.
7. **Agregar `ORDER BY`** si pide ordenar (también al final).
8. **Ejecutar y verificar** que el resultado responda exactamente a lo pedido.

**Ayuda visual:** tener el **DER** a mano. Es «el mapa» para saber por qué tablas hay que pasar cuando la relación no es directa. En el trabajo no siempre lo van a tener, así que hay que aprender a **identificar dónde está la FK**.

---

## 10. GROUP BY y HAVING

### 10.1 Para qué sirven

Hasta acá las funciones de agregación devolvían **un solo valor** para toda la tabla. `GROUP BY` permite **agrupar filas por el valor de una columna** y aplicar la función **dentro de cada grupo**.

**Sirve para obtener información resumida:** cuántos clientes hay por ciudad, cuántas reservas por destino, precio promedio por país, cuántos productos por categoría, cuántos préstamos por lector, cuántos libros por género.

- **Se usa siempre con una función de agregación** (`COUNT`, `SUM`, `AVG`, `MAX`, `MIN`).
- **Regla de oro:** **todo lo que se pone en el `GROUP BY` se repite en el `SELECT`** (y no al revés: puede haber agregaciones en el `SELECT` que no estén en el `GROUP BY`).

### 10.2 Estructura

```sql
SELECT columna_de_agrupación, FUNCIÓN(columna) AS alias
FROM tabla
[WHERE condición de filas]
GROUP BY columna_de_agrupación
[HAVING condición sobre el grupo]
[ORDER BY alias];
```

**Orden de las cláusulas:** `SELECT` → `FROM` → `JOIN`/`ON` → `WHERE` → `GROUP BY` → `HAVING` → `ORDER BY`.

### 10.3 Ejemplos

```sql
-- Cantidad de libros por género
SELECT genero, COUNT(*) AS cantidad_libros
FROM libros
GROUP BY genero;

-- Promedio del año de publicación por género
SELECT genero, AVG(anio_publicacion) AS promedio_anio
FROM libros
GROUP BY genero;

-- Con redondeo
SELECT genero, ROUND(AVG(anio_publicacion)) AS promedio_anio
FROM libros
GROUP BY genero;

-- Año más reciente de publicación por autor (requiere JOIN + MAX)
SELECT a.nombre AS autor, MAX(l.anio_publicacion) AS ultimo_anio
FROM libros l
INNER JOIN autores a ON l.id_autor = a.id_autor
GROUP BY a.nombre
ORDER BY ultimo_anio DESC;

-- Libro más antiguo por género
SELECT genero, MIN(anio_publicacion) AS mas_antiguo
FROM libros
GROUP BY genero;

-- Cantidad de ventas por categoría de producto (con JOIN)
SELECT p.categoria, COUNT(*) AS cantidad_ventas
FROM ventas v
INNER JOIN productos p ON v.id_producto = p.id_producto
GROUP BY p.categoria;

-- Cantidad de préstamos por lector
SELECT lector, COUNT(*) AS cantidad_prestamos
FROM prestamos
GROUP BY lector;

-- Cantidad de libros por nacionalidad del autor
SELECT a.nacionalidad, COUNT(l.id_libro) AS cantidad_libros
FROM autores a
INNER JOIN libros l ON a.id_autor = l.id_autor
GROUP BY a.nacionalidad;
```

### 10.4 Dos «tips» que resuelven casi todas las consultas de agrupación

1. **La primera parte del enunciado dice qué función usar**: «calculá el **promedio**» → `AVG`; «la **cantidad**» → `COUNT`; «el **más reciente**» → `MAX`; «el **más antiguo**» → `MIN`; «la **suma total**» → `SUM`.
2. **La última parte del enunciado dice cómo agrupar**: «por género», «por autor», «por lector», «por categoría» → eso va en el `GROUP BY` **y** en el `SELECT`.

**Truco de escritura:** empezar por el `GROUP BY` (ya sabe qué hay que agrupar), dejar el `SELECT` para después, y luego completar con la función de agregación y el alias. Así no se «enreda» la consulta.

### 10.5 HAVING: filtrar grupos

- **`WHERE` filtra filas** (antes de agrupar). **`HAVING` filtra grupos** (después de agrupar).
- `HAVING` **se usa exclusivamente** cuando ya hay un `GROUP BY` y se quiere condicionar el resultado del grupo (por ejemplo, «solo los géneros con más de un préstamo»).
- No se puede usar `WHERE` para filtrar el resultado de una agregación, porque en ese momento los grupos todavía no existen.

```sql
-- Géneros con más de un libro
SELECT genero, AVG(anio_publicacion) AS promedio
FROM libros
GROUP BY genero
HAVING COUNT(*) > 1;
```

**Caso con dos condiciones (ejercicio típico): «cantidad de préstamos por género, excluyendo el género infantil y mostrando solo los géneros con más de un préstamo».**

```sql
SELECT l.genero, COUNT(*) AS cantidad_prestamos
FROM libros l
INNER JOIN prestamos p ON l.id_libro = p.id_libro
WHERE l.genero <> 'infantil'
GROUP BY l.genero
HAVING COUNT(*) > 1;
```

**Regla práctica:** cuando el enunciado pide **dos condiciones**,
- la **primera** suele ser sobre las filas → **`WHERE`** (dentro de la consulta, antes de agrupar);
- la **segunda** es sobre el grupo → **`HAVING`** (después del `GROUP BY`).

### 10.6 Detalles y variantes

- **Se puede usar el alias en el `HAVING`**: `HAVING cantidad_prestamos > 1` funciona y es más corto. Es la forma más segura de no equivocarse (pensando en el parcial también sirve).
- `COUNT(*)`, `COUNT(id_prestamo)` y `COUNT(alias)` dan el mismo resultado cuando se cuenta todo el grupo. `COUNT(*)` es la forma más rápida de escribir.
- **`ORDER BY` con `GROUP BY`:** para ordenar el resultado agrupado hay que usar **el alias** de la agregación (o la misma expresión), no el nombre de la columna original:

```sql
SELECT a.nombre AS autor, MAX(l.anio_publicacion) AS ultimo_anio
FROM libros l
INNER JOIN autores a ON l.id_autor = a.id_autor
GROUP BY a.nombre
ORDER BY ultimo_anio DESC;    -- mayor → menor
```

- **Todo lo que está en el `GROUP BY` tiene que estar en el `SELECT`.** Si se agrupa por `genero` pero no se selecciona `genero`, el resultado no se entiende.
- `SUM` y `AVG` **solo** con columnas numéricas; `MAX` y `MIN` también aceptan texto.
- `COUNT(DISTINCT columna)` cuenta valores únicos dentro del grupo.
- **Con pocos datos** el `GROUP BY` parece innecesario (a veces se seleccionan muchos atributos y la consulta «ya trae todo»), pero en bases reales con miles de registros es indispensable.
- `SUM` **no** es lo mismo que `COUNT`: se cuenta con `COUNT`, se suma con `SUM`.

---

## 11. Caso práctico integrador: base de datos **biblioteca**

Esta es la práctica guiada de la clase del 3/11 y funciona como **repaso de todo**: consultas simples, modificaciones, borrado en cadena y JOIN. Vale la pena resolverla completa antes del parcial, porque el recorrido es el mismo que va a pedir el examen.

### 11.1 Estructura

| Tabla | Atributos | Rol |
|---|---|---|
| `autores` | `id_autor` (PK), `nombre`, `nacionalidad` | Tabla padre |
| `libros` | `id_libro` (PK), `titulo`, `genero`, `anio_publicacion`, `id_autor` (FK) | Tabla hija de `autores` |
| `prestamos` | `id_prestamo` (PK), `id_libro` (FK), `nombre_lector`, `fecha_prestamo`, `fecha_devolucion` | Tabla intermedia / hija de `libros` |

Cadena de dependencias: **`autores` → `libros` → `prestamos`**.

### 11.2 Consultas simples

```sql
-- 1. Todos los libros registrados
SELECT * FROM libros;

-- 2. Nombres y nacionalidades de autores
SELECT nombre, nacionalidad FROM autores;

-- 3. Libros publicados después de 1970
SELECT titulo, anio_publicacion FROM libros
WHERE anio_publicacion > 1970;

-- 4. Préstamos que aún no fueron devueltos  →  fecha_devolucion nula
SELECT * FROM prestamos WHERE fecha_devolucion IS NULL;

-- 5. Libros de género fantasía o ficción (dos formas equivalentes)
SELECT * FROM libros WHERE genero = 'fantasía' OR genero = 'ficción';
SELECT * FROM libros WHERE genero IN ('fantasía','ficción');
```

**Sobre la consulta 4:** `IS NULL` sirve para detectar el «no dato». Los préstamos sin fecha de devolución son los que todavía no volvieron. Se escribe **`IS NULL`**, no `= NULL` (y `NULL` en mayúscula, como todas las palabras reservadas).

**Sobre la consulta 5 y los valores exactos:**

- **Los datos del `WHERE` deben coincidir exactamente con lo cargado:** mayúsculas, minúsculas y **acentos**. `'ficción'` con acento ≠ `'ficcion'` sin acento: con el acento de menos no trae resultados.
- **Los nombres de tablas y columnas, en cambio, deben estar bien escritos:** si la columna se llama `género` (con acento) y se escribe `genero`, MySQL tira error de columna desconocida. El acento ahí **es un carácter distinto**.
- Mayúsculas/minúsculas en el *contenido* de los datos generalmente no generan error, pero **sí pueden hacer que un registro no aparezca** si hay valores escritos de las dos formas. Lo seguro es copiar el valor tal cual está en la tabla.

### 11.3 Modificaciones (`ALTER`, `UPDATE`, `DELETE`)

```sql
SET SQL_SAFE_UPDATES = 0;      -- desbloquear (si no, errores encadenados)

-- Agregar columna (estructura → ALTER)
ALTER TABLE autores ADD COLUMN telefono VARCHAR(20);

-- Cargar el dato de esa columna nueva (dato → UPDATE)
UPDATE autores SET telefono = '11-4444-5555' WHERE id_autor = 1;

-- Actualizar un dato puntual
UPDATE libros SET anio_publicacion = 1964 WHERE titulo = 'Rayuela';

-- Borrar un registro cargado por error
DELETE FROM prestamos WHERE id_prestamo = 3;

-- Renombrar una columna
ALTER TABLE prestamos CHANGE nombre_lector lector VARCHAR(50);
```

**Detalle clave del `CHANGE`:** al cambiar el nombre de una columna **no va coma** entre el nombre viejo y el nuevo: van separados solo por un espacio, y después el tipo de dato. Es el error más común en esta sentencia.

**Cuidado al renombrar columnas:** después del `CHANGE`, las consultas viejas que usaban `nombre_lector` **fallan**. Hay que actualizarlas al nombre nuevo (`lector`). Es un buen recordatorio de por qué conviene revisar los scripts después de cambiar una estructura.

### 11.4 JOIN

```sql
-- 6. Nombre del lector, título del libro y autor (3 tablas)
SELECT p.lector, l.titulo, a.nombre
FROM prestamos p
INNER JOIN libros  l ON p.id_libro = l.id_libro
INNER JOIN autores a ON l.id_autor = a.id_autor;

-- 7. Cada libro con su autor correspondiente (2 tablas)
SELECT l.titulo, a.nombre
FROM libros l
INNER JOIN autores a ON l.id_autor = a.id_autor;

-- 8. Nombre del autor y títulos publicados después de 1965
SELECT a.nombre, l.titulo, l.anio_publicacion
FROM libros l
INNER JOIN autores a ON l.id_autor = a.id_autor
WHERE l.anio_publicacion > 1965;

-- 9. Libros sin autor asignado (LEFT + IS NULL)
SELECT l.titulo
FROM libros l
LEFT JOIN autores a ON l.id_autor = a.id_autor
WHERE a.id_autor IS NULL;
```

- **Consulta 6:** aunque no se pida ningún dato de `prestamos` distinto del lector, hay que pasar por esa tabla porque es el único camino para llegar de `autores` a `libros`. Es el ejemplo perfecto de por qué existe el JOIN.
- **Consulta 7:** un solo `INNER JOIN` alcanza cuando la relación es directa.
- **Consulta 8:** el `WHERE` va **al final**, después de todos los JOIN.

### 11.5 Herramientas de Workbench que aparecieron en esta clase

- **`Ctrl + Shift + Enter`** ejecuta **todas** las consultas del script a la vez y abre un panel con varios resultados (pestañas «libros 10», «autores 11»…). Sirve para revisar el script completo, o para comparar resultados de varias consultas cliqueando entre ellas.
- **No se pueden ver dos resultados en paralelo** en el mismo espacio: MySQL Workbench muestra **un resultado por vez** (el de la última consulta ejecutada). Para comparar dos consultas hay que ejecutar una, sacar captura o anotar, y ejecutar la otra.

---

## 12. Vistas (VIEW)

### 12.1 Qué es

Una **vista** es una **consulta guardada con un nombre**, que se puede reutilizar como si fuera una tabla.

- Es el equivalente a una **función (`def`) en programación**: se guarda un bloque de código para no reescribirlo cada vez.
- Su utilidad aparece cuando **la misma consulta se repite** (por ejemplo, «todos los meses traeme la cantidad de ventas de estos 10 clientes»). En vez de reescribir todos los JOIN, se llama a la vista.

### 12.2 Crear, usar y borrar

```sql
-- Crear
CREATE VIEW vista_detalle_reserva AS
SELECT c.nombre, c.apellido, d.nombre_destino, r.fecha_reserva, r.cantidad_personas
FROM reservas r
INNER JOIN clientes c ON r.id_cliente = c.id_cliente
INNER JOIN destinos d ON r.id_destino = d.id_destino;

-- Consultar la vista (no muestra nada al crearla: hay que seleccionarla)
SELECT * FROM vista_detalle_reserva;

-- Consultar con condición
SELECT * FROM vista_detalle_reserva WHERE pais = 'Argentina';

-- Borrar
DROP VIEW vista_detalle_reserva;
```

- `CREATE VIEW` + **nombre representativo** + **`AS`** (obligatorio: sin `AS` no funciona) + **la consulta completa**.
- Al ejecutar el `CREATE VIEW`, **no se muestra el resultado**: solo se guarda. Para verlo hay que hacer `SELECT * FROM nombre_vista`.
- **Se le puede poner `WHERE`, `ORDER BY` o cualquier condición** al consultar la vista: es una consulta normal.
- `DROP VIEW nombre` borra la vista. **Hay que poner `VIEW`**: `DROP nombre` a secas no borra nada.
- Borrar una vista es más simple y seguro que borrar una tabla o una columna con FK.

### 12.3 Cuándo usarlas

- Con **consultas complejas** (JOIN de varias tablas) que se repiten.
- También con **consultas simples** que se usan todos los días.
- Se pueden crear vistas de una sola tabla: por ejemplo, una vista que muestre título y género desde `libros` con un `SELECT` simple es perfectamente válida.

### 12.4 Vistas con LEFT JOIN (caso de la base biblioteca)

```sql
-- Autores que no tienen libros
CREATE VIEW vista_autores_sin_libros AS
SELECT a.nombre
FROM autores a
LEFT JOIN libros l ON a.id_autor = l.id_autor
WHERE l.id_libro IS NULL;
```

- **Regla:** si la vista se arma con `LEFT JOIN` para priorizar una tabla, **todos** los JOIN de esa vista deben ser `LEFT` (usar un `INNER` y después un `LEFT` puede hacer perder registros que se querían conservar).
- **Ojo con los datos de prueba:** si en la base no hay ningún autor sin libros, la vista se ejecuta bien pero **no devuelve filas**. No es un error de la consulta: es que falta el caso en los datos.

### 12.5 Vistas de la práctica de biblioteca

```sql
-- Detalle de préstamos: lector, libro y autor (3 tablas)
CREATE VIEW vista_prestamos_detalle AS
SELECT p.lector, l.titulo, a.nombre
FROM prestamos p
LEFT JOIN libros  l ON p.id_libro = l.id_libro
LEFT JOIN autores a ON l.id_autor = a.id_autor;

-- Libros y sus géneros (una sola tabla → SELECT simple)
CREATE VIEW vista_libros_generos AS
SELECT titulo, genero FROM libros;

-- Autores sin libros (LEFT + IS NULL)
CREATE VIEW vista_autores_sin_libros AS
SELECT a.nombre
FROM autores a
LEFT JOIN libros l ON a.id_autor = l.id_autor
WHERE l.id_libro IS NULL;
```

- **Se pueden crear vistas de consultas simples**: la de `libros`/`generos` sale de una sola tabla y es perfectamente válida. La vista sirve para cualquier consulta que se repita, no solo para JOIN complejos.
- **Ojo con las vistas que ya existen:** si se quiere modificar una vista (`CREATE OR REPLACE` o cambiar un `INNER` por `LEFT`), primero hay que **borrarla** con `DROP VIEW` y volver a crearla. Sin eso, MySQL avisa que la vista ya existe.
- **Las vistas heredan el problema de los datos:** una vista de «autores sin libros» va a devolver vacío mientras no haya al menos un autor cargado sin libros.

---

## 13. Buenas prácticas, errores típicos y consejos de la cátedra

### 13.1 Buenas prácticas

- **Palabras reservadas en MAYÚSCULA**, nombres de tablas y columnas en minúscula.
- **Nombres de tablas y atributos en `singular`** y consistentes (`cliente`, no `clientes` en una parte y `Cliente` en otra).
- **Alias siempre en las funciones de agregación** (`AS cantidad_ventas`), y alias representativos.
- **Nombres de constraints representativos** (`fk_inscripciones_estudiantes`), no genéricos.
- **Separar `DDL` y `DML`** en archivos distintos (aunque en el parcial se unifiquen).
- **Guardar los scripts** en una carpeta ordenada, con nombres claros.
- **Comentar el código**: al menos una línea por consulta explicando qué hace.
- **Ejecutar de a una sentencia** al principio, para aislar errores.
- **Verificar con un `SELECT`** después de cada `UPDATE` o `ALTER`.
- **Tener el DER a mano** para las consultas con JOIN.
- **Antes de un `UPDATE` o `DELETE` masivo**, hacer el `SELECT` equivalente.
- **Probar**: si una consulta no sale, probar otra forma. «SQL no se rompe».

### 13.2 Errores más frecuentes (y cómo detectarlos)

| Error | Síntoma | Solución |
|---|---|---|
| **Coma de más o de menos** | Error incomprensible, a veces «arrastrado» desde la línea anterior | Revisar todas las comas: la última columna **no** lleva coma antes del paréntesis |
| **Espacio entre función y paréntesis** | `COUNT (*)` falla | La función va **pegada**: `COUNT(*)` |
| **Falta el punto y coma** | Error en la sentencia siguiente | Terminar cada sentencia en `;` |
| **Comillas faltantes o mal puestas** | Error de sintaxis o comparación que no trae resultados | Texto y fechas **siempre** entre comillas simples |
| **Nombre mal escrito** (tabla, columna, `producto` vs `producutos`) | «Table doesn't exist» / «Unknown column» | Revisar con el panel **Schemas** y refrescar |
| **Nombres con acento en los datos** | La consulta no trae el registro aunque parezca correcto | Escribir la condición **exactamente** como está cargado |
| **Alias incoherente** | Error de columna desconocida | Si se pone alias en el `SELECT`, usarlo en **todo** |
| **`WHERE` en lugar de `HAVING`** | Error de función de agregación | Las condiciones de grupo van en `HAVING` |
| **`UPDATE` sin `WHERE`** | Se modificó toda la tabla | Agregar la condición (y verificarla con un `SELECT` antes) |
| **Se intenta crear una FK a una tabla que no existe** | No ejecuta | Crear primero las tablas padre |
| **Base de datos con el mismo nombre** | Se trabaja sobre la base equivocada y aparecen columnas que «no existen» | Verificar con `USE`; como último recurso, `DROP DATABASE` y recrear |
| **Falta `SET SQL_SAFE_UPDATES = 0;`** | Errores encadenados al hacer muchos `UPDATE`/`ALTER` sin causa aparente | Ejecutar esa línea antes de las modificaciones |
| **Se ejecutó solo una parte del código** | La tabla no se crea o la consulta falla | Seleccionar **todas** las líneas necesarias y ejecutar |
| **`DELETE` sin `FROM`** (`DELETE prestamos ...`) | MySQL no sabe de dónde borrar | `DELETE FROM tabla WHERE ...` |
| **`= NULL`** | No filtra nada / no devuelve resultados | Usar **`IS NULL`** |
| **Acento en el nombre de una columna** (`género` escrito `genero`) | «Unknown column» | El acento es otro carácter: escribir el nombre exacto |
| **Coma entre nombre viejo y nuevo en `CHANGE`** | Error de sintaxis | `CHANGE viejo nuevo TIPO`, separados solo por espacio |
| **Se renombró una columna y las consultas viejas fallan** | «Unknown column» en consultas que antes funcionaban | Actualizar las consultas al nombre nuevo |
| **Se intenta modificar una vista existente** | «View already exists» | `DROP VIEW` y volver a crear |

### 13.3 Consejos de estudio que dio la profesora

- **No copiar y pegar**: tipear las consultas. Copiar y pegar hace que se pierda la noción de la estructura, y en el parcial no se puede copiar y pegar.
- **Aprender la lógica, no de memoria**: si se entiende *por qué* se une tal tabla con tal clave, se puede resolver con 3, 5 o 20 tablas.
- **Equivocarse es parte del proceso**: los errores aparecen siempre, incluso con años de experiencia. Leer el mensaje de error y buscar la causa.
- **Practicar sí o sí**: es la única forma de internalizar SQL.
- **Ajustarse a lo que pide el ejercicio**: ni más ni menos. Si se agrega un dato extra, no está mal, pero si falta algo que se pidió, sí.
- **Participar y compartir pantalla** en clase: ver los errores de otros es una de las formas más rápidas de aprender.

---

## 14. Bases de datos usadas para practicar

| Base | Tablas | Relación central | Ejercicios asociados |
|---|---|---|---|
| **escuela** | `estudiantes`, `cursos`, `inscripciones` | Estudiantes ↔ cursos: **muchos a muchos** vía `inscripciones` | Consultas simples, JOIN, prácticas de clase |
| **tienda / tienda_online** | `clientes`, `productos`, `ventas` | Clientes ↔ productos: **muchos a muchos** vía `ventas` | DDL + DML completos, JOIN, `LEFT`/`RIGHT`, agregaciones |
| **clínica** | `pacientes`, `médicos`, `turnos` | Pacientes ↔ médicos: **muchos a muchos** vía `turnos` | Práctica integral (estructura + datos + consultas) |
| **Travel Now** | `paises`, `destinos`, `clientes`, `reservas` | Clientes ↔ destinos vía `reservas`; destinos → países | Vistas, consultas simples, agregaciones |
| **instituto** | `docentes`, `estudiantes`, `cursos`, `inscripciones` | 4 tablas: estudiantes → inscripciones → cursos → docentes | JOIN múltiples, `LEFT`/`RIGHT`, `HAVING` |
| **biblioteca** | `autores`, `libros`, `prestamos` | Autores → libros; libros ↔ préstamos | `GROUP BY`/`HAVING`, vistas, `MAX`/`MIN`, práctica integral de la clase del 3/11 |

**Consigna tipo de la práctica «tienda»:**

- **Parte 1 (estructura y datos):** crear la base `tienda_online`; crear `clientes` (id entero PK, nombre texto 50 obligatorio, apellido 50 obligatorio, edad entero, email texto 100 obligatorio y único); crear `productos` (id PK, nombre producto 100 obligatorio, categoría 50, precio `DECIMAL(10,2)`); crear `ventas` (id PK, id_cliente FK, id_producto FK, fecha_venta `DATE`). Insertar al menos 5 registros en cada tabla.
- **Parte 2 (consultas):** consultas simples, actualizaciones (`UPDATE`), modificaciones de estructura (`ALTER`) y funciones de agregación.

**Recomendaciones sobre los datos de prueba:** como cada alumno carga sus propios datos, los resultados varían. Si una consulta pide una categoría que no existe en los datos («tecnología» cuando se cargó «informática»), la tabla sale vacía: **no es un error**, hay que ajustar el valor a los datos reales. Antes de escribir la condición, conviene mirar qué valores hay.

---

## 15. Cómo se evalúa (parcial)

**Formato:**

- **Un solo archivo `.sql`**, nombrado con **nombre y apellido** del alumno (no con el nombre de la base de datos).
- Se puede hacer **todo junto**: estructura (`CREATE DATABASE`/`TABLE`), carga de datos (`INSERT`) y consultas. No hace falta entregar dos archivos.
- Las respuestas de **verdadero/falso o múltiple choice** se escriben **comentadas** en el mismo archivo (`-- respuesta`), al final.

**Dos partes evaluadas por separado:**

1. **Base de datos propia:** crear la estructura y cargar los datos. Se corrige **cómo se armó** (tablas, constraints, tipos de datos, orden de creación, coherencia).
2. **Consultas:** se hacen sobre **otra base de datos, provista por la cátedra**, con su **DER impreso**. No se usan los datos propios.
   - **Motivo:** si las consultas se hicieran sobre la base creada por el alumno, un error en una FK o una PK haría fallar todo por una pavada. Separando, se evalúa cada cosa por su lado.
   - Lo que se evalúa en las consultas: que **el código se ejecute** y que **devuelva exactamente lo que pide la consigna**.

**Sobre los JOIN en el parcial:**

- **El tipo de JOIN estará indicado en el enunciado** (si es `LEFT` o `RIGHT`, se dice). No hay que adivinarlo.
- Se tomarán pocas consultas de `LEFT`/`RIGHT`; el **`INNER JOIN`** es el más usado y el más evaluado.
- Se tomarán **pocas consultas de vistas y de `GROUP BY`** (por una cuestión de tiempo), pero están.
- **`FULL JOIN` no se toma.**
- Se puede usar el alias en el `HAVING`.
- **El borrado en cadena (sin `ON DELETE CASCADE`) sí puede aparecer**, porque la estructura de la base del parcial probablemente no incluya las cascadas. Es el ejercicio de «borrar el autor y todas sus dependencias»: hay que resolverlo tabla por tabla, con el DER impreso a mano.
- El DER del parcial **se entrega impreso**: no hay que dibujarlo. (En el examen no se pide el DER; se evalúa en la primera parte de la cursada.)

**Lo que NO se descuenta:**

- No poner las palabras reservadas en mayúscula.
- Agregar `NOT NULL` cuando la consigna no lo pedía.
- Traer un dato extra (por ejemplo, el apellido cuando solo pedían el nombre, o el nombre del producto cuando solo pedían cliente y fecha).
- Usar nombres completos de tabla en lugar de alias (o al revés).

**Lo que SÍ importa:**

- Que la **estructura esté bien armada** (tablas, PK, FK, tipos de datos coherentes).
- Que **la consulta se ejecute** sin error.
- Que **el resultado sea el pedido**.
- Que se note que se entendieron los **conceptos centrales** (normalización, DER, lógica de los JOIN).

**Consejo para el día del parcial:** llevar la línea `SET SQL_SAFE_UPDATES = 0;` ya incluida arriba de todo, para no perder tiempo ni bloquearse con errores de actualización.

---

## 16. Chuleta de sintaxis

```sql
-- ============ DDL ============
CREATE DATABASE nombre_bd;
USE nombre_bd;
DROP DATABASE nombre_bd;

CREATE TABLE tabla (
    id          INT PRIMARY KEY AUTO_INCREMENT,
    nombre      VARCHAR(50)  NOT NULL,
    email       VARCHAR(100) NOT NULL UNIQUE,
    estado      ENUM('activo','inactivo') DEFAULT 'activo',
    fecha       DATE,
    precio      DECIMAL(10,2),
    id_otra     INT,
    CONSTRAINT fk_nombre FOREIGN KEY (id_otra) REFERENCES otra(id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

ALTER TABLE tabla ADD columna TIPO;
ALTER TABLE tabla DROP COLUMN columna;
ALTER TABLE tabla CHANGE columna_vieja columna_nueva TIPO;
ALTER TABLE tabla MODIFY columna TIPO;
DROP TABLE tabla;

-- ============ DML: datos ============
INSERT INTO tabla (col1, col2) VALUES ('a', 1), ('b', 2);

SELECT * FROM tabla;
SELECT col1, col2 FROM tabla;
SELECT * FROM tabla WHERE col1 = 'valor';
SELECT * FROM tabla WHERE col1 LIKE '%texto%';
SELECT * FROM tabla WHERE col1 BETWEEN 1 AND 10;
SELECT * FROM tabla WHERE col1 IN ('a','b');
SELECT DISTINCT col1 FROM tabla;
SELECT * FROM tabla ORDER BY col1 DESC;
SELECT * FROM tabla WHERE MONTH(fecha) = 4;

-- ============ DML: modificar / borrar ============
SET SQL_SAFE_UPDATES = 0;                  -- desbloquea UPDATE/ALTER

UPDATE tabla SET col1 = 'nuevo' WHERE id = 1;
DELETE FROM tabla WHERE id = 1;

-- ============ Agregación ============
SELECT COUNT(*)              AS total     FROM tabla;
SELECT SUM(col_numerica)     AS total     FROM tabla;
SELECT AVG(col_numerica)     AS promedio  FROM tabla;
SELECT MAX(col)              AS maximo    FROM tabla;
SELECT MIN(col)              AS minimo    FROM tabla;
SELECT ROUND(AVG(col))       AS promedio  FROM tabla;
SELECT COUNT(DISTINCT col)   AS distintos FROM tabla;

-- ============ GROUP BY / HAVING ============
SELECT col_grupo, COUNT(*) AS cantidad
FROM tabla
WHERE condicion
GROUP BY col_grupo
HAVING COUNT(*) > 1
ORDER BY cantidad DESC;

-- ============ JOIN ============
SELECT a.col, b.col
FROM tabla_a a
INNER JOIN tabla_b b ON a.id = b.id_a;

SELECT a.col, b.col
FROM tabla_a a
LEFT JOIN tabla_b b ON a.id = b.id_a;

SELECT a.col, b.col
FROM tabla_a a
RIGHT JOIN tabla_b b ON a.id = b.id_a;

-- Solo los que NO tienen pareja (left + is null)
SELECT a.col FROM tabla_a a
LEFT JOIN tabla_b b ON a.id = b.id_a
WHERE b.id IS NULL;

-- ============ Vistas ============
CREATE VIEW nombre_vista AS
SELECT a.col, b.col
FROM tabla_a a
INNER JOIN tabla_b b ON a.id = b.id_a;

SELECT * FROM nombre_vista;
SELECT * FROM nombre_vista WHERE col = 'valor';
DROP VIEW nombre_vista;

-- ============ Borrado en cadena (sin cascade) ============
-- Orden: primero lo que depende, al final el registro principal
DELETE FROM prestamos WHERE id_libro IN (3, 12);
DELETE FROM libros    WHERE id_autor = 3;
DELETE FROM autores   WHERE id_autor = 3;

-- ============ Workbench ============
-- Ctrl + Enter        → ejecutar la selección
-- Ctrl + Shift + Enter → ejecutar TODAS las consultas del script
```

---

## Glosario rápido

| Término | Significado |
|---|---|
| **DDL** | Lenguaje de definición de datos: estructura (tablas, columnas, restricciones) |
| **DML** | Lenguaje de manipulación de datos: insertar, consultar, actualizar, borrar |
| **PK (Primary Key)** | Clave primaria: identifica de forma única cada fila. Única y no nula |
| **FK (Foreign Key)** | Clave foránea: relaciona con la PK de otra tabla |
| **Constraint** | Restricción o regla aplicada a un atributo |
| **Tabla padre** | Tabla cuyos datos son referenciados por otras |
| **Tabla hija / intermedia** | Tabla que contiene las FK y resuelve una relación muchos a muchos |
| **DER** | Diagrama Entidad-Relación: el «mapa» de la base |
| **Normalización** | Proceso de organizar los datos para evitar redundancia (cada tabla con sus atributos y su PK) |
| **Alias** | Nombre abreviado para una tabla o una columna (`AS`) |
| **JOIN** | Operación que combina filas de dos o más tablas por una columna en común |
| **`ON`** | Condición que indica **por dónde** se unen las tablas |
| **`WHERE`** | Filtro de **filas** |
| **`HAVING`** | Filtro de **grupos** (después de `GROUP BY`) |
| **Agregación** | Función que resume muchas filas en un valor (`COUNT`, `SUM`, `AVG`, `MAX`, `MIN`) |
| **Vista** | Consulta guardada con un nombre, reutilizable como tabla |
| **`NULL`** | Ausencia de valor (distinto de vacío o de cero) |
