from django.forms import ModelForm
from bonnes_lectures.models import *


class BookForm (ModelForm) :
    class Meta :
        model = Book
        fields = ["title" , "publisher" , "year", "ISBN", "backCover", "cover"]

class ReviewForm (ModelForm) :
    class Meta :
        model = Review
        fields = ["review" , "text"]