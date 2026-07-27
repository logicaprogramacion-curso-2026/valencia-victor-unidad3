# -*- coding: utf-8 -*-
"""Gestor de preguntas: carga desde archivos, guarda en BD, exporta."""
import csv
import json
import re

try:
    from src.entidad import Pregunta
    from src.dao import PreguntaDAO
except ImportError:
    from entidad import Pregunta
    from dao import PreguntaDAO


class GestorPreguntas:
    def __init__(self, dao=None):
        self.dao = dao or PreguntaDAO()

    # ---------- CARGA ----------

    def cargar_desde_txt(self, ruta):
        preguntas = []
        with open(ruta, encoding="utf-8") as f:
            contenido = f.read()

        bloques = contenido.split("PREGUNTA #")[1:]
        for bloque in bloques:
            def buscar(patron, texto, defecto=""):
                m = re.search(patron, texto)
                return m.group(1).strip() if m else defecto

            id_ = buscar(r"^\s*\n.*?ID:\s*(\d+)", bloque) or buscar(r"ID:\s*(\d+)", bloque)
            tema = buscar(r"Tema:\s*(.+)", bloque)
            dificultad = buscar(r"Dificultad:\s*(.+)", bloque)
            enunciado = buscar(r"Enunciado:\s*(.+)", bloque)
            op_a = buscar(r"A\)\s*(.+)", bloque)
            op_b = buscar(r"B\)\s*(.+)", bloque)
            op_c = buscar(r"C\)\s*(.+)", bloque)
            op_d = buscar(r"D\)\s*(.+)", bloque)
            resp = buscar(r"Respuesta [Cc]orrecta:\s*([A-D])", bloque)

            if not (id_ and enunciado and resp):
                continue

            preguntas.append(Pregunta(
                int(id_), enunciado, op_a, op_b, op_c, op_d, resp, dificultad, tema
            ))
        return preguntas

    def cargar_desde_csv(self, ruta):
        preguntas = []
        with open(ruta, encoding="utf-8", newline="") as f:
            lector = csv.DictReader(f)
            for fila in lector:
                preguntas.append(Pregunta(
                    fila["ID"], fila["Pregunta"], fila["OpcionA"], fila["OpcionB"],
                    fila["OpcionC"], fila["OpcionD"], fila["RespuestaCorrecta"],
                    fila["Dificultad"], fila["Tema"]
                ))
        return preguntas

    def cargar_desde_json(self, ruta):
        with open(ruta, encoding="utf-8") as f:
            data = json.load(f)
        lista = data["cuestionario"]["preguntas"] if "cuestionario" in data else data
        preguntas = []
        for p in lista:
            opciones = p.get("opciones", {})
            preguntas.append(Pregunta(
                p["id"], p["pregunta"],
                opciones.get("A", p.get("opcion_a", "")),
                opciones.get("B", p.get("opcion_b", "")),
                opciones.get("C", p.get("opcion_c", "")),
                opciones.get("D", p.get("opcion_d", "")),
                p["respuesta_correcta"], p["dificultad"], p["tema"]
            ))
        return preguntas

    # ---------- BASE DE DATOS ----------

    def guardar_en_base_datos(self, preguntas):
        self.dao.insertar_muchas(preguntas)
        return self.dao.contar_preguntas()

    # ---------- EXPORTACIÓN ----------

    def exportar_a_txt(self, ruta, preguntas=None):
        preguntas = preguntas or self.dao.obtener_todas()
        with open(ruta, "w", encoding="utf-8") as f:
            f.write("=" * 80 + "\n")
            f.write("CUESTIONARIO DE PROGRAMACIÓN EN PYTHON\n")
            f.write(f"{len(preguntas)} PREGUNTAS DE SELECCIÓN MÚLTIPLE\n")
            f.write("=" * 80 + "\n\n")
            for p in preguntas:
                f.write(f"PREGUNTA #{p.id}\n")
                f.write("-" * 80 + "\n")
                f.write(f"ID: {p.id}\nTema: {p.tema}\nDificultad: {p.dificultad}\n")
                f.write(f"Enunciado: {p.pregunta}\n\nOpciones:\n")
                f.write(f"A) {p.opcion_a}\nB) {p.opcion_b}\nC) {p.opcion_c}\nD) {p.opcion_d}\n\n")
                f.write(f"Respuesta correcta: {p.respuesta_correcta}\n")
                f.write("=" * 80 + "\n\n")
        return ruta

    def exportar_a_csv(self, ruta, preguntas=None):
        preguntas = preguntas or self.dao.obtener_todas()
        with open(ruta, "w", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            escritor.writerow(["ID", "Pregunta", "OpcionA", "OpcionB", "OpcionC",
                                "OpcionD", "RespuestaCorrecta", "Dificultad", "Tema"])
            for p in preguntas:
                escritor.writerow([p.id, p.pregunta, p.opcion_a, p.opcion_b,
                                    p.opcion_c, p.opcion_d, p.respuesta_correcta,
                                    p.dificultad, p.tema])
        return ruta

    def exportar_a_json(self, ruta, preguntas=None):
        preguntas = preguntas or self.dao.obtener_todas()
        data = {
            "cuestionario": {
                "titulo": "Cuestionario de Programación en Python",
                "total_preguntas": len(preguntas),
                "preguntas": [
                    {
                        "id": p.id,
                        "pregunta": p.pregunta,
                        "opciones": {"A": p.opcion_a, "B": p.opcion_b,
                                     "C": p.opcion_c, "D": p.opcion_d},
                        "respuesta_correcta": p.respuesta_correcta,
                        "dificultad": p.dificultad,
                        "tema": p.tema,
                    } for p in preguntas
                ]
            }
        }
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return ruta
