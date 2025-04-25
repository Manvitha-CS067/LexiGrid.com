import csv
import random

# Initialize 16x16 grid
def create_grid():
    return [[" " for _ in range(20)] for _ in range(20)]

grid = create_grid()
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

# Sort words by length (descending) for better placement
words_with_clues = sorted(zip(words, clues), key=lambda x: len(x[0]), reverse=True)
words, clues = zip(*words_with_clues) if words_with_clues else ([], [])

def can_place(word, row, col, direction):
    """Check if word fits at position without conflicts"""
    length = len(word)
    if row < 0 or col < 0:
        return False
    if direction == "across" and col + length > 16:
        return False
    if direction == "down" and row + length > 16:
        return False

    intersections = 0
    for i in range(length):
        r = row + (i if direction == "down" else 0)
        c = col + (i if direction == "across" else 0)
        if r >= 16 or c >= 16:
            return False
        existing = grid[r][c]
        if existing != " ":
            if existing != word[i]:  # Mismatch
                return False
            intersections += 1
        else:
            # Check perpendicular adjacent cells
            if direction == "across":
                if (r > 0 and grid[r - 1][c] != " ") or (r < 15 and grid[r + 1][c] != " "):
                    return False
            elif direction == "down":
                if (c > 0 and grid[r][c - 1] != " ") or (c < 15 and grid[r][c + 1] != " "):
                    return False

    # Check head and tail to prevent continuation
    if direction == "across":
        if (col > 0 and grid[row][col - 1] != " ") or (col + length < 16 and grid[row][col + length] != " "):
            return False
    else:
        if (row > 0 and grid[row - 1][col] != " ") or (row + length < 16 and grid[row + length][col] != " "):
            return False

    # Require intersection if not first word
    return not placed_words or intersections >= 1

def place_word(word, row, col, direction, clue_number, clue):
    """Commit word to grid"""
    for i in range(len(word)):
        r = row + (i if direction == "down" else 0)
        c = col + (i if direction == "across" else 0)
        grid[r][c] = word[i]
    placed_words.append((word, row, col, direction, clue_number, clue))
    fitted_words.append(word)

def find_best_location(word):
    """Systematically find a position for the word"""
    if not placed_words:  # First word
        row = random.randint(0, 15)
        col = random.randint(0, 15)
        direction = random.choice(["across", "down"])
        if can_place(word, row, col, direction):
            return row, col, direction
    else:
        # Try all intersections with existing words
        for existing_word, erow, ecol, edir, _, _ in placed_words:
            for i, char in enumerate(existing_word):
                for letter in word:
                    if letter == char:
                        # Intersection point in existing word
                        base_row = erow + (i if edir == "down" else 0)
                        base_col = ecol + (i if edir == "across" else 0)
                        # Try perpendicular directions
                        for new_dir in ["across", "down"]:
                            if new_dir != edir:
                                word_idx = word.index(letter)
                                start_row = base_row - (word_idx if new_dir == "down" else 0)
                                start_col = base_col - (word_idx if new_dir == "across" else 0)
                                if start_row >= 0 and start_col >= 0:
                                    if can_place(word, start_row, start_col, new_dir):
                                        return start_row, start_col, new_dir
    return None

# Generate crossword
for idx, (word, clue) in enumerate(zip(words, clues)):
    if len(word) > 16:
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
print("   " + " ".join(f"{i:2}" for i in range(16)))
print("  +" + "-+" * 16)
for i, row in enumerate(grid):
    print(f"{i:2}|{'|'.join(row)}")
print("  +" + "-+" * 16)

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