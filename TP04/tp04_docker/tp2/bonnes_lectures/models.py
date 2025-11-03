from django.db import models
from django.core.validators import *

# Create your models here.
class Book(models.Model):
  title = models.CharField(max_length=255)
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