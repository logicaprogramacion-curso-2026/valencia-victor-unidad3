# -*- coding: utf-8 -*-
"""Entidad Pregunta."""


class Pregunta:
    """Representa una pregunta de selección múltiple."""

    def __init__(self, id, pregunta, opcion_a, opcion_b, opcion_c, opcion_d,
                 respuesta_correcta, dificultad, tema):
        self.id = int(id)
        self.pregunta = pregunta
        self.opcion_a = opcion_a
        self.opcion_b = opcion_b
        self.opcion_c = opcion_c
        self.opcion_d = opcion_d
        self.respuesta_correcta = respuesta_correcta.strip().upper()
        self.dificultad = dificultad
        self.tema = tema

    def __str__(self):
        return (f"[{self.id}] ({self.tema} - {self.dificultad}) {self.pregunta}\n"
                f"  A) {self.opcion_a}\n"
                f"  B) {self.opcion_b}\n"
                f"  C) {self.opcion_c}\n"
                f"  D) {self.opcion_d}\n"
                f"  Respuesta correcta: {self.respuesta_correcta}")

    def __repr__(self):
        return f"Pregunta(id={self.id}, tema='{self.tema}')"

    def to_dict(self):
        return {
            "id": self.id,
            "pregunta": self.pregunta,
            "opcion_a": self.opcion_a,
            "opcion_b": self.opcion_b,
            "opcion_c": self.opcion_c,
            "opcion_d": self.opcion_d,
            "respuesta_correcta": self.respuesta_correcta,
            "dificultad": self.dificultad,
            "tema": self.tema,
        }

    @staticmethod
    def from_dict(d):
        return Pregunta(
            d["id"], d["pregunta"], d["opcion_a"], d["opcion_b"],
            d["opcion_c"], d["opcion_d"], d["respuesta_correcta"],
            d["dificultad"], d["tema"],
        )

    def obtener_opcion(self, letra):
        return {
            "A": self.opcion_a,
            "B": self.opcion_b,
            "C": self.opcion_c,
            "D": self.opcion_d,
        }.get(letra.strip().upper())

    def es_correcta(self, respuesta):
        return respuesta.strip().upper() == self.respuesta_correcta
