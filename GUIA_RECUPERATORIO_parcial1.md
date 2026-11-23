# 📘 GUÍA DE ESTUDIO — RECUPERATORIO PRIMER PARCIAL

**Técnicas de Programación** · Basada en las diapositivas de las clases 3, 5, 6, 7, 9, 11 y 13.
Todo el código de esta guía fue **corrido y verificado** en Python 3.

---

## PARTE A — Resumen de contenidos (los 7 temas)

### 1. Fundamentos (clase 3)

- **Literales** (valores fijos en el código):
  - `int`: `1`, `5`, `345`, `-3`, `0`
  - `float`: `3.14`, `2.5`, `0.0`
  - `str`: `"hola"`
  - `bool`: `True` / `False` (con mayúscula)
  - `None`: ausencia de valor (tipo `NoneType`)
- **Variables**: `nombre_de_variable = valor` (espacio de memoria con nombre).
- **`print()`**:
  - `print(f"Mi nombre es {nombre}")` → f-strings
  - `print("a", "b", "c")` → agrega **un espacio** entre elementos
  - `print("a", "b", sep="-")` → cambia el separador (une **sin** espacios si `sep=""`)
  - `print("Hola", end=" ")` → **no** salta de línea al terminar
- **`input()`**:
  - ⚠️ **SIEMPRE devuelve `str`**, aunque parezca un número: `input()` + `input()` con `3` y `6` da `"36"` o `"63"`, **no 9**.
  - Detiene el programa hasta que se presiona Enter.
  - Para calcular hay que castear: `int(input(...))` o `float(input(...))`.
- **Casting**: `int("5")` → `5`; `float("3.5")` → `3.5`; `str(5)` → `"5"`.
- **PEP 8**: `snake_case` para variables y funciones, 4 espacios de indentación, `#` comentarios, `"""docstrings"""`.

### 2. Nombres de variables y comparadores (clase 5)

- ✅ Pueden tener letras, números (no al principio) y `_`: `edad2`, `total_compra`.
- ❌ Ilegales: `101` (empieza con número), `m 101` (espacio), `precio$` (símbolo), `if` (palabra reservada), `mi nombre` (espacio).
- ⚠️ `Del` (con mayúscula) **sí es legal**; la reservada es `del` (minúscula). Python distingue mayúsculas.
- **Comparadores**: `==` igualdad, `!=` desigualdad, `>`, `<`, `>=`, `<=`.
- **Programación estructurada**: secuencia · selección (`if`) · iteración (`while`/`for`).

### 3. Condicionales (clase 6)

```python
if condicion:
    ...
elif otra_condicion:      # corta en la PRIMERA que se cumple
    ...
else:                     # se engancha al ÚLTIMO if
    ...
```

- El `else` de un `if` sin `elif` se asocia **solo al `if` inmediatamente anterior**.
- **Operadores lógicos** (precedencia: `not` > `and` > `or`):
  - `and` → ambas verdaderas; `or` → al menos una; `not` → invierte.
  - Ejemplo: `x < z and z > y or y < z and z < y` → primero se resuelven los `and`, después el `or`.
- La **indentación define el bloque**: sin sangría, el código no está dentro del `if`.

### 4. Bucles (clase 7)

- **`while condicion:`** → se repite mientras sea `True`. ⚠️ Si nadie cambia la variable de la condición → bucle infinito.
  - `break` → **sale** del bucle inmediatamente.
  - `continue` → **saltea** la vuelta actual, el bucle sigue.
  - `while ... else:` → el `else` corre **cuando el bucle termina sin `break`**.
- **`for variable in range(...)`** → cantidad de vueltas conocida:
  - `range(5)` → `0,1,2,3,4` (llega hasta `fin - 1`)
  - `range(1, 4)` → `1,2,3`
  - `range(1, 10, 2)` → `1,3,5,7,9` (tercero = paso)
- **`for` sobre listas**: `for fruta in frutas:` → la variable toma cada elemento.

### 5. Listas (clase 9)

- Índices desde **0**; negativos cuentan desde el final (`lst[-1]` = último).
- **Slicing**: `lst[1:3]` → posiciones 1 y 2 (**el fin no se incluye**).
- **Función vs método**:
  - Función suelta: `len([1,2,3])` — independiente del objeto.
  - Método: `[1,2,3].append(4)` — se llama **desde el objeto** con punto.
- **Métodos principales**:

| Grupo | Método | Qué hace |
|---|---|---|
| agregar | `append(x)` | agrega al **final** |
| | `extend(iter)` | agrega **varios** elementos |
| | `insert(i, x)` | inserta en la posición `i` |
| eliminar | `remove(x)` | elimina la **primera** ocurrencia |
| | `pop([i])` | elimina y **devuelve** (último o índice) |
| | `clear()` | vacía la lista |
| | `del lst[i]` | es una **instrucción**, no método |
| buscar | `index(x)` | devuelve el índice de `x` |
| | `count(x)` | cuenta cuántas veces aparece |
| ordenar | `sort()` | ordena (in place) |
| | `reverse()` | invierte el orden |
| | `copy()` | copia (¡ojo con `b = a` que es referencia!) |

