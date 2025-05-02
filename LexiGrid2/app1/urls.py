from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('creator',views.creator,name="creator"),
     path('user',views.user,name="user"),
     path('',views.home,name="")
]
