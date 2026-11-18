"""Contenido del video: capítulos, láminas y narración.

Los textos de `narracion` son los mismos que se sintetizaron a audio.
Los subtítulos se generan automáticamente a partir de ese texto.
"""

# kind: "h" (título de lámina), "b" (viñeta), "code" (línea de código), "note" (destacado)
CHAPTERS = [
    {
        "n": 1,
        "dir": "cap01",
        "title": "Qué es una base de datos y DDL vs DML",
        "weight_per_scene": [1.0, 1.2, 1.4],
        "scenes": [
            {
                "title": "¿Qué es una base de datos?",
                "lines": [
                    ("b", "Datos organizados en TABLAS"),
                    ("b", "Filas  →  registros (cada elemento)"),
                    ("b", "Columnas  →  atributos (cada dato)"),
                    ("note", "Todo el curso gira alrededor de esto: estructura + datos"),
                ],
            },
            {
                "title": "DDL — Data Definition Language",
                "lines": [
                    ("b", "Define la ESTRUCTURA: bases, tablas, columnas"),
                    ("code", "CREATE DATABASE / CREATE TABLE"),
                    ("code", "ALTER TABLE   /   DROP"),
                    ("note", "Si cambia el ENVASE → es DDL"),
                ],
            },
            {
                "title": "DML — Data Manipulation Language",
                "lines": [
                    ("b", "Trabaja con los DATOS de adentro"),
                    ("code", "INSERT   SELECT   UPDATE   DELETE"),
                    ("note", "Si cambia el CONTENIDO → es DML"),
                    ("b", "Regla: primero existe la tabla (DDL), después se llena (DML)"),
                ],
            },
        ],
    },
    {
        "n": 2,
        "dir": "cap02",
        "title": "Tipos de datos en SQL",
        "weight_per_scene": [1.0, 1.0, 1.2, 1.3],
        "scenes": [
            {
                "title": "Texto: CHAR vs VARCHAR",
                "lines": [
                    ("code", "CHAR(8)      -- longitud FIJA, ocupa 8 siempre"),
                    ("code", "VARCHAR(50)  -- longitud VARIABLE, ocupa lo usado"),
                    ("b", "CHAR → datos de largo uniforme (DNI, código postal)"),
                    ("note", "VARCHAR es el que vas a usar casi siempre"),
                ],
            },
            {
                "title": "Números",
                "lines": [
                    ("code", "INT           -- enteros, IDs, cantidades"),
                    ("code", "DECIMAL(10,2) -- dinero: decimales EXACTOS"),
                    ("code", "FLOAT / DOUBLE -- aproximados, NO para precios"),
                    ("note", "FLOAT redondea → aparecen 'centavos fantasma'"),
                ],
            },
            {
                "title": "Fechas",
                "lines": [
                    ("code", "DATE      -- AAAA-MM-DD"),
                    ("code", "DATETIME  -- con hora"),
                    ("b", "Se compara como texto: '2025-03-10' < '2025-04-01'"),
                    ("b", "Para filtrar por mes → MONTH(fecha) = 3"),
                ],
            },
            {
                "title": "Especiales: BOOLEAN y ENUM",
                "lines": [
                    ("code", "activo BOOLEAN"),
                    ("code", "estado ENUM('activo','finalizado','abandonó')"),
                    ("b", "ENUM: la columna SOLO acepta esos valores"),
                    ("note", "ENUM + DEFAULT se combinan perfecto"),
                ],
            },
        ],
    },
    {
        "n": 3,
        "dir": "cap03",
        "title": "Constraints (restricciones)",
        "weight_per_scene": [1.0, 1.2, 1.2, 1.3, 1.0],
        "scenes": [
            {
                "title": "¿Qué son?",
                "lines": [
                    ("b", "Reglas que se ponen al CREAR la tabla"),
                    ("b", "Evitan datos repetidos o incorrectos"),
                    ("b", "Mantienen las relaciones entre tablas"),
                    ("b", "Obligan a que ciertos campos estén completos"),
                    ("note", "Sin constraints, MySQL acepta cualquier cosa"),
                ],
            },
            {
                "title": "Las 7 restricciones",
                "lines": [
                    ("b", "PRIMARY KEY  — única + no nula"),
                    ("b", "FOREIGN KEY  — apunta a la PK de otra tabla"),
                    ("b", "UNIQUE  — no repetidos (sí admite nulos)"),
                    ("b", "NOT NULL  — obligatorio"),
                    ("b", "CHECK  — condición (existe, no se usa en la cursada)"),
                    ("b", "DEFAULT  — valor si no se indica nada"),
                ],
            },
            {
                "title": "PK vs UNIQUE (se pregunta siempre)",
                "lines": [
                    ("b", "Ambas evitan repetir valores"),
                    ("b", "PK: única + NO nula → identificador de la fila"),
                    ("b", "UNIQUE: permite nulos, pero no dos iguales"),
                    ("code", "email VARCHAR(100) NOT NULL UNIQUE"),
                    ("note", "Si no ponés la restricción, no hay control"),
                ],
            },
            {
                "title": "AUTO_INCREMENT y claves compuestas",
                "lines": [
                    ("b", "AUTO_INCREMENT: MySQL numera solo (1, 2, 3…)"),
                    ("b", "Se usa en PK numéricas para no cargarlas a mano"),
                    ("b", "Una tabla puede tener VARIAS constraints"),
                    ("note", "Las FK de una tabla hija también son columnas"),
                ],
            },
            {
                "title": "Cascada",
                "lines": [
                    ("code", "ON DELETE CASCADE"),
                    ("code", "ON UPDATE CASCADE"),
                    ("b", "Va DENTRO de la definición de la FK"),
                    ("note", "Si no hay cascade → hay que borrar a mano, en orden"),
                ],
            },
        ],
    },
    {
        "n": 4,
        "dir": "cap04",
        "title": "DDL: crear la base, las tablas e INSERT",
        "weight_per_scene": [0.8, 1.3, 1.4, 1.3, 1.0],
        "scenes": [
            {
                "title": "Crear y usar la base",
                "lines": [
                    ("code", "CREATE DATABASE cineplus;"),
                    ("code", "USE cineplus;"),
                    ("note", "Sin USE, trabajás en otra base y no te enterás"),
                ],
            },
            {
                "title": "Orden de creación",
                "lines": [
                    ("b", "1° las tablas PADRE (no dependen de nadie)"),
                    ("b", "2° las tablas HIJA (tienen la FK)"),
                    ("note", "actores → películas → clientes → alquileres"),
                ],
            },
            {
                "title": "El error más común: la FK no crea la columna",
                "lines": [
                    ("code", "id_actor INT NOT NULL,   -- la columna"),
                    ("code", "FOREIGN KEY (id_actor) REFERENCES actores(id_actor)"),
                    ("b", "La FK solo MARCA la columna, no la inventa"),
                    ("note", "ERROR 1072: Key column doesn't exist in table"),
                ],
            },
            {
                "title": "INSERT",
                "lines": [
                    ("code", "INSERT INTO actores (nombre, nacionalidad)"),
                    ("code", "VALUES ('Keanu Reeves', 'Canadiense');"),
                    ("b", "Textos y fechas → comillas simples. Números → sin comillas"),
                    ("b", "Varias filas de una: separadas por coma"),
                    ("note", "Al AUTO_INCREMENT no se lo nombra"),
                ],
            },
            {
                "title": "El orden define los IDs",
                "lines": [
                    ("b", "1ª fila → id 1, 2ª → id 2, 3ª → id 3"),
                    ("b", "Si salteás o repetís un INSERT, todo se desplaza"),
                    ("note", "Verificá con SELECT id, nombre FROM actores;"),
                ],
            },
        ],
    },
    {
        "n": 5,
        "dir": "cap05",
        "title": "SELECT, filtros, NULL y agregación",
        "weight_per_scene": [1.0, 1.1, 1.2, 1.2, 1.2, 1.1],
        "scenes": [
            {
                "title": "Estructura del SELECT",
                "lines": [
                    ("code", "SELECT col1, col2 AS alias"),
                    ("code", "FROM tabla"),
                    ("code", "WHERE condición"),
                    ("code", "ORDER BY columna DESC;"),
                    ("note", "El * significa TODAS las columnas"),
                ],
            },
            {
                "title": "Ordenar y filtrar",
                "lines": [
                    ("b", "ORDER BY ... ASC (por defecto) / DESC"),
                    ("b", "WHERE filtra FILAS: solo pasan las que cumplen"),
                    ("code", "WHERE anio_estreno > 2018"),
                    ("note", "ORDER BY y WHERE van después del FROM/JOIN"),
                ],
            },
            {
                "title": "LIKE y BETWEEN",
                "lines": [
                    ("code", "WHERE titulo LIKE '%la%'   -- contiene 'la'"),
                    ("code", "WHERE titulo LIKE '_a%'    -- 2ª letra es 'a'"),
                    ("code", "WHERE anio BETWEEN 1990 AND 2000"),
                    ("b", "% = cualquier cantidad de caracteres"),
                    ("b", "_ = exactamente un carácter"),
                    ("note", "BETWEEN incluye los dos extremos"),
                ],
            },
            {
                "title": "Funciones de fecha",
                "lines": [
                    ("code", "WHERE MONTH(fecha_prestamo) = 4"),
                    ("code", "WHERE YEAR(fecha_venta) = 2025"),
                    ("b", "También DAY() y WEEK()"),
                    ("note", "La función va PEGADA al paréntesis"),
                ],
            },
            {
                "title": "NULL no es vacío ni cero",
                "lines": [
                    ("b", "NULL = ausencia de valor"),
                    ("code", "WHERE fecha_devolucion IS NULL"),
                    ("code", "WHERE fecha_devolucion IS NOT NULL"),
                    ("note", "= NULL nunca devuelve filas: siempre es falso"),
                ],
            },
            {
                "title": "DISTINCT vs COUNT",
                "lines": [
                    ("b", "DISTINCT → devuelve valores distintos (lista)"),
                    ("b", "COUNT → cuenta registros"),
                    ("code", "COUNT(*) / SUM() / AVG() / MAX() / MIN()"),
                    ("note", "COUNT cuenta filas; SUM suma NÚMEROS. No son intercambiables"),
                ],
            },
        ],
    },
    {
        "n": 6,
        "dir": "cap06",
        "title": "UPDATE, ALTER, DELETE y borrado en cadena",
        "weight_per_scene": [1.2, 1.3, 1.2, 1.3, 1.0],
        "scenes": [
            {
                "title": "UPDATE (DML)",
                "lines": [
                    ("code", "UPDATE libros"),
                    ("code", "SET anio_publicacion = 1964"),
                    ("code", "WHERE titulo = 'Rayuela';"),
                    ("note", "SIN WHERE se actualizan TODAS las filas. No hay deshacer"),
                ],
            },
            {
                "title": "ALTER TABLE (DDL)",
                "lines": [
                    ("code", "ADD COLUMN telefono VARCHAR(20)"),
                    ("code", "MODIFY precio DECIMAL(12,2)"),
                    ("code", "CHANGE nombre_viejo nombre_nuevo VARCHAR(50)"),
                    ("note", "CHANGE va SIN coma entre el nombre viejo y el nuevo"),
                ],
            },
            {
                "title": "DELETE (DML)",
                "lines": [
                    ("code", "DELETE FROM peliculas"),
                    ("code", "WHERE id_pelicula = 3;"),
                    ("b", "El FROM no es opcional"),
                    ("b", "Sin WHERE borra todas las FILAS (la tabla sigue)"),
                    ("note", "DROP TABLE sí borra la estructura"),
                ],
            },
            {
                "title": "Borrado en cadena manual (SÍ entra en el parcial)",
                "lines": [
                    ("code", "1) DELETE FROM alquileres"),
                    ("code", "   WHERE id_pelicula IN (SELECT ... WHERE id_actor = 3);"),
                    ("code", "2) DELETE FROM peliculas WHERE id_actor = 3;"),
                    ("code", "3) DELETE FROM actores WHERE id_actor = 3;"),
                    ("note", "Nietos → hijos → padre. Si no: ERROR 1451"),
                ],
            },
            {
                "title": "Si hay ON DELETE CASCADE",
                "lines": [
                    ("code", "DELETE FROM actores WHERE id_actor = 3;"),
                    ("b", "Una sola línea: MySQL arrastra todo"),
                    ("note", "El borrado manual se pide cuando NO hay cascade"),
                ],
            },
        ],
    },
    {
        "n": 7,
        "dir": "cap07",
        "title": "JOIN: combinar tablas",
        "weight_per_scene": [1.1, 1.2, 1.3, 1.2, 1.0],
        "scenes": [
            {
                "title": "La idea",
                "lines": [
                    ("b", "Las tablas se relacionan por claves"),
                    ("b", "El JOIN las combina usando esa relación"),
                    ("code", "ON tabla_hija.fk = tabla_padre.pk"),
                    ("note", "La condición ON dice POR DÓNDE se unen"),
                ],
            },
            {
                "title": "INNER JOIN",
                "lines": [
                    ("code", "FROM peliculas p"),
                    ("code", "INNER JOIN actores a ON p.id_actor = a.id_actor"),
                    ("b", "Solo devuelve las coincidencias"),
                    ("note", "Si una película no tiene actor, NO aparece"),
                ],
            },
            {
                "title": "LEFT y RIGHT JOIN",
                "lines": [
                    ("code", "FROM actores a LEFT JOIN peliculas p"),
                    ("code", "  ON a.id_actor = p.id_actor"),
                    ("b", "LEFT: todo lo de la izquierda + coincidencias"),
                    ("b", "RIGHT: lo mismo, al revés"),
                    ("note", "Donde no hay coincidencia, aparecen NULL"),
                ],
            },
            {
                "title": "El truco del LEFT JOIN + IS NULL",
                "lines": [
                    ("b", "¿Autores que NO tienen libros?"),
                    ("code", "LEFT JOIN peliculas p ON ..."),
                    ("code", "WHERE p.id_pelicula IS NULL"),
                    ("note", "Deja justo las filas SIN coincidencia"),
                ],
            },
            {
                "title": "Tres tablas: no saltees eslabones",
                "lines": [
                    ("code", "FROM alquileres al"),
                    ("code", "JOIN clientes  c  ON al.id_cliente  = c.id_cliente"),
                    ("code", "JOIN peliculas p  ON al.id_pelicula = p.id_pelicula"),
                    ("code", "JOIN actores   ac ON p.id_actor     = ac.id_actor"),
                    ("note", "FULL JOIN: existe, pero MySQL no lo implementa"),
                ],
            },
        ],
    },
    {
        "n": 8,
        "dir": "cap08",
        "title": "GROUP BY y HAVING",
        "weight_per_scene": [1.1, 1.2, 1.3, 1.2],
        "scenes": [
            {
                "title": "Para qué sirven",
                "lines": [
                    ("b", "Agrupan filas por el valor de una columna"),
                    ("b", "Aplican la función DENTRO de cada grupo"),
                    ("code", "SELECT genero, COUNT(*) FROM libros GROUP BY genero;"),
                    ("note", "Siempre con una función de agregación"),
                ],
            },
            {
                "title": "Regla de oro",
                "lines": [
                    ("b", "Todo lo que va en el SELECT y NO es agregación"),
                    ("b", "tiene que estar también en el GROUP BY"),
                    ("note", "Mejor agrupar por la PK que por el nombre"),
                ],
            },
            {
                "title": "WHERE vs HAVING",
                "lines": [
                    ("b", "WHERE  → filtra FILAS (antes de agrupar)"),
                    ("b", "HAVING → filtra GRUPOS (después de agrupar)"),
                    ("code", "GROUP BY genero HAVING COUNT(*) > 2"),
                    ("note", "WHERE COUNT(*) → error: todavía no hay grupos"),
                ],
            },
            {
                "title": "Orden de las cláusulas",
                "lines": [
                    ("code", "SELECT → FROM → JOIN/ON → WHERE"),
                    ("code", "       → GROUP BY → HAVING → ORDER BY"),
                    ("b", "Ejemplo: cuántas veces se alquiló cada película"),
                    ("code", "GROUP BY p.id_pelicula, p.titulo"),
                ],
            },
        ],
    },
    {
        "n": 9,
        "dir": "cap09",
        "title": "Vistas y buenas prácticas",
        "weight_per_scene": [1.2, 1.0, 1.2, 1.1],
        "scenes": [
            {
                "title": "¿Qué es una vista?",
                "lines": [
                    ("b", "Una consulta guardada con un nombre"),
                    ("b", "Se usa como si fuera una tabla"),
                    ("note", "NO guarda datos: guarda la consulta"),
                ],
            },
            {
                "title": "Crear y usar",
                "lines": [
                    ("code", "CREATE VIEW vista_alquileres_detalle AS"),
                    ("code", "SELECT c.nombre, p.titulo"),
                    ("code", "FROM alquileres al"),
                    ("code", "JOIN clientes c  ON al.id_cliente = c.id_cliente"),
                    ("code", "JOIN peliculas p ON al.id_pelicula = p.id_pelicula;"),
                    ("note", "Después: SELECT * FROM vista_alquileres_detalle;"),
                ],
            },
            {
                "title": "Modificar una vista",
                "lines": [
                    ("code", "DROP VIEW vista_alquileres_detalle;"),
                    ("b", "No hay un ALTER cómodo: se borra y se recrea"),
                    ("note", "Ojo: si renombrás una columna, la vista se rompe"),
                ],
            },
            {
                "title": "Tres errores que te costaron la tarde",
                "lines": [
                    ("b", "1. La FK no crea la columna → declarala primero"),
                    ("b", "2. AUTO_INCREMENT gasta IDs aunque falle el INSERT"),
                    ("b", "3. INSERT...SELECT sin coincidencias = 0 filas, sin error"),
                    ("note", "Siempre verificá con SELECT / COUNT"),
                ],
            },
        ],
    },
    {
        "n": 10,
        "dir": "cap10",
        "title": "Resolución del parcial CinePlus",
        "weight_per_scene": [1.0, 1.15, 1.0, 1.25, 1.05, 0.95, 0.75, 0.85],
        "scenes": [
            {
                "title": "El modelo CinePlus",
                "lines": [
                    ("b", "actores(id_actor, nombre, nacionalidad)"),
                    ("b", "peliculas(id_pelicula, titulo, genero, anio_estreno, id_actor)"),
                    ("b", "clientes(id_cliente, nombre, apellido, ciudad)"),
                    ("b", "alquileres(id_alquiler, id_pelicula, id_cliente, fecha, dias)"),
                    ("note", "alquileres = tabla intermedia (muchos a muchos)"),
                ],
            },
            {
                "title": "Consultas simples (1 a 5)",
                "lines": [
                    ("code", "1) SELECT * FROM peliculas;"),
                    ("code", "2) SELECT * FROM actores ORDER BY nombre;"),
                    ("code", "3) SELECT * FROM peliculas WHERE anio_estreno > 2018;"),
                    ("code", "4) SELECT a.* FROM alquileres a"),
                    ("code", "   JOIN clientes c ON a.id_cliente = c.id_cliente"),
                    ("code", "   WHERE c.nombre = 'Laura' AND c.apellido = 'Gómez';"),
                    ("code", "5) SELECT * FROM peliculas WHERE genero IN ('Acción','Comedia');"),
                ],
            },
            {
                "title": "ALTER / UPDATE / DELETE (6 a 9)",
                "lines": [
                    ("code", "6) ALTER TABLE clientes ADD COLUMN email VARCHAR(100);"),
                    ("code", "7) UPDATE peliculas SET anio_estreno = 1999"),
                    ("code", "   WHERE titulo = 'Matrix';"),
                    ("code", "8) DELETE FROM alquileres WHERE id_alquiler = 12;"),
                    ("code", "9) ALTER TABLE clientes CHANGE ciudad localidad VARCHAR(100);"),
                    ("note", "En el 9 va SIN coma entre ciudad y localidad"),
                ],
            },
            {
                "title": "JOIN (10 a 12)",
                "lines": [
                    ("code", "10) SELECT c.nombre, p.titulo, ac.nombre"),
                    ("code", "    FROM alquileres al"),
                    ("code", "    JOIN clientes  c  ON al.id_cliente  = c.id_cliente"),
                    ("code", "    JOIN peliculas p  ON al.id_pelicula = p.id_pelicula"),
                    ("code", "    JOIN actores   ac ON p.id_actor     = ac.id_actor;"),
                    ("note", "12) el mismo encadenado + WHERE ac.nombre = 'Leonardo DiCaprio'"),
                ],
            },
            {
                "title": "GROUP BY (13 y 14)",
                "lines": [
                    ("code", "13) SELECT genero, COUNT(*) FROM peliculas"),
                    ("code", "    GROUP BY genero;"),
                    ("b", "Cuenta películas por género"),
                    ("code", "14) SELECT c.nombre, AVG(al.dias_alquilada)"),
                    ("code", "    FROM clientes c JOIN alquileres al"),
                    ("code", "      ON c.id_cliente = al.id_cliente"),
                    ("code", "    GROUP BY c.id_cliente, c.nombre, c.apellido;"),
                    ("note", "Promedio de días por cliente"),
                ],
            },
            {
                "title": "GROUP BY (15)",
                "lines": [
                    ("code", "15) SELECT p.titulo, COUNT(al.id_alquiler)"),
                    ("code", "    FROM peliculas p JOIN alquileres al"),
                    ("code", "      ON p.id_pelicula = al.id_pelicula"),
                    ("code", "    GROUP BY p.id_pelicula, p.titulo;"),
                    ("b", "Cuántas veces se alquiló cada película"),
                    ("note", "Todo lo que no es agregación va en el GROUP BY"),
                ],
            },
            {
                "title": "La vista (16)",
                "lines": [
                    ("code", "CREATE VIEW vista_alquileres_detalle AS"),
                    ("code", "SELECT c.nombre AS cliente, p.titulo AS pelicula"),
                    ("code", "FROM alquileres al"),
                    ("code", "JOIN clientes  c ON al.id_cliente  = c.id_cliente"),
                    ("code", "JOIN peliculas p ON al.id_pelicula = p.id_pelicula;"),
                ],
            },
            {
                "title": "Verdadero/Falso y múltiple choice",
                "lines": [
                    ("b", "1 V · 2 F (UPDATE modifica, no inserta) · 3 V"),
                    ("b", "4 F (eso es FULL OUTER; INNER solo coincidencias)"),
                    ("b", "5 V · 6 V (muchos a muchos → tabla intermedia)"),
                    ("b", "MC: 1 c · 2 b · 3 c · 4 c"),
                    ("note", "Todo explicado en cineplus-solucionario.sql"),
                ],
            },
        ],
    },
]

