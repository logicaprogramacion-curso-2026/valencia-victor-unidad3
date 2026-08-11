import unittest
import sys, os, tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.entidad import Pregunta
from src.dao import PreguntaDAO


class TestPreguntaDAO(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.tmp.close()
        self.dao = PreguntaDAO(self.tmp.name)
        self.p1 = Pregunta(1, "¿2+2?", "3", "4", "5", "6", "B", "Fácil", "Aritmética")
        self.p2 = Pregunta(2, "¿3*3?", "6", "9", "12", "3", "B", "Media", "Aritmética")

    def tearDown(self):
        os.unlink(self.tmp.name)

    def test_insertar_y_contar(self):
        self.dao.insertar(self.p1)
        self.assertEqual(self.dao.contar_preguntas(), 1)

    def test_insertar_muchas_y_obtener_todas(self):
        self.dao.insertar_muchas([self.p1, self.p2])
        self.assertEqual(len(self.dao.obtener_todas()), 2)

    def test_obtener_por_id(self):
        self.dao.insertar(self.p1)
        p = self.dao.obtener_por_id(1)
        self.assertEqual(p.pregunta, "¿2+2?")

    def test_obtener_por_tema_y_dificultad(self):
        self.dao.insertar_muchas([self.p1, self.p2])
        self.assertEqual(len(self.dao.obtener_por_tema("Aritmética")), 2)
        self.assertEqual(len(self.dao.obtener_por_dificultad("Fácil")), 1)

    def test_actualizar(self):
        self.dao.insertar(self.p1)
        self.p1.pregunta = "Actualizada"
        self.dao.actualizar(self.p1)
        self.assertEqual(self.dao.obtener_por_id(1).pregunta, "Actualizada")

    def test_eliminar(self):
        self.dao.insertar(self.p1)
        self.dao.eliminar(1)
        self.assertIsNone(self.dao.obtener_por_id(1))

    def test_estadisticas(self):
        self.dao.insertar_muchas([self.p1, self.p2])
        self.assertEqual(self.dao.estadisticas_por_tema()["Aritmética"], 2)
        self.assertEqual(self.dao.estadisticas_por_dificultad()["Fácil"], 1)


if __name__ == "__main__":
    unittest.main()
