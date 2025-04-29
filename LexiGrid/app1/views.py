from django.shortcuts import render
from .crossword_generator import generate_crossword
from django.http import HttpResponse

def home(request):
    """
    Renders the homepage with the crossword clues and grid. 
    If the grid is not already in the session, generate it and store it in the session.
    """
    # Check if the crossword grid already exists in the session
    if 'grid' not in request.session:
        # Generate new grid and store it in the session
        grid, across_clues, down_clues = generate_crossword()
        request.session['grid'] = grid
        request.session['across_clues'] = across_clues
        request.session['down_clues'] = down_clues
    else:
        # Use the grid already stored in the session
        grid = request.session['grid']
        across_clues = request.session['across_clues']
        down_clues = request.session['down_clues']
    
    context = {
        'across_clues': across_clues,
        'down_clues': down_clues,
        'grid': grid
    }

    return render(request, 'app1/index.html', context)


def crossword_view(request):
    """
    Renders the page with the crossword grid. 
    This page will use the grid stored in the session.
    """
    # Check if the crossword grid exists in the session
    if 'grid' not in request.session:
        return HttpResponse("No crossword generated yet. Please visit the homepage first.")

    # Use the grid already stored in the session
    grid = request.session['grid']

    context = {
        'grid': grid
    }

    return render(request, 'app1/crossword.html', context)
