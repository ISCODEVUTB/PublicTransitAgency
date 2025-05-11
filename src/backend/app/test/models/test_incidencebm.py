import unittest
from backend.app.models.incidence import Incidence
from backend.app.logic.universal_controller_sqlserver import UniversalControllerSQLServer

class TestIncidence(unittest.TestCase):
    def setUp(self):
        """
        Configuración inicial para las pruebas.
        """
        self.controller = UniversalControllerSQLServer()
        self.incidencia = Incidence(ID=9999, IDTicket=1234, Descripcion="Prueba de incidencia", Tipo="Error", IDUnidad=5678)

        # Agregar la incidencia de prueba a la base de datos
        self.controller.add(self.incidencia)

    def tearDown(self):
        """
        Limpieza después de cada prueba.
        """
        # Eliminar la incidencia de prueba de la base de datos
        self.controller.delete(self.incidencia)

    def test_initialization(self):
        """
        Prueba la inicialización del modelo Incidence.
        """
        self.assertEqual(self.incidencia.ID, 9999)
        self.assertEqual(self.incidencia.IDTicket, 1234)
        self.assertEqual(self.incidencia.Descripcion, "Prueba de incidencia")
        self.assertEqual(self.incidencia.Tipo, "Error")
        self.assertEqual(self.incidencia.IDUnidad, 5678)

    def test_to_dict(self):
        """
        Prueba la conversión del modelo Incidence a un diccionario.
        """
        incidencia_dict = self.incidencia.to_dict()
        self.assertEqual(incidencia_dict["ID"], 9999)
        self.assertEqual(incidencia_dict["IDTicket"], 1234)
        self.assertEqual(incidencia_dict["Descripcion"], "Prueba de incidencia")
        self.assertEqual(incidencia_dict["Tipo"], "Error")
        self.assertEqual(incidencia_dict["IDUnidad"], 5678)

    def test_get_fields(self):
        """
        Prueba la obtención de los campos del modelo Incidence.
        """
        fields = Incidence.get_fields()
        self.assertIn("ID", fields)
        self.assertIn("IDTicket", fields)
        self.assertIn("Descripcion", fields)
        self.assertIn("Tipo", fields)
        self.assertIn("IDUnidad", fields)

if __name__ == "__main__":
    unittest.main()