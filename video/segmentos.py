# -*- coding: utf-8 -*-
"""
Segmentos del video explicativo del Parcial 2.
Cada segmento = 1 slide (frame) + 1 clip de narracion (texto).

tipos:
  titulo   -> titulo grande + subtitulo
  concepto -> titulo + bullets
  codigo   -> titulo + codigo con lineas resaltadas
             (funcion + patrones: se resaltan las lineas que contienen el patron)
             (marker: desde/hasta: se muestra un trozo del archivo)
"""

SEGMENTOS = [
    # ───────────────────────── INTRO ─────────────────────────
    {
        "id": 1, "tipo": "titulo", "tag": "PARCIAL 2",
        "titulo": "Repaso explicado línea por línea",
        "subtitulo": "Técnicas de Programación · Python — Los 3 ejercicios del modelo",
        "texto": (
            "Bienvenido al repaso del parcial de Técnicas de Programación. "
            "En este video vamos a recorrer, línea por línea, los tres ejercicios del modelo de segundo parcial: "
            "primero estudiantes y notas, después productos y stock, y por último el inventario con diccionarios anidados. "
            "Vas a ver qué hace cada línea de código, las fórmulas clave y las trampas más comunes. ¡Empecemos!"
        ),
    },
    {
        "id": 2, "tipo": "concepto", "tag": "GENERAL",
        "titulo": "El esqueleto de los 3 ejercicios",
        "bullets": [
            "Diccionario GLOBAL con los datos",
            "Funciones que SOLO leen: promedios, totales, filtros",
            "UNA función muta (agregar_*) — SIEMPRE al final, tras validar todo",
            "main() + guard: el único que arranca el menú",
        ],
        "texto": (
            "Antes de entrar a cada ejercicio, mirá lo que los tres tienen en común. "
            "Hay un diccionario global con los datos. Después, funciones que solo leen: promedios, totales, filtros. "
            "Una única función, la de agregar, es la que modifica el diccionario, y siempre al final, después de validar todo. "
            "Y por último, la función main con el guard if name igual a main, que arranca el menú. "
            "Si entendés este esqueleto, entendés los tres ejercicios."
        ),
    },

    # ───────────────────────── EJERCICIO 1 ─────────────────────────
    {
        "id": 3, "tipo": "codigo", "tag": "EJERCICIO 1",
        "titulo": "Los datos: nombre → lista de notas",
        "archivo": "ejercicio1_estudiantes.py",
        "marker": {"desde": "estudiantes = {", "hasta": "}"},
        "texto": (
            "Ejercicio uno: gestión de estudiantes y notas. El diccionario usa como clave el nombre y como valor una lista de notas. "
            "Ana tiene nueve coma cinco, nueve coma dos y ocho coma ocho. Luis, siete, seis coma cinco y siete coma dos. "
            "Marta, seis en adelante. Y Carlos tiene la lista vacía: ese es el caso borde, existe pero no tiene notas. "
            "Si tu código no lo contempla, revienta con división por cero."
        ),
    },
    {
        "id": 4, "tipo": "codigo", "tag": "EJERCICIO 1",
        "titulo": "agregar_estudiante() — el nombre",
        "archivo": "ejercicio1_estudiantes.py",
        "funcion": "agregar_estudiante",
        "patrones": [
            "nombre = input(\"Nombre del estudiante: \")",
            "if nombre == \"\"",
            "if not nombre.isalpha():",
        ],
        "texto": (
            "Empecemos con agregar estudiante. El input devuelve texto, así que le aplicamos strip, que borra los espacios del principio y del final. "
            "Sin eso, Ana con espacios y Ana sin espacios serían dos claves distintas del diccionario. "
            "Después preguntamos si quedó vacío: si lo quedó, avisamos y con continue volvemos a pedir. "
            "Luego isalpha verifica que haya solo letras; el not invierte la condición. Si no cumple, se repite la pregunta. "
            "Recién cuando el nombre es válido, el break sale del bucle."
        ),
    },
    {
        "id": 5, "tipo": "codigo", "tag": "EJERCICIO 1",
        "titulo": "agregar_estudiante() — ¿existe? y cuántas notas",
        "archivo": "ejercicio1_estudiantes.py",
        "funcion": "agregar_estudiante",
        "patrones": [
            "if nombre in estudiantes:",
            "cantidad = int(input(",
            "if cantidad <= 0:",
            "Eso no es un numero entero",
        ],
        "texto": (
            "Segundo paso: verificar que el estudiante no exista todavía. "
            "Si el nombre ya está en el diccionario, imprimimos un aviso y hacemos return: corta ahí, sin pedir nada más, y sin tocar el diccionario. "
            "Después pedimos cuántas notas quiere ingresar. Eso va dentro de un try: int convierte el texto, "
            "y si el usuario escribe letras, salta el except con ValueError y volvemos a pedir. "
            "Si el número es menor o igual a cero, con continue también se repite. "
            "El break solo se ejecuta cuando la cantidad es válida."
        ),
    },
    {
        "id": 6, "tipo": "codigo", "tag": "EJERCICIO 1",
        "titulo": "agregar_estudiante() — cada nota",
        "archivo": "ejercicio1_estudiantes.py",
        "funcion": "agregar_estudiante",
        "patrones": [
            "notas = []",
            "while len(notas) < cantidad:",
            "nota = float(input(",
            "notas.append(nota)",
            "Eso no es un numero. Intente",
        ],
        "texto": (
            "Ahora las notas, en un bucle que se repite mientras falten. "
            "Creamos una lista vacía y en cada vuelta pedimos una nota con float, porque las notas aceptan decimales. "
            "Si el usuario escribe ocho, queda ocho coma cero. Si escribe letras, ValueError, y el except avisa que no es un número. "
            "Si la nota es menor o igual a cero, no sirve: se avisa y con continue se vuelve a pedir. "
            "Si es válida, el append la agrega al final. Y acá el detalle clásico: append siempre lleva el argumento; "
            "append vacío es el error de tipo TypeError."
        ),
    },
    {
        "id": 7, "tipo": "codigo", "tag": "EJERCICIO 1",
        "titulo": "agregar_estudiante() — LA MUTACIÓN",
        "archivo": "ejercicio1_estudiantes.py",
        "funcion": "agregar_estudiante",
        "patrones": [
            "estudiantes[nombre] = notas",
            "Estudiante '{nombre}' agregado",
        ],
        "texto": (
            "Y llegamos a la línea más importante de la función: estudiantes entre corchetes nombre, igual a notas. "
            "Es la única que modifica el diccionario, y está al final, después de validar todo. "
            "Si en cualquier paso anterior falló, nunca se llega acá, y el diccionario queda intacto. "
            "Esto es exactamente lo que pide el enunciado: una vez validada toda la información, agregar el estudiante. "
            "Fijate que la lista de la variable local notas queda colgada del diccionario: cuando la función termina, la variable muere, "
            "pero la lista sigue viva adentro."
        ),
    },
    {
        "id": 8, "tipo": "codigo", "tag": "EJERCICIO 1",
        "titulo": "calcular_promedio() — y el papel de None",
        "archivo": "ejercicio1_estudiantes.py",
        "funcion": "calcular_promedio",
        "patrones": [
            "if nombre not in estudiantes:",
            "notas = estudiantes[nombre]",
            "if not notas:",
            "return sum(notas) / len(notas)",
        ],
        "texto": (
            "Calcular promedio recibe el diccionario y el nombre. Primero verifica si existe: si no está, imprime el mensaje y retorna nulo. "
            "Y acá el punto clave: el valor nulo significa que no hay resultado, no que el promedio sea cero. "
            "Después toma la lista; si está vacía, también informa y retorna nulo, evitando dividir por cero. "
            "Si hay notas, retorna sum dividido por len. En Python tres la división siempre da número real: "
            "o sea, siempre devuelve un número con decimales."
        ),
    },
    {
        "id": 9, "tipo": "codigo", "tag": "EJERCICIO 1",
        "titulo": "obtener_maximo_promedio() — el guard obligatorio",
        "archivo": "ejercicio1_estudiantes.py",
        "funcion": "obtener_maximo_promedio",
        "patrones": [
            "max_nombre = None",
            "if promedio is None:",
            "max_promedio is None or promedio > max_promedio",
        ],
        "texto": (
            "Para obtener el máximo promedio, arrancamos sin candidato: max nombre y max promedio en nulo. "
            "En cada vuelta del for llamamos a calcular promedio, que puede devolver un número o el valor nulo. "
            "Si devuelve nulo, con continue salta esa vuelta. "
            "La condición de actualización tiene dos partes: que max promedio sea nulo, que se cumple en la primera vuelta, "
            "o que el promedio sea mayor que el máximo actual. "
            "Esa primera parte es obligatoria: en Python tres, comparar nulo con un número lanza un error de tipo."
        ),
    },
    {
        "id": 10, "tipo": "codigo", "tag": "EJERCICIO 1",
        "titulo": "clasificar_estudiante() — EL ORDEN de los if",
        "archivo": "ejercicio1_estudiantes.py",
        "funcion": "clasificar_estudiante",
        "patrones": [
            "if promedio >= 9:",
            "return \"Excelente\"",
            "if promedio >= 7:",
            "return \"Aprobado\"",
            "return \"Reprobado\"",
        ],
        "texto": (
            "Clasificar estudiante traduce la tabla de rangos, y acá está la trampa: el orden de los if. "
            "Primero preguntamos si es mayor o igual a nueve: si se cumple, retornamos Excelente y la función termina ahí. "
            "Después, si es mayor o igual a siete, Aprobado. Y si no entró en ninguno, Reprobado. "
            "Si preguntaras primero mayor o igual a siete, Ana, con nueve coma diecisiete, caería en Aprobado, "
            "y nadie sería nunca Excelente. De mayor a menor, siempre."
        ),
    },
    {
        "id": 11, "tipo": "codigo", "tag": "EJERCICIO 1",
        "titulo": "mostrar_resumen() — orquestar sin romper",
        "archivo": "ejercicio1_estudiantes.py",
        "funcion": "mostrar_resumen",
        "patrones": [
            "promedio = calcular_promedio",
            "if promedio is None:",
            "clasificacion = clasificar_estudiante",
            ":.2f",
        ],
        "texto": (
            "Mostrar resumen junta todo. Llama a calcular promedio, y si el resultado es nulo, hace return inmediatamente: "
            "la función anterior ya informó el motivo, y así evitamos formatear un nulo con dos decimales, "
            "lo que tiraría un error de tipo. "
            "Si hay promedio, llama a clasificar estudiante, y muestra tres líneas: el nombre, el promedio con dos decimales, "
            "y la clasificación. Fijate que los dos decimales son solo para mostrar; en memoria sigue guardado el número completo."
        ),
    },
    {
        "id": 12, "tipo": "codigo", "tag": "EJERCICIO 1",
        "titulo": "obtener_aprobados() — comprensión + ERRATA",
        "archivo": "ejercicio1_estudiantes.py",
        "funcion": "obtener_aprobados",
        "patrones": [
            "estudiantes[nombre] and calcular_promedio",
            ">= 7",
        ],
        "texto": (
            "Obtener aprobados usa una lista por comprensión. "
            "Por cada nombre, primero mira si la lista de notas no está vacía: si está vacía, el cortocircuito del and evita "
            "llamar a calcular promedio, así no calcula de más ni imprime mensajes. "
            "Si tiene notas, pregunta si el promedio es mayor o igual a siete. "
            "Y ahora, la errata del enunciado: dice que el resultado es Ana y Luis, pero Luis promedia seis coma nueve, "
            "porque veinte coma siete dividido tres es seis coma nueve, menor que siete. "
            "Con estos datos, el resultado real es solo Ana. Confía en la regla, no en el ejemplo."
        ),
    },

    # ───────────────────────── EJERCICIO 2 ─────────────────────────
    {
        "id": 13, "tipo": "codigo", "tag": "EJERCICIO 2",
        "titulo": "Los datos: producto → cantidades ENTERAS",
        "archivo": "ejercicio2_stock.py",
        "marker": {"desde": "productos = {", "hasta": "}"},
        "texto": (
            "Ejercicio dos: productos y stock. La estructura es la misma del ejercicio uno, pero con dos diferencias. "
            "El valor sigue siendo una lista, pero ahora son cantidades enteras registradas en cada control de stock. "
            "Y el caso borde es Impresora, con la lista vacía. "
            "La diferencia grande con el ejercicio anterior: cada registro se pide con int y no con float, "
            "porque el enunciado dice número entero. Si el usuario escribe tres coma cinco, int lanza ValueError "
            "y hay que volver a pedir."
        ),
    },
    {
        "id": 14, "tipo": "codigo", "tag": "EJERCICIO 2",
        "titulo": "agregar_producto() — int, no float",
        "archivo": "ejercicio2_stock.py",
        "funcion": "agregar_producto",
        "patrones": [
            "nombre = input(\"Nombre del producto: \")",
            "cantidad = int(input(",
            "cantidad_stock = int(input(",
            "productos[nombre] = registros",
        ],
        "texto": (
            "Agregar producto repite el mismo esqueleto: pedir el nombre con strip, verificar que sea todo letras con isalpha, "
            "comprobar que el producto no exista con un return temprano, pedir la cantidad dentro de try y except, "
            "y después cada registro con int y el chequeo de entero positivo. "
            "Recién al final, productos nombre igual a registros. "
            "Si ya hiciste el ejercicio uno, este lo tenés casi de memoria: lo único nuevo es la conversión a entero."
        ),
    },
    {
        "id": 15, "tipo": "codigo", "tag": "EJERCICIO 2",
        "titulo": "Opción A: calcular_stock_promedio (B cambia 1 línea)",
        "archivo": "ejercicio2_stock.py",
        "funcion": "calcular_stock_promedio",
        "patrones": [
            "if nombre not in productos:",
            "if not registros:",
            "return sum(registros) / len(registros)",
        ],
        "texto": (
            "El punto dos te hace elegir entre una de dos opciones. "
            "La opción A calcula el stock promedio: verifica si existe, si la lista está vacía informa y retorna nulo, "
            "y si hay datos retorna sum dividido por len. "
            "La opción B suma el stock total: es prácticamente la misma función; cambia solo la última línea, "
            "en vez de dividir se suma, y el mensaje dice total en vez de promedio. "
            "Para el parcial elegí una sola, pero saber que son casi idénticas te ahorra medio ejercicio."
        ),
    },
    {
        "id": 16, "tipo": "codigo", "tag": "EJERCICIO 2",
        "titulo": "obtener_productos_bajo_stock() — guard + < 5",
        "archivo": "ejercicio2_stock.py",
        "funcion": "obtener_productos_bajo_stock",
        "patrones": [
            "productos[nombre] and calcular_stock_promedio",
        ],
        "texto": (
            "El punto tres es la lista por comprensión: devuelve los nombres de los productos cuyo stock promedio sea menor a cinco, "
            "excluyendo los que no tengan registros. Fijate en el orden de la condición. "
            "Primero, productos nombre, que es la lista: si está vacía es falsa, y el cortocircuito del and ni siquiera llama "
            "a calcular stock promedio. Después, el promedio menor a cinco, estricto: cuatro coma nueve entra, "
            "exactamente cinco no. Con los datos del parcial, el resultado es solo Monitor, igual que el ejemplo del enunciado."
        ),
    },

    # ───────────────────────── EJERCICIO 3 ─────────────────────────
    {
        "id": 17, "tipo": "codigo", "tag": "EJERCICIO 3",
        "titulo": "Diccionario ANIDADO: dos saltos de clave",
        "archivo": "ejercicio3_inventario.py",
        "marker": {"desde": "inventario = {", "hasta": "}"},
        "texto": (
            "Ejercicio tres: inventario con diccionarios anidados. Acá cambia la estructura de los datos. "
            "La clave sigue siendo el nombre del producto, pero el valor ya no es una lista: es otro diccionario, con tres campos: "
            "precio, stock y categoría. Para llegar a un dato hacen falta dos saltos: primero la clave del producto, "
            "y después la clave del campo. Es el ejercicio que más se complica en memoria, "
            "pero la lógica de validación es la misma de siempre."
        ),
    },
    {
        "id": 18, "tipo": "codigo", "tag": "EJERCICIO 3",
        "titulo": "agregar_producto() — precio, stock ≥ 0, categoría",
        "archivo": "ejercicio3_inventario.py",
        "funcion": "agregar_producto",
        "patrones": [
            "precio = float(input(",
            "stock = int(input(",
            "if stock < 0:",
            "categoria = input(",
        ],
        "texto": (
            "Agregar producto pide cuatro datos. El nombre, con el patrón de siempre: strip, isalpha, y verificar que no exista. "
            "El precio con float y chequeo de positivo: acepta decimales. "
            "El stock con int, pero con el chequeo distinto: stock menor a cero, porque el cero sí se permite, "
            "como pide el enunciado, mayor o igual a cero. Es la diferencia con los ejercicios anteriores. "
            "Y la categoría, que es texto: solo hay que verificar que no quede vacía, sin try, "
            "porque no hay ninguna conversión que pueda fallar."
        ),
    },
    {
        "id": 19, "tipo": "codigo", "tag": "EJERCICIO 3",
        "titulo": "Guardar: se CREA un diccionario nuevo",
        "archivo": "ejercicio3_inventario.py",
        "funcion": "agregar_producto",
        "patrones": [
            "inventario[nombre] = {",
            "\"precio\": precio,",
            "\"stock\": stock,",
            "\"categoria\": categoria,",
        ],
        "texto": (
            "Al guardar, se crea un diccionario nuevo con los tres campos: precio, stock y categoría, "
            "y se asigna como valor de la clave. Si te olvidas un campo, el producto queda incompleto, "
            "y después, al consultar, te tira un error de clave. "
            "Al igual que en los ejercicios anteriores, esta es la única línea que muta el inventario, y está al final, "
            "después de validar todo. Todo lo demás hasta acá fue solo pedir y chequear."
        ),
    },
    {
        "id": 20, "tipo": "codigo", "tag": "EJERCICIO 3",
        "titulo": "consultar_producto() — dos saltos y comillas",
        "archivo": "ejercicio3_inventario.py",
        "funcion": "consultar_producto",
        "patrones": [
            "if nombre not in inventario:",
            "producto = inventario[nombre]",
            "producto['precio']",
            "producto['categoria']",
        ],
        "texto": (
            "Consultar producto hace el chequeo de existencia: si el nombre no está, informa y retorna. "
            "Si está, toma el diccionario interno en la variable producto, y muestra precio, stock y categoría "
            "con dos saltos de clave. Un detalle con las comillas: adentro del f-string van comillas simples, "
            "porque afuera ya estás usando comillas dobles. Si pusieras dobles adentro, cerrarías el texto y el código rompería."
        ),
    },
    {
        "id": 21, "tipo": "codigo", "tag": "EJERCICIO 3",
        "titulo": "calcular_valor_inventario() — precio × stock",
        "archivo": "ejercicio3_inventario.py",
        "funcion": "calcular_valor_inventario",
        "patrones": [
            "total = 0",
            ".items()",
            "producto[\"precio\"] * producto[\"stock\"]",
            "total = total + valor",
            "return total",
        ],
        "texto": (
            "Calcular el valor total recorre el inventario con items, que entrega clave y valor juntos: "
            "el nombre y el diccionario del producto. En cada vuelta multiplica precio por stock y lo suma al acumulador. "
            "Con los datos del parcial: Mouse aporta ciento cincuenta mil, Teclado ciento veinticinco mil, "
            "Monitor quinientos cuarenta mil, e Impresora, con stock cero, aporta cero, porque acá no se divide nada. "
            "El total da ochocientos quince mil. Ese es el número para verificar tu programa."
        ),
    },
    {
        "id": 22, "tipo": "codigo", "tag": "EJERCICIO 3",
        "titulo": "filtrar_por_categoria() — comparación exacta",
        "archivo": "ejercicio3_inventario.py",
        "funcion": "filtrar_por_categoria",
        "patrones": [
            "inventario[nombre][\"categoria\"] == categoria",
        ],
        "texto": (
            "Filtrar por categoría es otra lista por comprensión: recorre los nombres y compara "
            "inventario nombre punto categoría con la categoría pedida. Es una comparación exacta. "
            "Si escribís perifericos con minúscula y los datos tienen Perifericos con mayúscula, no coincide, "
            "y devuelve una lista vacía. Con los datos del parcial, Perifericos devuelve Mouse y Teclado, "
            "y Pantallas devuelve Monitor."
        ),
    },
    {
        "id": 23, "tipo": "codigo", "tag": "EJERCICIO 3",
        "titulo": "productos_sin_stock() — stock == 0",
        "archivo": "ejercicio3_inventario.py",
        "funcion": "productos_sin_stock",
        "patrones": [
            "inventario[nombre][\"stock\"] == 0",
        ],
        "texto": (
            "Y productos sin stock compara el stock con cero exactamente: no es menor o igual, es igual a cero. "
            "Con los datos del parcial devuelve una lista con Impresora, igual que el ejemplo del enunciado. "
            "Si agregas un producto con stock cero, también entra en esa lista."
        ),
    },

    # ───────────────────────── CIERRE ─────────────────────────
    {
        "id": 24, "tipo": "concepto", "tag": "CIERRE",
        "titulo": "Las trampas que más se olvidan",
        "bullets": [
            "strip() ANTES de isalpha()",
            "None (nulo) NUNCA se formatea con :.2f",
            "Clasificación: de MAYOR a MENOR (>=9 antes que >=7)",
            "int para cantidades · float para notas",
            "Leé bien: > 0  vs  >= 0",
            "UN solo diccionario en todo el programa",
        ],
        "texto": (
            "Y para cerrar, las trampas que más se olvidan: strip antes de isalpha; el valor nulo nunca se formatea "
            "con dos decimales; la clasificación se pregunta de mayor a menor; int para cantidades y float para notas; "
            "leé bien si es mayor a cero o mayor o igual a cero; y un solo diccionario en todo el programa. "
            "Ya tenés las tres soluciones, la guía en PDF y este video. ¡Éxitos en el parcial!"
        ),
    },
]
