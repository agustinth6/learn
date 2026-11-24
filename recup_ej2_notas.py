"""
PRIMER PARCIAL - Practica, Ejercicio 2
Carga de notas y promedio en funciones separadas.
"""


def agregar_notas(notas):
    """Carga N notas en la lista recibida por parametro."""
    while True:
        try:
            cantidad = int(input("Cuantas notas desea cargar? "))
            if cantidad <= 0:
                print("  Debe ser un entero mayor a cero.")
                continue
            break
        except ValueError:
            print("  Eso no es un numero entero.")

    for i in range(cantidad):
        while True:
            try:
                nota = float(input(f"  Nota {i + 1}: "))
                notas.append(nota)      # <-- SIN ESTO la lista queda vacia
                break
            except ValueError:
                print("  Eso no es un numero.")


def calcular_promedio(notas):
    """Recorre la lista con for, suma y RETORNA el promedio."""
    total = 0
    for n in notas:
        total += n
    return total / len(notas)


# programa principal
notas = []
agregar_notas(notas)
promedio = calcular_promedio(notas)
print(f"Las notas cargadas son: {notas}")
print(f"El promedio final es: {promedio:.2f}")
