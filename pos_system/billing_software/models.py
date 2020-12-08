from django.db import models


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
class Company(models.Model):
    c_name=models.CharField(max_length=100)
    c_invoice=models.IntegerField(default=0)
    c_logo=models.ImageField(upload_to='comany_logo')
    c_gst_no=models.CharField(max_length=100)
    c_address=models.CharField(max_length=100)
    c_contact = models.CharField(max_length=100)
    c_website= models.CharField(max_length=100)
class Transactions(models.Model):
    bill_no=models.IntegerField()
    bill_date=models.CharField(max_length=20)
    bill_time=models.CharField(max_length=20)
    bill_to=models.CharField(max_length=50)
    bill_mod_pay=models.CharField(max_length=10)
    bill_amount=models.IntegerField()


