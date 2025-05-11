import unittest
from backend.app.models.routes import Route

class TestRouteModel(unittest.TestCase):
    def setUp(self):
        """
        Configuración inicial para las pruebas.
        """
        self.route = Route(ID=1, IDHorario=10, Nombre="Ruta de prueba")

    def test_initialization(self):
        """
        Prueba la inicialización del modelo Route.
        """
        self.assertEqual(self.route.ID, 1)
        self.assertEqual(self.route.IDHorario, 10)
        self.assertEqual(self.route.Nombre, "Ruta de prueba")

    def test_to_dict(self):
        """
        Prueba la conversión del modelo Route a un diccionario.
        """
        route_dict = self.route.to_dict()
        self.assertEqual(route_dict["ID"], 1)
        self.assertEqual(route_dict["IDHorario"], 10)
        self.assertEqual(route_dict["Nombre"], "Ruta de prueba")

    def test_get_fields(self):
        """
        Prueba la obtención de los campos del modelo Route.
        """
        fields = Route.get_fields()
        self.assertIn("ID", fields)
        self.assertIn("IDHorario", fields)
        self.assertIn("Nombre", fields)

if __name__ == "__main__":
    unittest.main()