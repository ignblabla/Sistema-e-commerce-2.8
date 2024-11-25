from pyexpat.errors import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import json
import datetime
from .models import * 
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .utils import cookieCart, cartData, guestOrder

def store(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)



def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

    else:
        customer, order = guestOrder(request, data)

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

    return JsonResponse('Payment submitted..', safe=False)


def categories(request):
    categories = Category.objects.all()
    for category in categories:
        category.product_count = category.product_set.count()

    context = {'categories': categories}
    return render(request, 'store/categories.html', context)


# def registro(request):
#     data = {
# 		'form': CustomUserCreationForm()
# 	}
#     if request.method == 'POST':
#         formulario = CustomUserCreationForm(data=request.POST)
#         if formulario.is_valid():
#             formulario.save()
#             user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
#             login(request, user)
#             messages.success(request, "Te has registrado correctamente")
#             return redirect(to="store")
#         data["form"] = formulario
#     return render(request, 'registration/registro.html', data)

def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            name = form.cleaned_data.get('username')  # Assuming the username is used as name for the Customer
            email = form.cleaned_data.get('email')  # Ensure email field exists in UserCreationForm or handle separately
            customer = Customer.objects.create(user=user, name=name, email=email)
            login(request, user)
            messages.success(request, "Te has registrado correctamente")
            return redirect('store')
    else:
        form = CustomUserCreationForm()
    
    context = {'form': form}
    return render(request, 'registration/registro.html', context)


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


def product_details(request, product_id):
	product= get_object_or_404(Product, id=product_id)
    
	context = {
        'product': product,
    }

	return render(request,'store/product_details.html', context)

@login_required
def list_orders(request):
    user = request.user
    # Obtener o crear el Customer asociado con el usuario
    customer = Customer.objects.get(user=user)
    # Obtener las órdenes asociadas al cliente
    orders = Order.objects.filter(customer=customer)
    context = {
        'orders': orders
    }
    return render(request, 'store/my_orders.html', context)


def view_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return render(request, 'store/order_not_found.html', {'order_id': order_id})

    order_items = order.orderitem_set.all()
    shipping_address = ShippingAddress.objects.filter(order=order).first()

    context = {
        'order': order,
        'order_items': order_items,
        'shipping_address': shipping_address,
    }
    
    return render(request, 'store/order.html', context)


def check_order_exists(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        return JsonResponse({'exists': True})
    except Order.DoesNotExist:
        return JsonResponse({'exists': False}, status=404)