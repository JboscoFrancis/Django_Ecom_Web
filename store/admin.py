from django.contrib import admin
from . models import Customer, Product, Order, CartItem, ShippingAddress, WishList
# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'email']
admin.site.register(Customer, CustomerAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'product', 'complete', 'transaction_id']
admin.site.register(Order, OrderAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'discount', 'category', 'date_added']
    search_fields = ['title', 'category', 'price']
    list_filter = ['title']
admin.site.register(Product,ProductAdmin)

class CartItemAdmin(admin.ModelAdmin):
    list_display = ['customer', 'product', 'order', 'quantity']
admin.site.register(CartItem,CartItemAdmin)

class WishListAdmin(admin.ModelAdmin):
    list_display = ['customer', 'product', 'date_added']
admin.site.register(WishList,WishListAdmin)


admin.site.register(ShippingAddress)