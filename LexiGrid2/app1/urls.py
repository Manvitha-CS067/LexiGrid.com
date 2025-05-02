from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('creator',views.creator,name="home"),
     path('user',views.user,name="home")
]
