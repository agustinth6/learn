# 📚 GUÍA DE ESTUDIO — Modelo de Segundo Parcial
### Técnicas de Programación · Python

> Guía de una sola lectura: el esqueleto común de los 3 ejercicios, las fórmulas,
> las trampas que se repiten y un checklist para rendir tranquilo.

---

## 1. EL ESQUELETO DE LOS 3 EJERCICIOS (todos son lo mismo)

```
DICCIONARIO GLOBAL  +  FUNCIONES QUE LEEN  +  UNA FUNCIÓN QUE ESCRIBE  +  main()
```

| Ejercicio | Clave | Valor (qué guarda) |
|---|---|---|
| **1. Estudiantes** | nombre | lista de notas (float) |
| **2. Stock** | producto | lista de cantidades (int) |
| **3. Inventario** | producto | **diccionario** `{precio, stock, categoria}` |

**Regla de oro #1:** solo **`agregar_*` muta** el diccionario, y **siempre al final**,
después de validar TODO. Las demás funciones solo leen.

**Regla de oro #2:** si el programa tiene dos archivos, el diccionario se define
**UNA sola vez** (en el archivo de funciones) y el principal lo **importa**:
`from funciones import *`. Definirlo en dos archivos = el bug *"agregué y no existe"*.

---

## 2. PLANTILLA MAESTRA DE VALIDACIÓN (la que hay que tener memorizada)

```python
def agregar_algo():
    # --- pedir hasta que sea válido ---
    while True:                       # bucle de reintento
        try:
            x = int(input("...: "))   # int() o float() según pida el enunciado
            if x <= 0:                # o < 0 si el cero está permitido
                print("invalido")
                continue              # vuelve a pedir (no sale del while)
            break                     # válido: sale del while
        except ValueError:            # entrada no numérica
            print("Eso no es un número. Intente de nuevo.")

    # ...validar todo lo demás (nombre, existencia, etc.)...

    # --- LA MUTACIÓN VA AL FINAL ---
    mi_diccionario[nuevo_clave] = valor
```

- `while True` + `break`/`continue` → repite hasta acertar.
- `try/except ValueError` → captura `int("abc")` y `float("caro")`.
- **`strip()` SIEMPRE antes de `isalpha()`** → `" Ana "` tiene espacios y fallaría.
- `nombre.isalpha()` → solo letras (acepta tildes y ñ; rechaza números y espacios).
- Verificar `if clave in diccionario:` → si ya existe, `return` **antes** de pedir más datos.

---

## 3. EJERCICIO 1 — Estudiantes y notas

**Funciones (6):**

1. `agregar_estudiante()` — valida nombre/cantidad/notas y guarda. Notas con **`float` > 0**.
2. `calcular_promedio(e, n)` → `sum(notas) / len(notas)`; si no existe o la lista está
   vacía → **imprime el motivo y retorna `None`**.
3. `obtener_maximo_promedio(e)` → recorre guardando el máximo; retorna **tupla**
   `(nombre, promedio)`. **Obligatorio:** `if max_promedio is None or promedio > max_promedio`
   (en Python 3, `None > float` = `TypeError`).
4. `clasificar_estudiante(p)` → **ORDEN IMPORTANTE:**
   ```python
   if p >= 9:  return "Excelente"   # primero el umbral más alto
   if p >= 7:  return "Aprobado"
   return "Reprobado"               # si no, nunca nadie es "Excelente"
   ```
5. `mostrar_resumen(e, n)` → llama a 2 y a 4; si el promedio es `None`, hace `return`
   antes de formatear (`f"{None:.2f}"` = `TypeError`).
6. `obtener_aprobados(e)` → comprensión usando `calcular_promedio()`:
   ```python
   return [n for n in estudiantes
           if estudiantes[n] and calcular_promedio(estudiantes, n) >= 7]
   ```
   (cortocircuito: lista vacía → no llama, no imprime de más)

**⚠️ ERRATA del enunciado:** dice que da `["Ana", "Luis"]`, pero
Luis promedia `(7.0 + 6.5 + 7.2) / 3 = 6.9` → **< 7** → el real es `["Ana"]`.
**Confío en la regla, no en el ejemplo.** (Ana: 9.17 → Excelente.)

---

## 4. EJERCICIO 2 — Productos y stock

**Datos:** igual al Ej 1 pero con enteros; `"Impresora": []` es el caso borde.

