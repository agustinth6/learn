# GROUP BY explicado (con resultados reales de `clinica_medica`)

> Cada resultado de esta hoja se obtuvo ejecutando la consulta sobre la base del material
> (8 especialidades · 15 pacientes · 15 médicos · 15 → 30 turnos). Podés reproducir todos con
> `python3 practica/run.py "…"`.

---

## 1. La idea en una frase

**`GROUP BY` parte las filas en "cajones" y devuelve UNA fila por cajón.**

Sin `GROUP BY` la tabla entera es un solo cajón:

```sql
SELECT COUNT(*) AS pacientes, AVG(edad) AS edad_prom FROM pacientes;
-- pacientes = 15 · edad_prom = 47.4      → 1 fila
```

Con `GROUP BY ciudad`, el cajón se define por ciudad:

```sql
SELECT ciudad, COUNT(*) AS pacientes, ROUND(AVG(edad),1) AS edad_prom
FROM pacientes
GROUP BY ciudad
ORDER BY pacientes DESC, ciudad;
-- Rosario 3 (58.7) · Buenos Aires 2 (37) · Córdoba 2 (26.5) · Mendoza 2 (48) · Salta 2 (50)
-- La Plata 1 (54) · Neuquén 1 (67) · San Juan 1 (58) · Tucumán 1 (33)      → 9 filas
```

El `COUNT(*)` ya no cuenta "todos": **cuenta dentro de cada cajón**. Lo mismo pasa con `AVG`, `SUM`, `MAX`, `MIN`.

---

## 2. Los términos

| Término | Qué es | Dónde lo ves |
|---|---|---|
| **clave de agrupamiento** (columna de grupo) | lo que va después de `GROUP BY`; define los cajones | `GROUP BY ciudad` |
| **clave compuesta** | agrupar por 2 o más columnas (cajón = combinación) | `GROUP BY ciudad, rango` |
| **función de agregación** | reduce N filas a 1 valor | `COUNT`, `SUM`, `AVG`, `MAX`, `MIN`, `GROUP_CONCAT` |
| **agregado por grupo** | la agregada evaluada dentro de cada cajón | `COUNT(*)` por ciudad |
| **filtro de filas (`WHERE`)** | se aplica **antes** de armar los cajones | `WHERE edad > 40` |
| **filtro de grupos (`HAVING`)** | se aplica **después**, sobre cada cajón ya armado | `HAVING COUNT(*) > 1` |
| **agrupar por expresión** | el cajón no es una columna, es un cálculo | `GROUP BY YEAR(fecha)`, `GROUP BY CASE…` |
| **`DISTINCT` dentro de la agregada** | contar valores sin repetir | `COUNT(DISTINCT id_paciente)` |
| **alias** | nombre que le ponés al agregado para leer/ordenar | `… AS pacientes` |
| **`ONLY_FULL_GROUP_BY` / error 1055** | el modo de MySQL que te obliga a la regla de oro | ver punto 3 |
| **dependencia funcional** | si agrupás por la PK, podés mostrar otras columnas de esa tabla | `GROUP BY m.id_medico` → `m.nombre` ✓ |
| **agregado ponderado** | el `JOIN` duplica filas y sesega el `AVG` | ver punto 6.h |

### Las agregaciones, una por una

| Función | Qué hace | Con NULLs | Ejemplo real |
|---|---|---|---|
| `COUNT(*)` | cuenta **filas** | los cuenta igual | 37 filas en `medicos LEFT JOIN turnos` |
| `COUNT(col)` | cuenta valores **no nulos** de esa columna | los ignora | 30 (los 7 `NULL` de los médicos sin turnos no cuentan) |
| `COUNT(DISTINCT col)` | valores distintos | ignora `NULL` | 9 ciudades en `pacientes` |
| `SUM(col)` | suma | ignora `NULL` | masa salarial Neurología 1.130.000 |
| `AVG(col)` | promedio de los no nulos | divide por la cantidad de no nulos, no por `COUNT(*)` | 483.666,67 |
| `MAX` / `MIN` | extremo; funciona con fecha y texto también | ignora `NULL` | `MAX(fecha_turno)` = 2025-10-30 |
| `GROUP_CONCAT(col)` (MySQL) | junta los valores en un string | ignora `NULL` | Rosario → `Juan,Laura,Pedro` |
| `ROUND(x, n)` | no es agregada: redondea el resultado | — | `ROUND(AVG(edad),1)` = 58.7 |

---

## 3. La regla de oro

> **Toda columna que aparezca en el `SELECT` y que no esté dentro de una agregación tiene que estar en el `GROUP BY`.**

¿Por qué? Porque al agrupar, cada cajón representa a **muchas filas**, y una columna suelta no tiene un valor único:

