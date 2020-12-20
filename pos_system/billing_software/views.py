from django.contrib import auth
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse

# Create your views here.
from .models import Users, Products, Customer, Company, Transactions
from . import operations
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent


def home(requests):
    if requests.user.is_authenticated:
        path= Company.objects.get(pk=1)
        return  render(requests,'home.html', {'date': operations.getdate(),'today_sell':operations.daily_total(),'comp_logo': path.c_logo})
    else:
        return render(requests, 'login.html')



def login(request):
    path = Company.objects.get(pk=1)
    if request.user.is_authenticated:
        return render(request, 'home.html',{'comp_logo': path.c_logo})
    else:
        if request.method == 'POST':
            username = request.POST.get("username")
            password = request.POST.get("password")
            print(username,password)

            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("/")

            else:
                messages.info(request, "Invalid user!")
                return redirect('login')


        else:
            return render(request, 'login.html',{'comp_logo': path.c_logo})
        user = list(Users.objects.all())
        print(user[0])


def logout(requests):
    auth.logout(requests)
    return redirect('/login')

def billing(requests):
    path = Company.objects.get(pk=1)
    if requests.method == 'POST':
        print("post")
        return redirect('/billing',{'date': operations.getdate(),'comp_logo': path.c_logo})
    else:
        return render(requests, 'billing.html',{'date': operations.getdate(),'comp_logo': path.c_logo})
def stocks(request):
    path = Company.objects.get(pk=1)
    if request.method == 'POST':
        item_name=request.POST['item_name']
        item_price=request.POST['item_price']
        item_quantity=request.POST['item_quantity']
        item_tax=request.POST['item_tax']
        product=Products(name=item_name,price=item_price,quantity=item_quantity,tax=item_tax,barcode=operations.generate_bar_num())
        product.save()
        return redirect('/stocks')
    else:
        return render(request, 'stocks.html',{'date': operations.getdate(), 'product_list': Products.objects.all(),'comp_logo': path.c_logo})
def delete_item(requests,item_id):
    print(item_id)
    product_to_del=Products.objects.get(id=item_id)
    product_to_del.delete()
    return redirect('/stocks')
def update_item(requests,item_id):
    path = Company.objects.get(pk=1)
    if requests.method=='POST':
        item_name = requests.POST['item_name']
        item_price = requests.POST['item_price']
        item_quantity = requests.POST['item_quantity']
        item_tax = int(requests.POST['item_tax'])
        product = Products.objects.get(pk=item_id)
        product.name=item_name
        product.price=item_price
        product.quantity=item_quantity
        product.tax=item_tax
        product.save()
        return redirect('/stocks')
    else:
        print("Update",item_id)
        product=Products.objects.get(id=item_id)
        return render(requests, 'item_update.html', {'itemdata': product,'comp_logo': path.c_logo})
def bulk_import(request):
    path = Company.objects.get(pk=1)
    if request.method == 'POST':
        print(request.POST['path'])
        return redirect('/bulk_import')
    else:
        return render(request,'bulk_import.html', {'comp_logo': path.c_logo})
def khata(requests):
    path = Company.objects.get(pk=1)
    return render(requests,'duekhata.html',{'date':operations.getdate(),'all_det':operations.get_due_cust() ,'comp_logo':path.c_logo})
def history(requests):
    if requests.method == "POST":
        date = requests.POST['billing_date']
        customer_name = requests.POST['consumer_name']
        invoice_no = requests.POST['invoice_no']
        print(date, customer_name,invoice_no)
        path = Company.objects.get(pk=1)
        alltnx = Transactions.objects.all()
        return render(requests, 'history.html',
                      {'all_tnx': alltnx, 'comp_logo': path.c_logo, 'date': operations.getdate(),
                       'search_date': operations.getsearchdate()})
    else:
        path = Company.objects.get(pk=1)
        alltnx = Transactions.objects.all()
        return render(requests, 'history.html',
                      {'all_tnx': alltnx, 'comp_logo': path.c_logo, 'date': operations.getdate(),
                       'search_date': operations.getsearchdate()})


def barcode(requests):
    return HttpResponse("barcode")
