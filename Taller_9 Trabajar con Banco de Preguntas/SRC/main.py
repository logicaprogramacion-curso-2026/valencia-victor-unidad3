# -*- coding: utf-8 -*-
"""Punto de entrada principal - Sistema de Banco de Preguntas."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.dao import PreguntaDAO
from src.gestor import GestorPreguntas
from src.simulador import Simulador

RUTA_TXT = "preguntas.txt"
RUTA_CSV = "preguntas.csv"
RUTA_JSON = "preguntas.json"


def menu():
    dao = PreguntaDAO("database/preguntas.db")
    gestor = GestorPreguntas(dao)

    while True:
        print("\n" + "=" * 50)
        print(" SISTEMA DE BANCO DE PREGUNTAS - PYTHON")
        print("=" * 50)
        print("1. Cargar preguntas desde archivo")
        print("2. Ver todas las preguntas")
        print("3. Ver estadísticas")
        print("4. Iniciar simulación")
        print("5. Exportar datos")
        print("6. Ver reportes")
        print("7. Salir")
        opcion = input("Elige una opción: ").strip()

        try:
            if opcion == "1":
                print("a) TXT  b) CSV  c) JSON")
                sub = input("Formato: ").strip().lower()
                if sub == "a":
                    preguntas = gestor.cargar_desde_txt(RUTA_TXT)
                elif sub == "b":
                    preguntas = gestor.cargar_desde_csv(RUTA_CSV)
                elif sub == "c":
                    preguntas = gestor.cargar_desde_json(RUTA_JSON)
                else:
                    print("Opción inválida.")
                    continue
                total = gestor.guardar_en_base_datos(preguntas)
                print(f"✅ {len(preguntas)} preguntas cargadas. Total en BD: {total}")

            elif opcion == "2":
                for p in dao.obtener_todas():
                    print(p, "\n")

            elif opcion == "3":
                print("Por tema:", dao.estadisticas_por_tema())
                print("Por dificultad:", dao.estadisticas_por_dificultad())

            elif opcion == "4":
                cantidad = int(input("¿Cuántas preguntas? "))
                sim = Simulador(dao)
                reporte = sim.iniciar_simulacion(cantidad)
                print(f"\nPuntaje: {reporte['puntaje']}/{reporte['total_preguntas']} "
                      f"({reporte['porcentaje']}%)")
                sim.guardar_resultados_txt(reporte)
                sim.guardar_estadisticas_csv(reporte)
                sim.guardar_reporte_json(reporte)
                print("✅ Resultados guardados en resultados/")

            elif opcion == "5":
                gestor.exportar_a_txt("resultados_exportados.txt")
                gestor.exportar_a_csv("resultados_exportados.csv")
                gestor.exportar_a_json("resultados_exportados.json")
                print("✅ Datos exportados desde la BD.")

            elif opcion == "6":
                for archivo in ["resultados/respuestas_usuario.txt",
                                "resultados/estadisticas.csv",
                                "resultados/reporte.json"]:
                    if os.path.exists(archivo):
                        print(f"\n--- {archivo} ---")
                        with open(archivo, encoding="utf-8") as f:
                            print(f.read()[:500])
                    else:
                        print(f"{archivo} no existe todavía.")

            elif opcion == "7":
                print("¡Hasta luego!")
                break
            else:
                print("Opción inválida.")
        except Exception as e:
            print(f"⚠️ Error: {e}")


if __name__ == "__main__":
    menu()
