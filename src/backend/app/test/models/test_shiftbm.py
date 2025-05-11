import unittest
from backend.app.models.shift import Shift
from backend.app.logic.universal_controller_sqlserver import UniversalController

class TestShift(unittest.TestCase):
    def setUp(self):
        """
        Configuración inicial para las pruebas.
        """
        self.controller = UniversalController()
        self.shift = Shift(ID=9999, TipoTurno="Prueba")

        # Agregar el turno de prueba a la base de datos
        self.controller.add(self.shift)

    def tearDown(self):
        """
        Limpieza después de cada prueba.
        """
        # Eliminar el turno de prueba de la base de datos
        self.controller.delete(self.shift)

    def test_initialization(self):
        """
        Prueba la inicialización del modelo Shift.
        """
        self.assertEqual(self.shift.ID, 9999)
        self.assertEqual(self.shift.TipoTurno, "Prueba")

    def test_to_dict(self):
        """
        Prueba la conversión del modelo Shift a un diccionario.
        """
        shift_dict = self.shift.to_dict()
        self.assertEqual(shift_dict["ID"], 9999)
        self.assertEqual(shift_dict["TipoTurno"], "Prueba")

    def test_get_fields(self):
        """
        Prueba la obtención de los campos del modelo Shift.
        """
        fields = Shift.get_fields()
        self.assertIn("ID", fields)
        self.assertIn("TipoTurno", fields)

if __name__ == "__main__":
    unittest.main()