- **Punto 1 — `agregar_producto()`:** mismo esqueleto, pero cada registro es
  **`int` positivo** → `int("3.5")` = error (a diferencia de las notas del Ej 1).
- **Punto 2 — elegir UNA:**
  - **Opción A** `calcular_stock_promedio(p, n)` → `sum / len` (igual que promedio del Ej 1).
  - **Opción B** `sumar_stock_total(p, n)` → solo `sum(registros)`.
  - Las dos: `¿existe?` → `¿lista vacía?` → calcula. Si no → `print` + `return None`.
- **Punto 3 — `obtener_productos_bajo_stock(p)`:**
  ```python
  return [n for n in productos
          if productos[n] and calcular_stock_promedio(productos, n) < 5]
  ```
  - `< 5` **estricto** (4.99 sí, 5 no).
  - Excluir vacías **sin mensajes** → el guard `productos[n] and ...` va primero.
  - Ejemplo del enunciado `["Monitor"]` → **correcto** (verificado).
  - Si elegiste la Opción B: calculá el promedio adentro (`sum(...)/len(...) < 5`).

---

## 5. EJERCICIO 3 — Inventario ANIDADO

**Estructura = dos saltos de clave:**

```python
inventario["Mouse"]["precio"]        # 1er salto: producto → 2do: campo
producto = inventario[nombre]        # atajo: tomar el diccionario interno una vez
producto["stock"]
```

- **Punto 1 — `agregar_producto()`:** 3 datos a pedir y validar:
  - nombre: `strip()` + `isalpha()` + no repetido;
  - **precio: `float` > 0** (acepta decimales);
  - **stock: `int` ≥ 0** → el **cero SÍ vale** → chequeo `if stock < 0` (¡no `<= 0`!);
  - categoría: texto no vacío (sin try/except, no hay conversión);
  - guardar crea un **diccionario nuevo**:
    `inventario[nombre] = {"precio": p, "stock": s, "categoria": c}`
- **Punto 2 — `consultar_producto(inv, n)`:** `if n not in inventario` → informa;
  si existe → imprime precio, stock y categoría. Comillas: **simples adentro** del f-string:
  `f"{producto['precio']}"`.
- **Punto 3 — `calcular_valor_inventario(inv)`:**
  ```python
  total = 0
  for nombre, producto in inventario.items():      # .items() da (clave, valor)
      total += producto["precio"] * producto["stock"]
  return total                                     # con los datos: 815000
  ```
  Impresora (`stock 0`) aporta `0` → no rompe (acá **no se divide** nada).
- **Punto 4 — `filtrar_por_categoria(inv, cat)`:** comprensión con
  `inventario[nombre]["categoria"] == categoria` → **comparación exacta**
  (`"perifericos"` ≠ `"Perifericos"` → `[]`).
- **Punto 5 — `productos_sin_stock(inv)`:** comprensión con `["stock"] == 0`
  → con los datos: `["Impresora"]` ✅ (ejemplo correcto).

---

## 6. LAS 7 TRAMPAS QUE SE REPITEN

1. **`strip()` antes de `isalpha()`** (sino el nombre con espacios no pasa).
2. **Caso borde = lista/diccionario vacío** → siempre preguntarlo **antes** de dividir:
   `if not lista: print(...); return None` (evita `ZeroDivisionError`).
3. **`None` no se formatea** → `f"{None:.2f}"` = `TypeError`. Siempre:
   `if resultado is None: return` **antes** de imprimir con formato.
4. **Orden de los `if` de clasificación** → de mayor a menor (`>= 9` antes que `>= 7`).
5. **`float` vs `int` según el enunciado:** notas/precios → `float`;
   cantidades/stock → `int` (y `int("3.5")` falla a propósito).
6. **`> 0` vs `>= 0`:** notas/cantidad → positivo estricto; stock inicial del Ej 3 →
   **el cero vale**. Leé bien "mayor a cero" vs "mayor o igual a cero".
7. **Duplicar el diccionario en dos archivos** → el alta va a un lado y la consulta al
   otro. Un solo diccionario + `from archivo import *`.

---

## 7. CONCEPTOS DE PYTHON QUE CAEN GARANTIZADOS

- **Variable = etiqueta**, no caja. `b = a` apunta al **mismo objeto** (no copia).
- **Scope local vs global:** las variables de una función mueren al hacer `return`;
  la global vive siempre. `mi_dic[x] = y` (asignación a un elemento) usa la global
  sin necesidad de `global`; `mi_dic = {...}` (reasignar el nombre) sí la crearía local.
