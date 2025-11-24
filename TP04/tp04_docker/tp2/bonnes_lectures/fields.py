from django.db import models
from django.core.exceptions import ValidationError
from .isbn import Isbn

class IsbnField(models.CharField):

    description = "Champ ISBN avec validation ISBN-13"

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 17  
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if isinstance(value, Isbn):
            return value
        if value is None:
            return None
        return Isbn.from_string(value)

    def get_prep_value(self, value):
        """
        Valeur stockée en base = string compactée
        """
        if isinstance(value, Isbn):
            return str(value).replace("-", "")
        return value

    def validate(self, value, model_instance):
        """
        Appelle le validateur Isbn.validate_isbn13
        """
        super().validate(value, model_instance)
        if isinstance(value, Isbn):
            Isbn.validate_isbn13(value.to_int().__str__())
        else:
            Isbn.validate_isbn13(str(value))

    def to_python(self, value):
        if isinstance(value, str):
            return value 
        if isinstance(value, Isbn):
            return str(value)
        if value is None:
            return None
        return str(Isbn.from_string(value)) 

    def get_prep_value(self, value):
        if isinstance(value, Isbn):
            return str(value).replace("-", "")
        return value