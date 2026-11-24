# 📚 RESUMEN DE ESTUDIO — Clases de Técnicas de Programación (6/10 → 2/11)

> Resumen organizado **por temas** a partir de las 6 clases grabadas (6/10 → 2/11): tuplas, diccionarios completos con sus métodos, funciones sobre diccionarios, comprensiones, módulos, excepciones, el ejercicio integrador y cadenas de texto.

---

## 🎯 Fechas y formato del parcial (lo que dijo el profe en clase)

- **Segundo parcial: lunes 16 de noviembre de 2026.**
- **Recuperatorio: martes 24 de noviembre** (se corrió una semana por el feriado del 9/11; ese mismo día el profe pasa las notas).
- **Formato:** parte **teórica en papel** + parte **práctica en las computadoras** (igual que la clase pasada).
- **NO entran módulos** en el parcial (quizás puede pedir importar un módulo **preinstalado** de Python, por ejemplo `math` para la raíz cuadrada).
- El ejercicio va a ser **muy parecido a las prácticas**: un ejercicio con **diccionario** (posiblemente **anidado**), **validaciones** y **excepciones `try/except`**, y puede sumar algún **método de cadenas** (upper/lower/strip).
- **No habrá tantos métodos ni tantas funciones: una o dos funciones como mucho** — la práctica es más pesada para llegar "holgados" al parcial.
- El **modelo de parcial = contenidos definitivos** de la materia (ya no hay contenido nuevo, solo repaso y prácticas modelo parcial).

---

## 1. Tuplas (clase 6/10)

### Qué es
- Tipo de dato para guardar **conjuntos de datos**: números, strings, booleanos o mezcla — incluso otras listas o tuplas adentro.
- Se definen con **paréntesis** `()` (las listas usan corchetes `[]`):
  ```python
  tupla = (1, 2, 3)
  frutas = ("manzana", "pera", "banana")
  ```
- **Son inmutables**: una vez creada la tupla no se pueden agregar, borrar ni modificar elementos. Intentar asignar por índice (`frutas[2] = "limón"`) **da error**.
- Si hacés `t = t + (x,)`, Python lo permite pero **crea otra tupla** (una copia con el agregado) — no modifica la original. Para verificarlo se puede mirar la dirección de memoria con una función de Python.
- **Ventajas** respecto de las listas: son más rápidas y ocupan menos memoria, porque el espacio de memoria se define **al momento de crearse** (las listas dejan espacio reservado para agregar elementos después).

### Operaciones (las mismas que con listas)
- Acceso por **índice**: `frutas[2]` → elemento en la posición 2 (cuenta desde 0).
- **Slicing**: `frutas[1:3]` → porción de la tupla.
- **`len(tupla)`** → cantidad de elementos.
- **Unión** con `+` y **duplicado** con `*`.
- **`in` / `not in`** → verifica si un elemento puntual está dentro de la tupla.
- Se pueden extraer porciones y **copiar** la información a otra tupla o lista, pero la original queda intacta.

---

## 2. Diccionarios (clases 6/10 y 13/10)

### Qué es
- Estructura que almacena **pares `clave: valor`**: cada elemento tiene dos partes.
- Se crean con **llaves** `{}`; los elementos se separan con **coma** y la clave del valor con **dos puntos**:
  ```python
  ubicacion = {"direccion": "Monroe", "lugar": "Digital House", "mail": "ana@mail.com"}
  personas = {"Juan": 23, "Pedro": 43, "Pepe": 22}
  ruedas = {"auto": 4, "bicicleta": 2, "triciclo": 3}
  ```
- Ventaja sobre "dos listas paralelas" (una de nombres y otra de edades): con diccionarios la clave y el valor **viajan juntos** y no se corren de lugar.

### Reglas de las claves
- Pueden ser **strings o números** (el valor también puede ser de cualquier tipo: string, número, lista...). Ejemplo con clave numérica: `{38: "Roberto"}` (podría ser un documento/ID).
- **No deben repetirse**: si repetís una clave, el nuevo valor **pisa** el anterior. Esto es justamente por qué en el parcial los puntos "agregar" piden **verificar que la clave no exista** antes de asignar.
- El orden dentro de cada elemento es siempre: **primero la clave, después el valor**.

### Acceso
- `diccionario[clave]` → devuelve **el valor** de esa clave (no un índice numérico):
  ```python
  print(ubicacion["direccion"])   # "Monroe"
  ```
- En las listas se accedía por subíndice numérico; en los diccionarios el "subíndice" es **la clave**.

