"""CartProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from CartApp.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/",loginPage,name="login"),
    path("logout/",logoutUser,name="logout"),
    path("register/",registerPage,name="register") ,
    path("account/",account_settings,name="account"),
    path("", home, name="home"),
    path("products/", products, name="products"),
    path("user/",userPage,name="userPage"),
    path("customer/<int:pk_>/", customer, name="customer"),
    path("create_order/<int:pk>/", createOrder, name="createOrder"),
    path("update_order/<int:pk>/",updateOrder,name="updateOrder" ),
    path("delete_order/<int:pk>/",deleteOrder,name="deleteOrder")
    
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)