```sql
SELECT ciudad, nombre, COUNT(*) AS n FROM pacientes GROUP BY ciudad;  -- mal
```

En SQLite corre y te tira algo:

```
Buenos Aires  María   2      ← ¿María o Jorge? Son 2 pacientes…
Córdoba       Lucía   2        eligió uno al azar. MIENTE.
```

En MySQL con `ONLY_FULL_GROUP_BY` (viene prendido por defecto desde 5.7) **no corre**:

```
ERROR 1055 (42000): Expression #2 of SELECT list is not in GROUP BY clause…
```

Tres salidas válidas:

```sql
-- a) sacarla
SELECT ciudad, COUNT(*) AS n FROM pacientes GROUP BY ciudad;

-- b) agruparla también (cajón = ciudad + nombre)
SELECT ciudad, nombre, COUNT(*) AS n FROM pacientes GROUP BY ciudad, nombre;

-- c) agregarla (forzar un valor por grupo)
SELECT ciudad, GROUP_CONCAT(nombre) AS nombres, COUNT(*) AS n FROM pacientes GROUP BY ciudad;
-- Rosario → 'Juan,Laura,Pedro' · 3
```

**Excepción que sí vale:** si el `GROUP BY` usa la **clave primaria**, MySQL deja seleccionar cualquier otra columna de esa tabla (dependencia funcional):

```sql
SELECT m.id_medico, m.nombre, m.apellido, COUNT(t.id_turno) AS turnos   -- OK en MySQL 8
FROM medicos m LEFT JOIN turnos t ON t.id_medico = m.id_medico
GROUP BY m.id_medico;
```

---

## 4. El orden de ejecución (esto explica el 90 % de las dudas)

Vos **escribís**: `SELECT` → `FROM` → `WHERE` → `GROUP BY` → `HAVING` → `ORDER BY` → `LIMIT`.
La base **ejecuta**:

```
FROM  →  WHERE  →  GROUP BY  →  HAVING  →  SELECT (acá nacen los alias)  →  ORDER BY  →  LIMIT
 1         2          3            4              5                            6           7
```

De ahí se desprende todo:

- En `WHERE` todavía **no existe** `COUNT(*)` → `WHERE COUNT(*) > 1` es ilegal.
- En `HAVING` los grupos ya existen → ahí van las agregadas.
- El alias (`AS n`) nace en el paso 5, por eso **no** se puede usar en `WHERE`, pero **sí** en `HAVING` y en `ORDER BY` (MySQL lo permite; el estándar solo en `ORDER BY`).

```sql
-- ✅ filtrar grupos con alias (MySQL lo acepta)
SELECT ciudad, COUNT(*) AS n FROM pacientes GROUP BY ciudad HAVING n > 1;
-- ❌ ERROR 1111 / "misuse of aggregate" si ponés COUNT(*) en el WHERE
```

### `WHERE` vs `HAVING`, lado a lado con los mismos datos

```sql
SELECT ciudad, COUNT(*) AS n FROM pacientes WHERE edad > 40 GROUP BY ciudad;
```
```
Rosario 3 · Mendoza 2 · La Plata 1 · Neuquén 1 · Salta 1 · San Juan 1     → 6 filas
```
Filtra **pacientes** (los de 40 o menos nunca entran al conteo).

```sql
SELECT ciudad, COUNT(*) AS n FROM pacientes GROUP BY ciudad HAVING COUNT(*) > 1;
```
```
Rosario 3 · Buenos Aires 2 · Córdoba 2 · Mendoza 2 · Salta 2              → 5 filas
```
Cuenta **todos** y después tira los cajones chicos.

```sql
-- los dos: primero filas, después grupos
SELECT ciudad, COUNT(*) AS n
FROM pacientes
WHERE edad > 40
GROUP BY ciudad
HAVING COUNT(*) > 1;
```
```
Rosario 3 · Mendoza 2      → 2 filas
```

---

## 5. La plantilla

```sql
SELECT   columna_grupo,                              -- solo lo que está en GROUP BY…
         AGREGACION(otra_columna) AS alias           -- …o dentro de una agregada
FROM     tabla
WHERE    filtro_sobre_filas                           -- opcional (no lleva agregadas)
GROUP BY columna_grupo                                -- los cajones
HAVING   filtro_sobre_grupos                           -- opcional (acá sí agregadas)
ORDER BY alias DESC, columna_grupo                    -- opcional
LIMIT    n;                                           -- opcional
```

---

## 6. Los patrones que hay que tener domados

### a) Varias agregadas a la vez (mismo `GROUP BY`)