### Métodos principales (clase 13/10)
- **`dic.update({"clave": valor})`** → agrega elementos nuevos (y si la clave ya existe, **actualiza** el valor). Los métodos siempre llevan paréntesis.
- **`del dic["clave"]`** → **elimina el elemento completo** (clave y valor) por su clave. No borra "solo el valor".
- **`len(dic)`** → cantidad de elementos del diccionario.
- **`"clave" in dic`** / **`not in`** → verifica si existe esa clave (funciona igual que en listas y tuplas, pero evaluando claves).
- **`dic.keys()`** → devuelve todas las **claves**.
- **`dic.values()`** → devuelve todos los **valores**.
- **`dic.items()`** → devuelve los pares **clave-valor** (lista de tuplas). Es el más usado para recorrer.
- **`dic.get(clave, valor_defecto)`** → devuelve el valor de la clave; si la clave **no existe**, devuelve el valor por defecto (si no se pasa defecto, devuelve `None`). Preguntar sin arriesgar un error.
- **`dic.pop(clave)`** → **elimina la clave y devuelve su valor**. Sirve, por ejemplo, para sacar a alguien de un diccionario y guardarlo en otro ("de candidato a empleado"), o para mostrar qué se borró.
- **`dic.popitem()`** → elimina el **último par agregado**.
- **`dic.clear()`** → borra **todos** los elementos (queda vacío).
- **`dic.copy()`** → crea una **copia exacta** del diccionario, en otra ubicación de memoria.
- **`dic.setdefault(clave, valor)`** → si la clave existe, devuelve su valor; si **no** existe, la **crea** con ese valor (verifica/crea en un solo paso).
- **`dict.fromkeys(claves)`** → crea un diccionario a partir de las claves de otro.
- **Modificar un valor existente**: misma sintaxis que en las listas pero con la clave:
  ```python
  persona["edad"] = 26          # cambia el valor de la clave "edad"
  persona["nombre"] = "Luis"
  ```
- Nota de la clase: los que más se usan en la práctica son `items()`, `update` y `pop`; el resto conviene conocerlos y **aprender a leer la ayuda del editor** (pasar el mouse sobre lo rojo → explica el error, p. ej. *"Did you mean items?"* si escribís `item`).

### Recorrer un diccionarios (clases 6/10 y 13/10)
- `for clave in dic:` → por defecto un `for` sobre el diccionario **recorre las claves**. Con `dic.keys()` se ve igual: devuelve la lista de claves.
- **`for clave, valor in dic.items():`** → recorre con **dos variables**: una guarda la clave, otra el valor. Es la forma estándar de recorrer un diccionario.
- Ejemplo resuelto en clase — *informar quién es la persona de mayor edad*:
  ```python
  mayor_edad = 0          # ← se inicializa FUERA del for
  nombre = ""
  for clave, valor in personas.items():   # clave = nombre, valor = edad
      if valor > mayor_edad:
          mayor_edad = valor
          nombre = clave
  print(nombre, mayor_edad)               # Pedro 43
  ```
- **Trampa corregida en vivo:** la variable bandera (`mayor`) debe inicializarse **afuera** del `for`. Si queda adentro, se borra en cada iteración y solo se conserva el último elemento.
- También se puede imprimir el resultado **al final** del bucle (una sola vez) en vez de en cada vuelta.
- Idea general (la que retomó el parcial): recorrer la lista/diccionario, comparar cada valor con el "mayor" actual, y si es mayor, actualizar tanto el valor como la clave asociada (para saber *quién* es el mayor).

---

## 3. Funciones que trabajan sobre diccionarios (ejercicio de la clase 13/10)

**Ejercicio:** crear un diccionario `notas_estudiantes` donde la clave sea el **nombre** del estudiante (texto) y el valor sea una **lista de números** (sus notas). Después, funciones para: agregar estudiantes, agregar una nota y calcular el promedio.

### Patrón 1 — Recibir el diccionario por parámetro (código genérico)
```python
def agregar_estudiante(diccionario):
    nombre = input("Nombre: ")
    diccionario[nombre] = []              # le asigna una lista vacía
    # equivalente: diccionario.update({nombre: []})
```
- Que la función **reciba el diccionario** (en vez de usar una variable global) la hace **genérica y reutilizable**: la misma función sirve para `notas_estudiantes`, para notas de secundaria, para cualquier diccionario con la misma forma.
- El nombre del parámetro es un nombre "genérico" (`diccionario`, `algo`, `d`...): lo único que importa es que sea **el mismo nombre adentro** de la función.
- El nombre del estudiante puede pedirse con `input()` **dentro** de la función o recibirse por parámetro — ambas formas valen.

### Patrón 2 — Agregar una nota (validar ANTES de tocar la lista)
```python
def agregar_nota(diccionario, nombre, nota):
    if nombre in diccionario:                 # ¿existe ese estudiante?
        diccionario[nombre].append(nota)      # agrega a SU lista
    else:
        print("No existe ese estudiante.")
```
- **Primero** se valida con `in` que el nombre exista en el diccionario; **recién ahí** se modifica.
- **Trampa importante:** NO usar `update` para agregar una nota — `update` **pisaría la lista completa** con una lista de una sola nota. Como el valor es una lista, lo correcto es **`append`** sobre `diccionario[nombre]`.
- Cadena de acceso: `diccionario[nombre]` → devuelve la lista → `.append(nota)` la incrementa al final.

