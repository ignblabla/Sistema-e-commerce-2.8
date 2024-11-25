from django.contrib import admin
from .models import *


# Registro de modelos
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)  # Uso de OrderAdmin personalizado
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Category)
admin.site.register(Manufacturer)