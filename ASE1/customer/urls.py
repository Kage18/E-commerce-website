from django.urls import path, include
from customer import views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView

app_name = 'customer'

urlpatterns = [
    path('home/', views.list_categories, name='home'),
    path('home/<int:pk>/', views.itemsview, name='items'),
    path('authentication/', include('actor_authentication.urls')),
    path('search_results/', views.Search_Results, name="search_results"),
    path('profile/', views.profile, name='profile'),
    path('password_reset/', PasswordResetView.as_view(), name='forgot_pass'),
    path('password_reset_done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
