

from time import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from .models import Book
from bonnes_lectures.forms import *

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

def newBook(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            newbook = form.save(commit=True)  # Pas de sauvegarde BD
            newbook.save()  # Sauvegarde en base de données
            return HttpResponseRedirect(f"/book/{newbook.id}")
    else:
        form = BookForm()  # Formulaire vide

    return render(request, "bonnes_lectures/BookForm.html", {"form": form})

def delete_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == "POST":
        book.delete()
        return redirect("bookBoard")

    return render(request, "bonnes_lectures/delete_book.html", {"book": book})

def edit_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        id = check_save(form)
        return redirect("book", book_id=id)
    else:
        form = BookForm(instance=book)

    return render(request, "bonnes_lectures/BookForm.html", {"form": form, "button_label": "Modifier"})

def check_save(form):
    if form.is_valid():
        message = form.save(commit=False)
        message.save()
        return message.id
