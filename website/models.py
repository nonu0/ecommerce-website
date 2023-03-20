from django.db import models

# Create your models here.

class Admin(models.Model):
    user_admin = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images')
    phone = models.BigIntegerField()


    def __str__(self):
        return self.user_admin

class Customer(models.Model):
    customer = models.EmailField(unique=True)
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    email = models.EmailField()
    username = models.CharField(max_length=20)
    address = models.CharField(max_length=20, null=True , blank=True)
    joined_on = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.fname


class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField()
    
    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images')
    price = models.PositiveIntegerField()
    description = models.TextField(max_length=800)

    def __str__(self):
        return self.title

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.product.title

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,null=True,blank=True)
    total = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return 'Cart: ' + str(self.id)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()   
    sub_total = models.PositiveIntegerField()   

    def __str__(self):
        return 'Cart: ' + str(self.cart.id) + 'CartItem' + str(self.id)



class Order(models.Model):
    ORDER_STATUS = (
    ('Order Processing','Order Processing'),
    ('Order Received','Order Received'),
    ('Order On The Way','Order On The Way'),
    ('Order Completed','Order Completed'),
    ('Order Canceled','Order Canceled'),
)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    shipping_address = models.CharField(max_length=50)
    ordered_by = models.CharField(max_length=20)
    phone = models.BigIntegerField()
    email = models.EmailField()
    sub_total = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    order_status = models.CharField(max_length=50,choices=ORDER_STATUS)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Order: '+ str(self.id) 