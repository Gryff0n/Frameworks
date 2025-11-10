from django.forms import ModelForm
from bonnes_lectures.models import *


class BookForm (ModelForm) :
    class Meta :
        model = Book
        fields = ["title" ,"author", "publisher" , "year", "ISBN", "backCover", "cover"]

class ReviewForm (ModelForm) :
    class Meta :
        model = Review
        fields = ["review" , "text"]

class AuthorForm (ModelForm) :
    class Meta :
        model = Author
        fields = ["prenom" , "nom"]