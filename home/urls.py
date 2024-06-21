from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('', views.index),
    path('home', views.home),
    path('login', views.loginUser),
    path('logout', views.loginUser),
    path('signin', views.signin),
    path('details', views.details),

]