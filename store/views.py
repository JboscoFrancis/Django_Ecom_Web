from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .filter import ProductFilter
from . models import Product, Order, CartItem, Customer, ShippingAddress, WishList
from django.core.paginator import Paginator
from .forms import UserRegistration
from django.http import JsonResponse
import datetime
import json
import sweetify

# Create your views here.
def home(request):
    product = Product.objects.all().order_by('-date_added')
    filter = ProductFilter(request.GET, queryset=product)   #filter
    product = filter.qs
    
    paginator = Paginator(product,12)   #pagination
    page_num = request.GET.get('page')
    product = paginator.get_page(page_num)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartitems = order.total_cart_items
        wishlist = WishList.objects.filter(customer=customer)
        wishcount = wishlist.count()
    else:
        wishcount = 0
        order = {'total_cart_cost':0, 'total_cart_items':0,}
        cartitems = order['total_cart_items']

    context = {'product': product, 'cartitems': cartitems, 'filter':filter, 'wishcount':wishcount}
    return render(request, 'store/home.html', context)

def userlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            messages.success(request, f'Hello! ' + username + f' Welcome to our store, get quality Product from best Known seller in the world')
            return redirect('home')
        else:
            messages.error(request, f'sorry incorrect username/password')
            return redirect('login')
    return render(request, 'store/login.html')

def userlogout(request):
    logout(request)
    return redirect('home')

def register(request):
    form = UserRegistration()
    if request.method == 'POST':
        form = UserRegistration(request.POST)
        if form.is_valid:
            user = form.save()

            #add user to group, default is customer
            group = Group.objects.get(name='customer')
            user.groups.add(group)

            #ounce user is created, then attach to customer also
            Customer.objects.create(
                user = user,
                name = user.username,
                email = user.email
            )
            messages.info(request, f'Account for ' + user.username + f' Created successful now Login')
            return redirect('login')
        else:
            messages.warning(request, f'something wrong with registration, try again!!.')
            return redirect('register')
    context = {'form': form}
    return render(request, 'store/register.html', context)

#@login_required(login_url='login')
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,create = Order.objects.get_or_create(customer=customer, complete=False)
        cartitems = order.total_cart_items
        cartcost = order.total_cart_cost
        items = order.cartitem_set.all()
        wishlist = WishList.objects.filter(customer=customer)
        wishcount = wishlist.count()
    else:
        wishcount = 0
        items = []
        order = {'total_cart_cost':0, 'total_cart_items':0,}
        cartitems = order['total_cart_items']
        cartcost = order['total_cart_cost']
        messages.warning(request, f'Not logged in please login to see your cart item')
    context = {'items': items, 'cartitems':cartitems, 'cartcost': cartcost, 'wishcount':wishcount}
    return render(request, 'store/cart.html', context)

#@login_required(login_url='login')
def wish_list(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        wishlist = WishList.objects.filter(customer=customer)
        wishcount = wishlist.count()

        order,create = Order.objects.get_or_create(customer=customer, complete=False)
        cartitems = order.total_cart_items

        context = {'wishlist':wishlist, 'wishcount':wishcount, 'cartitems':cartitems}
    else:
        messages.warning(request, f'Not logged in please login to see your wish list')
        return redirect('login')
    return render(request, 'store/wishlist.html', context)

def detail(request, pk):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartitems = order.total_cart_items
        wishlist = WishList.objects.filter(customer=customer)
        wishcount = wishlist.count()
    else:
        wishcount = 0
        order = {'total_cart_cost':0, 'total_cart_items':0,}
        cartitems = order['total_cart_items']

    try:
        product = Product.objects.get(id=pk)
        category = product.category
        p_category = Product.objects.filter(category=category).exclude(id=pk)
        context = {'product': product, 'cartitems':cartitems, 'p_category':p_category, 'wishcount':wishcount}
        return render(request, 'store/detail.html', context)
    except Product.DoesNotExist:
        messages.error(request, f'Product with that id doesnt exist/available')

    return render(request, 'store/detail.html')

@login_required(login_url='login')
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,create = Order.objects.get_or_create(customer=customer, complete=False)
        cartitems = order.total_cart_items
        cartcost = order.total_cart_cost
        wishlist = WishList.objects.filter(customer=customer)
        wishcount = wishlist.count()
    else:
        wishcount = 0
        order = {'total_cart_cost':0, 'total_cart_items':0,}
        cartitems = order['total_cart_items']
        cartcost = order['total_cart_cost']

    context = {'cartitems':cartitems, 'cartcost': cartcost, 'wishcount':wishcount}
    return render(request, 'store/checkout.html', context)

def add_Cart(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    if request.user.is_authenticated:
        customer = request.user.customer
        product = Product.objects.get(id=productId)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartitem, created = CartItem.objects.get_or_create(order=order, product=product)

        if action == 'add':     # if action is add then we add item to the cart, if item already exist then add the quantity
            cartitem.customer = customer
            cartitem.quantity = (cartitem.quantity +1)
            cartitem.save()
            messages.info(request, f'Product added successfull')
            
        elif action == 'remove':    # this for decreasing quantity of cartitem
            cartitem.quantity = (cartitem.quantity -1)
            cartitem.save()
            messages.info(request, f'Product quantity updated')
            
        elif action == 'delete':    #delete the product from the cart
            cartitem.customer = customer
            cartitem.delete()
            messages.info(request, f'Product remove from Cart')

        if cartitem.quantity <=0:   #if product quantity in cart item is 0 means no product, then delete it
            cartitem.delete()
            messages.info(request, f'Product remove from Cart')
    else:
        messages.warning(request, f'please login to add Cart')

    return JsonResponse('data returned', safe=False)

def add_wishlist(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    if request.user.is_authenticated:
        customer = request.user.customer
        product = Product.objects.get(id=productId)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartitem, created = CartItem.objects.get_or_create(order=order, product=product)
        wishlist, created = WishList.objects.get_or_create(customer=customer, product=product)

        if action == 'add':
            wishlist.save()
            messages.info(request, f'Product added to wish list')
        elif action == 'remove':
            wishlist.delete()
            messages.info(request, f'Product removed from wish list')
        elif action =='addtocart':      # product is removed from wish list then added to cart item
            cartitem.customer = request.user.customer
            cartitem.quantity = (cartitem.quantity +1)
            cartitem.save()
            wishlist.delete()
            messages.info(request, f'Product added to Cart')
                
    else:
        messages.warning(request, f'please login to add product to wishlist')
    return JsonResponse('data returned', safe=False)

@login_required(login_url='login')
def processorder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.total_cart_cost:
            order.complete = True
        order.save()

        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode']
        )
    else:
        pass

    return JsonResponse('data returned', safe=False)
