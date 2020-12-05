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
class Customer(models.Model):
    customerName=models.CharField(max_length=30)
    customerAddress=models.CharField(max_length=50)
    customerContact=models.CharField(max_length=12)
    customerGST=models.CharField(max_length=20, default= "null")
    customerDue=models.IntegerField(default=0)
