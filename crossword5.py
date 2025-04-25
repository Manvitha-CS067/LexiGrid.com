import random

import csv
words = []
with open('physics2.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        if len(row) >= 2:  # Safely check row length
            words.append(row[0].strip().upper())
           

# Words to fit (sorted by length descending)

    
words.sort(key=len, reverse=True)

GRID_SIZE = 16
grid = [[" " for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
placed_words = []  # Stores (word, row, col, direction)

def get_index(row, col):
    """Convert 2D grid coordinates to 0-399 index"""
    return row * GRID_SIZE + col

def can_place(word, row, col, direction):
    """Check if word fits at position without conflicts"""
    length = len(word)

    # Reject negative starting coordinates
    if row < 0 or col < 0:
        return False

    # Check grid boundaries
    if direction == "across" and col + length > GRID_SIZE:
        return False
    if direction == "down" and row + length > GRID_SIZE:
        return False

    intersections = 0
    for i in range(length):
        r = row + (i if direction == "down" else 0)
        c = col + (i if direction == "across" else 0)

        # Ensure we stay within grid bounds during check
        if r < 0 or r >= GRID_SIZE or c < 0 or c >= GRID_SIZE:
            return False

        existing = grid[r][c]
        if existing != " ":
            if existing != word[i]:  # Mismatch
                return False
            intersections += 1
        else:
            # Check adjacent cells (perpendicular only)
            if direction == "across":
                if (row > 0 and grid[row - 1][c] != " ") or (row < GRID_SIZE - 1 and grid[row + 1][c] != " "):
                    return False
            elif direction == "down":
                if (col > 0 and grid[r][col - 1] != " ") or (col < GRID_SIZE - 1 and grid[r][col + 1] != " "):
                    return False

    # Check head and tail of word to prevent direct continuation into another word
    if direction == "across":
        if (col > 0 and grid[row][col - 1] != " ") or (col + length < GRID_SIZE and grid[row][col + length] != " "):
            return False
    else:
        if (row > 0 and grid[row - 1][col] != " ") or (row + length < GRID_SIZE and grid[row + length][col] != " "):
            return False

    # Require at least one intersection if not the first word
    if not placed_words:
        return True
    return intersections >= 1



def place_word(word, row, col, direction):
    """Commit word to grid"""
    for i in range(len(word)):
        r = row + (i if direction == "down" else 0)
        c = col + (i if direction == "across" else 0)
        grid[r][c] = word[i]
    placed_words.append((word, row, col, direction))

def find_best_location(word):
    """Find best position for word using existing letters"""
    for attempt in range(100):
        if placed_words:
            random_letter = random.choice(word)
            for (w, row, col, dir) in placed_words:
                for idx, char in enumerate(w):
                    if char == random_letter:
                        # Intersection point in existing word
                        base_row = row + (idx if dir == "down" else 0)
                        base_col = col + (idx if dir == "across" else 0)

                        # Try perpendicular directions
                        for new_dir in ["across", "down"]:
                            if new_dir != dir:
                                word_idx = word.index(random_letter)
                                start_row = base_row - (word_idx if new_dir == "down" else 0)
                                start_col = base_col - (word_idx if new_dir == "across" else 0)

                                # Ensure non-negative starting positions before checking placement
                                if start_row >= 0 and start_col >= 0:
                                    if can_place(word, start_row, start_col, new_dir):
                                        return start_row, start_col, new_dir
        else:
            # First word: random placement
            row = random.randint(0, GRID_SIZE - 1)
            col = random.randint(0, GRID_SIZE - 1)
            direction = random.choice(["across", "down"])
            if can_place(word, row, col, direction):
                return row, col, direction
    return None

# Generate crossword
for word in words:
    if len(word) > GRID_SIZE:
        print(f"Skipping {word} (too long)")
        continue
    
    location = find_best_location(word)
    if location:
        row, col, direction = location
        place_word(word, row, col, direction)
        print(f"Placed {word} at ({row},{col}) {direction}")
    else:
        print(f"Couldn't place {word}")

# Print crossword grid
print("\nFinal Crossword Grid (0-399 indices):")
for i, row in enumerate(grid):
    print(f"{i*GRID_SIZE:03}-{(i+1)*GRID_SIZE-1:03}: {' '.join(row)}")
for row in enumerate(grid):
    print(row)