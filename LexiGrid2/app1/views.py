from django.shortcuts import render,redirect

def home(request):
    return render(request,'app1/login.html')
def creator(request):
    # if 'reset' in request.GET:
    #     # Clear crossword session data
    #     request.session.flush()
    #     return redirect('home') 
    # # Check if crossword is already stored in session
    # if 'grid' in request.session and 'across_clues' in request.session and 'down_clues' in request.session:
    #     grid = json.loads(request.session['grid'])
    #     across_clues = json.loads(request.session['across_clues'])
    #     down_clues = json.loads(request.session['down_clues'])
    # else:
        # Generate new crossword
    grid, across_clues, down_clues = generate_crossword()
    
    # Store in session as JSON strings (since session data must be JSON-serializable)
    # request.session['grid'] = json.dumps(grid)
    # request.session['across_clues'] = json.dumps(across_clues)
    # request.session['down_clues'] = json.dumps(down_clues)
    clue_numbers = {(clue['row'], clue['col']): clue['num'] for clue in across_clues + down_clues}
    

# Build the indexed list with optional clue numbers
    indexed_list = [
        [
            {
                'row': i,
                'col': j,
                'letter': grid[i][j] if grid[i][j]!=" " else None,
                'clue_num': clue_numbers.get((i, j), None)
            }
            for j in range(len(grid))
        ]
        for i in range(len(grid))
    ]

    context = {
        'indexed_list': indexed_list,
        'across_clues': across_clues,
        'down_clues': down_clues,
    }
    return render(request, 'app1/creator.html', context)

def user(request):
    # if 'reset' in request.GET:
    #     # Clear crossword session data
    #     request.session.flush()
    #     return redirect('home') 
    # # Check if crossword is already stored in session
    # if 'grid' in request.session and 'across_clues' in request.session and 'down_clues' in request.session:
    #     grid = json.loads(request.session['grid'])
    #     across_clues = json.loads(request.session['across_clues'])
    #     down_clues = json.loads(request.session['down_clues'])
    # else:
        # Generate new crossword
    grid, across_clues, down_clues = generate_crossword()
    # Store in session as JSON strings (since session data must be JSON-serializable)
    # request.session['grid'] = json.dumps(grid)
    # request.session['across_clues'] = json.dumps(across_clues)
    # request.session['down_clues'] = json.dumps(down_clues)
    clue_numbers = {(clue['row'], clue['col']): clue['num'] for clue in across_clues + down_clues}

# Build the indexed list with optional clue numbers
    indexed_list = [
        [
            {
                'row': i,
                'col': j,
                'letter': grid[i][j] if grid[i][j]!=" " else None,
                'clue_num': clue_numbers.get((i, j), None)
            }
            for j in range(len(grid))
        ]
        for i in range(len(grid))
    ]

    context = {
        'indexed_list': indexed_list,
        'across_clues': across_clues,
        'down_clues': down_clues,
    }
    from datetime import datetime

# Generate crossword
    from datetime import datetime
    import os

# Get grid and clues
    grid, across_clues, down_clues = generate_crossword()

    if grid is not None and across_clues is not None and down_clues is not None:
        # Timestamp for filename
        timestamp = datetime.now().strftime("%Y_%m_%d_%H-%M")

        # Directory and filenames
        base_dir = r'E:\LexiGrid\LexiGrid2\Files'
        blank_file = os.path.join(base_dir, f'lexigrid_blank_{timestamp}.txt')
        filled_file = os.path.join(base_dir, f'lexigrid_filled_{timestamp}.txt')
        clue_file = os.path.join(base_dir, f'clue_{timestamp}.txt')  # Already used in generate_crossword

        os.makedirs(base_dir, exist_ok=True)

        # Save blank grid (hide letters with '.')
        with open(blank_file, 'a') as f:
            for row in grid:
                f.write(' '.join('.' if cell.isalpha() else cell for cell in row) + '\n')
            f.write('\n')

        # Save filled grid
        with open(filled_file, 'a') as f:
            for row in grid:
                f.write(' '.join(cell if cell.strip() else ' ' for cell in row) + '\n')
            f.write('\n')

        # Save clues (append to clue.txt)
        with open(clue_file, 'a') as f:
            f.write(f"\n=== Clues for crossword {timestamp} ===\n")
            f.write("Across:\n")
            for clue in across_clues:
                f.write(f"{clue['num']}. {clue['clue']} ({clue['length']})\n")
            f.write("Down:\n")
            for clue in down_clues:
                f.write(f"{clue['num']}. {clue['clue']} ({clue['length']})\n")
            f.write("\n")

    return render(request, 'app1/user.html', context)

import csv
import random
import os


# logger = logging.getLogger(__name__)

GRID_SIZE = 20
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_path = os.path.join(BASE_DIR,  'Questions','space.csv')


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
            for line in file:
                parts = line.strip().split(',', 1)
                if parts and parts[0].strip():
                    word = parts[0].strip().upper()
                    if word.isalpha():
                        words.append(word)
                        clues.append(parts[1].strip() if len(parts) > 1 else "No clue provided")
                    else:
                        unfitted_words.append(word)
    except FileNotFoundError:
        print("CSV file not found")
        return None, None, None
    except csv.Error:
        print("Invalid CSV format")
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
            'length':len(word)
        }
        if direction == "across":
            across_clues.append(entry)
        else:
            down_clues.append(entry)
    
    

    return grid, across_clues, down_clues
 