### Patrón 3 — Calcular el promedio de un estudiante
```python
def calcular_promedio(diccionario, nombre):
    if nombre in diccionario:
        notas = diccionario[nombre]        # la lista de notas de ese nombre
        if notas:                         # ¿tiene al menos una nota?
            return sum(notas) / len(notas)
    # si no existe o no tiene notas:
    return None
```
- Acceder al elemento → obtener la lista → `sum(notas) / len(notas)`.
- Si el nombre **no existe** o **no tiene notas** → avisar y devolver `None` (señal de fallo para quien llame).

### Variantes y extras sugeridos en clase
- Agregar **varias notas**: pedir cuántas quiere cargar y recorrer un `range` llamando a la función de agregar en cada vuelta.
- Función **`borrar_estudiante(diccionario, nombre)`**: si `nombre in diccionario` → `del diccionario[nombre]`.
- Mismo ejercicio pero con **productos** (mostrarlos, buscarlos).
- Los estudiantes de la clase armaron también la opción de que el nombre llegue por `input()` y la actualización se haga con `update` — ambas válidas, pero conviene **centrarse en lo que pide el ejercicio** y no complicar de más.

---

## 4. Comprensiones (el profe les dice "compresión") — clase 20/10

### Por qué sirven
- Forma de escribir en **una sola línea** lo que antes era un `for` recorriendo + `append` construyendo una lista nueva.
- Menos escritura, y además es la sintaxis que se va a usar más adelante con **funciones `lambda`** y limpieza de datos (y sirve para cuatrimestre que viene).
- Vale aclarar: es una forma **distinta de escribir** lo mismo — no hace nada que el `for` tradicional no hiciera.

### 4.1 Estructura básica de lista por comprensión
```
[ expresión  for  elemento  in  iterable ]
```
- **expresión** → qué se guarda en la lista nueva (puede ser una cuenta, p. ej. `n * 2`; o simplemente `n`).
- **elemento** → la variable temporal del `for` (misma idea de siempre).
- **iterable** → la colección a recorrer (lista, `range`, string...).
- Ejemplo — lista de precios duplicada:
  ```python
  # tradicional
  dobles = []
  for n in numeros:
      dobles.append(n * 2)

  # comprensión (una línea)
  dobles = [n * 2 for n in numeros]
  ```
- Ejemplo con `range`: `lista = [n for n in range(1, 6)]` → `[1, 2, 3, 4, 5]` (el final del `range` es **exclusivo**: siempre hasta el último menos uno).
- La expresión se evalúa **por cada elemento** y ese resultado es lo que se va guardando en la lista nueva (equivalente al `append`, pero sin escribirlo).

### 4.2 Con condicional (filtrar) — estructura
```
[ expresión  for  elemento  in  iterable  if  condición ]
```
- El `if` va **al final** (después del `for`) y **no lleva `else`**: solo filtra.
- **Flujo de evaluación:** el `for` toma un elemento → se evalúa el `if` → si es verdadero, se ejecuta la **expresión** → recién ahí se agrega a la lista. Si el `if` es falso, se descarta el elemento y se vuelve al `for`.
- Ejemplos:
  ```python
  pares = [n for n in numeros if n % 2 == 0]                     # solo filtra
  cuadrados_pares = [n ** 2 for n in range(1, 11) if n % 2 == 0] # filtra y transforma
  ```
- `n % 2 == 0` → el **módulo** (resto de la división) entre 2 es cero → el número es **par**.
- Para "transformar y filtrar al mismo tiempo" (p. ej. el cuadrado de los pares): primero se evalúa el `for`, luego el `if`, y para los que cumplen se aplica la operación de la expresión.

### 4.3 Diccionarios por comprensión
- Estructura (misma idea, con llaves):
  ```
  {  clave : valor   for  elemento  in  iterable   [if condición]  }
  ```
- Ejemplo — cuadrados:
  ```python
  cuadrados = {n: n ** 2 for n in range(1, 6)}
  # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
  ```
  La clave es `n` y el valor es `n ** 2`; el resultado va quedando elemento por elemento.

### Crear un diccionario desde DOS listas — `zip()`
```python
nombres = ["Ana", "Luis", "Marta"]
edades  = [20, 25, 33]
personas = {nombre: edad for nombre, edad in zip(nombres, edades)}
# {'Ana': 20, 'Luis': 25, 'Marta': 33}
```
- **`zip(l1, l2)`** combina los elementos que ocupan la **misma posición** de cada lista (posición 0 con posición 0, etc.).
- En el `for` se usan **dos variables** (una por lista), igual que con `items()`.
- Comportamiento verificado en clase: si las listas tienen **distinta longitud**, solo se combinan las posiciones que coinciden — los elementos de más **se ignoran** (no se crean claves incompletas).

