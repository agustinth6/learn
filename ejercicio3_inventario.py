"""
Ejercicio 3 - Modelo de Segundo Parcial
Tecnicas de Programacion - Python
Gestion de productos y precios  ->  DICCIONARIO ANIDADO
"""

# ===========================================================================
# Datos iniciales (entregados por el enunciado)
#   clave  -> nombre del producto (str)
#   valor -> OTRO diccionario con tres campos:
#              "precio"    -> numero positivo
#              "stock"     -> entero >= 0  (el cero SI se permite)
#              "categoria" -> texto
# ===========================================================================
inventario = {
    "Mouse": {"precio": 15000, "stock": 10, "categoria": "Perifericos"},
    "Teclado": {"precio": 25000, "stock": 5, "categoria": "Perifericos"},
    "Monitor": {"precio": 180000, "stock": 3, "categoria": "Pantallas"},
    "Impresora": {"precio": 95000, "stock": 0, "categoria": "Impresion"},
}


# --------------------------------------------------------------------------
# 1) Agregar productos
# --------------------------------------------------------------------------
def agregar_producto():
    """Pide nombre, precio, stock y categoria; valida TODO;
    recien ahi crea un diccionario nuevo dentro del inventario."""

    # --- a) Nombre: unicamente letras, sin espacios sobrantes --------------
    while True:
        nombre = input("Nombre del producto: ").strip()      # (1)
        if nombre == "":                                     # (2)
            print("  El nombre no puede quedar vacio.")
            continue
        if not nombre.isalpha():                             # (3)
            print("  El nombre debe contener unicamente letras.")
            continue
        break                                                # (4)

    # --- b) No debe existir todavia ----------------------------------------
    if nombre in inventario:                                 # (5)
        print(f"  '{nombre}' ya esta cargado; no se repite.")
        return                                               # (6)

    # --- c) Precio: numero POSITIVO (acepta decimales) ---------------------
    while True:
        try:
            precio = float(input("Precio: "))                # (7)
            if precio <= 0:                                  # (8)
                print("  El precio debe ser un numero positivo.")
                continue
            break
        except ValueError:                                   # (9)
            print("  Eso no es un numero. Intente de nuevo.")

    # --- d) Stock: entero MAYOR O IGUAL A cero (el 0 SI vale) --------------
    while True:
        try:
            stock = int(input("Stock inicial: "))            # (10)
            if stock < 0:                                    # (11) ojo: < 0, no <= 0
                print("  El stock debe ser un entero mayor o igual a cero.")
                continue
            break
        except ValueError:                                   # (12)
            print("  Eso no es un numero entero. Intente de nuevo.")

    # --- e) Categoria: texto no vacio ---------------------------------------
    while True:
        categoria = input("Categoria: ").strip()             # (13)
        if categoria == "":                                  # (14)
            print("  La categoria no puede quedar vacia.")
            continue
        break

    # --- f) Recien AHORA se muta el inventario ------------------------------
    #     Se CREA un diccionario nuevo con los tres campos y se asigna
    #     como valor de la clave `nombre`.
    inventario[nombre] = {                                   # (15)
        "precio": precio,                                    # (16)
        "stock": stock,                                      # (17)
        "categoria": categoria,                              # (18)
    }                                                        # (19)
    print(f"  Producto '{nombre}' agregado al inventario.")


# --------------------------------------------------------------------------
# 2) Consultar producto
# --------------------------------------------------------------------------
def consultar_producto(inventario, nombre):
    """Muestra precio, stock y categoria. Avisa si no existe."""
    if nombre not in inventario:                             # (1) existe?
        print(f"  El producto '{nombre}' no existe.")
        return                                               # (2)
    producto = inventario[nombre]                            # (3) diccionario INTERNO
    print(f"  Producto  : {nombre}")
    print(f"  Precio    : {producto['precio']}")             # (4) dos saltos de clave
    print(f"  Stock     : {producto['stock']}")
    print(f"  Categoria : {producto['categoria']}")


# --------------------------------------------------------------------------
# 3) Valor total del inventario  (precio x stock, sumado)
# --------------------------------------------------------------------------
def calcular_valor_inventario(inventario):
    total = 0                                                # (1) acumulador
    for nombre, producto in inventario.items():              # (2) clave, valor
        valor = producto["precio"] * producto["stock"]       # (3) precio x stock
        total = total + valor                                # (4) suma al total
    return total                                             # (5)


# --------------------------------------------------------------------------
# 4) Filtrar productos por categoria (LISTA POR COMPRENSION)
# --------------------------------------------------------------------------
def filtrar_por_categoria(inventario, categoria):
    """Nombres de los productos cuya categoria coincida exactamente."""
    return [
        nombre
        for nombre in inventario
        if inventario[nombre]["categoria"] == categoria      # exacto, sin ignorar mayusculas
    ]


# --------------------------------------------------------------------------
# 5) Productos sin stock (LISTA POR COMPRENSION)
# --------------------------------------------------------------------------
def productos_sin_stock(inventario):
    """Nombres de los productos cuyo stock sea exactamente 0."""
    return [
        nombre
        for nombre in inventario
        if inventario[nombre]["stock"] == 0                  # cero, no negativo
    ]


# --------------------------------------------------------------------------
# Programa principal (menu)
# --------------------------------------------------------------------------
def main():
    while True:
        print("\n===== INVENTARIO =====")
        print("1) Agregar producto")
        print("2) Consultar producto")
        print("3) Valor total del inventario")
        print("4) Filtrar por categoria")
        print("5) Productos sin stock")
        print("0) Salir")
        opcion = input("Opcion: ").strip()

        if opcion == "1":
            agregar_producto()
        elif opcion == "2":
            consultar_producto(inventario, input("Producto: ").strip())
        elif opcion == "3":
            print(f"  Valor total: {calcular_valor_inventario(inventario)}")
        elif opcion == "4":
            cat = input("Categoria: ").strip()
            print(f"  Productos: {filtrar_por_categoria(inventario, cat)}")
        elif opcion == "5":
            print(f"  Sin stock: {productos_sin_stock(inventario)}")
        elif opcion == "0":
            print("Hasta luego!")
            break
        else:
            print("  Opcion invalida.")


if __name__ == "__main__":
    main()