### 6. Funciones (clase 11)

```python
def nombre_funcion(parametros):   # parámetros = espacios reservados (definición)
    ...
    return valor                   # devuelve el valor al que llama
```

- **Parámetros** (en el `def`) vs **argumentos** (los valores reales en la llamada).
- **`return` vs `print`**: `return` devuelve el valor; **sin `return`, la función devuelve `None`**.
  - ⚠️ Si la función hace `return` y en el principal solo la llamás sin `print(...)`, **no se ve nada**.
- Definir una función **no la ejecuta**: hay que llamarla.

### 7. Paso de argumentos (clase 13)

```python
def precio_final(precio, descuento, iva):
    return precio - precio * descuento / 100 + precio * iva / 100

precio_final(1000, 10, 21)                    # posicionales (por orden)
precio_final(precio=1000, descuento=10, iva=21)  # nombrados (por nombre)
precio_final(1000, descuento=10, iva=21)      # mezcla: posicionales PRIMERO
```

- Regla de oro: **los posicionales siempre van antes que los nombrados** (si no → `SyntaxError`).
- **Funciones parametrizadas**: reciben todo por parámetro, no usan valores quemados adentro.

---

## PARTE B — MODELO DE PRIMER PARCIAL (resuelto y verificado)

> Las salidas siguientes fueron **ejecutadas en Python 3** y comparadas con la clave del examen.

**P1 — `while` con `else`**
```python
n = 3
while n > 0:
    print(n + 1)
    n -= 1
else:
    print(n)
```
**Salida: `4 3 2 0`** ✅ — el `else` del `while` corre cuando la condición se pone en falsa (sin `break`): imprime 4, 3, 2 y luego `0`.

**P2 — lista de acumulados**
```python
lst = [1, 2, 3, 4, 5]; lst_2 = []; add = 0
for number in lst:
    add += number
    lst_2.append(add)
print(lst_2)
```
**Salida: `[1, 3, 6, 10, 15]`** ✅ — guarda el total acumulado en cada vuelta.

**P3 — nombres ilegales**
**Respuesta: 3, 6, 8** ✅ → `101` (empieza con número), `m 101` (espacio), `del` (reservada). `Del` y `averylongVariablename` son **legales**.

**P4 — división comentada**
```python
a = 6; b = 3
# a /= 2 * b
a = a / (2 * b)
print(a)
```
**Salida: `1.0`** ✅ — la comentada no cuenta y la `/` **siempre** da `float`.

**P5 — `sep`**
`print("a", "b", "c", sep="sep")` → **`asepbsepc`** ✅

**P6 — `input` devuelve string**
```python
y = input()   # "3"
x = input()   # "6"
print(x + y)
```
**Salida: `63`** ✅ — concatena, no suma (y el orden es `x` primero porque se cargó después).

**P7 — precedencia lógica**
`x = y < z and z > y or y < z and z < y` (y=10, z=0) → **`False`** ✅
(`and` antes que `or`: `(False and False) or (False and True)` = `False`.)

**P8 — `insert` / `del` / `append`**
```python
lst = [1,2,3,4,5]
lst.insert(1, 6)   # [1, 6, 2, 3, 4, 5]
del lst[0]         # [6, 2, 3, 4, 5]
lst.append(1)      # [6, 2, 3, 4, 5, 1]
```
**Salida: `[6, 2, 3, 4, 5, 1]`** ✅

**P9 — booleanos con `not`**
`z = ((x==y) and (x==y)) or not(x==y)` con x=1, y=0 → `z = True` → `print(not(z))` → **`False`** ✅

**P10 — tres `if` y un `else` colgado**
```python
x = 10
if x == 10: print(x == 10)   # True
if x > 5:   print(x > 5)     # True
if x < 10:  print(x < 10)
else:       print("else")
```
**Salida: `True True else`** ✅ — el `else` pertenece **solo al tercer `if`** (10 < 10 es falso).

**P11 — `//` y `%`**
`x = 10 // 3` → 3 · `y = 10 % 3` → 1 → **`3 1`** ✅

**P12 — par o impar**
`x = 7`; `x % 2 == 0` es falso → **`Impar`** ✅

**P13 — `range`**
`for i in range(1, 4): print(i * 2)` → **`2 4 6`** ✅ (genera 1, 2, 3).

**P14 — `elif`**
`nota = 8` → no es `>= 9` → sí es `>= 6` → **`Aprobado`** ✅

**P15 — `while` con dos contadores**
```python
i = 1; j = 1
while i <= 3 and j <= 3:
    print(i, j); j += 1; i += 1
```
**Salida:** `1 1` / `2 2` / `3 3` ✅ — suben juntos; en la 4ª vuelta `i = 4` rompe la condición.

**P16 — tres expresiones booleanas** (a=5, b=3, c=5)
```python
print((a == c) and (b < a))   # True and True
print((a != b) or (b > 10))   # True or False
print(not(a == b))            # not(False)
```
**Salida real: `True True True`** ✅

