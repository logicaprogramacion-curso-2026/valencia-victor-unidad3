# -*- coding: utf-8 -*-
"""DAO para la entidad Pregunta usando SQLite."""
import sqlite3
import os

try:
    from src.entidad import Pregunta
except ImportError:
    from entidad import Pregunta


class PreguntaDAO:
    def __init__(self, ruta_db="database/preguntas.db"):
        os.makedirs(os.path.dirname(ruta_db) or ".", exist_ok=True)
        self.ruta_db = ruta_db
        self.crear_tabla()

    def _conectar(self):
        conn = sqlite3.connect(self.ruta_db)
        conn.row_factory = sqlite3.Row
        return conn

    def crear_tabla(self):
        with self._conectar() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS preguntas (
                    id INTEGER PRIMARY KEY,
                    pregunta TEXT NOT NULL,
                    opcion_a TEXT NOT NULL,
                    opcion_b TEXT NOT NULL,
                    opcion_c TEXT NOT NULL,
                    opcion_d TEXT NOT NULL,
                    respuesta_correcta TEXT NOT NULL,
                    dificultad TEXT NOT NULL,
                    tema TEXT NOT NULL
                )
            """)
            conn.commit()

    def insertar(self, pregunta):
        with self._conectar() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO preguntas
                (id, pregunta, opcion_a, opcion_b, opcion_c, opcion_d,
                 respuesta_correcta, dificultad, tema)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (pregunta.id, pregunta.pregunta, pregunta.opcion_a,
                  pregunta.opcion_b, pregunta.opcion_c, pregunta.opcion_d,
                  pregunta.respuesta_correcta, pregunta.dificultad, pregunta.tema))
            conn.commit()

    def insertar_muchas(self, preguntas):
        with self._conectar() as conn:
            conn.executemany("""
                INSERT OR REPLACE INTO preguntas
                (id, pregunta, opcion_a, opcion_b, opcion_c, opcion_d,
                 respuesta_correcta, dificultad, tema)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, [(p.id, p.pregunta, p.opcion_a, p.opcion_b, p.opcion_c,
                   p.opcion_d, p.respuesta_correcta, p.dificultad, p.tema)
                  for p in preguntas])
            conn.commit()

    def _fila_a_pregunta(self, fila):
        return Pregunta(fila["id"], fila["pregunta"], fila["opcion_a"],
                         fila["opcion_b"], fila["opcion_c"], fila["opcion_d"],
                         fila["respuesta_correcta"], fila["dificultad"], fila["tema"])

    def obtener_todas(self):
        with self._conectar() as conn:
            filas = conn.execute("SELECT * FROM preguntas ORDER BY id").fetchall()
            return [self._fila_a_pregunta(f) for f in filas]

    def obtener_por_id(self, id):
        with self._conectar() as conn:
            fila = conn.execute("SELECT * FROM preguntas WHERE id = ?", (id,)).fetchone()
            return self._fila_a_pregunta(fila) if fila else None

    def obtener_por_tema(self, tema):
        with self._conectar() as conn:
            filas = conn.execute("SELECT * FROM preguntas WHERE tema = ?", (tema,)).fetchall()
            return [self._fila_a_pregunta(f) for f in filas]

    def obtener_por_dificultad(self, dificultad):
        with self._conectar() as conn:
            filas = conn.execute("SELECT * FROM preguntas WHERE dificultad = ?", (dificultad,)).fetchall()
            return [self._fila_a_pregunta(f) for f in filas]

    def actualizar(self, pregunta):
        with self._conectar() as conn:
            conn.execute("""
                UPDATE preguntas SET pregunta=?, opcion_a=?, opcion_b=?, opcion_c=?,
                opcion_d=?, respuesta_correcta=?, dificultad=?, tema=? WHERE id=?
            """, (pregunta.pregunta, pregunta.opcion_a, pregunta.opcion_b,
                  pregunta.opcion_c, pregunta.opcion_d, pregunta.respuesta_correcta,
                  pregunta.dificultad, pregunta.tema, pregunta.id))
            conn.commit()

    def eliminar(self, id):
        with self._conectar() as conn:
            conn.execute("DELETE FROM preguntas WHERE id = ?", (id,))
            conn.commit()

    def contar_preguntas(self):
        with self._conectar() as conn:
            return conn.execute("SELECT COUNT(*) FROM preguntas").fetchone()[0]

    def estadisticas_por_tema(self):
        with self._conectar() as conn:
            filas = conn.execute("""
                SELECT tema, COUNT(*) as total FROM preguntas
                GROUP BY tema ORDER BY total DESC
            """).fetchall()
            return {f["tema"]: f["total"] for f in filas}

    def estadisticas_por_dificultad(self):
        with self._conectar() as conn:
            filas = conn.execute("""
                SELECT dificultad, COUNT(*) as total FROM preguntas
                GROUP BY dificultad ORDER BY total DESC
            """).fetchall()
            return {f["dificultad"]: f["total"] for f in filas}