```sql
SELECT ciudad, MAX(edad) AS mayor, MIN(edad) AS menor
FROM pacientes GROUP BY ciudad ORDER BY (MAX(edad) - MIN(edad)) DESC;
```
```
Salta 70/30 · Rosario 73/41 · Mendoza 51/45 · Buenos Aires 39/35 · Córdoba 28/25 · …
```
El `ORDER BY` también puede llevar una cuenta entre agregadas (`MAX - MIN`), porque se evalúa al final. Y `MIN`/`MAX` sirven igual con `DATE` o con texto.

### b) SUM + ranking (top-N)

```sql
SELECT e.nombre_especialidad, SUM(m.salario) AS masa_salarial
FROM especialidades e INNER JOIN medicos m ON m.id_especialidad = e.id_especialidad
GROUP BY e.nombre_especialidad
ORDER BY masa_salarial DESC
LIMIT 3;
```
```
Neurología 1.130.000 · Oftalmología 1.050.000 · Cardiología 1.050.000
```

### c) Contar "cuántos" vs "cuáles": `COUNT(DISTINCT x)`

```sql
SELECT e.nombre_especialidad,
       COUNT(t.id_turno) AS turnos,
       COUNT(DISTINCT t.id_paciente) AS pacientes_distintos
FROM turnos t
INNER JOIN medicos m ON t.id_medico = m.id_medico
INNER JOIN especialidades e ON m.id_especialidad = e.id_especialidad
GROUP BY e.nombre_especialidad;
```
```
Cardiología 4/4 · Clínica General 4/4 · Dermatología 4/4 · Neurología 4/4 · Pediatría 4/4
Traumatología 4/4 · Ginecología 3/3 · Oftalmología 3/3   (suma de turnos = 30 ✓)
```
Si un paciente se atendiera 2 veces en la misma especialidad, `turnos` y `pacientes_distintos` se separarían. Fijate que el truco de sumar los grupos y comprobar que da el total (30) es la mejor forma de verificar que un `JOIN` no duplicó filas.

### d) Agrupar por un rango que no existe como columna (`CASE`)

```sql
SELECT CASE WHEN edad < 40 THEN '18 a 39' WHEN edad < 60 THEN '40 a 59' ELSE '60 y más' END AS rango,
       COUNT(*) AS pacientes, ROUND(AVG(edad),1) AS edad_prom
FROM pacientes
GROUP BY rango
ORDER BY rango;
```
```
18 a 39 → 6 (31.7) · 40 a 59 → 5 (49.8) · 60 y más → 4 (68)
```
`GROUP BY rango` funciona porque MySQL permite agrupar por alias (el estándar no; en Postgres hay que repetir el `CASE`).

### e) Dos columnas de grupo (cajón = combinación)

```sql
SELECT ciudad,
       CASE WHEN edad < 40 THEN '1: 18-39' ELSE '2: 40+' END AS rango,
       COUNT(*) AS n
FROM pacientes
GROUP BY ciudad, rango
ORDER BY ciudad, rango;
```
```
10 filas: Salta 18-39 → 1 · Salta 40+ → 1 · Rosario 40+ → 3 · …
```
`Salta` aparece dos veces porque ahora es "Salta × rango".

### f) Agrupar por una parte de la fecha

```sql
SELECT SUBSTR(fecha_turno, 1, 7) AS mes, COUNT(*) AS turnos FROM turnos GROUP BY mes;
-- en MySQL: DATE_FORMAT(fecha_turno, '%Y-%m') o YEAR(fecha_turno), MONTH(fecha_turno)
```
```
2025-10 → 30     → 1 fila (todos los turnos son de octubre)
```

### g) El `GROUP BY` después de un `LEFT JOIN`: "los que no tienen nada"

```sql
SELECT m.nombre, COUNT(*) AS filas, COUNT(t.id_turno) AS turnos_reales
FROM medicos m LEFT JOIN turnos t ON t.id_medico = m.id_medico
GROUP BY m.id_medico
ORDER BY turnos_reales, m.nombre;
```
```
Camila 1/0 · Gabriela 1/0 · Javier 1/0 · Natalia 1/0 · … (7 médicos sin turnos)
```
`COUNT(*)` dice **1** y `COUNT(t.id_turno)` dice **0**: el `LEFT JOIN` creó una fila con `NULL` en `t.*` para el médico que no atendió a nadie, `COUNT(*)` la cuenta y `COUNT(col)` no. Ese par de números es la diferencia entre "1 turno" y "0 turnos". Por eso:

```sql
… GROUP BY m.id_medico HAVING COUNT(t.id_turno) = 0;   -- los 7 sin turnos
```
con `INNER JOIN` esta consulta devolvería **0 filas**: el `INNER` descarta justamente las filas sin turno, que son las que estabas buscando. Y el total de filas del `LEFT JOIN` es 37 (30 con turno + 7 con `NULL`), no 15.

