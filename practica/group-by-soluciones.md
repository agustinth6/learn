# GROUP BY · soluciones comentadas

Todas estas consultas fueron **ejecutadas** sobre `clinica_medica` con los datos del material,
así que los resultados de abajo son los reales (no "de memoria"). Si te da otro número,
revisá el `JOIN` o el `GROUP BY` antes de seguir.

## Nivel 1

**1. Cantidad de pacientes por ciudad.**

```sql
SELECT ciudad, COUNT(*) AS pacientes
FROM pacientes
GROUP BY ciudad
ORDER BY pacientes DESC, ciudad;
```

9 filas: Rosario 3 · Buenos Aires, Córdoba, Mendoza y Salta 2 · La Plata, Neuquén, San Juan y Tucumán 1.
`ORDER BY pacientes DESC, ciudad` desempata alfabéticamente; sin la segunda clave el orden de los empates es indeterminado.

**2. Especialidades con más de un médico.**

```sql
SELECT e.nombre_especialidad, COUNT(m.id_medico) AS medicos
FROM especialidades e
LEFT JOIN medicos m ON m.id_especialidad = e.id_especialidad
GROUP BY e.nombre_especialidad
HAVING COUNT(m.id_medico) > 1;
```

7 filas (queda afuera Ginecología, que tiene un solo médico).
Con `LEFT JOIN` + `COUNT(m.id_medico)` una especialidad sin médicos daría `0`; con `INNER JOIN` directamente desaparecería de la lista.

**3. Salario máximo, mínimo y promedio.**

```sql
SELECT MAX(salario) AS maximo, MIN(salario) AS minimo, ROUND(AVG(salario), 2) AS promedio
FROM medicos;
```

`570000 · 410000 · 483666.67`. Una sola fila: **agrupar no es obligatorio para usar agregadas**, sin `GROUP BY` todo el resultado es un único grupo.

**4. Edad promedio y cantidad por ciudad.**

```sql
SELECT ciudad, ROUND(AVG(edad), 1) AS edad_promedio, COUNT(*) AS pacientes
FROM pacientes
GROUP BY ciudad
ORDER BY edad_promedio DESC;
```

Neuquén 67 (1 paciente) · Rosario 58.7 (3) · San Juan 58 · La Plata 54 · Salta 50 · Mendoza 48 · Buenos Aires 37 · Tucumán 33 · Córdoba 26.5.
Fijate que el `ORDER BY` puede usar el alias porque se aplica **después** del `SELECT`.

**5. Turnos por mes.**

```sql
SELECT SUBSTR(fecha_turno, 1, 7) AS mes, COUNT(*) AS turnos
FROM turnos
GROUP BY mes;
```

1 fila: `2025-10` con 30. En MySQL podés usar `DATE_FORMAT(fecha_turno, '%Y-%m')` o `YEAR()`/`MONTH()`; `SUBSTR` funciona en los dos porque la fecha es `YYYY-MM-DD`.

## Nivel 2

**6. Turnos por especialidad.**

```sql
SELECT e.nombre_especialidad, COUNT(t.id_turno) AS turnos
FROM turnos t
INNER JOIN medicos m ON t.id_medico = m.id_medico
INNER JOIN especialidades e ON m.id_especialidad = e.id_especialidad
GROUP BY e.nombre_especialidad;
```

8 filas · Cardiología, Clínica General, Dermatología, Neurología, Pediatría y Traumatología con **4**; Ginecología y Oftalmología con **3**. Suma 30 ✓ (buena forma de verificar que el JOIN no duplicó filas).

**7. Top 5 de ciudades por turnos.**

```sql
SELECT p.ciudad, COUNT(t.id_turno) AS turnos
FROM turnos t
INNER JOIN pacientes p ON t.id_paciente = p.id_paciente
GROUP BY p.ciudad
ORDER BY turnos DESC, p.ciudad
LIMIT 5;
```

Rosario 6 · Buenos Aires, Córdoba, Mendoza y Salta 4.

**8. Médicos que no atendieron ningún turno.**

```sql
SELECT m.nombre, m.apellido, COUNT(t.id_turno) AS turnos
FROM medicos m
LEFT JOIN turnos t ON t.id_medico = m.id_medico
GROUP BY m.id_medico
HAVING COUNT(t.id_turno) = 0;
```

7 filas: Natalia Herrera, Sebastián López, Gabriela Martínez, Javier Molina, Camila Ortega, Tomás Rivas, Ricardo Silva.
Con `INNER JOIN` esta lista sale **vacía**: el inner echa afuera justo las filas que teníamos que encontrar.

**9. Turnos y pacientes distintos por médico.**

```sql
SELECT m.id_medico,
       COUNT(t.id_turno) AS turnos,
       COUNT(DISTINCT t.id_paciente) AS pacientes
FROM medicos m
LEFT JOIN turnos t ON t.id_medico = m.id_medico
GROUP BY m.id_medico
ORDER BY m.id_medico
LIMIT 8;
```

