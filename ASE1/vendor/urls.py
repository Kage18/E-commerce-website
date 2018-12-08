from django.urls import path, include
from vendor import views

app_name = 'vendor'

urlpatterns = [
    path('home/', views.list_categories, name='home'),
    path('home/<int:pk>/', views.itemsview, name='items'),
    path('add/', views.add_products, name='add_products'),
    path('view/', views.view_products, name='view_products'),
    path('modify/<int:id>/', views.modify_products, name='modify_products'),
    path('show-orders/', views.view_orders, name='view-orders'),
    path('delete_product/<int:id>', views.delete_product, name='delete_product'),
    path('authentication/', include('actor_authentication.urls')),

]