### h) La trampa del JOIN que sesga el promedio

```sql
SELECT ROUND(AVG(salario),2) FROM medicos;                                        -- 483666.67
SELECT ROUND(AVG(m.salario),2) FROM medicos m INNER JOIN turnos t
     ON t.id_medico = m.id_medico;                                                -- 480166.67
```
Hay **dos efectos** mezclados, y conviene tenerlos separados:

1. el `INNER JOIN` **excluye** a los 7 médicos sin turnos (el promedio pasa a ser de 8, no de 15);
2. y repite el sueldo de cada médico **una vez por turno**, así que el resultado queda ponderado:

```
peso 4: Luis 420000 · Valeria 430000 · Andrés 450000 · Pedro 470000 · Carla 510000 · Romina 560000
peso 3: Lucas 495000 · Marina 520000
```
Por eso 483666.67 (los 15) → 481875 (los 8 que atendieron) → 480166.67 (ponderado por turno).
Ninguno está "mal": son preguntas distintas. Elegí primero qué pregunta querés responder. Si lo que querías era "el promedio de los médicos que atendieron", separá los pasos:

```sql
SELECT ROUND(AVG(salario),2) FROM medicos
WHERE id_medico IN (SELECT id_medico FROM turnos);        -- 481875
```

### i) Porcentaje sobre el total, con `GROUP BY`

```sql
SELECT e.nombre_especialidad,
       COUNT(*) AS turnos,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM turnos), 1) AS porcentaje
FROM turnos t
INNER JOIN medicos m ON t.id_medico = m.id_medico
INNER JOIN especialidades e ON m.id_especialidad = e.id_especialidad
GROUP BY e.nombre_especialidad;
```
```
13.3 % (seis especialidades) · 10 % (dos)   → el total da 100 %
```
El `* 100.0` (con punto decimal) evita la división entera, y el `(SELECT COUNT(*) …)` es el total contra el que se calcula el porcentaje: no lo saques del `GROUP BY`, ponelo en un subquery.

### j) Bonus MySQL: `WITH ROLLUP` (el total al pie)

```sql
SELECT ciudad, COUNT(*) AS n FROM pacientes GROUP BY ciudad WITH ROLLUP;
```
Agrega una última fila con `NULL` en `ciudad` y el total (15). Útil para un informe, no lo pidieron en el material.

---

## 7. Errores típicos y su antídoto

| Síntoma | Causa | Arreglo |
|---|---|---|
| `ERROR 1055 … not in GROUP BY clause` | columna suelta en el `SELECT` | agrupala, sacala o metela en una agregada |
| `ERROR 1111 Invalid use of group function` | `COUNT()` en el `WHERE` | movelo al `HAVING` |
| `ERROR 1054 Unknown column 'n' in 'where clause'` | usaste un alias del `SELECT` en el `WHERE` | el alias nace en el paso 5: usá `HAVING`/`ORDER BY` o repetí la expresión |
| `AVG`/`SUM` más grandes o más chicos de lo esperado | el `JOIN` de 1:N duplicó filas | verificá con `COUNT(*)` contra el total, o agregá antes de joinear (subquery) |
| `COUNT(*)` dice 1 y "no hay datos" | `LEFT JOIN` sin coincidencia | contá con `COUNT(clave_hija)` |
| Un grupo "desaparece" | `INNER JOIN` filtró los que no tenían nada | `LEFT JOIN` + `HAVING COUNT(...) = 0` |
| El orden de los empates cambia cada vez | `ORDER BY` sin desempate | agregá la columna de grupo al final: `ORDER BY n DESC, ciudad` |
| `GROUP BY` no agrupa por lo que creías | agrupás por `id` pero mostrás `nombre`, y hay nombres duplicados | agrupá por la misma columna que mostrás, o por ambas |
| SQLite te deja hacer algo que MySQL rechaza | SQLite no valida `ONLY_FULL_GROUP_BY` | no te confíes del resultado "arbitrario" |

---

## 8. Checklist para el parcial

1. ¿Qué **fila** quiero que me devuelva la consulta? → esa es la clave del `GROUP BY`.
2. Lo que no esté en esa fila (ni en agregada) **no va en el `SELECT`**.
3. Filtro de filas → `WHERE`. Filtro de grupos → `HAVING`.
4. ¿Joinee antes o después de agregar? (si joinear duplica, agregá primero en un subquery).
5. `ORDER BY alias DESC, clave_de_grupo` para que el resultado sea estable.
6. Sumá los grupos y compará contra el total real: si no cierra, hay duplicados por `JOIN`.
7. `ROUND(x, 2)` para los promedios, `* 100.0` para porcentajes.