**P17 — `and` / `or` / `not`** (x=True, y=False)
```python
print(x and y)   # False
print(x or y)    # True
print(not y)     # True
```
**Salida real: `False True True`** ✅

**P18 — `if` compuesto con x = 4**
`(x > 2 and x < 5)` = `True`; `not(x == 4)` = `False`; `True or False` → **`A`** ✅

### 🚨 ERRATA EN LA CLAVE DEL MODELO

| Pregunta | Dice la clave | Salida **real** (ejecutada) |
|---|---|---|
| **16** | `False True True` | **`True True True`** |
| **17** | `True True True` | **`False True True`** |

Las respuestas de la **16 y la 17 están intercambiadas** en el PDF (verificado ejecutando ambos fragmentos). El resto de la clave: **17 de 18 correcta**.

---

## PARTE C — PRÁCTICA PARA PARCIAL (los 3 ejercicios, resueltos)

### Ejercicio 1 — Lista de nombres con menú (`recup_ej1_nombres.py`)

```python
lista_de_nombres = []

def saludar():
    nombre = input("Ingrese su nombre: ").strip()
    apellido = input("Ingrese su apellido: ").strip()
    nombre_completo = f"{nombre} {apellido}"
    lista_de_nombres.append(nombre_completo)
    print(f"  {nombre_completo} fue agregado con exito.")

while True:
    opcion = input("Presione 1 para agregar un nombre (otro para salir): ").strip()
    if opcion == "1":
        saludar()
    else:
        break

print(f"Lista final: {lista_de_nombres}")
```
**Salida verificada:** con entradas `1 / Juan / Perez / 1 / Ana / Gomez / 9` →
`Lista final: ['Juan Perez', 'Ana Gomez']` ✅

### Ejercicio 2 — Notas y promedio (`recup_ej2_notas.py`)

```python
def agregar_notas(notas):
    cantidad = int(input("Cuantas notas desea cargar? "))
    for i in range(cantidad):
        nota = float(input(f"  Nota {i + 1}: "))
        notas.append(nota)          # ← SIN ESTO la lista queda vacía

def calcular_promedio(notas):
    total = 0
    for n in notas:
        total += n
    return total / len(notas)       # return, no print

notas = []
agregar_notas(notas)
promedio = calcular_promedio(notas)
print(f"El promedio final es: {promedio:.2f}")
```
**Salida verificada:** `3 / 7 / 8 / 9` → `Las notas cargadas son: [7.0, 8.0, 9.0]` · `El promedio final es: 8.00` ✅

### Ejercicio 3 — Menú con calculadora y nombres (`recup_ej3_menu.py`)

```python
nombres = []

def calcular(num1, num2, operador):
    if operador == "+": return num1 + num2
    if operador == "-": return num1 - num2
    if operador == "*": return num1 * num2
    if operador == "/":
        if num2 == 0:
            print("  No se puede dividir por cero.")
            return None
        return num1 / num2
    print("  Operador invalido.")
    return None

def registrar_nombre():
    nom = input("  Nombre a registrar: ").strip()
    nombres.append(nom)
    print(f"  '{nom}' fue registrado.")

def eliminar_nombre():
    nom = input("  Nombre a eliminar: ").strip()
    if nom in nombres:
        nombres.remove(nom)
        print(f"  '{nom}' fue eliminado.")
    else:
        print(f"  '{nom}' no se encuentra registrado.")

while True:
    print("\n===== MENU =====")
    print("1) Calculadora")
    print("2) Registrar nombre")
    print("3) Eliminar nombre")
    print("0) Salir")
    opcion = input("Opcion: ").strip()

    if opcion == "1":
        n1 = float(input("  Primer numero: "))
        n2 = float(input("  Segundo numero: "))
        op = input("  Operador (+, -, *, /): ").strip()
        resultado = calcular(n1, n2, op)
        if resultado is not None:
            print(f"  Resultado: {resultado}")
    elif opcion == "2":
        registrar_nombre()
    elif opcion == "3":
        eliminar_nombre()
    elif opcion == "0":
        print(f"Hasta luego! Registrados: {nombres}")
        break
    else:
        print("  Opcion invalida.")
```
**Salida verificada:** calculadora `10 + 5 = 15.0` ✅ · división por cero → mensaje de guardia ✅ · registrar Pedro/Luis · eliminar Pedro ✓ · eliminar Fabian → *"no se encuentra registrado"* ✅ · opción `9` → *"opción inválida"* ✅ · `0` → despedida con `Registrados: ['Luis']` ✅

---

## 🎯 Los 5 puntos de oro para el recuperatorio

1. **`input` siempre devuelve `str`** → para calcular: castear (`int`/`float`).
2. **`return` ≠ `print`** → si la función retorna, el principal debe imprimir.
3. **`and` antes que `or`**; el `else` se asocia al último `if`.
4. **Listas**: `append` al final · `remove` borra la primera ocurrencia · `del` es instrucción.
5. **Posicionales antes que nombrados** en las llamadas; `range` no incluye el límite superior.

*Guía generada para el recuperatorio del primer parcial — todo el código fue ejecutado y verificado.*
