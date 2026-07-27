# -*- coding: utf-8 -*-
"""Simulador de evaluación de preguntas."""
import random
import json
import csv
import os
from datetime import datetime


class Simulador:
    def __init__(self, dao):
        self.dao = dao
        self.resultados = []
        self.puntaje = 0
        self.fecha_inicio = None

    def iniciar_simulacion(self, cantidad, entrada=input):
        todas = self.dao.obtener_todas()
        cantidad = min(cantidad, len(todas))
        seleccion = random.sample(todas, cantidad)

        self.resultados = []
        self.puntaje = 0
        self.fecha_inicio = datetime.now()

        for i, pregunta in enumerate(seleccion, 1):
            self.mostrar_pregunta(pregunta, i, cantidad)
            respuesta = entrada(f"Tu respuesta (A/B/C/D): ")
            correcta = self.validar_respuesta(pregunta, respuesta)
            if correcta:
                self.puntaje += 1
            self.resultados.append({
                "id": pregunta.id,
                "pregunta": pregunta.pregunta,
                "tema": pregunta.tema,
                "dificultad": pregunta.dificultad,
                "respuesta_usuario": respuesta.strip().upper(),
                "respuesta_correcta": pregunta.respuesta_correcta,
                "correcta": correcta,
            })
        return self.generar_reporte()

    def mostrar_pregunta(self, pregunta, numero=None, total=None):
        encabezado = f"Pregunta {numero}/{total}" if numero else "Pregunta"
        print(f"\n{encabezado} - [{pregunta.tema} | {pregunta.dificultad}]")
        print(pregunta.pregunta)
        print(f"A) {pregunta.opcion_a}")
        print(f"B) {pregunta.opcion_b}")
        print(f"C) {pregunta.opcion_c}")
        print(f"D) {pregunta.opcion_d}")

    def validar_respuesta(self, pregunta, respuesta):
        return pregunta.es_correcta(respuesta)

    def generar_reporte(self):
        total = len(self.resultados)
        correctas = sum(1 for r in self.resultados if r["correcta"])
        porcentaje = (correctas / total * 100) if total else 0

        por_tema = {}
        por_dificultad = {}
        for r in self.resultados:
            por_tema.setdefault(r["tema"], {"total": 0, "correctas": 0})
            por_tema[r["tema"]]["total"] += 1
            por_tema[r["tema"]]["correctas"] += 1 if r["correcta"] else 0

            por_dificultad.setdefault(r["dificultad"], {"total": 0, "correctas": 0})
            por_dificultad[r["dificultad"]]["total"] += 1
            por_dificultad[r["dificultad"]]["correctas"] += 1 if r["correcta"] else 0

        return {
            "fecha": self.fecha_inicio.strftime("%Y-%m-%d %H:%M:%S") if self.fecha_inicio else "",
            "total_preguntas": total,
            "respuestas_correctas": correctas,
            "puntaje": correctas,
            "porcentaje": round(porcentaje, 2),
            "detalle": self.resultados,
            "estadisticas_por_tema": por_tema,
            "estadisticas_por_dificultad": por_dificultad,
        }

    # ---------- GUARDADO DE RESULTADOS ----------

    def guardar_resultados_txt(self, reporte, ruta="resultados/respuestas_usuario.txt"):
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            f.write("REPORTE DE SIMULACIÓN\n")
            f.write(f"Fecha: {reporte['fecha']}\n")
            f.write(f"Puntaje: {reporte['puntaje']}/{reporte['total_preguntas']} "
                     f"({reporte['porcentaje']}%)\n")
            f.write("=" * 60 + "\n\n")
            for r in reporte["detalle"]:
                f.write(f"[{r['id']}] {r['pregunta']}\n")
                f.write(f"  Tema: {r['tema']} | Dificultad: {r['dificultad']}\n")
                f.write(f"  Tu respuesta: {r['respuesta_usuario']} | "
                         f"Correcta: {r['respuesta_correcta']} | "
                         f"{'CORRECTO' if r['correcta'] else 'INCORRECTO'}\n\n")
        return ruta

    def guardar_estadisticas_csv(self, reporte, ruta="resultados/estadisticas.csv"):
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            escritor.writerow(["Tipo", "Categoria", "Total", "Correctas", "Porcentaje"])
            for tema, datos in reporte["estadisticas_por_tema"].items():
                pct = round(datos["correctas"] / datos["total"] * 100, 2)
                escritor.writerow(["Tema", tema, datos["total"], datos["correctas"], pct])
            for dif, datos in reporte["estadisticas_por_dificultad"].items():
                pct = round(datos["correctas"] / datos["total"] * 100, 2)
                escritor.writerow(["Dificultad", dif, datos["total"], datos["correctas"], pct])
        return ruta

    def guardar_reporte_json(self, reporte, ruta="resultados/reporte.json"):
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(reporte, f, ensure_ascii=False, indent=2)
        return ruta
