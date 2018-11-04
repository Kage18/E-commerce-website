from django.urls import path
from vendor import views

app_name = 'vendor'

urlpatterns = [
    path('home/', views.IndexView.as_view(), name='home'),
    path('home/<int:pk>/', views.ItemsView.as_view(), name='items'),

    path('add/', views.add_products, name='add_products'),
    path('view/', views.view_products, name='view_products'),
    path('modify/<int:id>/', views.modify_products, name='modify_products'),

    path('login/', views.vendor_login, name='login'),
    path('logout/', views.vendor_logout, name='logout'),
    path('signup/', views.vendor_signup, name='signup')
]
