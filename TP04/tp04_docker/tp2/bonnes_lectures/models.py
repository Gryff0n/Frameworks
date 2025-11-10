from django.db import models
from django.core.validators import *


class Author(models.Model):
  prenom = models.CharField(max_length=255)
  nom = models.CharField(max_length=255)

  def __str__(self):
    return f"{self.prenom} {self.nom}"

# Create your models here.
class Book(models.Model):
  title = models.CharField(max_length=255)
  author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="livres", null=True)
  publisher = models.CharField(max_length=255)
  year = models.IntegerField()
  ISBN=models.IntegerField()
  backCover = models.CharField()
  cover = models.BooleanField()




class Review(models.Model):
  date = models.DateField(auto_now_add=True)
  text = models.CharField()
  review = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
  book = models.ForeignKey (Book , on_delete=models.CASCADE, related_name="reviews")