from django.db import models
from django.contrib.auth.models import User

# Create your models here.

CATEGORY = (
    ('FS', 'Fashion'),
    ('SP', 'SportWear'),
    ('OW', 'Outwear')
)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    email =models.EmailField(max_length=100, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    discount = models.FloatField(null=True, blank=True)
    category = models.CharField(choices=CATEGORY, max_length=2)
    description = models.TextField(max_length=200, null=True)
    image = models.ImageField(default='image/default.png')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url

    @property
    def setlabel(self):
        if self.category == 'FS':   
            label = 'success'   #label for fashion
        elif self.category == 'SP':
            label = 'info'  #label for sportwear
        elif self.category == 'OW':
            label = 'warning'   #label for outwear
        return label

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
    @property
    def total_cart_cost(self):
        cartitems = self.cartitem_set.all()
        total = sum([items.items_cost for items in cartitems])
        return total

    @property
    def total_cart_items(self):
        cartitems = self.cartitem_set.all()
        total = sum([items.quantity for items in cartitems])
        return total

class CartItem(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title
    @property
    def items_cost(self):
        if self.product.discount:
            total = self.quantity * self.product.discount
        else:
            total = self.quantity * self.product.price
        return total

class WishList(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    zipcode = models.CharField(max_length=50, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer.name