NARRACION = {
    1: "Bienvenidos a este repaso de Administración y Gestión de Bases de Datos. La idea es recorrer los temas de la materia en orden y terminar resolviendo el modelo de segundo parcial de CinePlus, consulta por consulta. Empezamos por lo más básico: qué es una base de datos y en qué se diferencian los dos grandes grupos de sentencias. Una base de datos es un conjunto de datos organizados que se guardan en tablas, y cada tabla tiene filas, que son los registros, y columnas, que son los atributos. Para trabajar con esa base usamos distintos lenguajes. El DDL, Data Definition Language, define la estructura: crear bases de datos, crear tablas, agregar columnas, borrarlas. Sus palabras clave son CREATE, ALTER y DROP. El DML, Data Manipulation Language, trabaja con los datos que van dentro de esa estructura: insertar, consultar, actualizar y borrar filas. Sus palabras clave son INSERT, SELECT, UPDATE y DELETE. La regla mental es simple: si cambia el envase, es DDL; si cambia el contenido, es DML.",
    2: "Ahora los tipos de datos, porque elegir bien el tipo es la mitad del trabajo. Para texto tenemos dos opciones. CHAR es de longitud fija: si declarás CHAR de ocho y guardás cinco caracteres, igual ocupa ocho. Se usa cuando todos los valores tienen el mismo largo, por ejemplo un DNI. VARCHAR es de longitud variable y es el que vas a usar casi siempre, porque ocupa solo lo que necesita. Para números, INT es el entero que usamos para identificadores y cantidades, y DECIMAL se usa para dinero, porque guarda los decimales de forma exacta. FLOAT o DOUBLE existen pero no conviene para precios, porque redondean y te pueden aparecer centavos fantasma. Para fechas está DATE, que guarda año, mes y día en formato año mes día, y DATETIME cuando además necesitás la hora. Después están los tipos especiales. BOOLEAN guarda verdadero o falso. Y ENUM es una lista de valores permitidos: escribís ENUM con las opciones entre paréntesis y la columna solo acepta esos valores. Por ejemplo, el estado de una inscripción como activo, completado o cancelado. Se combina muy bien con DEFAULT, que completa el campo solo si no le indicás nada.",
    3: "Las constraints son reglas que se le ponen a los atributos de una tabla al crearla, para que los datos se guarden correctamente y no se almacene cualquier cosa. Sirven para tres cosas: evitar datos repetidos o incorrectos, mantener las relaciones entre tablas y obligar a que ciertos campos estén completos. Vamos con las siete. PRIMARY KEY identifica de forma única cada fila: no se puede repetir y no admite nulos. FOREIGN KEY relaciona una tabla con otra y solo admite valores que ya existan en la tabla padre; se declara con la palabra REFERENCES. UNIQUE evita valores repetidos en esa columna, pero a diferencia de la primaria sí admite nulos. NOT NULL impide valores vacíos: el dato es obligatorio. CHECK define una condición que el dato debe cumplir al cargarse; existe, pero en la cursada no se usa. DEFAULT define un valor por defecto si no indicás ninguno. Y AUTO_INCREMENT genera el valor solo, sumando uno a cada registro nuevo; se usa en las claves primarias numéricas para no cargarlas a mano. Una diferencia que se pregunta siempre: la primaria es única y no nula, o sea mucho más restrictiva; UNIQUE permite nulos, así que un email con UNIQUE puede quedar vacío en alguna fila, pero no puede haber dos emails iguales. Y un detalle importante: si a un atributo no le ponés la restricción, MySQL lo trata como un atributo común y admite cualquier cosa, incluso repetidos.",
    4: "Pasamos al DDL en acción: crear la base, las tablas y cargar datos. Primero, CREATE DATABASE con el nombre, y después USE con el mismo nombre para trabajar dentro de esa base. Para crear una tabla se escribe CREATE TABLE, el nombre, y entre paréntesis los atributos separados por coma. Cada atributo lleva su nombre, su tipo y sus restricciones. El orden de creación importa: primero las tablas que no dependen de nadie, y después las que contienen la clave foránea. Y acá aparece el error más frecuente: la clave foránea no crea la columna. La columna hay que declararla como cualquier otra, y recién después, al final de la tabla, agregar la restricción FOREIGN KEY con REFERENCES. Si falta la columna, MySQL avisa que esa columna no existe en la tabla. Para cargar datos usamos INSERT INTO, el nombre de la tabla, entre paréntesis las columnas, la palabra VALUES y los datos. Los textos y las fechas van entre comillas simples, los números no. Se pueden cargar varias filas de una vez separándolas por coma, y a las columnas con AUTO_INCREMENT no se las nombra. Y un detalle clave para el parcial: el orden de los INSERT define los identificadores. La primera fila de actores es la uno, la segunda la dos, la tercera la tres. Si se saltea una o se inserta dos veces, todas las referencias posteriores dejan de coincidir.",
    5: "Seguimos con SELECT, que es la sentencia que más vas a usar. La estructura es SELECT las columnas que querés ver, FROM la tabla, y después las cláusulas opcionales. El asterisco significa todas las columnas. Con AS le ponés un alias a una columna, para que el encabezado se lea mejor. ORDER BY ordena el resultado: ASC de menor a mayor, que es lo que se usa por defecto, y DESC de mayor a menor. WHERE filtra filas: solo pasan las que cumplen la condición. Ahí tenés los operadores de siempre, igual, distinto, mayor, menor. LIKE sirve para búsquedas parciales: el símbolo de porcentaje significa cualquier cantidad de caracteres y el guion bajo significa exactamente un carácter. Y BETWEEN filtra un rango con los dos extremos incluidos. Después están las funciones de fecha: MONTH, YEAR, DAY y WEEK, que se pegan al paréntesis, porque si separás el nombre de la función del paréntesis, MySQL tira error. Y dos conceptos que se confunden seguido. Por un lado, NULL no es vacío ni cero: es ausencia de valor, y por eso no se compara con igual, se compara con IS NULL y IS NOT NULL. Por el otro, DISTINCT devuelve un solo valor por cada valor distinto encontrado, mientras que COUNT cuenta filas. DISTINCT lista, COUNT cuenta. Y las funciones de agregación van sobre un conjunto de filas y devuelven un solo valor: COUNT cuenta registros, SUM suma, AVG promedia, MAX el máximo y MIN el mínimo. COUNT puede contar cualquier cosa, incluso un texto; SUM y AVG solo números. No son intercambiables.",
    6: "Ahora modificar datos y modificar estructura, que es donde se mezclan DML y DDL. UPDATE es DML y cambia el contenido de las filas. La estructura es UPDATE, la tabla, SET la columna igual al nuevo valor, y WHERE para elegir qué filas. Y acá va la advertencia más importante de toda la materia: si te olvidás el WHERE, se actualizan todas las filas de la tabla. No hay botón de deshacer. ALTER TABLE es DDL y cambia la estructura. ADD COLUMN agrega una columna, MODIFY cambia el tipo, y CHANGE renombra: se escribe CHANGE, el nombre viejo, el nombre nuevo y el tipo, todo seguido y sin coma en el medio. Si ponés una coma entre el nombre viejo y el nuevo, es error de sintaxis. Y ese renombre puede romper consultas o vistas viejas que usaban el nombre anterior. DELETE es DML y borra filas. Ojo con la sintaxis: DELETE FROM, el nombre de la tabla, WHERE la condición. El FROM no es opcional; DELETE peliculas sin FROM es un error clásico. Sin WHERE, borra todas las filas, pero la tabla sigue existiendo. Y cuando hay claves foráneas, el orden del borrado importa: primero los hijos, después los padres. Si borrás un padre que todavía tiene hijos, MySQL lo impide. Eso se llama borrado en cadena manual, y se resuelve de la punta de la cadena hacia la raíz: nietos, hijos, padre. Si la clave foránea se declaró con ON DELETE CASCADE, alcanza con borrar el padre y MySQL arrastra todo solo.",
    7: "Los JOIN son la parte que más cuesta, pero con una idea clara salen solos. La idea es esta: las tablas están relacionadas por claves, y el JOIN las combina usando esa relación. La condición ON dice por dónde se unen, y siempre es clave foránea igual a clave primaria. Hay tres tipos que tenés que manejar. INNER JOIN devuelve solo las filas que coinciden en las dos tablas: si una película no tiene alquileres, no aparece. LEFT JOIN devuelve todo lo de la tabla de la izquierda, y donde no hay coincidencia completa con nulos. RIGHT JOIN es lo mismo al revés. Y FULL JOIN no se toma en la cursada, entre otras cosas porque MySQL no lo implementa. El LEFT JOIN tiene un truco muy útil que vale para el parcial: si querés los autores que no tienen ningún libro, hacés LEFT JOIN desde autores y filtrás por IS NULL en la columna de la otra tabla. Eso te deja justo las filas que no tuvieron coincidencia. Sobre el orden: el JOIN va después del FROM, y el WHERE va después del JOIN. Y el método para pensar una consulta es siempre el mismo: primero identificá qué querés mostrar, después desde dónde arrancás, después uní las claves, y recién al final filtrá. Para tres tablas, la cadena es préstamos con libros por el identificador de libro, y libros con autores por el identificador de autor. Nunca saltees un eslabón.",
    8: "GROUP BY y HAVING. Hasta acá las funciones de agregación devolvían un solo valor para toda la tabla. GROUP BY permite otra cosa: agrupar filas por el valor de una columna y aplicar la función dentro de cada grupo. Sirve para obtener información resumida: cuántos libros hay por género, cuántos clientes hay por ciudad, cuántos préstamos tiene cada lector. Siempre se usa con una función de agregación. Y hay una regla de oro: todo lo que se pone en el SELECT y no es una función de agregación tiene que estar también en el GROUP BY. Si no, MySQL no sabe qué valor mostrarte. Después está HAVING, que es el filtro de los grupos. WHERE filtra filas antes de agrupar; HAVING filtra grupos después de agrupar. Por eso, cuando el filtro usa COUNT o AVG, va en HAVING y no en WHERE. Poner WHERE COUNT da error, porque en ese momento todavía no existen los grupos. El orden de las cláusulas, que conviene memorizar, es: SELECT, FROM, JOIN con ON, WHERE, GROUP BY, HAVING y ORDER BY. Y un consejo: para agrupar conviene poner en el GROUP BY la clave primaria de la tabla, no el nombre, así dos registros con el mismo nombre no se mezclan.",
    9: "Las vistas. Una vista es una consulta guardada con un nombre, que después se puede usar como si fuera una tabla. No guarda datos: guarda la consulta, y cada vez que la consultás se ejecuta de nuevo. Sirven para simplificar consultas complejas, para reutilizar lógica y para mostrar solo ciertas columnas. Se crean con CREATE VIEW, el nombre de la vista, AS, y la consulta. Para usarla, hacés SELECT sobre el nombre de la vista como si fuera una tabla. Y un punto importante para el parcial: para modificar una vista existente no se usa un ALTER cómodo; lo habitual es borrarla con DROP VIEW y volver a crearla con la definición nueva. Antes de cerrar la teoría, tres buenas prácticas. Primero, verificá antes de borrar: un SELECT con el mismo WHERE te muestra exactamente qué filas se van a ir. Segundo, después de un INSERT con SELECT, comprobá con COUNT, porque si la consulta no encuentra nada, inserta cero filas y no da error: es silencioso. Y tercero, nunca asumas los identificadores. Consultalos. El contador automático gasta números aunque la operación falle, así que después de un error los identificadores pueden quedar desplazados.",
}

