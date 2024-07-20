class Contact:
    def __init__(self, phone_number, email, address=None):
        self.phone_number = phone_number
        self.email = email
        self.address = address

    def to_dict(self):
        return {
            "phone_number": self.phone_number,
            "email": self.email,
            "address": self.address
        }

    @staticmethod
    def from_dict(data):
        return Contact(data['phone_number'], data['email'], data.get('address'))