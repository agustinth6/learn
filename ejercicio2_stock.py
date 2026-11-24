"""
Ejercicio 2 - Modelo de Segundo Parcial
Tecnicas de Programacion - Python
Gestion de productos y stock
"""

# ===========================================================================
# Datos iniciales (entregados por el enunciado)
#   clave  -> nombre del producto (str)
#   valor -> lista de cantidades registradas en controles de stock (int)
#            [] = todavia sin registros  (caso borde: "Impresora")
# ===========================================================================
productos = {
    "Mouse": [10, 8, 12],
    "Teclado": [5, 7, 6],
    "Monitor": [3, 4, 2],
    "Impresora": [],
}


# --------------------------------------------------------------------------
# 1) Agregar productos y cantidades  (mismo patron que el Ejercicio 1)
# --------------------------------------------------------------------------
def agregar_producto():
    """Pide los datos, los valida TODO y recien ahi muta el diccionario."""

    # --- a) Nombre: unicamente letras, sin espacios sobrantes --------------
    while True:
        nombre = input("Nombre del producto: ").strip()      # (1)
        if nombre == "":                                     # (2)
            print("  El nombre no puede quedar vacio.")
            continue
        if not nombre.isalpha():                             # (3)
            print("  El nombre debe contener unicamente letras.")
            continue
        break                                                # (4) nombre valido

    # --- b) El producto no debe existir todavia ----------------------------
    if nombre in productos:                                  # (5)
        print(f"  '{nombre}' ya esta cargado; no se repite.")
        return                                               # (6)

    # --- c) Cuantas cantidades quiere registrar? ---------------------------
    while True:
        try:
            cantidad = int(input("Cuantas cantidades desea registrar? "))  # (7)
            if cantidad <= 0:                                # (8)
                print("  Debe ser un entero mayor a cero.")
                continue
            break                                            # (9)
        except ValueError:                                   # (10)
            print("  Eso no es un numero entero. Intente de nuevo.")

    # --- d) Cada cantidad: numero ENTERO positivo --------------------------
    registros = []                                           # (11)
    while len(registros) < cantidad:                         # (12)
        try:
            cantidad_stock = int(input("  Cantidad %d: " % (len(registros) + 1)))  # (13)
            if cantidad_stock <= 0:                          # (14)
                print("  La cantidad debe ser un entero positivo.")
                continue
            registros.append(cantidad_stock)                 # (15)
        except ValueError:                                   # (16)
            print("  Eso no es un entero. Intente de nuevo.")

    # --- e) Recien AHORA se toca el diccionario ----------------------------
    productos[nombre] = registros                            # (17)
    print(f"  Producto '{nombre}' agregado con {cantidad} registro(s).")


# --------------------------------------------------------------------------
# 2) Opcion A: Calcular stock promedio  (la que elegi desarrollar)
# --------------------------------------------------------------------------
def calcular_stock_promedio(productos, nombre):
    """Promedio de las cantidades registradas de `nombre`.
    Retorna None (y avisa) si no existe o no tiene registros."""
    if nombre not in productos:                              # (1) existe?
        print(f"  El producto '{nombre}' no existe.")
        return None                                          # (2)
    registros = productos[nombre]                            # (3)
    if not registros:                                        # (4) lista vacia?
        print(f"  '{nombre}' no posee registros de stock.")
        return None                                          # (5)
    return sum(registros) / len(registros)                   # (6)


# --------------------------------------------------------------------------
# 2) Opcion B: Sumar stock total
#   (el parcial pide elegir UNA opcion; esta es practicamente identica
#    a la A, cambia solo la ultima linea y el mensaje)
# --------------------------------------------------------------------------
def sumar_stock_total(productos, nombre):
    """Suma de las cantidades registradas de `nombre`."""
    if nombre not in productos:
        print(f"  El producto '{nombre}' no existe.")
        return None
    registros = productos[nombre]
    if not registros:
        print(f"  '{nombre}' no posee registros de stock.")
        return None
    return sum(registros)


# --------------------------------------------------------------------------
# 3) Productos con stock promedio menor a 5 (LISTA POR COMPRENSION)
# --------------------------------------------------------------------------
def obtener_productos_bajo_stock(productos):
    """Nombres de productos con promedio < 5, excluyendo los sin registros."""
    return [
        nombre
        for nombre in productos
        # cortocircuito: si la lista esta vacia NO se llama a
        # calcular_stock_promedio (no calcula ni imprime de mas)
        if productos[nombre] and calcular_stock_promedio(productos, nombre) < 5
    ]


# --------------------------------------------------------------------------
# Programa principal (menu)
# --------------------------------------------------------------------------
def main():
    while True:
        print("\n===== PRODUCTOS Y STOCK =====")
        print("1) Agregar producto y cantidades")
        print("2) Stock promedio de un producto (Opcion A)")
        print("3) Suma total de stock de un producto (Opcion B)")
        print("4) Productos con stock promedio menor a 5")
        print("0) Salir")
        opcion = input("Opcion: ").strip()

        if opcion == "1":
            agregar_producto()
        elif opcion == "2":
            nom = input("Producto: ").strip()
            prom = calcular_stock_promedio(productos, nom)
            if prom is not None:                 # None no admite :.2f
                print(f"  Stock promedio de {nom}: {prom:.2f}")
        elif opcion == "3":
            nom = input("Producto: ").strip()
            total = sumar_stock_total(productos, nom)
            if total is not None:
                print(f"  Stock total de {nom}: {total}")
        elif opcion == "4":
            print(f"  Bajo stock: {obtener_productos_bajo_stock(productos)}")
        elif opcion == "0":
            print("Hasta luego!")
            break
        else:
            print("  Opcion invalida.")


if __name__ == "__main__":
    main()
