from django.urls import path,include
from vendor import views
from actor_authentication import views as OurAuthViews

app_name = 'vendor'

urlpatterns = [
    path('home/', views.IndexView.as_view(), name='home'),
    path('home/<int:pk>/', views.ItemsView.as_view(), name='items'),

    path('add/', views.add_products, name='add_products'),
    path('view/', views.view_products, name='view_products'),
    path('modify/<int:id>/', views.modify_products, name='modify_products'),
    path('delete_product/<int:id>', views.delete_product, name='delete_product'),
    path('authentication/', include('actor_authentication.urls')),
    # path('login/', OurAuthViews.login_all, name='login'),
    # path('logout/', OurAuthViews.logout_all, name='logout'),
    # path('signup/', OurAuthViews.vendor_signup, name='signup')
]
