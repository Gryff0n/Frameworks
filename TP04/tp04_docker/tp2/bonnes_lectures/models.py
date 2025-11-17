from django.db import models
from django.core.validators import *
from django.contrib.auth.models import User


class Author(models.Model):
    prenom = models.CharField(max_length=255)
    nom = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="authors")

    def __str__(self):
        return f"{self.prenom} {self.nom}"


class Book(models.Model):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author, related_name="livres")
    publisher = models.CharField(max_length=255)
    year = models.IntegerField()
    ISBN = models.IntegerField()
    backCover = models.CharField()
    cover = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="books")

    def __str__(self):
        return f"{self.title}"



class Review(models.Model):
  date = models.DateField(auto_now_add=True)
  text = models.CharField()
  review = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
  book = models.ForeignKey (Book , on_delete=models.CASCADE, related_name="reviews")
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
