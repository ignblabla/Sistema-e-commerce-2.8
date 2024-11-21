from django.contrib import admin
from .models import *

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'date_ordered', 'complete', 'product_list')
    list_filter = ('status', 'complete', 'date_ordered')
    search_fields = ('user__username', 'id')

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'order_id', 'quantity', 'date_added')
    list_filter = ('date_added',)
    search_fields = ('product__name', 'order__id')

    @admin.display(description='Product Name')
    def product_name(self, obj):
        return obj.product.name if obj.product else 'N/A'

    @admin.display(description='Order ID')
    def order_id(self, obj):
        return obj.order.id if obj.order else 'N/A'

admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ShippingAddress)
admin.site.register(Category)
admin.site.register(Manufacturer)