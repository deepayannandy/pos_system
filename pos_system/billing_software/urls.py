from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('billing', views.billing, name='billing'),
    path('stocks', views.stocks, name='stocks'),
    path('khata', views.khata, name='khata'),
    path('history', views.history, name='history')
]