### Filtrar y transformar entradas de un diccionario (con `items()`)
```python
notas = {"Ana": 8, "Luis": 5, "Marta": 9, "Juan": 4, "Sofia": 7}

# filtrar: solo quienes promocionan (nota >= 7)
promocionados = {nombre: nota for nombre, nota in notas.items() if nota >= 7}
# {'Ana': 8, 'Marta': 9, 'Sofia': 7}

# filtrar + operar en la expresión: duplicar las notas >= 4
notas_duplicadas = {nombre: nota * 2 for nombre, nota in notas.items() if nota >= 4}
# {'Ana': 16, 'Luis': 10, 'Marta': 18, 'Juan': 8, 'Sofia': 14}
```
- Se desempaquetan **clave y valor** en dos variables con `.items()`.
- El `if` decide quién entra; la **expresión** se ejecuta **después** del `if` y **antes** de guardarse (por eso la nota se duplica recién al pasar el filtro).
- Si la operación es larga, se puede escribir la comprensión en varias líneas respetando la estructura (no todo debe quedar en una línea física).

### Ejercicios que dejaron en esta clase
1. Crear diccionarios a partir de dos listas (con `zip`).
2. Filtrar y duplicar precios.
3. (al final del archivo de la clase) tres ejercicios más para practicar.

---

## 5. Módulos, paquetes y bibliotecas (clase 26/10) — Unidad 5

### Para qué sirven
- **Organizar y reutilizar** código: llevar funciones, variables o bloques a archivos aparte. El archivo principal queda **limpio** y solo hace los llamados.

### Módulo
- Un **módulo = un archivo `.py`**.
- Puede contener funciones, variables, diccionarios, lo que sea. Ejemplo: `funciones.py` con `sumar(a, b)`, `restar(a, b)`, `multiplicar(a, b)`.
- El archivo donde se **usa** todo eso se llama principal (`main.py`).
- **Los dos archivos deben estar en la misma carpeta** para que Python los encuentre; si están en carpetas distintas hay que indicar la ruta.

### Formas de importar
- `import modulo` → uso con **punto**: `modulo.sumar(2, 3)`.
- `import modulo as alias` → pseudónimo para nombres largos: `import funciones as f` → `f.sumar(2, 3)`.
- `from modulo import funcion` → la función queda **suelta** en el entorno: `sumar(2, 3)` (sin punto).
- `from modulo import funcion, variable` → se traen cosas **puntuales**, separadas por coma.
- `from modulo import *` → el asterisco significa **todo**: trae todo el contenido del módulo.
- Analogía del profe: importar solo el módulo = *"traer la caja con cosas adentro"* (hay que usar el punto para llegar); `from ... import` = *"vaciar la caja en mi código"* (acceso directo).
- **Buena práctica:** importar **solo lo que necesites** — importar todo consume más memoria y a mayor escala importa.

### Módulos preinstalados de Python (los más conocidos)
- **`math`**: funciones matemáticas — raíz cuadrada (`sqrt`), `pi`, logaritmos, trigonometría. (Python no tiene operador de raíz directo; con `math.sqrt` se resuelve.)
- **`random`**: valores aleatorios.
- **`datetime`**: trabajo con fechas.
- **`os`**: sistema operativo.
- **`statistics`**: cálculo de estadística.
- **`sys`**: funciones de sistema (p. ej. limpiar la consola).
- Todas se usan igual: primero `import`, después con punto.

### Paquetes
- Un **paquete = una carpeta que agrupa módulos**.
- Para que Python la reconozca como paquete: crear dentro un archivo **`__init__.py`** (doble guion bajo + `init` + doble guion bajo + `.py`; puede estar vacío — solo identifica la carpeta como paquete).
- Estructura de ejemplo (la que armó en clase):
  ```
  sistema_ventas/          ← carpeta general
      main.py              ← el principal va ACÁ (en la raíz)
      clientes/            ← paquete
          __init__.py
          clientes.py
      operaciones/         ← paquete
          __init__.py
          operaciones.py
  ```
- Import jerárquico: `from clientes import clientes` → primero la **carpeta**, después el **módulo** (sin poner `.py`). Con subcarpetas: `from paquete.subcarpeta import modulo`.
- El **punto `.`** atraviesa toda la jerarquía: carpeta → subcarpeta → módulo → función/variable.
- **Error típico resuelto en clase:** el `main.py` debe estar en la **carpeta general (raíz)**, **no** dentro de una carpeta paquete — si no, Python no encuentra las rutas (habría que "salir" de carpetas con rutas relativas). Regla práctica: **el principal siempre arriba de todo**.
- Con imports puntuales o `*`, el principal queda prácticamente en "una línea": más limpio y ordenado.
- Diferencia módulo vs paquete: **módulo = archivo `.py`** con código reutilizable; **paquete = carpeta** que agrupa módulos (con su `__init__.py`).

