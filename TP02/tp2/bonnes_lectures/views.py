from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from .models import Book

# Create your views here.
def about(request):
    return HttpResponse(" Application Bonnes Lectures, développée en TP de Framework Web, Université d’Orléans, 2024")

def welcome(request):
    return render(request, "bonnes_lectures/welcome.html")

def book(request , book_id ) :
    books = Book.objects.get(pk=book_id)
    return render(request, "bonnes_lectures/book.html",{"book" : books})

def bookBoard ( request ) :
    books = Book.objects.all()
    return render(request, "bonnes_lectures/Book_board.html",{"books" : books})