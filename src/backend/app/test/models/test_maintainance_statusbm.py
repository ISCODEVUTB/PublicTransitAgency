import unittest
from backend.app.models.maintainance_status import MaintainanceStatus
from backend.app.logic.universal_controller_sqlserver import UniversalController

class TestMaintainanceStatus(unittest.TestCase):
    def setUp(self):
        """
        Configuración inicial para las pruebas.
        """
        self.controller = UniversalController()
        self.estado = MaintainanceStatus(ID=9999, TipoEstado="Prueba")

        # Agregar el estado de prueba a la base de datos
        self.controller.add(self.estado)

    def tearDown(self):
        """
        Limpieza después de cada prueba.
        """
        # Eliminar el estado de prueba de la base de datos
        self.controller.delete(self.estado)

    def test_initialization(self):
        """
        Prueba la inicialización del modelo MaintainanceStatus.
        """
        self.assertEqual(self.estado.ID, 9999)
        self.assertEqual(self.estado.TipoEstado, "Prueba")

    def test_to_dict(self):
        """
        Prueba la conversión del modelo MaintainanceStatus a un diccionario.
        """
        estado_dict = self.estado.to_dict()
        self.assertEqual(estado_dict["ID"], 9999)
        self.assertEqual(estado_dict["TipoEstado"], "Prueba")

    def test_get_fields(self):
        """
        Prueba la obtención de los campos del modelo MaintainanceStatus.
        """
        fields = MaintainanceStatus.get_fields()
        self.assertIn("ID", fields)
        self.assertIn("TipoEstado", fields)

if __name__ == "__main__":
    unittest.main()