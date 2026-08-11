# Sistema de Evaluación Docente – Pseudocódigo corregido

## Problemas encontrados en la versión original

1. **Comentarios usados como `Escribir`**: frases como *"Saludar al usuario y ofrecer opciones"* no son salidas reales para el usuario, son notas de diseño. Deben ir como comentario (`//`).
2. **Datos simulados con texto literal**: `Escribir "Mostrar docentes de la carrera seleccionada"` no muestra nada real. Se agregaron vectores de carreras y docentes para que la selección sea funcional.
3. **Variables sin declarar**: se agregó el bloque `Definir` con los tipos correspondientes.
4. **Submenú de evaluaciones sin repetición**: ahora usa su propio `Repetir...Hasta Que` para poder consultar varias veces sin salir al menú principal.
5. **Falta de opción "De Otro Modo"** en varios `Segun`/`Si`, agregada para manejar entradas inválidas de forma explícita.
6. **Tipos de dato mezclados**: `opcion` y `opcionEvaluacion` ahora son `Entero` de forma consistente en todo el algoritmo.

## Pseudocódigo corregido (PSeInt)

```
Algoritmo EvaluacionDocentes

    Definir opcion, opcionEvaluacion, i, indiceCarrera, indiceDocente Como Entero
    Definir respuesta, respuestaDocente, regresar Como Caracter
    Definir carreras(3) Como Caracter
    Definir docentes(3,2) Como Caracter

    // --- Datos de ejemplo (simulan una base de datos) ---
    carreras(1) <- "Ingeniería en Sistemas"
    carreras(2) <- "Administración de Empresas"
    carreras(3) <- "Marketing"

    docentes(1,1) <- "Juan Perez"
    docentes(1,2) <- "Maria Lopez"
    docentes(2,1) <- "Carlos Ruiz"
    docentes(2,2) <- "Ana Torres"
    docentes(3,1) <- "Pedro Vera"
    docentes(3,2) <- "Lucia Mora"

    Inicio
        Escribir "Bienvenido al sistema de evaluación docente"
        // Se saluda al usuario una sola vez al iniciar el programa

        Repetir
            Escribir "===== MENÚ DE OPCIONES ====="
            Escribir "1. Especialidad / carrera"
            Escribir "2. Mostrar evaluaciones"
            Escribir "3. Salir"
            Escribir "Ingrese una opción: "
            Leer opcion

            Segun opcion Hacer
                1:
                    Escribir "¿Desea seleccionar una carrera? (SI/NO)"
                    Leer respuesta
                    Si respuesta = "SI" Entonces
                        Escribir "===== CARRERAS DISPONIBLES ====="
                        Para i <- 1 Hasta 3 Con Paso 1 Hacer
                            Escribir i, ". ", carreras(i)
                        FinPara
                        Escribir "Seleccione el número de la carrera: "
                        Leer indiceCarrera

                        Si indiceCarrera >= 1 Y indiceCarrera <= 3 Entonces
                            Escribir "===== DOCENTES DE ", carreras(indiceCarrera), " ====="
                            Para i <- 1 Hasta 2 Con Paso 1 Hacer
                                Escribir i, ". ", docentes(indiceCarrera, i)
                            FinPara
                            Escribir "¿Desea seleccionar un docente? (SI/NO)"
                            Leer respuestaDocente

                            Si respuestaDocente = "SI" Entonces
                                Escribir "Seleccione el número del docente: "
                                Leer indiceDocente
                                Si indiceDocente >= 1 Y indiceDocente <= 2 Entonces
                                    Escribir "Docente seleccionado: ", docentes(indiceCarrera, indiceDocente)
                                SiNo
                                    Escribir "Número de docente inválido"
                                FinSi
                            SiNo
                                Escribir "Regresando al menú de opciones"
                            FinSi
                        SiNo
                            Escribir "Carrera inválida"
                        FinSi
                    SiNo
                        Escribir "Regresando al menú de opciones"
                    FinSi

                2:
                    Repetir
                        Escribir "===== MOSTRAR EVALUACIONES ====="
                        Escribir "1. Mostrar evaluaciones al docente"
                        Escribir "2. Regresar"
                        Leer opcionEvaluacion

                        Segun opcionEvaluacion Hacer
                            1:
                                Escribir "Mostrando evaluaciones al docente..."
                                Escribir "¿Desea regresar al submenú? (SI/NO)"
                                Leer regresar
                            2:
                                Escribir "Regresando al menú de opciones"
                            De Otro Modo:
                                Escribir "Opción no válida"
                        FinSegun
                    Hasta Que opcionEvaluacion = 2

                3:
                    Escribir "Saliendo del sistema..."

                De Otro Modo:
                    Escribir "Opción no válida"
            FinSegun

        Hasta Que opcion = 3
    Fin
FinAlgoritmo
```

## Notas de diseño

- Los vectores `carreras` y `docentes` son datos de ejemplo; en una versión real vendrían de una base de datos o archivo.
- El submenú de evaluaciones ahora tiene su propio ciclo, así que podés consultar evaluaciones de varios docentes sin volver al menú principal cada vez.
- Se validan los índices ingresados (`indiceCarrera`, `indiceDocente`) para evitar que el usuario seleccione una opción fuera de rango.
