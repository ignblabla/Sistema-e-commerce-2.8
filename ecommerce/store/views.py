from django.shortcuts import render
from .models import *

# Create your views here.


def store(request):
    products = Product.objects.all()
    context={'products':products}
    return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        try:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
        except Customer.DoesNotExist:
            # Si el usuario no tiene un cliente relacionado, maneja el caso aquí
            items = []
            order = None
    else:
        items = []
        order = None

    context = {'items': items, 'order': order}
    return render(request, 'store/cart.html', context)

def checkout(request):
    context={}
    return render(request, 'store/checkout.html', context)