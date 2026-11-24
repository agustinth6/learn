"""
PRIMER PARCIAL - Practica, Ejercicio 3
Menu con calculadora, registro y eliminacion de nombres.
"""

nombres = []


def calcular(num1, num2, operador):
    """Devuelve el resultado de la operacion pedida."""
    if operador == "+":
        return num1 + num2
    if operador == "-":
        return num1 - num2
    if operador == "*":
        return num1 * num2
    if operador == "/":
        if num2 == 0:
            print("  No se puede dividir por cero.")
            return None
        return num1 / num2
    print("  Operador invalido (use +, -, * o /).")
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


# menu activo hasta la opcion 0
while True:
    print("\n===== MENU =====")
    print("1) Calculadora")
    print("2) Registrar nombre")
    print("3) Eliminar nombre")
    print("0) Salir")
    opcion = input("Opcion: ").strip()

    if opcion == "1":
        try:
            n1 = float(input("  Primer numero: "))
            n2 = float(input("  Segundo numero: "))
            op = input("  Operador (+, -, *, /): ").strip()
            resultado = calcular(n1, n2, op)
            if resultado is not None:
                print(f"  Resultado: {resultado}")
        except ValueError:
            print("  Eso no es un numero.")
    elif opcion == "2":
        registrar_nombre()
    elif opcion == "3":
        eliminar_nombre()
    elif opcion == "0":
        print(f"Hasta luego! Registrados: {nombres}")
        break
    else:
        print("  Opcion invalida.")
