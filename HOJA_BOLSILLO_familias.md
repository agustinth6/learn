# 📌 HOJA DE BOLSILLO — Las 5 familias de puntos del parcial

**Esqueleto de TODO el programa (lo que se repite en los 3 ejercicios):**
diccionario global → funciones que SOLO leen → UNA función que muta (siempre al final, después de validar) → `main()` + guard `if __name__ == "__main__":`

**Decodificador del enunciado (leé la consigna y clasificás el punto):**
- Dice **"agregar / registrar"** + requisitos de validación → Familia A
- Dice **"reciba como parámetros el diccionario"** y pide calcular/retornar/mostrar → Familia B
- Dice **"listas por comprensión"** → Familia C
- Te da **una tabla** y pide "retornar la clasificación" → Familia D
- Dice **"utilice las funciones anteriores"** → Familia E

---

## Familia A — ALTA con validación (LA PLANTILLA MAESTRA)

**Dónde:** Ej1 punto 1, Ej2 punto 1, Ej3 punto 1 (uno por ejercicio).
**Por qué:** es el único punto donde entra data cruda del teclado → es el único con `try/except`.

```python
def agregar_xxx():
    # 1) NOMBRE: SIEMPRE strip() antes de isalpha()
    while True:                          # bucle de reintento
        nombre = input("Nombre: ").strip()
        if nombre == "":
            print("No puede quedar vacio."); continue
        if not nombre.isalpha():
            print("Solo letras."); continue
        break                            # nombre valido: sale del while

    # 2) ¿YA EXISTE? → return ANTES de pedir el resto
    if nombre in diccionario:
        print("Ya existe."); return     # corta aca, no pide mas nada

    # 3) NUMEROS: un while True + try/except POR CADA requisito numerico
    while True:
        try:
            valor = int(input("...: "))  # int() o float() segun pida el enunciado
            if valor <= 0:               # o < 0 si el cero esta permitido (Ej3 stock)
                print("Invalido."); continue
            break                        # valor valido
        except ValueError:               # int("abc") / float("caro")
            print("Eso no es un numero. Intente de nuevo.")

    # ...el resto de validaciones... TODO ANTES de tocar el diccionario

    # 4) LA MUTACION VA AL FINAL (recien ahi se toca el diccionario)
    diccionario[nombre] = valor
    print("Agregado OK.")
```

**Variantes entre los tres (la unica diferencia real):**

- **Ej1:** pide *cuántas notas* → `while len(notas) < cantidad:` pidiendo floats `> 0` → `estudiantes[nombre] = notas`.
- **Ej2:** mismo molde, pero pide *cantidades* **enteras** `> 0` → `productos[nombre] = registros`.
- **Ej3:** **no** pide cantidad; pide precio (float `> 0`), stock (int **`>= 0`** → la condición mala es `if stock < 0`, NO `<= 0`) y categoría (texto no vacío, sin `isalpha`); la muta creando un **diccionario anidado**: `inventario[nombre] = {"precio":..., "stock":..., "categoria":...}`.

---

## Familia B — LECTURA con parámetros (guard + cálculo + return)

**Dónde:** Ej1 p2 `calcular_promedio`, Ej1 p3 `obtener_maximo_promedio`, Ej2 p2 (Opción A/B), Ej3 p2 `consultar_producto`, Ej3 p3 `calcular_valor_inventario`.
**Por qué NO hay try/except:** no hay `input()` — los datos llegan como parámetro ya convertido.

```python
def calcular_xxx(diccionario, nombre):
    if nombre not in diccionario:        # guardia 1: ¿existe?
        print("No existe."); return None
    datos = diccionario[nombre]
    if len(datos) == 0:                  # guardia 2: ¿sin registros?
        print("Sin datos."); return None
    # calculo y retorno
    return sum(datos) / len(datos)
```

- **Ej1 p3:** recorre todos, mantiene el maximo, retorna `(nombre, promedio)` — ojo con `Carlos: []` (no dividir por cero).
- **Ej3 p3:** no recibe nombre; recorre el inventario sumando `precio * stock` y retorna el total.

---

## Familia C — LISTAS POR COMPRENSIÓN (guardia PRIMERO)

**Dónde:** Ej1 p6 `obtener_aprobados`, Ej2 p3 `obtener_productos_bajo_stock`, Ej3 p4 `filtrar_por_categoria`, Ej3 p5 `productos_sin_stock`.

```python
# sin riesgo: condicion directa adentro de los corchetes
return [k for k in diccionario
        if diccionario[k]["categoria"] == "Perifericos"]

# CON riesgo (promedios / divisiones): filtrar ANTES, si no revienta con []
validos = [k for k in diccionario if len(diccionario[k]) > 0]
return [k for k in validos if calcular_promedio(diccionario, k) >= 7]
```

Regla: **la condicion/guardia siempre primero** (dentro de la comprension o filtrando antes).

---

## Familia D — FUNCIÓN PURA (tabla → if/elif)

**Dónde:** Ej1 p4 `clasificar_estudiante`. Ni diccionario, ni input, ni validacion.

```python
def clasificar(promedio):
    if promedio >= 9:
        return "Excelente"
    elif promedio >= 7:
        return "Aprobado"
    else:
        return "Reprobado"
```

---

## Familia E — ORQUESTADORA (llama a las anteriores)

**Dónde:** Ej1 p5 `mostrar_resumen`. No inventa nada: junta resultados y formatea.

```python
def mostrar_resumen(diccionario, nombre):
    prom = calcular_promedio(diccionario, nombre)
    if prom is None:                     # NUNCA imprimir None con :.2f
        return
    print(f"{nombre} - {prom:.2f} - {clasificar(prom)}")
```

---

## Recordatorios de ultimo minuto

- `None` **nunca** se formatea con `:.2f` → corta antes con `return`.
- `<5` es estricto; en Ej3 el stock `0` es **valido** (`< 0` es lo malo).
- `strip()` SIEMPRE antes de `isalpha()`.
- Comprension: guardia primero.
- `try/except ValueError` solo donde hay `input()` + `int()`/`float()`.
- La mutacion de la familia A: **validar TODO primero, mutar al final**.
- `def main()` + guard `if __name__ == "__main__": main()` al final del archivo.
