"""
import unittest
from backend.app.models.payments import Payment

class TestPayment(unittest.TestCase):
    def setUp(self):
        self.payment = Payment(
            id=1,
            user="John Doe",
            payment_quantity=100.50,
            payment_method=True,
            vehicle_type=2,
            card_id=1234
        )

    def test_initialization(self):
        self.assertEqual(self.payment.id, 1)
        self.assertEqual(self.payment.user, "John Doe")
        self.assertEqual(self.payment.payment_quantity, 100.50)
        self.assertEqual(self.payment.payment_method, True)
        self.assertEqual(self.payment.vehicle_type, 2)
        self.assertEqual(self.payment.card_id, 1234)

    def test_to_dict(self):
        payment_dict = self.payment.to_dict()
        self.assertEqual(payment_dict["id"], 1)
        self.assertEqual(payment_dict["user"], "John Doe")
        self.assertEqual(payment_dict["payment_quantity"], 100.50)
        self.assertEqual(payment_dict["payment_method"], True)
        self.assertEqual(payment_dict["vehicle_type"], 2)
        self.assertEqual(payment_dict["card_id"], 1234)

    def test_get_fields(self):
        fields = Payment.get_fields()
        self.assertIn("id", fields)
        self.assertIn("user", fields)
        self.assertIn("payment_quantity", fields)
        self.assertIn("payment_method", fields)
        self.assertIn("vehicle_type", fields)
        self.assertIn("card_id", fields)

if __name__ == "__main__":
    unittest.main()
    """