### Bibliotecas (librerías)
- Igual que módulos/paquetes pero **no vienen instaladas** en Python: hay que instalarlas con el instalador de paquetes de Python: **`pip install nombre`** (p. ej. `pip install pandas`).
- Después se importan igual: `import pandas as pd` (el alias es la costumbre en ese ecosistema).
- Spoiler del profe: se usan para **análisis de datos** (pandas y demás) en cursos posteriores.

---

## 6. Excepciones — capturar errores con `try/except` (clase 26/10)

### El problema
- `input()` siempre devuelve **texto**. Si el usuario escribe `"abc"` y hacemos `int(...)`, Python lanza **`ValueError`** y **el programa se corta** con el cartel de error rojo.
- Ídem: dividir entre 0 → **`ZeroDivisionError`**; pedir la posición 15 de una cadena/lista de 10 → **`IndexError`**.
- Objetivo: **capturar** esos errores → el usuario ve un mensaje claro y **el programa sigue corriendo**.

### Estructura `try/except`
```python
try:
    numero = int(input("Ingresá un número: "))
    resultado = 50 / numero
except ValueError:
    print("Debés ingresar un número válido.")
except ZeroDivisionError:
    print("No se puede dividir por cero.")
```
- `try:` → *"intentá ejecutar este bloque"* (el código que puede fallar va tabulado adentro).
- `except TipoError:` → si adentro salta **ese** error, se ejecuta el bloque del `except` en vez de cortarse.
- Los tres tipos que más se cruzan:
  - **`ValueError`** → valor inválido (p. ej. `int("abc")`).
  - **`ZeroDivisionError`** → división por cero.
  - **`IndexError`** → índice fuera de rango.
- Se pueden apilar varios `except` (uno por tipo) y dejar un **`except` general** (sin tipo) al final "por las dudas", para capturar cualquier otro error.
- Alias opcional: `except ZeroDivisionError as e:` → permite mostrar el error original (`print(e)`), útil si quien usa el programa es otro programador.

### `else` y `finally`
- **`else`** → se ejecuta **solo si NO hubo ningún error** (camino feliz: imprime el resultado). Es el equivalente a "si no saltó ninguna excepción".
- **`finally`** → se ejecuta **SIEMPRE**, pase lo que pase (con error, sin error, con números, con letras...). Sirve para tareas de cierre: limpiar/resetear variables, verificar que un archivo se guardó bien, desconectar una base de datos. No se usa mucho, pero hay que conocerlo.

### ⭐ El patrón estrella: `while True` + `try` + `break` (¡la base de la plantilla del parcial!)
```python
while True:
    try:
        numero = int(input("Número: "))
        break                 # todo salió bien → sale del while
    except ValueError:
        print("No es un número. Intentá de nuevo.")
```
- El `while True` **repite** pedir el dato hasta que sea válido.
- Dato malo → mensaje → el `while` vuelve a pedir (el `break` no llegó a ejecutarse).
- Dato bueno → `break` → sale del bucle y el programa sigue.
- Esto **reemplaza** a los `if` de validación de a uno: mientras el usuario no acierte, se sigue pidiendo. Es literalmente el origen de la **plantilla maestra de validación** de los puntos `agregar_*` del parcial.
- Ejemplo resuelto en clase: pedir 2 números y multiplicar — si el primero falla, captura y sigue pidiendo; recién cuando ambos son válidos calcula y sale con `break`.
- Ejemplo con cadenas: pedir una palabra (se queda como texto) y un índice (int) → imprimir el carácter en esa posición. Se capturan `IndexError` (posición fuera de rango) y `ValueError` (índice no numérico). Las cadenas son **iterables**: `"hola"` equivale a h(0), o(1), l(2), a(3).

### Ejercicios y lo que viene
- Seis ejercicios de manejo de excepciones para practicar.
- La idea de las próximas clases: prácticas **combinadas** tipo parcial — una función que tenga comprensiones, dentro de un `while`, que use un módulo y tenga su bloque `try`.

---

## 7. Práctica integradora — Alumnos y calificaciones (clase 27/10)

### Organización de archivos (módulos en la práctica)
- **Una carpeta por ejercicio** (`ejercicio1/`, `ejercicio2/`...) y **todos los archivos adentro** (`principal.py`, `funciones.py`). Si los creás "afuera" o con el mismo nombre en carpetas distintas, Python se confunde al importar (varios `principal.py`).
- Crear archivos con **clic derecho sobre la carpeta** (o arrastrarlos adentro) para que queden dentro.
- **Sobre el parcial:** el profe dijo textual que *probablemente **no** entre lo de módulos* en el parcial (es engorroso para tomarlo/entregarlo y nunca lo tomó), pero que es un tema importante que hay que practicar igual.
- Ejercicio de la clase = **instancia previa al modelo de parcial** ("preparcial"): combina todo — módulos + diccionario + validaciones + try/except + menú while. Hay que hacerlo sí o sí.

