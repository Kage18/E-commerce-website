"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from . import views

app_name = 'blog'

urlpatterns = [
    path('',views.post_list,name='post_list'),
    path("<int:id>/edit_post/",views.post_edit,name = 'post_edit'),
    path("<int:id>/post_delete/",views.post_delete,name = 'post_delete'),
    path('<int:id>/<slug:slug>/',views.post_detail,name = 'post_detail'),
    path('post_create/',views.post_create,name='post_create'),
    path('like/',views.like_post,name = 'like_post'),
    path('my_posts/',views.user_posts,name="my_posts"),
    path('my_drafts/',views.user_drafts,name="my_drafts"),
]
