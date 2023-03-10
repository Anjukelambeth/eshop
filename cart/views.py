
from django.shortcuts import get_object_or_404, redirect, render
from accounts.models import Product
from . models import Cart, CartItem
from django.contrib.auth.decorators import login_required


# Create your views here.


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request,product_id):
    product = Product.objects.get(product_id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()
    if request.user.is_authenticated:
        try:
            
            cart_item =  CartItem.objects.get(product=product,cart=cart,user=request.user)
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                quantity = 1,
                cart = cart,
                user = request.user,
            )

            cart_item.save()
    else:
        try:
            
            cart_item =  CartItem.objects.get(product=product,cart=cart)
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                quantity = 1,
                cart = cart,
            )

            cart_item.save()
        #to return to the same page by using url
    return redirect(request.META.get('HTTP_REFERER'))

def remove_cart(request,product_id):
    
    product = get_object_or_404(Product, product_id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product,user=request.user)
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_item = CartItem.objects.get(product=product,cart=cart)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

#delete an item from cart
def delete_item(request,product_id):
    
    product = get_object_or_404(Product, product_id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.filter(product=product,user=request.user).first()
    else:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_item = CartItem.objects.get(product=product,cart=cart)
    cart_item.delete()
    return redirect('cart')


def cart(request, sub_total=0, quantity=0, cart_items=None):
   
    if request.user.is_authenticated:
        
        cart_items = CartItem.objects.filter(user=request.user,is_active=True)
        
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)


    context = {
        'sub_total': sub_total,
        'quantity': quantity,
        'cart_items': cart_items,
    }
    return render(request, 'cart.html', context)    

@login_required
def checkout(request, sub_total=0, quantity=0, cart_items=None,coupon=None, final_price=0,deduction =0):
   
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    for cart_item in cart_items:
        new_price =  cart_item.product.price
        sub_total += (new_price * cart_item.quantity)
        print('heheeh')
   
   
   
    
    final_price = sub_total

        
    context = {
        'sub_total': sub_total,
        'final_price':final_price,
        'quantity': quantity,
        'cart_items': cart_items,
       

    }
    return render (request,'checkout.html',context)
