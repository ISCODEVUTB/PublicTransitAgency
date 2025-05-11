"""
import unittest
from backend.app.models.rutaparada import RutaParada
from backend.app.logic.universal_controller_sqlserver import UniversalController

class TestRutaParada(unittest.TestCase):
    def setUp(self):
        
        self.controller = UniversalController()
        self.rutaparada = RutaParada(IDParada=9999, IDRuta=8888)

        # Agregar la relación de prueba a la base de datos
        self.controller.add(self.rutaparada)

    def tearDown(self):
        
        # Eliminar la relación de prueba de la base de datos
        self.controller.delete(self.rutaparada)

    def test_initialization(self):
        
        self.assertEqual(self.rutaparada.IDParada, 9999)
        self.assertEqual(self.rutaparada.IDRuta, 8888)

    def test_to_dict(self):
        "
        rutaparada_dict = self.rutaparada.to_dict()
        self.assertEqual(rutaparada_dict["IDParada"], 9999)
        self.assertEqual(rutaparada_dict["IDRuta"], 8888)

    def test_get_fields(self):
        
        fields = RutaParada.get_fields()
        self.assertIn("IDParada", fields)
        self.assertIn("IDRuta", fields)

if __name__ == "__main__":
    unittest.main()
    """