"""
PRIMER PARCIAL - Practica, Ejercicio 1
Lista de nombres dinamica con funcion + menu while True.
"""

lista_de_nombres = []


def saludar():
    # pide nombre y apellido por separado
    nombre = input("Ingrese su nombre: ").strip()
    apellido = input("Ingrese su apellido: ").strip()

    # combina con un espacio en medio
    nombre_completo = f"{nombre} {apellido}"

    # agrega a la lista global
    lista_de_nombres.append(nombre_completo)

    # confirmacion con f-string
    print(f"  {nombre_completo} fue agregado con exito.")


# menu principal: 1 = agregar, cualquier otra cosa = salir
while True:
    opcion = input("Presione 1 para agregar un nombre (otro para salir): ").strip()
    if opcion == "1":
        saludar()
    else:
        break

# por ultimo: como queda la lista
print(f"Lista final: {lista_de_nombres}")
