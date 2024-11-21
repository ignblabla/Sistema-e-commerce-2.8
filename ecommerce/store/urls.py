from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('categories/', views.categories, name="categories"),
    path('registro/', views.registro, name="registro"),
    path('categories/<int:category_id>/', views.products_by_category, name="products_by_category"),
    path('search/', views.store, name='search_products'),
]