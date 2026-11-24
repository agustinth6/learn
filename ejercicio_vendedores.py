"""
EJERCICIO - Gestion de vendedores y ventas (parcial)
5 puntos: alta valida (x2), total, destacados con comprension, principal.
"""

# ===========================================================================
# Datos iniciales (enunciado)
# ===========================================================================
ventas = {
    "Ana": [15000, 22000, 18000],
    "Luis": [30000, 25000],
    "Marta": [12000, 14000, 16000],
    "Carlos": [],
}


# ---------------------------------------------------------------------------
# 1) Agregar vendedores y sus ventas  (plantilla maestra, sin parametros)
# ---------------------------------------------------------------------------
def agregar_vendedor():
    # --- a) nombre: strip + vacio + solo letras ---
    while True:
        nombre = input("Nombre del vendedor: ").strip()
        if nombre == "":
            print("  El nombre no puede estar vacio.")
            continue
        if not nombre.isalpha():
            print("  El nombre debe contener unicamente letras.")
            continue
        break

    # --- b) que no exista previamente ---
    if nombre in ventas:
        print(f"  '{nombre}' ya esta registrado.")
        return

    # --- c) cuantas ventas quiere registrar? ---
    while True:
        try:
            cantidad = int(input("Cuantas ventas desea registrar? "))
            if cantidad <= 0:
                print("  Debe ser un entero mayor a cero.")
                continue
            break
        except ValueError:
            print("  Eso no es un numero entero. Intente de nuevo.")

    # --- d) cada importe: numero positivo ---
    importes = []
    while len(importes) < cantidad:
        try:
            importe = float(input("  Venta %d: " % (len(importes) + 1)))
            if importe <= 0:
                print("  El importe debe ser un numero positivo.")
                continue
            importes.append(importe)
        except ValueError:
            print("  Eso no es un numero. Intente de nuevo.")

    # --- e) recien AHORA se muta el diccionario ---
    ventas[nombre] = importes
    print(f"  Vendedor '{nombre}' agregado con {cantidad} venta(s).")


# ---------------------------------------------------------------------------
# 2) Agregar una venta a un vendedor existente  (recibe diccionario + nombre)
# ---------------------------------------------------------------------------
def agregar_venta(ventas, nombre):
    if nombre not in ventas:
        print(f"  El vendedor '{nombre}' no existe.")
        return

    while True:
        try:
            importe = float(input("Importe de la nueva venta: "))
            if importe <= 0:
                print("  El importe debe ser un numero positivo.")
                continue
            break
        except ValueError:
            print("  Eso no es un numero. Intente de nuevo.")

    ventas[nombre].append(importe)          # append, NUNCA update (pisaria la lista)
    print(f"  Venta registrada para '{nombre}'.")


# ---------------------------------------------------------------------------
# 3) Calcular el total de ventas de un vendedor  (Familia B: guardias + return)
# ---------------------------------------------------------------------------
def calcular_total_ventas(ventas, nombre):
    if nombre not in ventas:
        print(f"  El vendedor '{nombre}' no existe.")
        return None
    if not ventas[nombre]:
        print(f"  '{nombre}' no tiene ventas registradas.")
        return None
    return sum(ventas[nombre])


# ---------------------------------------------------------------------------
# 4) Vendedores destacados  (Familia C: comprension + guardia primero)
# ---------------------------------------------------------------------------
def obtener_vendedores_destacados(ventas, monto):
    return [
        nombre
        for nombre in ventas
        # cortocircuito: si la lista esta vacia NO se llama a la funcion
        if ventas[nombre] and calcular_total_ventas(ventas, nombre) > monto
    ]


# ---------------------------------------------------------------------------
# 5) Programa principal (menu de pruebas) + guard
# ---------------------------------------------------------------------------
def main():
    while True:
        print("\n===== VENDEDORES Y VENTAS =====")
        print("1) Agregar vendedor y ventas")
        print("2) Agregar una venta a un vendedor existente")
        print("3) Total de ventas de un vendedor")
        print("4) Vendedores destacados (monto)")
        print("0) Salir")
        opcion = input("Opcion: ").strip()

        if opcion == "1":
            agregar_vendedor()
        elif opcion == "2":
            nom = input("Vendedor: ").strip()
            agregar_venta(ventas, nom)
        elif opcion == "3":
            nom = input("Vendedor: ").strip()
            total = calcular_total_ventas(ventas, nom)
            if total is not None:                 # None no admite impresion rara
                print(f"  Total de {nom}: {total}")
        elif opcion == "4":
            try:
                monto = float(input("Monto: "))
                destacados = obtener_vendedores_destacados(ventas, monto)
                print(f"  Destacados: {destacados}")
            except ValueError:
                print("  Eso no es un numero.")
        elif opcion == "0":
            print("Hasta luego!")
            break
        else:
            print("  Opcion invalida.")


if __name__ == "__main__":
    main()