### El ejercicio armado (módulo `funciones.py` + `principal.py`)
El diccionario global `notas = {}` vive en el módulo (clave = nombre, valor = nota).

**Función `agregar_alumno` — la cadena completa de validaciones (¡esto es la plantilla del parcial!):**
```python
def agregar_alumno():
    nombre = input("Ingresá el nombre: ")

    # 1) ¿vacío? → corta (return termina la función, como el break del while)
    if nombre == "":
        print("El nombre no puede estar vacío.")
        return

    # 2) ¿ya existe? → corta (antes de pedir la nota)
    if nombre in notas:
        print("El alumno ya está registrado.")
        return

    # 3) la nota: tiene que ser número → try/except
    try:
        nota = float(input("Ingresá la nota: "))
    except ValueError:
        print("Tenés que ingresar un número.")
        return

    # 4) rango: entre 1 y 10 (1 y 10 incluidos → se chequea lo contrario con OR)
    if nota < 1 or nota > 10:
        print("La nota tiene que estar entre 1 y 10.")
        return

    # 5) recién AHORA se muta el diccionario
    notas[nombre] = nota
```
- **Orden importa:** primero lo del nombre (vacío → existe), **recién después** pedir la nota — si el nombre está mal o ya existe, no tiene sentido preguntar la nota.
- `return` sin valor **termina la función** (funciona como el `break` del `while`).
- `if nota < 1 or nota > 10` → el `or` hace que con que una de las dos se cumpla, la sentencia sea verdadera. Como 1 y 10 **están incluidos**, se valida lo contrario (`< 1` o `> 10`).
- Conversión con `float` → la nota cargada desde teclado queda como decimal (9 → se ve 9.0); la que se pone a mano en el diccionario queda como esté.
- Se puede recibir el diccionario por parámetro (`def agregar_alumno(diccionario)`) para que la función sea genérica — acá se decidió dejarlo laburando sobre la estructura directamente.

**Función `consultar_nota` — acceder por clave:**
```python
def consultar_nota():
    nombre = input("Nombre a consultar: ")
    if nombre in notas:
        print(f"La nota de {nombre} es {notas[nombre]}")
    else:
        print(f"{nombre} no está en el diccionario.")
```
- Misma sintaxis que las listas pero **con la clave** en vez del índice: `notas[nombre]` → el valor.

**Función `calcular_promedio` — `values()` y validar el vacío:**
```python
def calcular_promedio():
    if len(notas) == 0:          # diccionario vacío → no hay nada que calcular
        print("No hay alumnos.")
        return
    return sum(notas.values()) / len(notas)
```
- **`notas.values()`** devuelve **todos los valores** (todas las notas) → se puede pasar directo a `sum()`: `sum(notas.values())`.
- Primero la guardia del diccionario vacío; después el cálculo.
- Esta función **retorna** el número (no imprime) → quien la llama debe imprimirlo: `print(calcular_promedio())`. **Error que pasó en vivo:** el menú no mostraba nada porque la función hacía `return` y nadie hacía el `print`.

**Función `mostrar_todos` — recorrer con `items()`:**
```python
def mostrar_todos():
    if len(notas) == 0:
        print("No hay alumnos registrados.")
        return
    for nombre, nota in notas.items():     # ojo la S de items
        print(f"{nombre}: {nota}")
```
- Si está vacío → avisa y corta; si no, recorre con `for` de dos variables e imprime cada par.

**Menú en `principal.py` — `while True` + `if/elif` + `break`:**
```python
while True:
    print("1) Consultar nota")
    print("2) Promedio general")
    print("3) Listar alumnos")
    print("4) Agregar alumno")
    print("5) Salir")
    opcion = input("Ingrese una opción: ")

    if opcion == "1":
        consultar_nota()
    elif opcion == "2":
        print(calcular_promedio())
    elif opcion == "3":
        mostrar_todos()
    elif opcion == "4":
        agregar_alumno()
    elif opcion == "5":
        break
    else:
        print("Opción no válida.")
```
- Opciones comparadas **como texto** (`== "1"`, porque `input` devuelve string).
- El programa queda corriendo **todo el tiempo** hasta que el usuario elige la opción de salir (`break`).
- Si el usuario escribe una letra u otra cosa → el `else` avisa y el menú se repite.
- Se puede envolver la lectura en un `try/except ValueError` (con mensaje "ingresá un número válido") para el caso de que se pida un número y llegue texto.

