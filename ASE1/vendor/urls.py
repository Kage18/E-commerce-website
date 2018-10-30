from django.urls import path
from vendor import views

app_name = 'vendor'

urlpatterns = [
    path('add/', views.add_products, name='add_products'),
    path('view/', views.view_products, name='view_products'),
    path('login/', views.vendor_login, name='login'),
    path('logout/', views.vendor_logout, name='logout'),
    path('signup/', views.vendor_signup, name='signup')
]
