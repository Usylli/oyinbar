"""oyinbar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from .views import indexView, signIn, postsign, logout, signUp, postsignup, add_cart, cartView, delete_from_cart, profileView, logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', indexView, name="index"),
    path('signIn/', signIn, name="signIn"),
    path('postsign/', postsign),
    path('logout/', logout, name="log"),
    path('signup/', signUp, name="signup"),
    path('postsignup/', postsignup, name="postsignup"),
    path('add_cart/<int:game_id>',add_cart, name="add_cart"),
    path('cart', cartView, name="cart"),
    path('delete_cart/<int:game_id>', delete_from_cart, name="delete_from_cart"),
    path('profile', profileView, name="profile"),
    path('logout', logout, name="logout")
]
