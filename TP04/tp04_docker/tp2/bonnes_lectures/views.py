

from time import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from .models import *
from bonnes_lectures.forms import *

# Create your views here.
def about(request):
    return HttpResponse(" Application Bonnes Lectures, développée en TP de Framework Web, Université d’Orléans, 2024")

def welcome(request):
    return render(request, "bonnes_lectures/welcome.html")

def book(request , book_id ) :
    thebook = Book.objects.get(pk=book_id)
    return render(request, "bonnes_lectures/book.html",{"book" : thebook})

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

    return render(request, "bonnes_lectures/BookForm.html", {"form": form, "button_label": "Ajouter"})

def newReview(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            newreview = form.save(commit=False)  # Pas de sauvegarde BD
            newreview.book=book
            newreview.save()  # Sauvegarde en base de données
            return HttpResponseRedirect(f"/book/{book_id}")
    else:
        form = ReviewForm()  # Formulaire vide
    return render(request, "bonnes_lectures/ReviewForm.html", {"form": form, "button_label": "Ajouter", "book" : book})

def delete_review(request, book_id, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if request.method == "POST":
        review.delete()
        return redirect("book", book_id=book_id)

    return render(request, "bonnes_lectures/delete_review.html", {"book_id":book_id, "review": review})

def edit_review(request, book_id, review_id):
    review = get_object_or_404(Review, pk=review_id)
    book = get_object_or_404(Book, pk=book_id)
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            updated_review = form.save(commit=False)
            updated_review.book = book
            updated_review.save()
            return redirect("book", book_id=book.id)
    else:
        form = ReviewForm(instance=review)
    return render(request, "bonnes_lectures/ReviewForm.html", {"form": form, "button_label": "Modifier", "book" : book})

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

def author(request , author_id ) :
    theauthor = Author.objects.get(pk=author_id)
    return render(request, "bonnes_lectures/author.html",{"author" : theauthor})

def authorBoard ( request ) :
    authors = Author.objects.all()
    return render(request, "bonnes_lectures/Author_board.html",{"authors" : authors})

def newAuthor(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            newauthor = form.save(commit=False)  # Pas de sauvegarde BD
            newauthor.save()  # Sauvegarde en base de données
            return HttpResponseRedirect(f"/author/{newauthor.id}")
    else:
        form = AuthorForm()  # Formulaire vide

    return render(request, "bonnes_lectures/AuthorForm.html", {"form": form, "button_label": "Ajouter"})

def delete_author(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    if request.method == "POST":
        author.delete()
        return redirect("authorBoard")

    return render(request, "bonnes_lectures/delete_author.html", {"author": author})

def edit_author(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    if request.method == "POST":
        form = AuthorForm(request.POST, instance=author)
        id = check_save(form)
        return redirect("author", author_id=id)
    else:
        form = AuthorForm(instance=author)

    return render(request, "bonnes_lectures/AuthorForm.html", {"form": form, "button_label": "Modifier"})


def check_save(form):
    if form.is_valid():
        message = form.save(commit=False)
        message.save()
        return message.id
