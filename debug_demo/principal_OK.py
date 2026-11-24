from estudiantes import *   # trae las funciones Y el mismo diccionario (mismo objeto)

print("--- OPCION 1: agregar ---")
agregar_estudiante()
print("[principal.py] el diccionario que YO veo:", estudiantes)
print("--- OPCION 2: promedio de Pedro ---")
print("[principal.py] resultado:", calcular_promedio(estudiantes, "Pedro"))
