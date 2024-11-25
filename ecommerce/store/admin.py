from django.contrib import admin
from .models import *

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')

    def order(self, obj):
        return f"Order {obj.order.id}"
    order.short_description = 'Order'

    def product(self, obj):
        return obj.product.name
    product.short_description = 'Product'

    def quantity(self, obj):
        return obj.quantity
    quantity.short_description = 'Quantity'

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_email', 'date_ordered', 'complete', 'product_list')

    def customer_email(self, obj):
        return obj.customer.email if obj.customer else 'No customer'
    customer_email.short_description = 'Customer Email'

    def product_list(self, obj):
        items = obj.orderitem_set.all()
        return ", ".join([f"{item.product.name} (x{item.quantity})" for item in items if item.product])
    product_list.short_description = 'Products (Quantity)'

# Registrar los modelos en el admin
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ShippingAddress)
admin.site.register(Category)
admin.site.register(Manufacturer)