### Errores comunes que aparecieron en vivo (todos clásicos)
- Llamar a una función que **retorna** sin hacer `print` en el llamador → "no muestra nada".
- Escribir `item` en vez de **`items`** → el editor tira *"Did you mean items?"* (leer los mensajes rojos).
- Correr el programa desde la carpeta equivocada → terminal: `cd` a la carpeta y `python principal.py` (o botón derecho en la carpeta → abrir terminal ahí).

### Lo que sigue (y viene para los siguientes ejercicios)
- Hay ejercicios donde hay que **filtrar** (p. ej. "mostrar los productos baratos") usando **comprensión de diccionarios filtrando en la misma línea**.
- Próxima clase: **métodos de cadenas** — validar nombres con espacios/mayúsculas (p. ej. "Juan Pérez" vs "juan perez"): pasar todo a mayúscula/minúscula y manejar los espacios.

---

## 8. Ejercicio "sistema de ventas" — diccionarios anidados en acción (clase 2/11)

Estructura de datos del ejercicio: `productos` donde la clave es el nombre y el valor **otro diccionario** con `precio` y `stock`; más una lista `ventas` para registrar lo vendido.

### 8.1 La idea del diccionario anidado (demo previa)
```python
productos = {
    "reloj":     1000,                                  # valor simple
    "parlante":  [2000, 3000],                          # valor lista
    "monitor":   {"precio": 10000, "modelo": "curvo"},  # valor diccionario
}
```
- `productos["reloj"]` → `1000`
- `productos["parlante"][0]` → `2000` (clave → lista → índice)
- `productos["monitor"]` → **el diccionario entero**
- `productos["monitor"]["precio"]` → `10000` — **doble salto**: primero la clave del producto, después la clave interna.
- Regla: con listas se accede por **índice**, con diccionarios por **clave**; si el valor es otro diccionario, se encadenan corchetes.
- Ojo: `productos["mouse"]["stock"]` **no imprime la palabra "stock"** — imprime el **valor** guardado en esa clave (p. ej. 10). Eso es lo "más rebuscado de entender" según el profe, y es exactamente el corazón del Ej3 del parcial.

### 8.2 Las funciones del sistema

**`agregar_producto`** — la cadena de siempre, con mutación **anidada** al final:
- nombre vacío → `return`; ya existe → `return`; bloque `try` para precio y stock (si llega texto → excepción "ingresá un precio y un stock válidos").
- Validaciones de rango: el precio debe ser **al menos 1** (no puede ser 0 ni negativo) y el stock no puede ser cero ni negativo en este ejercicio de práctica.
  > ⚠️ Contraste con el **modelo del parcial (Ej3)**: ahí el stock **0 sí vale** y la única condición mala es `stock < 0`.
- **La mutación crea el diccionario interno en el momento:**
  ```python
  productos[nombre] = {"precio": precio, "stock": stock}
  ```
  (las variables se llamaron `pre` y `stock` para no confundirlas con los strings de las claves `"precio"`, `"stock"`).

**`consultar_stock`:**
- Pedir nombre → `.strip()` → `if nombre in productos:` → imprimir `productos[nombre]["stock"]` (doble salto) → si no está, avisa y `return`.

**`registrar_venta`** — la más completa:
1. `if nombre not in productos:` → "no existe" → `return`. (Se usó la **negación**: conviene cuando el caso fallo es el de entrada.)
2. Cantidad con `try/except` (tiempo que sea número).
3. `if cantidad <= 0:` → "vendiste nada" → `return`.
4. ¿Hay stock? `if cantidad > productos[nombre]["stock"]:` → "no hay stock suficiente" → `return`.
5. **Descuento:** `productos[nombre]["stock"] -= cantidad`.
6. Registrar en la lista `ventas` (agregar el nombre del producto; el enunciado es ambiguo entre agregarlo una vez o una por unidad — ambas válidas).
7. Total de la venta: `productos[nombre]["precio"] * cantidad` → imprimir (con `:.2f` opcional, es solo mostrar dos decimales).

**`mostrar_inventario`:**
- `if len(productos) == 0:` → "no hay ningún producto registrado" → `return`.
- `for nombre, datos in productos.items():` → acá `datos` es **otro diccionario** → imprimir `datos["precio"]` y `datos["stock"]`.

**Valor total del inventario** — acá conviene **`.values()`** (cuando solo necesitás los valores, no la clave):
```python
total = 0
for datos in productos.values():
    total += datos["precio"] * datos["stock"]
return total
```
- precio × stock por producto y sumar — **mismo cálculo que el Ej3 del parcial**.

### 8.3 Comprensiones sobre el diccionario anidado
```python
sin_stock   = [nombre for nombre, datos in productos.items() if datos["stock"] == 0]
economicos  = [nombre for nombre, datos in productos.items() if datos["precio"] < umbral]
```
- El `for` desempaqueta clave y valor; el `if` se fija **dentro del diccionario interno** (`datos["stock"]`).
- Dos formas de devolver: crear la variable y `return` la variable, o hacer `return [comprensión]` directo — quien llame debe guardar/imprimir el resultado. Ambas válidas.
- Aclaración del profe: la comprensión es para **crear una lista nueva**; simularla con `extend` no tiene sentido — si el ejercicio pide comprensión, se hace con corchetes.

