from django.contrib import auth
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse

# Create your views here.
from .models import Users


def home(requests):
    if requests.user.is_authenticated:
        return  render(requests,'home.html')
    else:
        return render(requests, 'login.html')



def login(request):
    if request.method == 'POST':
        username=password=""
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username,password)

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            print("ok")
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
