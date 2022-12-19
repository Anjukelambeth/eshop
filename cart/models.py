from django.db import models

# Create your models here.
from calendar import c
from django.db import models
from accounts.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=50,blank=True)
    date_added = models.DateTimeField(auto_now_add =True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def item_total(self):
        return self.product.price * self.quantity


    def __str__(self):
        return self.product.product_name