def acounts(requests):
    if requests.method=="POST":
        date=requests.POST['billing_date']
        customer_name=requests.POST['consumer_name']
        print(date,customer_name)
        path = Company.objects.get(pk=1)
        alltnx = Transactions.objects.all()
        return render(requests, 'accounts.html',{'all_tnx': alltnx, 'comp_logo': path.c_logo, 'date': operations.getdate(),'search_date': operations.getsearchdate()})
    else:
        path = Company.objects.get(pk=1)
        alltnx= Transactions.objects.all()
        return render(requests,'accounts.html',{'all_tnx':alltnx,'comp_logo': path.c_logo,'date':operations.getdate(),'search_date': operations.getsearchdate()})

def addcustomer(request):
    if request.method == 'POST':
        consumer_name = request.POST['consumerName']
        consumer_address = request.POST['Address']
        consumer_contact = request.POST['contact']
        consumer_gst= request.POST['gst_no']
        if consumer_contact in Customer.objects.values_list('customerContact', flat=True):
            operations.set_consumersdata(consumer_contact)
            return redirect('/cart', {'date': operations.getdate(),})
        else:
            print(len(consumer_contact))
            if len(consumer_contact)<10:
                messages.info(request, "Number Invalid!")
                return redirect('/billing', {'date': operations.getdate()})
            elif len(consumer_name)==0 or len(consumer_address)==0 :
                messages.info(request, "Customer Does not Exist! please fill Name and Address ")
                return redirect('/billing', {'date': operations.getdate()})
            elif len(consumer_name)!=0 and len(consumer_address)!=0 and len(consumer_contact)>9:
                consumer = Customer(customerName=consumer_name, customerAddress=consumer_address,customerContact=consumer_contact, customerGST=consumer_gst, customerDue=0)
                consumer.save()
                messages.info(request, "User Added!")
                operations.set_consumersdata(consumer_contact)
                return redirect('/cart', {'date': operations.getdate()})

    else:
        pass

def cart(requests):
    path = Company.objects.get(pk=1)
    if requests.method=='POST':
        product_name=requests.POST['item_name']
        product_quantity=requests.POST['quantity']
        prod_det=Products.objects.get(name=product_name)
        if int(prod_det.quantity)>int(product_quantity):
            messages.info(requests, "Item added")
            product_dis = requests.POST['discount']
            cart_items = operations.calculate(product_name, product_quantity, product_dis)
        if int(prod_det.quantity)<int(product_quantity):
            messages.info(requests, "Only" + str(prod_det.quantity) + "Available!")
            if int(prod_det.quantity)>0:
                product_quantity=int(prod_det.quantity)
                product_dis = requests.POST['discount']
                cart_items = operations.calculate(product_name, product_quantity, product_dis)
            else:
                cart_items = operations.get_cart()
        if int(prod_det.quantity)==0:
            messages.info(requests, "Out Of Stock!")
            cart_items=operations.get_cart()
        return render(requests, 'cart.html',
                      {'date': operations.getdate(), 'customerdata': operations.get_customerdata(),
                       'items': Products.objects.values_list('name', flat=True), 'cart_items': cart_items,'total':operations.get_total_cart(),'comp_logo': path.c_logo})
    else:
        return render(requests, 'cart.html', {'date': operations.getdate(),'customerdata': operations.get_customerdata(),'items': Products.objects.values_list('name', flat=True),'cart_items': operations.get_cart(),'total':operations.get_total_cart(),'comp_logo': path.c_logo})
def settle(requests):
    return render(requests,'print.html',{'total':operations.get_total_cart(),'date':operations.getdate()})
def printbill(requests):
    if requests.method=='POST':
        fs = FileSystemStorage()
        pmode=requests.POST['paymentmode']
        if pmode=="Cash":
            details = "Cash"
        if pmode=="Cradit":
            details=requests.POST['details']
            c_contact=operations.get_customerdata()[2]
            customer = Customer.objects.get(customerContact=c_contact)
            old_cred=customer.customerDue
            customer.customerDue=old_cred+operations.get_total_cart()
            customer.save()
        else:
            details = requests.POST['details']
        billpath = operations.settelment(pmode+" TXRef:"+details)
        billpath = str(BASE_DIR) + "/" + billpath
        print(billpath)
        responce = HttpResponse(fs.open(billpath), content_type='application/pdf')
        return responce