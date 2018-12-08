from django.urls import path
from cart import views

app_name = 'cart'

urlpatterns = [
    path('order-summary/', views.order_details, name='order_summary'),
    path('add-to-cart/<int:prod_id>/', views.add_to_cart, name='add_to_cart'),
    path('delete-from-cart/<int:item_id>/', views.delete_from_cart, name='delete_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_transaction_records/', views.update_transaction_records, name='update'),
    path('qtyupdate/',views.qtyupdate, name='qtyupate'),
]