from pyexpat.errors import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import json
import datetime
from .models import * 
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

def store(request):
	if request.user.is_authenticated:
		customer = request.user
		order, created = Order.objects.get_or_create(user=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		#Create empty cart for now for non-logged in user
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)

def cart(request):

	if request.user.is_authenticated:
		customer = request.user
		order, created = Order.objects.get_or_create(user=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		#Create empty cart for now for non-logged in user
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	if request.user.is_authenticated:
		customer = request.user
		order, created = Order.objects.get_or_create(user=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(user=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user
		order, created = Order.objects.get_or_create(user=customer, complete=False)
		total = float(data['form']['total'])
		order.transaction_id = transaction_id

		if total == order.get_cart_total:
			order.complete = True
		order.save()

		if order.shipping == True:
			ShippingAddress.objects.create(
			customer=customer,
			order=order,
			address=data['shipping']['address'],
			city=data['shipping']['city'],
			state=data['shipping']['state'],
			zipcode=data['shipping']['zipcode'],
			)
	else:
		print('User is not logged in')

	return JsonResponse('Payment submitted..', safe=False)

def categories(request):
    categories = Category.objects.all()
    for category in categories:
        category.product_count = category.product_set.count()

    context = {'categories': categories}
    return render(request, 'store/categories.html', context)

def registro(request):
    data = {
		'form': CustomUserCreationForm()
	}
    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user)
            messages.success(request, "Te has registrado correctamente")
            return redirect(to="store")
        data["form"] = formulario
    return render(request, 'registration/registro.html', data)

def products_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = category.product_set.all()

    manufacturers = category.product_set.values('manufacturer__id', 'manufacturer__name').distinct()

    manufacturer_id = request.GET.get('manufacturer')
    if manufacturer_id:
        products = products.filter(manufacturer_id=manufacturer_id)

    context = {
        'category': category,
        'products': products,
        'manufacturers': manufacturers,
        'selected_manufacturer': manufacturer_id,
    }
    return render(request, 'store/products_by_category.html', context)