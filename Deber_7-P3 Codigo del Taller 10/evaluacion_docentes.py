carreras = {
    1: "Ingeniería en Sistemas",
    2: "Administración de Empresas",
    3: "Marketing"
}

docentes = {
    1: {1: "Juan Perez", 2: "Maria Lopez"},
    2: {1: "Carlos Ruiz", 2: "Ana Torres"},
    3: {1: "Pedro Vera", 2: "Lucia Mora"}
}

evaluaciones = {
    "Juan Perez": [8.5, 9.0, 7.5],
    "Maria Lopez": [9.5, 9.0, 10.0],
    "Carlos Ruiz": [7.0, 6.5, 8.0],
    "Ana Torres": [9.0, 8.5, 9.5],
    "Pedro Vera": [6.0, 7.0, 6.5],
    "Lucia Mora": [8.0, 8.5, 9.0]
}


def leer_opcion_entera(mensaje):
    while True:
        valor = input(mensaje).strip()
        if valor.isdigit():
            return int(valor)
        print("Entrada inválida, ingrese un número.")


def menu_carreras():
    respuesta = input("¿Desea seleccionar una carrera? (SI/NO): ").strip().upper()
    if respuesta != "SI":
        print("Regresando al menú de opciones")
        return

    print("===== CARRERAS DISPONIBLES =====")
    for i, nombre in carreras.items():
        print(f"{i}. {nombre}")

    indice_carrera = leer_opcion_entera("Seleccione el número de la carrera: ")
    if indice_carrera not in carreras:
        print("Carrera inválida")
        return

    print(f"===== DOCENTES DE {carreras[indice_carrera]} =====")
    for i, nombre in docentes[indice_carrera].items():
        print(f"{i}. {nombre}")

    respuesta_docente = input("¿Desea seleccionar un docente? (SI/NO): ").strip().upper()
    if respuesta_docente != "SI":
        print("Regresando al menú de opciones")
        return

    indice_docente = leer_opcion_entera("Seleccione el número del docente: ")
    if indice_docente not in docentes[indice_carrera]:
        print("Número de docente inválido")
        return

    nombre_docente = docentes[indice_carrera][indice_docente]
    print(f"Docente seleccionado: {nombre_docente}")


def menu_evaluaciones():
    while True:
        print("===== MOSTRAR EVALUACIONES =====")
        print("1. Mostrar evaluaciones al docente")
        print("2. Regresar")
        opcion_evaluacion = leer_opcion_entera("Ingrese una opción: ")

        if opcion_evaluacion == 1:
            nombre = input("Ingrese el nombre del docente: ").strip()
            if nombre in evaluaciones:
                notas = evaluaciones[nombre]
                promedio = sum(notas) / len(notas)
                print(f"Evaluaciones de {nombre}: {notas}")
                print(f"Promedio: {promedio:.2f}")
            else:
                print("Docente no encontrado")

            regresar = input("¿Desea regresar al submenú? (SI/NO): ").strip().upper()
            if regresar != "SI":
                break
        elif opcion_evaluacion == 2:
            print("Regresando al menú de opciones")
            break
        else:
            print("Opción no válida")


def main():
    print("Bienvenido al sistema de evaluación docente")

    while True:
        print("===== MENÚ DE OPCIONES =====")
        print("1. Especialidad / carrera")
        print("2. Mostrar evaluaciones")
        print("3. Salir")
        opcion = leer_opcion_entera("Ingrese una opción: ")

        if opcion == 1:
            menu_carreras()
        elif opcion == 2:
            menu_evaluaciones()
        elif opcion == 3:
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida")


if __name__ == "__main__":
    main()
