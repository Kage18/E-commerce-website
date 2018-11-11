from django.urls import path
from customer import views

app_name = 'customer'

urlpatterns = [
    path('home/', views.IndexView.as_view(), name='home'),
    path('home/<int:pk>/', views.itemsview, name='items'),
    path('login/', views.customer_login, name='login'),
    path('logout/', views.customer_logout, name='logout'),
    path('signup/', views.customer_signup, name='signup'),
    path('profile/', views.profile, name='profile')
    # path('home/', views.list_categories, name='home'),
]
