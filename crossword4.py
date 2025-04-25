import csv

# Initialize 16x16 grids
def create_grid():
    grid = []
    for i in range(16):
        row = []
        for j in range(16):
            row.append(" ")
        grid.append(row)
    return grid

grid = create_grid()
temp_grid = create_grid()

def pos(letter):
    for i in range(len(temp_grid)):
        for j in range(len(temp_grid[i])):
            if letter == temp_grid[i][j]:
                return i, j
    return None, None

def clear_grid():
    for i in range(len(temp_grid)):
        for j in range(len(temp_grid[i])):
            temp_grid[i][j] = " "

unfitted_words = []
fitted_words = []

def place_word(word, start_row, start_col, direction):
    # Check if word fits and has no conflicts
    if direction == "across":
        if start_col + len(word) > 16:
            unfitted_words.append(word)
            return False
        for i in range(len(word)):
            current = grid[start_row][start_col + i]
            if current != ' ' and current != word[i]:
                unfitted_words.append(word)
                return False
    elif direction == "down":
        if start_row + len(word) > 16:
            unfitted_words.append(word)
            return False
        for i in range(len(word)):
            current = grid[start_row + i][start_col]
            if current != ' ' and current != word[i]:
                unfitted_words.append(word)
                return False
    # Place word if valid
    if direction == "across":
        for i in range(len(word)):
            grid[start_row][start_col + i] = word[i]
            temp_grid[start_row][start_col + i] = word[i]
    elif direction == "down":
        for i in range(len(word)):
            grid[start_row + i][start_col] = word[i]
            temp_grid[start_row + i][start_col] = word[i]
    fitted_words.append(word)
    return True

# Load answers and clues
answers = []
clues = []
try:
    with open('physics2.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 2 and row[0].strip():
                answers.append(row[0].strip().upper())
                clues.append(row[1].strip())
except FileNotFoundError:
    print("Error: physics2.csv file not found.")
    exit(1)

# Place the first word: OPTICS
if answers:
    first_word = answers.pop(0)
    if first_word == "OPTICS":
        place_word(first_word, 0, 0, "across")
    else:
        print("Error: First word must be OPTICS.")
        unfitted_words.append(first_word)
else:
    print("Error: No words in CSV.")
    exit(1)

# Define a direction pattern
direction_pattern = ["down", "across"] * 10
for idx, word in enumerate(answers[:19]):
    # Skip invalid words (e.g., all lowercase or non-letters)
    if not word.isalpha() or word.islower():
        unfitted_words.append(word)
        print(f"Skipped invalid word: {word}")
        continue
    placed = False
    for letter in word:
        r, c = pos(letter)
        print(f"row -{r} column -{c} letter -{letter}")
        if r is not None:
            clear_grid()
            direction = direction_pattern[idx % len(direction_pattern)]
            start_row = r - (word.index(letter) if direction == "down" else 0)
            start_col = c - (word.index(letter) if direction == "across" else 0)
            if start_row >= 0 and start_col >= 0 and (start_col + (len(word) if direction == "across" else 0) <= 16) and (start_row + (len(word) if direction == "down" else 0) <= 16):
                if place_word(word, start_row, start_col, direction):
                    placed = True
                    break
    if not placed:
        unfitted_words.append(word)
        print(f"No match for {word}, moving to next word")

# Print final grid
for row in grid:
    print(row)

# Print fitted and unfitted words (unique)
fitted_unique_values = sorted(list(set(fitted_words)))
unfitted_unique_values = sorted(list(set(unfitted_words)))
print(f"fitted words {fitted_unique_values}")
print(f"Unfitted words {unfitted_unique_values}")