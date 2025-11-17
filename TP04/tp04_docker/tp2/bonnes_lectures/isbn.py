from django.core.exceptions import ValidationError

class Isbn:
    """
    Représente un ISBN-13 découpé en parties.
    Ex : 978-2-1234-5680-3
    """
    def __init__(self, prefix, registration_group, registrant, publication, check_digit):
        self.prefix = prefix
        self.registration_group = registration_group
        self.registrant = registrant
        self.publication = publication
        self.check_digit = check_digit


    @staticmethod
    def validate_isbn13(isbn_digits):
        """
        isbn_digits = liste de 13 chiffres sous forme de string
        """
        if len(isbn_digits) != 13 or not isbn_digits.isdigit():
            raise ValidationError("ISBN doit contenir 13 chiffres")

        total = 0
        for i, digit in enumerate(isbn_digits[:-1]): 
            weight = 1 if i % 2 == 0 else 3
            total += weight * int(digit)

        calculated = (10 - (total % 10)) % 10

        if calculated != int(isbn_digits[-1]):
            raise ValidationError(f"ISBN invalide : chiffre de contrôle incorrect.")


    @classmethod
    def from_string(cls, text):
        """
        Transforme "9782123456803" ou "978-2-1234-5680-3"
        en objet Isbn
        """
        digits = "".join(filter(str.isdigit, text))
        cls.validate_isbn13(digits)

        return cls(
            prefix=digits[0:3],
            registration_group=digits[3],
            registrant=digits[4:8],
            publication=digits[8:12],
            check_digit=digits[12],
        )

    def __str__(self):
        return f"{self.prefix}-{self.registration_group}-{self.registrant}-{self.publication}-{self.check_digit}"

    def to_int(self):
        return int(f"{self.prefix}{self.registration_group}{self.registrant}{self.publication}{self.check_digit}")
