from django.urls import path
from django.contrib.auth import views
from .views import (home,UserLoginForm)

urlpatterns = [
    path('', views.LoginView.as_view(template_name='main/home.html',authentication_form=UserLoginForm), name='vietcatholic-home'),
]