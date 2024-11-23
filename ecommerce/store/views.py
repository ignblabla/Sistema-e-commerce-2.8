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
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)


def cart(request):
      
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)


def checkout(request):

	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    order, created = Order.objects.get_or_create(user=request.user, complete=False)
    product = Product.objects.get(id=productId)

    if action == 'add':
        if product.stock > 0:
            order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

            order_item.quantity += 1
            order_item.save()

            product.stock -= 1
            product.save()

        else:
            return JsonResponse({'error': 'No hay suficiente stock disponible'}, status=400)

    elif action == 'remove':
        order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

        order_item.quantity -= 1
        order_item.save()

        if order_item.quantity <= 0:
            order_item.delete()

        product.stock += 1
        product.save()

    cartItems = order.get_cart_items
    return JsonResponse({'cartItems': cartItems}, safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
    else:
        user, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
        # Reducir el stock de los productos en el carrito
        for item in order.orderitem_set.all():
            product = item.product
            product.stock -= item.quantity
            product.save()
    order.save()

    if order.shipping:
        shipping_data = data.get('shipping', {})
        address = shipping_data.get('address', '')
        city = shipping_data.get('city', '')
        state = shipping_data.get('state', '')
        zipcode = shipping_data.get('zipcode', '')

        if not address or not city or not state or not zipcode:
            return JsonResponse({'error': 'Faltan datos de envío'}, status=400)

        ShippingAddress.objects.create(
            user=user,
            order=order,
            address=address,
            city=city,
            state=state,
            zipcode=zipcode,
        )

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


def product_details(request, product_id):
	product= get_object_or_404(Product, id=product_id)
    
	context = {
        'product': product,
    }

	return render(request,'store/product_details.html', context)


@login_required
def list_orders(request):
    user = request.user
    orders = Order.objects.filter(user=user)
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