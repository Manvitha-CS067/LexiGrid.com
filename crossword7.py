import csv
import random

# Initialize 16x16 grid
GRID_SIZE = 25

grid = [[" " for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
placed_words = []  # Stores (word, row, col, direction, clue_number, clue)
fitted_words = []
unfitted_words = []
clue_number = 1

# Load words and clues from CSV
words = []
clues = []
try:
    with open('physics3.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0].strip():  # Check non-empty first column
                word = row[0].strip().upper()
                if word.isalpha():  # Validate word (letters only)
                    words.append(word)
                    clues.append(row[1].strip() if len(row) > 1 else "No clue provided")
                else:
                    unfitted_words.append(word)
                    print(f"Skipped invalid word: {word}")
except FileNotFoundError:
    print("Error: physics2.csv not found.")
    exit(1)
except csv.Error:
    print("Error: Invalid CSV format.")
    exit(1)

# Sort words by length (descending)
word_lengths = [len(word) for word in words]


avg_length = sum(word_lengths) / len(words) if word_lengths else 1

print(avg_length)

if avg_length <(GRID_SIZE/2) :  # Threshold based on grid size
    words_with_clues = sorted(zip(words, clues), key=lambda x: len(x[0]), reverse=True)
else:
    words_with_clues = sorted(zip(words, clues), key=lambda x: len(x[0]), reverse=False)
words, clues = zip(*words_with_clues) if words_with_clues else ([], [])

def can_place(word, row, col, direction, require_intersection=True):
    """Check if word fits at position without conflicts"""
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
            if existing != word[i]:  # Mismatch
                return False
            intersections += 1
        else:
            # Check perpendicular adjacent cells
            if direction == "across":
                if (row > 0 and grid[row - 1][c] != " ") or (row < GRID_SIZE - 1 and grid[row + 1][c] != " "):
                    return False
            elif direction == "down":
                if (col > 0 and grid[r][col - 1] != " ") or (col < GRID_SIZE - 1 and grid[r][col + 1] != " "):
                    return False

    # Check head and tail
    if direction == "across":
        if (col > 0 and grid[row][col - 1] != " ") or (col + length < GRID_SIZE and grid[row][col + length] != " "):
            return False
    else:
        if (row > 0 and grid[row - 1][col] != " ") or (row + length < GRID_SIZE and grid[row + length][col] != " "):
            return False

    # Intersection requirement (optional)
    if require_intersection and placed_words:
        return intersections >= 1
    return True

def place_word(word, row, col, direction, clue_number, clue):
    """Commit word to grid"""
    for i in range(len(word)):
        r = row + (i if direction == "down" else 0)
        c = col + (i if direction == "across" else 0)
        grid[r][c] = word[i]
    
    for r1 in grid:
        print(r1)
    placed_words.append((word, row, col, direction, clue_number, clue))
    fitted_words.append(word)
    


def find_best_location(word):
    """Systematically find a position for the word"""
    # Shuffle placed words to vary intersection attempts
    placed_words_shuffled = placed_words[:]
    random.shuffle(placed_words_shuffled)

    if not placed_words:  # First word
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                for direction in ["across", "down"]:
                    if can_place(word, row, col, direction, require_intersection=False):
                        return row, col, direction
        return None

    # Try intersecting placements
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

    # Fallback: Try non-intersecting placements
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            for direction in ["across", "down"]:
                if can_place(word, row, col, direction, require_intersection=False):
                    return row, col, direction
    return None

# Generate crossword
for idx, (word, clue) in enumerate(zip(words, clues)):
    if len(word) > GRID_SIZE:
        unfitted_words.append(word)
        print(f"Skipping {word} (too long)")
        continue
    location = find_best_location(word)
    if location:
        row, col, direction = location
        place_word(word, row, col, direction, clue_number, clue)
        print(f"Placed {word} at ({row},{col}) {direction} (Clue {clue_number}: {clue})")
        clue_number += 1
    else:
        unfitted_words.append(word)
        print(f"Couldn't place {word}")

# Print crossword grid
print("\nCrossword Grid:")
print("   " + " ".join(f"{i:2}" for i in range(GRID_SIZE)))
print("  +" + "-+" * GRID_SIZE)
for i, row in enumerate(grid):
   
    print(f"{i:2}|{'|'.join(row)}|")
print("  +" + "-+" * GRID_SIZE)

# Print clue list
print("\nClues:")
print("Across:")
for word, row, col, direction, num, clue in sorted(placed_words, key=lambda x: x[4]):
    if direction == "across":
        print(f"{num}. {clue} ({word}) at ({row},{col})")
print("Down:")
for word, row, col, direction, num, clue in sorted(placed_words, key=lambda x: x[4]):
    if direction == "down":
        print(f"{num}. {clue} ({word}) at ({row},{col})")

# Print fitted and unfitted words
print("\nWord Summary:")
print(f"Fitted words: {sorted(list(set(fitted_words)))}")
print(f"Unfitted words: {sorted(list(set(unfitted_words)))}")