from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

import json
# crossword_generator.py
import csv
import random
import os

GRID_SIZE = 20
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_path = os.path.join(BASE_DIR, 'app1', 'physics3.csv')


def generate_crossword():
    # Initialize grid and variables
    grid = [[" " for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    placed_words = []
    fitted_words = []
    unfitted_words = []
    clue_number = 1

    words = []
    clues = []
    try:
        with open(csv_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0].strip():
                    word = row[0].strip().upper()
                    if word.isalpha():
                        words.append(word)
                        clues.append(row[1].strip() if len(row) > 1 else "No clue provided")
                    else:
                        unfitted_words.append(word)
    except FileNotFoundError:
        print("Error: CSV not found.")
        return None, None, None
    except csv.Error:
        print("Error: Invalid CSV format.")
        return None, None, None

    word_lengths = [len(word) for word in words]
    avg_length = sum(word_lengths) / len(words) if word_lengths else 1

    if avg_length < (GRID_SIZE/2):
        words_with_clues = sorted(zip(words, clues), key=lambda x: len(x[0]), reverse=True)
    else:
        words_with_clues = sorted(zip(words, clues), key=lambda x: len(x[0]), reverse=False)

    words, clues = zip(*words_with_clues) if words_with_clues else ([], [])

    def can_place(word, row, col, direction, require_intersection=True):
        length = len(word)
        if row < 0 or col < 0:
            return False
        if direction == "across" and col + length > GRID_SIZE:
            return False
        if direction == "down" and row + length > GRID_SIZE:
            return False

        intersections = 0
        for i in range(length):
            r = row + (i if direction == "down" else 0)
            c = col + (i if direction == "across" else 0)
            if r >= GRID_SIZE or c >= GRID_SIZE:
                return False
            existing = grid[r][c]
            if existing != " ":
                if existing != word[i]:
                    return False
                intersections += 1
            else:
                if direction == "across":
                    if (row > 0 and grid[row - 1][c] != " ") or (row < GRID_SIZE - 1 and grid[row + 1][c] != " "):
                        return False
                elif direction == "down":
                    if (col > 0 and grid[r][col - 1] != " ") or (col < GRID_SIZE - 1 and grid[r][col + 1] != " "):
                        return False

        if direction == "across":
            if (col > 0 and grid[row][col - 1] != " ") or (col + length < GRID_SIZE and grid[row][col + length] != " "):
                return False
        else:
            if (row > 0 and grid[row - 1][col] != " ") or (row + length < GRID_SIZE and grid[row + length][col] != " "):
                return False

        if require_intersection and placed_words:
            return intersections >= 1
        return True

    def place_word(word, row, col, direction, clue_number, clue):
        for i in range(len(word)):
            r = row + (i if direction == "down" else 0)
            c = col + (i if direction == "across" else 0)
            grid[r][c] = word[i]
           

        placed_words.append((word, row, col, direction, clue_number, clue))
        fitted_words.append(word)

    def find_best_location(word):
        placed_words_shuffled = placed_words[:]
        random.shuffle(placed_words_shuffled)

        if not placed_words:
            for row in range(GRID_SIZE):
                for col in range(GRID_SIZE):
                    for direction in ["across", "down"]:
                        if can_place(word, row, col, direction, require_intersection=False):
                            return row, col, direction
            return None

        for existing_word, erow, ecol, edir, _, _ in placed_words_shuffled:
            for i, char in enumerate(existing_word):
                for letter in word:
                    if letter == char:
                        base_row = erow + (i if edir == "down" else 0)
                        base_col = ecol + (i if edir == "across" else 0)
                        for new_dir in ["across", "down"]:
                            if new_dir != edir:
                                word_idx = word.index(letter)
                                start_row = base_row - (word_idx if new_dir == "down" else 0)
                                start_col = base_col - (word_idx if new_dir == "across" else 0)
                                if start_row >= 0 and start_col >= 0:
                                    if can_place(word, start_row, start_col, new_dir):
                                        return start_row, start_col, new_dir

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                for direction in ["across", "down"]:
                    if can_place(word, row, col, direction, require_intersection=False):
                        return row, col, direction
        return None

    # Build crossword
    for idx, (word, clue) in enumerate(zip(words, clues)):
        if len(word) > GRID_SIZE:
            unfitted_words.append(word)
            continue
        location = find_best_location(word)
        if location:
            row, col, direction = location
            place_word(word, row, col, direction, clue_number, clue)
            clue_number += 1
        else:
            unfitted_words.append(word)

    across_clues = []
    down_clues = []

    for word, row, col, direction, num, clue in sorted(placed_words, key=lambda x: x[4]):
        entry = {
            'num': num,
            'clue': clue,
            'answer': word,
            'row': row,
            'col': col,
        }
        if direction == "across":
            across_clues.append(entry)
        else:
            down_clues.append(entry)
    print(across_clues)
    for row in grid:
        print(row)

    return grid,across_clues,down_clues
def home(request):
    """
    Renders the homepage with crossword clues and a link to play.
    Generates a new crossword if not in session.
    """
    try:
        if 'grid' not in request.session:
            grid, across_clues, down_clues = generate_crossword()
            if not grid or not across_clues or not down_clues:
                return HttpResponse("Error generating crossword. Please try again.", status=500)
            
            # Store in session with 1-hour expiry
            request.session['grid'] = grid
            request.session['across_clues'] = across_clues
            request.session['down_clues'] = down_clues
            request.session['user_grid'] = [[" " for _ in range(20)] for _ in range(20)]
            request.session.set_expiry(3600)
        else:
            grid = request.session['grid']
            across_clues = request.session['across_clues']
            down_clues = request.session['down_clues']

        context = {
            'across_clues': across_clues,
            'down_clues': down_clues,
        }
        return render(request, 'app1/index.html', context)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)

def crossword_view(request):
    """
    Renders the crossword grid and clues using session data.
    """
    try:
        if 'grid' not in request.session:
            return HttpResponse("No crossword generated yet. Please visit the homepage first.", status=400)

        grid = request.session['grid']
        user_grid = request.session.get('user_grid', [[" " for _ in range(20)] for _ in range(20)])
        across_clues = request.session['across_clues']
        down_clues = request.session['down_clues']

        context = {
            'grid': grid,
            'user_grid': user_grid,
            'across_clues': across_clues,
            'down_clues': down_clues,
        }
        return render(request, 'app1/crossword.html', context)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)

def submit_answers(request):
    """
    Submits user answers and checks if all are correct.
    Expects POST with user_grid (20x20 array of letters or spaces).
    Returns JSON with all_correct boolean.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    try:
        if 'grid' not in request.session:
            return JsonResponse({'error': 'No crossword in session'}, status=400)

        user_grid = json.loads(request.body).get('user_grid')
        correct_grid = request.session['grid']

        if not user_grid or len(user_grid) != 20 or any(len(row) != 20 for row in user_grid):
            return JsonResponse({'error': 'Invalid grid size'}, status=400)

        # Update user_grid in session
        request.session['user_grid'] = user_grid
        request.session.modified = True

        # Check correctness
        all_correct = True
        for r in range(20):
            for c in range(20):
                if correct_grid[r][c] != " " and user_grid[r][c].upper() != correct_grid[r][c]:
                    all_correct = False
                    break
            if not all_correct:
                break

        return JsonResponse({
            'all_correct': all_correct,
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def reset_crossword(request):
    """
    Clears the session and redirects to the homepage.
    """
    request.session.flush()
    return render(request, 'app1/index.html')