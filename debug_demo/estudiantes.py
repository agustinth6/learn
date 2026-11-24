# El UNICO diccionario del programa vive en ESTE archivo
estudiantes = {
    "Ana": [9.5, 9.2, 8.8],
    "Carlos": [],
}

def agregar_estudiante():
    nombre, notas = "Pedro", [8.0, 9.0]
    estudiantes[nombre] = notas          # muta el diccionario de ESTE archivo
    print("  [estudiantes.py] guarde. Mi diccionario:", estudiantes)

def calcular_promedio(dic, nombre):
    if nombre not in dic:
        print("  El estudiante '%s' no existe." % nombre)
        return None
    return sum(dic[nombre]) / len(dic[nombre])
