from django.urls import path, include
from customer import views
from django.conf.urls import url
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView,PasswordResetCompleteView

app_name = 'customer'

urlpatterns = [
    path('home/', views.list_categories, name='home'),
    url(r'^review/(?P<categ>\w+)/(?P<product>\w+)/$', views.reviewtext, name='review'),
    path('home/<int:pk>/', views.itemsview, name='items'),
    path('home/<int:pk>/<int:ck>/', views.itemdetailview,name='specificitem'),
    path('authentication/', include('actor_authentication.urls')),
    path('search_results/', views.Search_Results, name="search_results"),
    path('faq/', views.faq, name='faq'),
    path('about-us/', views.about_us, name='about_us'),
    path('profile/', views.profile, name='profile'),
    path('password_reset/', PasswordResetView.as_view(), name='forgot_pass'),
    path('password_reset_done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('QrCode/<int:id>/',views.QrCode,name="QrCode"),
]
