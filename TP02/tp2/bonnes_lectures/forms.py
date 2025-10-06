from django.forms import ModelForm
from bonnes_lectures.models import Book


class BookForm (ModelForm) :
    class Meta :
        model = Book
        fields = ["title" , "publisher" , "year", "ISBN", "backCover", "cover"]