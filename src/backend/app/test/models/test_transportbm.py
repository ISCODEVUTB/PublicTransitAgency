import unittest
from backend.app.models.transport import Transport

class TestTransportModel(unittest.TestCase):
    def setUp(self):
        """
        Configuración inicial para las pruebas.
        """
        self.transport = Transport(ID=1, Ubicacion="Estación Central", Capacidad=50, IDRuta=1, IDTipo=2)

    def test_initialization(self):
        """
        Prueba la inicialización del modelo Transport.
        """
        self.assertEqual(self.transport.ID, 1)
        self.assertEqual(self.transport.Ubicacion, "Estación Central")
        self.assertEqual(self.transport.Capacidad, 50)
        self.assertEqual(self.transport.IDRuta, 1)
        self.assertEqual(self.transport.IDTipo, 2)

    def test_to_dict(self):
        """
        Prueba la conversión del modelo Transport a un diccionario.
        """
        transport_dict = self.transport.to_dict()
        self.assertEqual(transport_dict["ID"], 1)
        self.assertEqual(transport_dict["Ubicacion"], "Estación Central")
        self.assertEqual(transport_dict["Capacidad"], 50)
        self.assertEqual(transport_dict["IDRuta"], 1)
        self.assertEqual(transport_dict["IDTipo"], 2)

    def test_get_fields(self):
        """
        Prueba la obtención de los campos del modelo Transport.
        """
        fields = Transport.get_fields()
        self.assertIn("ID", fields)
        self.assertIn("Ubicacion", fields)
        self.assertIn("Capacidad", fields)
        self.assertIn("IDRuta", fields)
        self.assertIn("IDTipo", fields)

if __name__ == "__main__":
    unittest.main()