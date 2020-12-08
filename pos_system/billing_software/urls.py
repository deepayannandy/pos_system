from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('billing', views.billing, name='billing'),
    path('stocks', views.stocks, name='stocks'),
    path('khata', views.khata, name='khata'),
    path('history', views.history, name='history'),
    path('barcode', views.barcode, name='barcode'),
    path('delete_item/<int:item_id>/', views.delete_item, name='delete_item'),
    path('update_item/<int:item_id>/', views.update_item, name='update_item'),
    path('bulk_import', views.bulk_import, name='bulk_import'),
    path('addcustomer', views.addcustomer, name='addcustomer'),
    path('cart', views.cart, name='cart'),
    path('settle', views.settle, name='settle'),
    path('acounts', views.acounts, name='acounts'),
]