### 8.4 Detalles del menú (errores en vivo)
- El `try` debe envolver **las comparaciones de las opciones**: si queda por fuera, nunca atrapa el error (lo movió y funcionó).
- `break` en la opción de salir → si no está, el `while True` **nunca sale** del menú.
- Sobre el parcial (dijo el profe): **no habrá tantos métodos ni tantas funciones** — un ejercicio parecido pero con **una función o dos como mucho**; esta práctica es más pesada para llegar "holgados".

---

## 9. Cadenas de texto (strings) — Unidad 6 (clase 2/11)

### Qué son
- Sucesiión de caracteres entre comillas (simples o dobles: es lo mismo).
- Son **iterables**: se recorren con `for` letra por letra, se accede por índice (`texto[0]`), índice negativo (desde el final) y con *slicing*.
- **Inmutables** (igual que las tuplas): no se puede modificar un carácter en su lugar — los métodos devuelven **una cadena nueva**. (El tema de referencias/copias —misma variable vs copia— se vio como avance y no se usa en el parcial.)

### Operaciones
- `+` → concatena (no suma), `*` → repite la cadena.
- `in` → ¿está esa letra/palabra adentro de la cadena?
- `len(texto)` → cantidad de caracteres.
- `texto.count("o")` → cuántas veces aparece ese carácter.

### Métodos principales
- **`.upper()`** → todo a MAYÚSCULA.
- **`.lower()`** → todo a minúscula.
- **`.strip()`** → saca los **espacios del principio y del final** (limpiar lo que ingresa el usuario).
- **`.replace("viejo", "nuevo")`** → reemplaza ocurrencias (p. ej. "hola" → "chau").
- **`.split()`** → separa por espacios y devuelve una **lista** de palabras.
- **`.isalpha()`** → `True` **solo si todos** los caracteres son letras (False si hay espacios, números o símbolos).
- **`.isdigit()`** → `True` si **todos** son dígitos (validar documentos o números escritos como texto).
- **`.capitalize()`** → primera letra en mayúscula, el resto minúscula.
- **`.format()`** → forma anterior a los f-strings para insertar variables en un texto; saber que existe, no hace falta usarlo.

### Comparación "insensible a mayúsculas" (muy probable en el parcial)
- Python compara **letra por letra**: `"Ana"` **no** es igual a `"ana"` → si el usuario escribe distinto, el programa cree que "no existe".
- Solución: **unificar antes de comparar** — `.strip()` para los espacios y `.upper()` (o `.lower()`) en **ambos lados**:
  ```python
  nombre = input("Nombre: ").strip().upper()
  # ... recorrer la lista comparando nombre == elemento.upper()
  ```
- Ejemplo de la clase: lista `[Ana, Juan, Pedro, María]` → pedir un nombre → verificar si está (sin importar mayúsculas) → si **no** está → `append` → mostrar la lista actualizada.
- Variante con **bandera**: `encontrado = False` → recorrer con `for` → al coincidir: `encontrado = True` y **`break`** (dejar de recorrer — eficiencia en listas largas) → después `if encontrado: ... else: ...`.
- Variante más directa: `if nombre in lista` cuando no hace falta normalizar, o un `if/else` anidado.

### Ejercicios del archivo de la clase (para practicar)
1. Pedir una cadena → mostrar cuántos caracteres tiene (`len`).
2. Pedir una cadena → mostrarla en mayúscula.
3. Verificar si contiene la palabra "Python" (`in`).
4. Mostrarla sin espacios al inicio y al final (`strip`).
5. Mostrar su primera letra.
6-8. (variantes cortas de lo mismo)
9. Lista de nombres: pedir nombre, buscar con comparación **insensible a mayúsculas**; si no está → `append` → mostrar lista.
10. Ídem pero con una lista de ciudades.
11. Dos funciones (agregar y eliminar tareas de una lista) con validaciones, y mostrar la lista tras cada operación.

---

## 10. Cierre — qué espera el parcial y qué practicar

- Frase del profe: *"si pudieron hacer estos ejercicios, están muy bien para el parcial porque **va a ser esto**"*.
- **Contenido de la materia cerrado** — no queda contenido nuevo, solo práctica.
- La última clase es **repaso + ejercicios modelo de parcial**: combinando diccionario con diccionario, excepciones, validaciones y probablemente métodos de cadenas (upper/lower/strip).
- Sugerencia de estudio: repasar **listas y diccionarios**, pero siempre pensando en el **ejercicio completo** (estructura + validaciones + impresiones), no temas aislados.
- Para las dudas que queden: los ejercicios "preparcial" están en el aula virtual; practicar el fin de semana largo.
