from django.urls import path, re_path
from cart import views

app_name = 'cart'

urlpatterns = [
    re_path(r'^order-summary/$', views.order_details, name="order_summary"),
    re_path('add-to-cart/(?P<item_id>\d+)/(?P<cat_id>\d+)/$', views.add_to_cart, name="add_to_cart"),
    path('delete-from-cart/<int:item_id>/', views.delete_from_cart, name="delete_from_cart"),
    path('checkout/', views.checkout, name='checkout'),
    path('update_transaction_records/', views.update_transaction_records, name='update')
]