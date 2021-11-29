from typing_extensions import Required
from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from .models.product import Product
from .models.category import Category
from store.models import product
from .models.customer import Customer
from store.models import customer



def index(request):
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Product.get_all_products_by_categoryid(categoryID)
    else:
        products = Product.get_all_products()
    data = {}
    data['products'] = products
    data['categories'] = categories
    #return render(request, 'orders/order.html')
    print(products)
    return render(request,'index.html',data)


def validateCustomer(customer):
        error_message = None
        if(not customer.first_name):
                error_message = "First Name Required !!"
        elif len(customer.first_name) < 4:
            error_message = 'First Name must be 4 char long'

        if(not customer.last_name):
            error_message = "Last Name Required !!"
        elif len(customer.last_name) < 4:
            error_message = 'Last Name must be 4 char long'
        
        elif(not customer.phone):
            error_message = "Phone Number Required !!"
        elif len(customer.phone) < 10:
            error_message = 'Phone Number must be 10 char long'

        elif len(customer.password) < 6:
            error_message = 'Password must must be 6 char long'

        elif len(customer.email) < 6:
            error_message = 'Email must must be 5 char long'

        #saving
        return error_message


def registerUser(request):
    postData = request.POST
    first_name = postData.get('firstname')
    last_name = postData.get('lastname')
    phone = postData.get('phone')
    email = postData.get('email')
    password = postData.get('password')
        #validation
    value = {
            'first_name' : first_name,
            'last_name'  : last_name,
            'phone' : phone,
            'email' : email
        }
    error_message = None

    if not error_message:
        customer = Customer(
                first_name = first_name,
                last_name = last_name,
                phone = phone,
                email = email,
                password = password
            )
        customer.password = make_password(customer.password)
        customer.register()
        return redirect('homepage')
    else:
            data = {
                'error': error_message,
                'values' : value
            }
            return render(request,'signup.html', data)


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    else:
        return registerUser(request)
        
        


        