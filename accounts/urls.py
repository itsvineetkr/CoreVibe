from django.urls import path
from accounts import views

urlpatterns = [
    path('login/', views.login, name="login"),
    path('logout/', views.login, name="logout"),
    path('signup/', views.signup, name="signup"),
    path('details/', views.details, name="details")
]