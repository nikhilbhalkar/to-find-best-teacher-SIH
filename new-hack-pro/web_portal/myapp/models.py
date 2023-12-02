from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class OurUser(models.Model):
     
     sno= models.AutoField(primary_key=True)
     username = models.CharField(max_length=255 , default="")
     interest= models.CharField(max_length=255, default="")
     level= models.CharField(max_length=255 , default="")
     learningstyle= models.CharField(max_length=255 , default="")
     password= models.CharField(max_length=13 , default="")
     email= models.CharField(max_length=100 , default="")
     


     
     