NARRACION[10] = (
    "Y llegamos al examen. El modelo se llama CinePlus y es una plataforma de alquiler de películas. "
    "Tiene cuatro tablas. Actores, con identificador, nombre y nacionalidad. Películas, con identificador, "
    "título, género, año de estreno y el actor principal como clave foránea. Clientes, con identificador, "
    "nombre, apellido y ciudad. Y alquileres, la tabla intermedia, con dos claves foráneas, una a películas "
    "y otra a clientes, más la fecha y la cantidad de días. La relación entre actores y películas es uno a "
    "muchos, porque cada película tiene un solo actor principal. Y la relación entre clientes y películas es "
    "muchos a muchos, y por eso existe la tabla intermedia. "
    "Con la estructura resuelta, vamos a las consultas simples. Para todas las películas, SELECT asterisco "
    "FROM películas. Para los actores ordenados, ORDER BY nombre, que va al final, y en orden ascendente. "
    "Para las estrenadas después de dos mil dieciocho, WHERE año de estreno mayor que dos mil dieciocho. "
    "Para los alquileres de Laura Gómez hay que unir alquileres con clientes, porque en la tabla alquileres "
    "no está el nombre: ese es el punto donde el profe espera un JOIN. Y para Acción o Comedia, WHERE género "
    "IN con los dos valores entre paréntesis. Después, la parte de estructura. Agregar una columna se hace "
    "con ALTER TABLE y ADD COLUMN. Actualizar el año de Matrix se hace con UPDATE, SET y WHERE, nunca sin el "
    "WHERE. Borrar un alquiler puntual, con DELETE FROM y WHERE por el identificador. Y renombrar la columna "
    "ciudad a localidad, con CHANGE, el nombre viejo, el nombre nuevo y el tipo, todo seguido y sin coma en "
    "el medio. "
    "Los tres JOIN del examen. El primero pide cliente, película y actor principal, y es el más largo: cuatro "
    "tablas encadenadas. Se arranca por alquileres, se une con clientes por el identificador de cliente, con "
    "películas por el identificador de película, y con actores por el identificador de actor. Cada eslabón "
    "usa su clave, y no se saltea ninguno. El segundo es más corto: películas con su actor, un solo JOIN. Y "
    "el tercero pide los clientes que alquilaron películas de Leonardo DiCaprio. Es el mismo encadenado de "
    "cuatro tablas, más un WHERE sobre el nombre del actor, y conviene agregar DISTINCT para que un cliente "
    "que alquiló dos películas del mismo actor no aparezca repetido. Después, agrupar. Contar películas por "
    "género: se selecciona el género y COUNT, y se agrupa por género. Promediar los días de alquiler por "
    "cliente: se une clientes con alquileres, se usa AVG sobre los días y se agrupa por el identificador del "
    "cliente y su nombre. Y contar cuántas veces se alquiló cada película: se une películas con alquileres y "
    "se agrupa por película. En los tres casos, todo lo que no es función de agregación va también en el "
    "GROUP BY. "
    "La vista del punto dieciséis: CREATE VIEW vista_alquileres_detalle AS, y la consulta que une alquileres "
    "con clientes y con películas, para mostrar el nombre del cliente y el título de la película. Después se "
    "consulta como si fuera una tabla. Y cerramos con las preguntas teóricas. Verdadero o falso. La primera "
    "es verdadera: GROUP BY agrupa valores iguales y permite usar COUNT o AVG. La segunda es falsa: UPDATE "
    "modifica filas existentes, para insertar se usa INSERT. La tercera es verdadera: DELETE FROM con WHERE "
    "borra las filas que cumplen la condición. La cuarta es falsa: el que muestra todos los registros "
    "coincidan o no es el FULL OUTER JOIN, no el INNER, que solo devuelve coincidencias. La quinta es "
    "verdadera: la clave foránea garantiza integridad referencial. Y la sexta también: en una relación "
    "muchos a muchos la tabla intermedia es obligatoria. Múltiple choice: la uno es la opción C, la única "
    "que agrupa por cliente y cuenta sus alquileres. La dos es la B, ALTER TABLE con ADD COLUMN. La tres es "
    "la C, borra la fila de Matrix. Y la cuatro es la C, UPDATE. Con esto tenés el recorrido completo. "
    "Éxitos en el parcial."
)
