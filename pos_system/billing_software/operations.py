from datetime import datetime
import pytz
from . import invoice_2inch_gen
from .models import Customer, Products, Company, Transactions

cart_consumer_data=[]
cart_items=[]
total=0
def getdate():
    IST = pytz.timezone('Asia/Kolkata')
    datetime_ist = datetime.now(IST)
    return datetime_ist.strftime('%a %d/%b/%y')
def generate_bar_num():
    IST = pytz.timezone('Asia/Kolkata')
    datetime_ist = datetime.now(IST)
    return datetime_ist.strftime('%H%M%S%d%m%y')
def set_consumersdata(number):
    global cart_consumer_data,cart_items,total
    cart_consumer_data=[]
    cart_items=[]
    total = 0
    data= Customer.objects.filter(customerContact=number)
    for i in data:
        cart_consumer_data.append(i.customerName)
        cart_consumer_data.append(i.customerAddress)
        cart_consumer_data.append(i.customerContact)
        cart_consumer_data.append(i.customerGST)
    print(cart_consumer_data)
def get_customerdata():
    return cart_consumer_data
def calculate(item_name,quantity,discount):
    item=Products.objects.filter(name=item_name)
    r_data=[]
    global total,cart_items
    for item_data in item:
        r_data.append(item_data.name)
        r_data.append(item_data.price)
        r_data.append(quantity)
        r_data.append((item_data.price/100)*item_data.tax)
        r_data.append((item_data.price+(item_data.price/100)*item_data.tax)*int(quantity))
    cart_items.append(r_data)
    total= total+(item_data.price*int(quantity))
    return cart_items
def get_cart():
    global cart_items
    return cart_items
def get_total_cart():
    return total
def stocks_update(item_name,b_quantity):
    item = Products.objects.get(name=item_name)
    old_q=item.quantity
    new_q=old_q-int(b_quantity)
    item.quantity=new_q
    item.save()
def settelment():
    for i in cart_items:
        print(i[0],i[2])
        stocks_update(i[0],i[2])
    return print_bill()
def print_bill():
    global cart_consumer_data, cart_items, total
    company_data=Company.objects.all()
    for i in company_data:
        print(i)
        cdata=[i.c_name,i.c_invoice,getdate(),i.c_address,i.c_contact,18]

    print(cdata)
    print(cart_consumer_data)
    print(cart_items)
    print(total)
    bill_path=invoice_2inch_gen.genpdf(cdata,cart_items,total)
    tnsx_update()
    return bill_path
def tnsx_update():
    global cart_consumer_data,total
    IST = pytz.timezone('Asia/Kolkata')
    datetime_ist = datetime.now(IST)
    date=datetime_ist.strftime('%d/%m/%y')
    time=datetime_ist.strftime('%H:%M:%S')
    company_data = Company.objects.get(pk='1')
    invoiceto=company_data.c_invoice
    company_data.c_invoice=invoiceto+1
    company_data.save()
    tnsx1= Transactions(bill_no=invoiceto,bill_date=date,bill_time=time,bill_to=cart_consumer_data[0],bill_mod_pay='',bill_amount=total)
    tnsx1.save()
def daily_total():
    IST = pytz.timezone('Asia/Kolkata')
    datetime_ist = datetime.now(IST)
    date = datetime_ist.strftime('%d/%m/%y')
    total=0
    for i in Transactions.objects.filter(bill_date= date):
        print(i.bill_amount)
        total=total+i.bill_amount
    print(total)
    return total

