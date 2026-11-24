from estudiantes import agregar_estudiante, calcular_promedio

# ❌ CLASICO: principal define SU PROPIA copia del diccionario
estudiantes = {
    "Ana": [9.5, 9.2, 8.8],
    "Carlos": [],
}

print("--- OPCION 1: agregar ---")
agregar_estudiante()
print("[principal.py] el diccionario que YO veo:", estudiantes)
print("--- OPCION 2: promedio de Pedro ---")
print("[principal.py] resultado:", calcular_promedio(estudiantes, "Pedro"))