- **`return` entrega / `print` muestra.** `None` = "no tengo resultado".
- **Comprensión de lista:** `[x for x in coleccion if condicion]` → recorre, filtra
  y construye **una lista nueva** sin tocar el original.
- **Cortocircuito de `and`:** si la primera parte es falsa, la segunda **no se ejecuta**
  → sirve como guard: `if lista and calculo(...) < 5`.
- **`.items()`** → pares (clave, valor) para recorrer diccionarios.
- **Tupla + unpacking:** `nom, prom = obtener_maximo(...)`.
- **`if __name__ == "__main__": main()`** → solo corre el menú si ejecutás el archivo;
  si lo importan, solo carga las funciones (contar **2 guiones bajos** en cada lado).
- **`from archivo import *`** comparte el **mismo objeto** (por eso arregla el bug
  de los diccionarios duplicados).

---

## 8. ERRORES TÍPICOS (los que salieron en la práctica) → SOLUCIÓN

| Error | Causa | Solución |
|---|---|---|
| `TypeError: list.append() takes exactly one argument (0 given)` | `notas.append()` sin argumento | `notas.append(nota)` — siempre llevar el valor |
| `NameError: name 'estudiantes' is not defined` | falta el diccionario arriba del archivo | pegarlo **antes** del primer `def` |
| "Agregué y luego dice que no existe" | **dos copias** del diccionario (uno por archivo) | una sola definición en el de funciones + importar en el principal |
| El programa corre pero **no muestra nada** | falta/guarda mal el `if __name__ == "__main__":` o `main` sin `()` | últimas dos líneas: guard con 2+2 guiones bajos y `main()` con paréntesis; **Ctrl+S** |
| `ZeroDivisionError` | promedio con lista vacía | chequear `if not lista` antes de dividir |
| `TypeError: '<' not supported between 'NoneType' and 'float'` | comparar el candidato inicial `None` | `if maximo is None or x > maximo:` |
| El menú no aparece al importar otro archivo | código suelto sin guard | envolver en `def main()` + guard |

---

## 9. MÉTODO DE ATAQUE PARA EL PARCIAL (5 pasos)

1. **Identificar la estructura:** clave → ¿lista? (Ej 1-2) o ¿dict anidado? (Ej 3).
2. **Listar los casos borde ANTES de codear:** clave inexistente, lista vacía,
   entrada no numérica, negativo/cero, repetido.
3. **Separar leer de escribir:** solo `agregar_*` muta, y al final.
4. **Escribir el código** con la plantilla de validación (sección 2).
5. **Probar con 1 caso normal + 1 caso borde** y verificar el ejemplo del enunciado
   (si no cierra, **vale la regla, no el ejemplo** — Ej 1).

## 10. CHECKLIST ANTES DE ENTREGAR

- [ ] El diccionario está **una sola vez**, arriba de todo del archivo de funciones.
- [ ] `strip()` antes de `isalpha()` en todos los altas.
- [ ] Todo `input` numérico dentro de `try/except ValueError`.
- [ ] La mutación del diccionario es la **última línea** de `agregar_*`.
- [ ] Los casos borde retornan `None` **avisando**, y el llamador chequea `is None`
      antes de formatear.
- [ ] Las comprensiones tienen el guard de lista vacía **primero**.
- [ ] `clasificar_estudiante` pregunta `>= 9` **antes** que `>= 7`.
- [ ] `int` donde pide enteros, `float` donde pide números; `> 0` vs `>= 0` correcto.
- [ ] `main()` termina con `if __name__ == "__main__":` + `main()` en la columna 0.
- [ ] **Ctrl+S** antes de correr.

---

### 🧪 Datos de prueba oficiales (para verificar rápido)

```
Ej 1: Ana 9.17 (Excelente) · Luis 6.90 (Reprobado) · Marta 6.0 · Carlos sin notas
      max_promedio = ("Ana", 9.1666…) · aprobados = ["Ana"]   ← errata del enunciado
Ej 2: Mouse 10 · Teclado 6 · Monitor 3 · Impresora sin registros
      bajo stock < 5 = ["Monitor"]                            ← ejemplo correcto
Ej 3: valor total = 815000 · sin stock = ["Impresora"]        ← ejemplo correcto
      Perifericos = ["Mouse", "Teclado"]
```

*Archivos con las soluciones completas: `ejercicio1_estudiantes.py`,
`ejercicio2_stock.py`, `ejercicio2_principal.py`, `ejercicio3_inventario.py`.*
