# from django.db import models

# # Create your models here.

# class Post(models.Model):
#     title = models.CharField(max_length=50)
#     text = models.TextField()
    
#     def __str__(self):
#         return self.text
    
from unittest.util import _MAX_LENGTH

from django.db import models

# Create your models here.

class Symptom(models.Model):
    #id = models.BigIntegerField()
    name = models.TextField(max_length=10)
    email = models.TextField(max_length=50)
    age = models.TextField(max_length=3)
    etc_symptom = models.TextField(max_length=150)
    result = models.TextField(max_length=10)
    
    class Meta:
       db_table = 'symptom'




