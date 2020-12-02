from django.contrib import auth
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse

# Create your views here.
from .models import Users, Products
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
    return HttpResponse("billing")
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