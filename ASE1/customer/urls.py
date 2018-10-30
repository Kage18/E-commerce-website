from django.urls import path
from customer import views

app_name = 'customer'

urlpatterns = [
    path('home', views.home, name='home'),
    path('login/', views.customer_login, name='login'),
    path('logout/', views.customer_logout, name='logout'),
    path('signup/', views.customer_signup, name='signup')
]
