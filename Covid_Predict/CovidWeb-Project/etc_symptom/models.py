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

class Etc_Symptom(models.Model):
    name = models.TextField(max_length=10)
    email = models.EmailField()
    etc_symptom = models.TextField()
    age = models.TextField(max_length=3)
    
    class Meta:
      db_table = 'etc_symptom_post'




