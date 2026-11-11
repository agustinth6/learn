# Gimnasio de GROUP BY · base `clinica_medica`

El material no tiene un tema aparte de `GROUP BY`, pero es el compañero natural de las
agregaciones y cae en cualquier parcial de SQL. Esta hoja lo practica de a poco sobre una
base real, con **resultado esperado** para que te corrijas solo.

## Cómo trabajar

**Opción A (en tu PC, sin instalar nada):**

```bash
python3 practica/run.py              # consola interactiva, escribí y Enter
python3 practica/run.py "SELECT …"   # una consulta suelta
python3 practica/run.py --tablas      # resumen de las tablas
```

El `run.py` carga `practica/clinica_medica.sql` en SQLite, así que **no hace falta MySQL**.
Si escribís una consulta que en MySQL reventaría por `ONLY_FULL_GROUP_BY`, te avisa con ⚠️.
Comandos útiles: `.tablas`, `.load` (deshace `UPDATE`/`DELETE`), `.help`, `.quit`.

**Opción B (Workbench):** ejecutá `practica/clinica_medica.sql` completo y después probá
las consultas ahí. Los datos son los mismos, así que los conteos de esta hoja coinciden.

## Las tablas

| Tabla | Filas | Campos |
|---|---|---|
| `especialidades` | 8 | `id_especialidad`, `nombre_especialidad` |
| `pacientes` | 15 | `id_paciente`, `nombre`, `apellido`, `edad`, `ciudad` |
| `medicos` | 15 | `id_medico`, `nombre`, `apellido`, `salario`, `id_especialidad` (FK) |
| `turnos` | 30 | `id_turno`, `id_paciente` (FK), `id_medico` (FK), `fecha_turno`, `motivo` |

Dos detalles de los datos que van a importar: **todos los turnos son de octubre de 2025**
(un turno por día) y **7 médicos no atendieron a nadie** (sólo los `id_medico` 1 a 8 tienen turnos).

---

## Nivel 1 · agrupar sobre una tabla

1. **Cantidad de pacientes por ciudad**, ordenado de mayor a menor (y por nombre de ciudad para desempatar).
   _Esperado: 9 filas · primera Rosario con 3._
2. **Cantidad de médicos por especialidad**, pero solo las especialidades con **más de 1 médico**.
   _Esperado: 7 filas · Ginecología queda afuera porque tiene 1._
3. **Salario máximo, mínimo y promedio** de los médicos (una sola fila, sin agrupar).
   _Esperado: 570000 · 410000 · 483666.67._
4. **Edad promedio y cantidad de pacientes por ciudad**, ordenado por edad promedio de mayor a menor.
   _Esperado: 9 filas · primera Neuquén con 67 años._
5. **Cuántos turnos hay por mes**, usando `SUBSTR(fecha_turno,1,7)` como clave de agrupamiento.
   _Esperado: 1 fila · `2025-10` con 30._

## Nivel 2 · agrupar después de JOIN

6. **Cantidad de turnos por especialidad** (`turnos` → `medicos` → `especialidades`).
   _Esperado: 8 filas · 6 especialidades con 4 turnos y 2 con 3._
7. **Top 5 de ciudades por cantidad de turnos** (`turnos` → `pacientes`).
   _Esperado: Rosario 6 · Buenos Aires, Córdoba, Mendoza y Salta 4 cada una._
8. **Médicos que no atendieron ningún turno.** Pensalo: ¿`INNER JOIN` o `LEFT JOIN`?
   _Esperado: 7 filas · Herrera, López, Martínez, Molina, Ortega, Rivas y Silva._
9. **Turnos y pacientes distintos atendidos por cada médico** (`COUNT(t.id_turno)` y
   `COUNT(DISTINCT t.id_paciente)` en la misma consulta), mostrando solo los 8 primeros por id.
   _Esperado: médicos 1 a 6 con 4 turnos y 4 pacientes · 7 y 8 con 3 y 3._
10. **Motivos de consulta que se repiten**, con su cantidad, de más a menos.
    _Esperado: 5 filas · Control general 4 · Chequeo cardíaco 3 · Control clínico, Control visual y Dermatitis 2._

## Nivel 3 · las trampas que toman en los parciales

11. `SELECT ROUND(AVG(salario),2) FROM medicos` da **483666.67**, pero
    `SELECT ROUND(AVG(m.salario),2) FROM medicos m INNER JOIN turnos t ON t.id_medico = m.id_medico`
    da **480166.67**. **Escribí las dos y explicá por qué cambia el promedio.**
12. `SELECT nombre, ciudad, COUNT(*) FROM pacientes GROUP BY ciudad` corre en SQLite pero
    **en MySQL da error 1055**. ¿Por qué? Reescribila para que sea válida en MySQL.
13. ¿Por qué `WHERE COUNT(*) > 1` es inválido y `HAVING COUNT(*) > 1` no? Respondé mirando
    el orden lógico de ejecución de una consulta (`FROM` → `WHERE` → `GROUP BY` → `HAVING` → `SELECT` → `ORDER BY`).
14. **Porcentaje de turnos que atiende cada especialidad** sobre el total, con una subconsulta
    en el denominador: `ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM turnos), 1)`.
    _Esperado: 13.3 % para seis especialidades y 10 % para dos._
15. **Reto integrador.** Por especialidad que haya atendido exactamente 4 turnos: nombre de la
    especialidad, cantidad de turnos, cantidad de pacientes distintos, edad promedio de los
    pacientes atendidos (1 decimal) y el porcentaje sobre el total. Ordenalo por edad promedio
    de mayor a menor y, a igualdad, por especialidad.
    _Esperado: 6 filas · primera Pediatría con 62 años de promedio · todas 13.3 %._

---

### Reglas que conviene tener memorizadas

- **Toda columna del `SELECT` que no esté dentro de `COUNT/SUM/AVG/MAX/MIN` tiene que aparecer en el `GROUP BY`** (o ser funcionalmente dependiente de la clave agrupada, ej. `GROUP BY m.id_medico` deja seleccionar `m.nombre`).
- `WHERE` filtra **filas antes** de agrupar, `HAVING` filtra **grupos después**. Las agregadas van en `HAVING`.
- `GROUP BY` puede recibir un alias (`GROUP BY rango`) en MySQL, pero `WHERE` no puede usar alias del `SELECT`.
- `COUNT(*)` cuenta filas, `COUNT(col)` ignora los `NULL` — con `LEFT JOIN` esa diferencia es la que te dice si hubo coincidencia o no.
- `ORDER BY` se aplica al resultado ya agrupado; por eso ahí sí podés usar el alias del agregado.

📄 Las resoluciones paso a paso están en `practica/group-by-soluciones.md` (no las abras antes de intentar).
