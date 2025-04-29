# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('crossword/', views.crossword_view, name='crossword'),
    path('',views.home,name="home")
]
