from cgi import print_exception
from curses.ascii import HT
from datetime import datetime
import json
from pickletools import read_int4
from urllib.robotparser import RequestRate
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.cache import cache_control
from accounts.models import Product
from .forms import OrderForm
from cart.models import CartItem
from order.models import Order
from . models import OrderProduct, Payment, RazorPay
import datetime
import razorpay
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from accounts.models import Product



# Create your views here.
def place_order(request,total = 0,quantity = 0):
   
    current_user = request.user
   
    #if cart is empty return to login
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if (cart_count <= 0):
        return redirect('store')
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity


    if request.method=='POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            #store all billing info
            data = Order()
            data.user = current_user
            
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone_number = form.cleaned_data['phone_number']
            data.email = form.cleaned_data['email']
            data.address_line1 = form.cleaned_data['address_line1']
            data.address_line2 = form.cleaned_data['address_line2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.zip = form.cleaned_data['zip']
            data.order_note = form.cleaned_data['order_note']
            data.order_total=total
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            #generate order number yr/m/day/hr/mn/second
            order_number = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            data.order_number = order_number
            data.save()

            cart_item = CartItem.objects.filter(user=current_user)
            
           
            order_data = Order.objects.get(order_number=order_number)
            # order_item = OrderProduct.objects.filter(order=order_data)
            
            sub_total=0
            for item in cart_item:
                new_price =  item.product.price
                sub_total += (new_price * item.quantity)
               
            
        
            else:
        


                sub_total = sub_total

# authorize razorpay client with API Keys.
           
            #createe cliten
            razorpay_client = razorpay.Client(
            auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

            currency = 'INR'
            amount = sub_total

            #create order
            razorpay_order = razorpay_client.order.create(  {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"})
            # order id of newly created order.
        
            razorpay_order_id = razorpay_order['id']
            callback_url = 'http://127.0.0.1:8000/razor_success/'   
        
            # we need to pass these details to frontend.
            context = {
            'razorpay_order_id' : razorpay_order_id,
            'razorpay_merchant_key' : settings.RAZOR_KEY_ID,
            'razorpay_amount' : amount,
            'currency' : currency ,
            'callback_url' : callback_url,
            'user': current_user,
            
            'order_data':order_data,
            'sub_total':sub_total,
            'cart_item':cart_item,

            }
            razor_model =RazorPay()
            razor_model.order = order_data
            razor_model.razor_pay = razorpay_order_id
            razor_model.save()
            return render(request,'payments.html',context)
            
        else:
            return HttpResponse('form not valid')
        
    else:
        return redirect('checkout')



@csrf_exempt
def razor_success(request):
    print('razor')
    transID = request.POST.get('razorpay_payment_id')
    razorpay_order_id = request.POST.get('razorpay_order_id')
    signature = request.POST.get('razorpay_signature')
  
            #transaction details store
    razor = RazorPay.objects.get(razor_pay=razorpay_order_id)
    order = Order.objects.get(order_number = razor)
    current_user=request.user
    print(current_user,'haii')
    print('razor success page')
    payment = Payment()
    payment.user= current_user
    payment.payment_id = transID
    payment.payment_method = "Razorpapy"
    payment.amount_paid = order.order_total
    payment.status = "Completed"
    payment.save()

    order.payment=payment
    order.save()
            
    cart_item = CartItem.objects.get(user=current_user)
    
    
    #taking order_id to show the invoice

    
   
    for item in cart_item:
       
        OrderProduct.objects.create(
        order = order,
        product = item.product,
        user = current_user,
        quantity = item.quantity,
        product_price = item.product.price,
        payment = payment,
        ordered = True,
        )
    
        #decrease the product quantity from product
        orderproduct = Product.objects.filter(id=item.product_id).first()
        orderproduct.stock = orderproduct.stock-item.quantity
        orderproduct.save()
        #delete cart item from usercart after ordered
        CartItem.objects.filter(user=current_user).delete()
      
    order = Order.objects.get(order_number = razor )
    order_product = OrderProduct.objects.filter(order=order)
    transID = OrderProduct.objects.filter(order=order).first()
    context = {
        'order':order,
        'order_product':order_product,
        'transID':transID
    }
    return render(request,'success.html',context)
    
    
    

   
