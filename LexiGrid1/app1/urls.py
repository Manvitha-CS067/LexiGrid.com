from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('crossword/', views.crossword_view, name='crossword'),
    path('submit/', views.submit_answers, name='submit'),
    path('results/', views.results, name='results'),
    path('reset/', views.reset_crossword, name='reset'),
    path('debug-session/', views.debug_session, name='debug_session'),
]