Médicos 1 a 6: `4 turnos / 4 pacientes` · 7 y 8: `3 / 3`. `COUNT(DISTINCT …)` responde "¿a cuántos clientes distintos?", que no es lo mismo que "¿cuántas filas?".

**10. Motivos que se repiten.**

```sql
SELECT motivo, COUNT(*) AS veces
FROM turnos
GROUP BY motivo
HAVING COUNT(*) > 1
ORDER BY veces DESC, motivo;
```

Control general 4 · Chequeo cardíaco 3 · Control clínico, Control visual y Dermatitis 2.

## Nivel 3 · las trampas

**11. Por qué cambia el promedio al JOINEAR.**

```sql
SELECT ROUND(AVG(salario), 2) FROM medicos;                                  -- 483666.67
SELECT ROUND(AVG(m.salario), 2)
FROM medicos m INNER JOIN turnos t ON t.id_medico = m.id_medico;              -- 480166.67
```

Porque el `JOIN` **repite el médico tantas veces como turnos tenga** (de 15 filas se pasa a 30: 6 médicos aportan 4 filas y 2 aportan 3), y el `AVG` queda ponderado: pesan más los sueldos de los médicos con más turnos. Lección: antes de agregar sobre un `JOIN` de 1:N, confirmá que el `COUNT(*)` te dé las filas que esperabas.
Si querés "el promedio de los médicos que atendieron", primero filtrás con un subquery y después promediás:

```sql
SELECT ROUND(AVG(salario), 2) FROM medicos
WHERE id_medico IN (SELECT id_medico FROM turnos);                            -- 481875
```

**12. Columna suelta en el `SELECT`.**

```sql
SELECT nombre, ciudad, COUNT(*) FROM pacientes GROUP BY ciudad;  -- MySQL: ERROR 1055
```

`nombre` no está agrupada ni agregada: la base no sabe **qué** nombre mostrar de los 3 de Rosario (SQLite muestra el primero que encuentra y te miente). Dos formas válidas:

```sql
SELECT ciudad, COUNT(*) AS pacientes FROM pacientes GROUP BY ciudad;          -- sacarla
SELECT ciudad, GROUP_CONCAT(nombre) AS nombres, COUNT(*) AS pacientes         -- o agregarla
FROM pacientes GROUP BY ciudad;
```

**13. `WHERE` vs `HAVING`.**

`WHERE` se evalúa **antes** de agrupar, así que todavía no existe ningún `COUNT(*)`: de ahí el error. `HAVING` se evalúa **después**, sobre los grupos ya formados. Orden lógico real de una consulta:

```
FROM → WHERE → GROUP BY → HAVING → SELECT (aparecen los alias) → ORDER BY → LIMIT
```

Por eso el alias del agregado (`veces`, `pacientes`) se puede usar en `HAVING` y `ORDER BY`, pero **nunca** en `WHERE`.

**14. Porcentaje por especialidad.**

```sql
SELECT e.nombre_especialidad,
       COUNT(*) AS turnos,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM turnos), 1) AS porcentaje
FROM turnos t
INNER JOIN medicos m ON t.id_medico = m.id_medico
INNER JOIN especialidades e ON m.id_especialidad = e.id_especialidad
GROUP BY e.nombre_especialidad
ORDER BY porcentaje DESC, e.nombre_especialidad;
```

13.3 % (seis especialidades) y 10 % (dos). El `* 100.0` en vez de `* 100` evita la división entera.

**15. Reto integrador.**

```sql
SELECT e.nombre_especialidad AS especialidad,
       COUNT(t.id_turno) AS turnos,
       COUNT(DISTINCT t.id_paciente) AS pacientes,
       ROUND(AVG(p.edad), 1) AS edad_promedio,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM turnos), 1) AS porcentaje
FROM turnos t
INNER JOIN medicos m ON t.id_medico = m.id_medico
INNER JOIN especialidades e ON m.id_especialidad = e.id_especialidad
INNER JOIN pacientes p ON t.id_paciente = p.id_paciente
GROUP BY e.id_especialidad, e.nombre_especialidad
HAVING COUNT(t.id_turno) = 4
ORDER BY edad_promedio DESC, especialidad;
```

| especialidad | turnos | pacientes | edad_promedio | porcentaje |
|---|---|---|---|---|
| Pediatría | 4 | 4 | 62 | 13.3 |
| Clínica General | 4 | 4 | 51.3 | 13.3 |
| Dermatología | 4 | 4 | 51.3 | 13.3 |
| Neurología | 4 | 4 | 47.5 | 13.3 |
| Cardiología | 4 | 4 | 45.5 | 13.3 |
| Traumatología | 4 | 4 | 34.3 | 13.3 |

Lo difícil no es la sintaxis sino tener claro **de qué tabla sale cada columna** (la edad vive en `pacientes`, por eso hace falta el cuarto JOIN) y que `HAVING COUNT(t.id_turno) = 4` filtra grupos, no filas.
