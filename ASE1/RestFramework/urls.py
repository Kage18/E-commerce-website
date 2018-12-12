from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from RestFramework import views

urlpatterns = [
    path('products/', views.ProductsList.as_view()),
    path('products/<int:pk>/', views.ProductDetail.as_view()),
    path('orders/', views.OrdersList.as_view()),
    path('orders/<int:pk>', views.OrderDetail.as_view()),
    # path('rest-auth/', include('rest_auth.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
