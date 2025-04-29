from django.urls import path
from app1.views import home, crossword_view, submit_answers, reset_crossword

urlpatterns = [
    path('', home, name='home'),
    path('crossword/', crossword_view, name='crossword'),
    path('submit-answers/', submit_answers, name='submit_answers'),
    path('reset/', reset_crossword, name='reset'),
]