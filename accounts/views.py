from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib import auth
from django.contrib import messages
from django.shortcuts import get_object_or_404, render,redirect

from accounts.models import Product
# Create your views here.
def signout(request):
    
    if request.user.is_authenticated:
        logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('/')

def store(request):
    products = Product.objects.all().filter(is_available =True)
    product_count = products.count()
    context = {
        'products':products,
        'count': product_count,
        
    }
    print(request.user)
    return render (request,'index.html',context)
