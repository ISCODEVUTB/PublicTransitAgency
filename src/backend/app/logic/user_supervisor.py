from user import User

class Supervisor(User):
    def __init__(self, id_user, type_identification,identification, name, email, password, role):
        super().__init__(id_user,type_identification,identification, name, email, password, role)
                
        if not self.verify_name(name):
            raise ValueError("Invalid Name")
        if not self.verify_email(email):
            raise ValueError("Invalid Email")
        if not self.verify_password(password):
            raise ValueError("Invalid Password")
    def get_driver_assigment(self, driver):
        """
        Purpose: Get information of driver's routes assigmented
        """
    def create_driver_assigment_report(self, driver):
        """
        Purpose: Create reports of driver's routes assigmented
        """
    def set_driver_assigment(self, driver):
        """
        Purpose: Actualize information of driver's routes assigmented
        """