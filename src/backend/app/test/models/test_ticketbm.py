import unittest
from backend.app.models.ticket import Ticket
from backend.app.logic.universal_controller_sqlserver import UniversalController

class TestTicket(unittest.TestCase):
    def setUp(self):
        """
        Configuración inicial para las pruebas.
        """
        self.controller = UniversalController()
        self.ticket = Ticket(ID=9999, EstadoIncidencia="Pendiente")

        # Agregar el ticket de prueba a la base de datos
        self.controller.add(self.ticket)

    def tearDown(self):
        """
        Limpieza después de cada prueba.
        """
        # Eliminar el ticket de prueba de la base de datos
        self.controller.delete(self.ticket)

    def test_initialization(self):
        """
        Prueba la inicialización del modelo Ticket.
        """
        self.assertEqual(self.ticket.ID, 9999)
        self.assertEqual(self.ticket.EstadoIncidencia, "Pendiente")

    def test_to_dict(self):
        """
        Prueba la conversión del modelo Ticket a un diccionario.
        """
        ticket_dict = self.ticket.to_dict()
        self.assertEqual(ticket_dict["ID"], 9999)
        self.assertEqual(ticket_dict["EstadoIncidencia"], "Pendiente")

    def test_get_fields(self):
        """
        Prueba la obtención de los campos del modelo Ticket.
        """
        fields = Ticket.get_fields()
        self.assertIn("ID", fields)
        self.assertIn("EstadoIncidencia", fields)

if __name__ == "__main__":
    unittest.main()