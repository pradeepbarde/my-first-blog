"""Defines URL patterns for users"""
from django.http import HttpResponseRedirect
from django.contrib.auth import logout, login
from django.urls import path
# import url
from django.conf.urls import url
from . import views
app_name='users'
urlpatterns = [
    # home page
    #path('', views.index, name='index'),
    # login Page
    path('login/', views.loginreq, name='login'),

   # logout page
    path("logout", views.logout_request, name="logout"),

   # Registration page
    path("register/", views.register, name="register"),
]