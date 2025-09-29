from django.db import models

# Create your models here.
class Book(models.Model):
  title = models.CharField(max_length=255)
  publisher = models.CharField(max_length=255)
  year = models.IntegerField()
  ISBN=models.IntegerField()
  backCover = models.CharField()
  cover = models.BooleanField()