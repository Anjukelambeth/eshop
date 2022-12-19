from django.db import models

# Create your models here.
class Product(models.Model):
    product_id=models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=200, unique=True)
    product_slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(max_length=500, blank=True)
    strap_color=models.CharField(max_length=200, null=True, blank=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to = 'photos/products')
    images1 = models.ImageField(upload_to = 'photos/products', null=True, blank=True)
    images2 = models.ImageField(upload_to = 'photos/products', null=True, blank=True)
    images3 = models.ImageField(upload_to = 'photos/products',null=True, blank=True)
    images4 = models.ImageField(upload_to = 'photos/products', null=True, blank=True)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    
    
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name
