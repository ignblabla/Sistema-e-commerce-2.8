import json, random, string
from django.contrib.auth.models import User
from .models import *

def cookieCart(request):
	#Create empty cart for now for non-logged in user
	try:
		cart = json.loads(request.COOKIES['cart'])
	except:
		cart = {}
		print('CART:', cart)

	items = []
	order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
	cartItems = order['get_cart_items']

	for i in cart:
		try:
			cartItems += cart[i]['quantity']

			product = Product.objects.get(id=i)
			total = (product.price * cart[i]['quantity'])

			order['get_cart_total'] += total
			order['get_cart_items'] += cart[i]['quantity']

			item = {
				'id':product.id,
				'product':{'id':product.id,'name':product.name, 'price':product.price, 
				'imageURL':product.imageURL}, 'quantity':cart[i]['quantity'],
				# 'digital':product.digital,'get_total':total,
				}
			items.append(item)

			# if product.digital == False:
			# 	order['shipping'] = True
		except:
			pass
			
	return {'cartItems':cartItems ,'order':order, 'items':items}

def cartData(request):
	if request.user.is_authenticated:
		user = request.user
		order, created = Order.objects.get_or_create(user=user, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		cookieData = cookieCart(request)
		cartItems = cookieData['cartItems']
		order = cookieData['order']
		items = cookieData['items']

	return {'cartItems':cartItems ,'order':order, 'items':items}

def generate_unique_username(base="guest"):
    """Genera un nombre de usuario único basado en un prefijo."""
    while True:
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        username = f"{base}_{random_suffix}"
        if not User.objects.filter(username=username).exists():
            return username

# def guestOrder(request, data):
#     print('User is not logged in')

#     name = data['form']['name']
#     email = data['form']['email']

#     # Generar un nombre de usuario único para el usuario invitado
#     username = generate_unique_username()

#     # Crear o recuperar un usuario con ese nombre único
#     user, created = User.objects.get_or_create(
#         username=username,
#         defaults={'email': email, 'first_name': name}
#     )

#     # Crear la orden para el usuario invitado
#     order = Order.objects.create(
#         user=user,
#         complete=False,
#     )

#     return user, order

def guestOrder(request, data):
    print('User is not logged in')

    name = data['form']['name']
    email = data['form']['email']

    # Generar un nombre de usuario único para el usuario invitado
    username = generate_unique_username()

    # Crear o recuperar un usuario con ese nombre único
    user, created = User.objects.get_or_create(
        username=username,
        defaults={'email': email, 'first_name': name}
    )

    # Crear la orden para el usuario invitado
    order = Order.objects.create(
        user=user,
        complete=False,
    )

    # Obtener los productos del carrito de las cookies
    cookieData = cookieCart(request)
    items = cookieData['items']

    # Crear OrderItem para cada producto en el carrito
    for item in items:
        product = Product.objects.get(id=item['id'])
        OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity'],
        )

    return user, order