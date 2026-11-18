# Guion del video — Repaso de Bases de Datos + parcial CinePlus

**Duración:** 18:42 (10 capítulos, todos narrados) · **Formato:** 1280×720, 25 fps, H.264 + AAC ·
**Subtítulos:** incrustados en el video y además `subtitulos-es.srt` (pista aparte).

Todos los capítulos están narrados. El capítulo 10 se armó pegando cuatro tramos de voz
(`cap10a`…`cap10d.mp3`) en un solo `cap10.mp3`.

## Capítulos

| # | Capítulo | Inicio | Duración | Qué cubre |
|---|---|---|---|---|
| 1 | Qué es una base de datos y DDL vs DML | 00:00 | 1:13 | tablas/filas/columnas, CREATE-ALTER-DROP vs INSERT-SELECT-UPDATE-DELETE |
| 2 | Tipos de datos en SQL | 01:13 | 1:19 | CHAR vs VARCHAR, INT/DECIMAL/FLOAT, DATE/DATETIME, BOOLEAN, ENUM |
| 3 | Constraints | 02:32 | 1:28 | las 7 restricciones, PK vs UNIQUE, AUTO_INCREMENT, CASCADE |
| 4 | DDL: crear base, tablas e INSERT | 04:00 | 1:38 | orden de creación, la FK no crea la columna, INSERT y el orden de los IDs |
| 5 | SELECT, filtros, NULL y agregación | 05:38 | 1:48 | WHERE, ORDER BY, LIKE, BETWEEN, MONTH/YEAR, NULL, DISTINCT vs COUNT |
| 6 | UPDATE, ALTER, DELETE y borrado en cadena | 07:26 | 1:39 | SET sin WHERE, CHANGE sin coma, DELETE FROM, nietos→hijos→padre |
| 7 | JOIN | 09:05 | 1:34 | INNER, LEFT/RIGHT, LEFT+IS NULL, tres tablas |
| 8 | GROUP BY y HAVING | 10:39 | 1:22 | regla de oro, WHERE vs HAVING, orden de cláusulas |
| 9 | Vistas y buenas prácticas | 12:01 | 1:24 | CREATE VIEW, DROP VIEW, los tres errores de la práctica |
| 10 | Resolución del parcial CinePlus | 13:24 | 4:46 | modelo, consultas 1-16, V/F y múltiple choice (pendiente de audio) |

## Cómo regenerar

```bash
cd video
# 1. audios narrados en audio/capXX.mp3  (capítulo 10 → audio/cap10a.mp3)
# 2. render de todos los capítulos
python3 build.py
# 3. unir los capítulos
ffmpeg -f concat -safe 0 -i out/lista_final.txt -c copy Repaso-Bases-de-Datos-Parcial.mp4
```

Todo el contenido (texto de las láminas y narración) está en `video/contenido.py`.
Los tiempos de los subtítulos se calculan automáticamente desde la duración real de cada audio.
