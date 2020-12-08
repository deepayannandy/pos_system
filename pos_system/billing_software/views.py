from django.contrib import auth
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse

# Create your views here.
from .models import Users, Products, Customer
from . import operations


def home(requests):
    if requests.user.is_authenticated:
        return  render(requests,'home.html', {'date': operations.getdate()})
    else:
        return render(requests, 'login.html')



def login(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
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
            return render(request, 'login.html')
        user = list(Users.objects.all())
        print(user[0])


def logout(requests):
    auth.logout(requests)
    return redirect('/login')

def billing(requests):
    if requests.method == 'POST':
        print("post")
        return redirect('/billing',{'date': operations.getdate()})
    else:
        return render(requests, 'billing.html',{'date': operations.getdate()})
def stocks(request):
    if request.method == 'POST':
        item_name=request.POST['item_name']
        item_price=request.POST['item_price']
        item_quantity=request.POST['item_quantity']
        item_tax=request.POST['item_tax']
        product=Products(name=item_name,price=item_price,quantity=item_quantity,tax=item_tax,barcode=operations.generate_bar_num())
        product.save()
        return redirect('/stocks')
    else:
        return render(request, 'stocks.html',{'date': operations.getdate(), 'product_list': Products.objects.all()})
def delete_item(requests,item_id):
    print(item_id)
    product_to_del=Products.objects.get(id=item_id)
    product_to_del.delete()
    return redirect('/stocks')
def update_item(requests,item_id):
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
        return render(requests, 'item_update.html', {'itemdata': product})
def bulk_import(request):
    if request.method == 'POST':
        print(request.POST['path'])
        return redirect('/bulk_import')
    else:
        return render(request,'bulk_import.html')
def khata(requests):
    return HttpResponse("khata")
def history(requests):
    return HttpResponse("history")
def barcode(requests):
    return HttpResponse("barcode")

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
    if requests.method=='POST':
        product_name=requests.POST['item_name']
        product_quantity=requests.POST['quantity']
        prod_det=Products.objects.get(name=product_name)
        if int(prod_det.quantity)<int(product_quantity):
            product_quantity=int(prod_det.quantity)
            messages.info(requests, "Only"+str(prod_det.quantity)+"Available!")
        product_dis=requests.POST['discount']
        cart_items=operations.calculate(product_name,product_quantity,product_dis)
        return render(requests, 'cart.html',
                      {'date': operations.getdate(), 'customerdata': operations.get_customerdata(),
                       'items': Products.objects.values_list('name', flat=True), 'cart_items': cart_items,'total':operations.get_total_cart()})
    else:
        return render(requests, 'cart.html', {'date': operations.getdate(),'customerdata': operations.get_customerdata(),'items': Products.objects.values_list('name', flat=True),'cart_items': operations.get_cart(),'total':operations.get_total_cart()})
def settle(requests):
    operations.settelment()
    return redirect('/')