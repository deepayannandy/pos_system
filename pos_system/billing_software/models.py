from django.db import models

# Create your models here.
class Products(models.Model):
    name= models.CharField(max_length=100)
    price= models.IntegerField()
    quantity= models.IntegerField()
    tax= models.IntegerField(default=0)
    barcode =models.CharField(max_length=13)
class Users(models.Model):
    userid=models.CharField(max_length=10)
    password= models.CharField(max_length=20)

