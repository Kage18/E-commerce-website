from django.urls import path, include
from customer import views

app_name = 'customer'

urlpatterns = [
    path('home/', views.list_categories, name='home'),
    path('home/<int:pk>/', views.itemsview, name='items'),
    path('authentication/', include('actor_authentication.urls')),
    path('search_results/', views.Search_Results, name="search_results"),
    # path('login/', OurAuthViews.login_all, name='login'),
    # path('logout/', OurAuthViews.logout_all, name='logout'),
    # path('signup/', OurAuthViews.customer_signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    # path('home/', views.list_categories, name='home'),
]
