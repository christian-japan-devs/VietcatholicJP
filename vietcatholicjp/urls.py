"""vietcatholicjp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth import views as auth_views #new

admin.site.site_header = 'Viet Catholic Japan'                    # default: "Django Administration"
admin.site.index_title = 'Viet Catholic Japan Admintration'       # default: "Site administration"
admin.site.site_title = 'Viet Catholic Japan Admintration'       # default: "Django site admin"

urlpatterns = [
    path('',include('home.urls'),name="vcj-home"),
    path('',include('users.urls')),
    path('',include('kanri.urls')),
    path('',include('event.urls')),
    #path('admin/login/', auth_views.LoginView.as_view(template_name='main/home.html'), name='login'), #new
    path('admin/', admin.site.urls),
]
