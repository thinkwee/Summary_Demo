from __future__ import unicode_literals
from django.db import models

# Create your models here.

class message(models.Model):
    username = models.CharField(max_length=1000)
    password = models.CharField(max_length=1000)  
    predict_result=models.CharField(max_length=1000)
