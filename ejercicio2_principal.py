"""
Ejercicio 2 - archivo PRINCIPAL (el que se ejecuta).
Trae las funciones y el diccionario de ejercicio2_stock.py
y arma el menu.  Ejecutar con:  python ejercicio2_principal.py
"""
from ejercicio2_stock import (
    productos,
    agregar_producto,
    calcular_stock_promedio,
    sumar_stock_total,
    obtener_productos_bajo_stock,
)


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
            if prom is not None:
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
