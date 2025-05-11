import unittest
from backend.app.models.stops import Parada
from backend.app.logic.universal_controller_sqlserver import UniversalController

class TestParada(unittest.TestCase):
    def setUp(self):
        """
        Configuración inicial para las pruebas.
        """
        self.controller = UniversalController()
        self.parada = Parada(ID=9999, Nombre="Parada Test", Ubicacion="Ubicación Test")

        # Agregar la parada de prueba a la base de datos
        self.controller.add(self.parada)

    def tearDown(self):
        """
        Limpieza después de cada prueba.
        """
        # Eliminar la parada de prueba de la base de datos
        self.controller.delete(self.parada)

    def test_initialization(self):
        """
        Prueba la inicialización del modelo Parada.
        """
        self.assertEqual(self.parada.ID, 9999)
        self.assertEqual(self.parada.Nombre, "Parada Test")
        self.assertEqual(self.parada.Ubicacion, "Ubicación Test")

    def test_to_dict(self):
        """
        Prueba la conversión del modelo Parada a un diccionario.
        """
        parada_dict = self.parada.to_dict()
        self.assertEqual(parada_dict["ID"], 9999)
        self.assertEqual(parada_dict["Nombre"], "Parada Test")
        self.assertEqual(parada_dict["Ubicacion"], "Ubicación Test")

    def test_get_fields(self):
        """
        Prueba la obtención de los campos del modelo Parada.
        """
        fields = Parada.get_fields()
        self.assertIn("ID", fields)
        self.assertIn("Nombre", fields)
        self.assertIn("Ubicacion", fields)

if __name__ == "__main__":
    unittest.main()