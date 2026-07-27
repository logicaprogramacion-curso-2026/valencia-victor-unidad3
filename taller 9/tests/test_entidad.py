import unittest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.entidad import Pregunta


class TestPregunta(unittest.TestCase):
    def setUp(self):
        self.p = Pregunta(1, "¿2+2?", "3", "4", "5", "6", "b", "Fácil", "Aritmética")

    def test_atributos(self):
        self.assertEqual(self.p.id, 1)
        self.assertEqual(self.p.respuesta_correcta, "B")

    def test_to_dict(self):
        d = self.p.to_dict()
        self.assertEqual(d["tema"], "Aritmética")
        self.assertEqual(d["opcion_b"], "4")

    def test_es_correcta(self):
        self.assertTrue(self.p.es_correcta("b"))
        self.assertFalse(self.p.es_correcta("A"))

    def test_obtener_opcion(self):
        self.assertEqual(self.p.obtener_opcion("C"), "5")


if __name__ == "__main__":
    unittest.main()
