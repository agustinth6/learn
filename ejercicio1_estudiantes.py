"""
Ejercicio 1 - Modelo de Segundo Parcial
Tecnicas de Programacion - Python
Gestion de estudiantes y notas
"""

# ===========================================================================
# Datos iniciales (entregados por el enunciado)
#   clave  -> nombre del estudiante (str)
#   valor -> lista de notas (list de float).  [] = todavia sin notas
# ===========================================================================
estudiantes = {
    "Ana": [9.5, 9.2, 8.8],
    "Luis": [7.0, 6.5, 7.2],
    "Marta": [6.0, 5.8, 6.2],
    "Carlos": [],
}


# --------------------------------------------------------------------------
# 1) Agregar estudiantes y notas
#     El enunciado la pide SIN parametros -> trabaja sobre la variable
#     global `estudiantes` (en la vida real la pasariamos como parametro).
# --------------------------------------------------------------------------
def agregar_estudiante():
    """Pide los datos al usuario, los valida TODO y recien ahi muta el diccionario."""

    # --- a) Nombre: unicamente letras, sin espacios sobrantes --------------
    while True:
        nombre = input("Nombre del estudiante: ").strip()   # (1) saca espacios
        if nombre == "":                                    # (2) quedo vacio?
            print("  El nombre no puede quedar vacio.")
            continue
        if not nombre.isalpha():                            # (3) solo letras?
            print("  El nombre debe contener unicamente letras.")
            continue
        break                                               # (4) nombre valido

    # --- b) El estudiante no debe existir todavia --------------------------
    if nombre in estudiantes:                               # (5) ya existe?
        print(f"  '{nombre}' ya esta cargado; no se repite.")
        return                                              # (6) corta aca

    # --- c) Cuantas notas quiere cargar? ----------------------------------
    while True:
        try:
            cantidad = int(input("Cuantas notas quiere ingresar? "))  # (7)
            if cantidad <= 0:                               # (8) entero positivo?
                print("  Debe ser un entero mayor a cero.")
                continue
            break                                           # (9) cantidad valida
        except ValueError:                                  # (10) int() fallo
            print("  Eso no es un numero entero. Intente de nuevo.")

    # --- d) Cada nota: numero positivo ------------------------------------
    notas = []                                              # (11) lista nueva
    while len(notas) < cantidad:                            # (12) faltan notas?
        try:
            nota = float(input("  Nota %d: " % (len(notas) + 1)))  # (13)
            if nota <= 0:                                   # (14) positiva?
                print("  La nota debe ser un numero positivo.")
                continue
            notas.append(nota)                              # (15) acumula
        except ValueError:                                  # (16) float() fallo
            print("  Eso no es un numero. Intente de nuevo.")

    # --- e) Recien AHORA se toca el diccionario ----------------------------
    estudiantes[nombre] = notas                             # (17) mutacion final
    print(f"  Estudiante '{nombre}' agregado con {cantidad} nota(s).")


# --------------------------------------------------------------------------
# 2) Calcular promedio
# --------------------------------------------------------------------------
def calcular_promedio(estudiantes, nombre):
    """Promedio de las notas de `nombre`.
    Retorna None (y avisa) si el estudiante no existe o no tiene notas."""
    if nombre not in estudiantes:                           # (1) existe?
        print(f"  El estudiante '{nombre}' no existe.")
        return None                                         # (2) senal de fallo
    notas = estudiantes[nombre]                             # (3) referencia
    if not notas:                                           # (4) lista vacia?
        print(f"  '{nombre}' no tiene notas cargadas.")
        return None                                         # (5) senal de fallo
    return sum(notas) / len(notas)                          # (6) division real


# --------------------------------------------------------------------------
# 3) Obtener el maximo promedio
# --------------------------------------------------------------------------
def obtener_maximo_promedio(estudiantes):
    """Retorna una tupla (nombre, promedio) del mejor promedio."""
    max_nombre = None
    max_promedio = None
    for nombre in estudiantes:
        promedio = calcular_promedio(estudiantes, nombre)
        if promedio is None:                                # sin notas -> salta
            continue
        # "None o ..." protege la primera vuelta: en Python 3 NO se puede
        # comparar None con un numero (TypeError).
        if max_promedio is None or promedio > max_promedio:
            max_nombre = nombre
            max_promedio = promedio
    return max_nombre, max_promedio


# --------------------------------------------------------------------------
# 4) Clasificar estudiante
#     OJO EL ORDEN: primero el umbral mas alto, si no nunca llegarias
#     a "Excelente" (Ana tambien cumple >= 7).
# --------------------------------------------------------------------------
def clasificar_estudiante(promedio):
    if promedio >= 9:
        return "Excelente"
    if promedio >= 7:                   # aca ya sabemos que es < 9
        return "Aprobado"
    return "Reprobado"


# --------------------------------------------------------------------------
# 5) Mostrar resumen (reutiliza 2 y 4)
# --------------------------------------------------------------------------
def mostrar_resumen(estudiantes, nombre):
    promedio = calcular_promedio(estudiantes, nombre)
    if promedio is None:                # ya se informo el motivo arriba
        return
    clasificacion = clasificar_estudiante(promedio)
    print(f"  Estudiante   : {nombre}")
    print(f"  Promedio     : {promedio:.2f}")
    print(f"  Clasificacion: {clasificacion}")


# --------------------------------------------------------------------------
# 6) Aprobados con LISTA POR COMPRENSION
#     Debe usar calcular_promedio() -> lo llamamos dentro del filtro.
#     `estudiantes[nombre] and ...` = cortocircuito: si la lista esta
#     vacia NO se llama a calcular_promedio (no calcula ni imprime de mas).
# --------------------------------------------------------------------------
def obtener_aprobados(estudiantes):
    return [
        nombre
        for nombre in estudiantes
        if estudiantes[nombre] and calcular_promedio(estudiantes, nombre) >= 7
    ]


# --------------------------------------------------------------------------
# Programa principal (menu minimo para que sea un "programa")
# --------------------------------------------------------------------------
def main():
    while True:
        print("\n===== ESTUDIANTES =====")
        print("1) Agregar estudiante y notas")
        print("2) Calcular promedio")
        print("3) Resumen (promedio + clasificacion)")
        print("4) Estudiante con maximo promedio")
        print("5) Lista de aprobados")
        print("0) Salir")
        opcion = input("Opcion: ").strip()

        if opcion == "1":
            agregar_estudiante()
        elif opcion == "2":
            nom = input("Nombre: ").strip()
            prom = calcular_promedio(estudiantes, nom)
            if prom is not None:
                print(f"  Promedio de {nom}: {prom:.2f}")
        elif opcion == "3":
            mostrar_resumen(estudiantes, input("Nombre: ").strip())
        elif opcion == "4":
            nom, prom = obtener_maximo_promedio(estudiantes)
            if prom is None:            # ojo: None no admite :.2f
                print("  No hay estudiantes con notas.")
            else:
                print(f"  Maximo promedio: {nom} ({prom:.2f})")
        elif opcion == "5":
            print(f"  Aprobados: {obtener_aprobados(estudiantes)}")
        elif opcion == "0":
            print("Hasta luego!")
            break
        else:
            print("  Opcion invalida.")


if __name__ == "__main__":
    main()
