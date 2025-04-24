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

# Find the position of a letter in temp_grid
def pos(letter):
    for i in range(len(temp_grid)):
        for j in range(len(temp_grid[i])):
            if letter == temp_grid[i][j]:
                return i, j
    return None, None

# Clear temp_grid
def clear_grid():
    for i in range(len(temp_grid)):
        for j in range(len(temp_grid[i])):
            temp_grid[i][j] = " "

unfitted_words = []
fitted_words = []

# Place a word on the grid in the given direction
def place_word(word, start_row, start_col, direction):
    can_place = True

    for i in range(len(word)):
        if direction == "across":
            if start_col + len(word) > 16 or (grid[start_row][start_col + i] != " " and grid[start_row][start_col + i] != word[i]):
                can_place = False
                break
        elif direction == "down":
            if start_row + len(word) > 16 or (grid[start_row + i][start_col] != " " and grid[start_row + i][start_col] != word[i]):
                can_place = False
                break

    if not can_place:
        return False

    for i in range(len(word)):
        if direction == "across":
            grid[start_row][start_col + i] = word[i]
            temp_grid[start_row][start_col + i] = word[i]
        elif direction == "down":
            grid[start_row + i][start_col] = word[i]
            temp_grid[start_row + i][start_col] = word[i]

    fitted_words.append(word)
    return True

# Load answers and clues from CSV
answers = []
clues = []

with open('physics2.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        if len(row) >= 2:
            answers.append(row[0].strip().upper())
            clues.append(row[1].strip())

# Place the first word at the top-left corner
first_word = answers.pop(0)
place_word(first_word, 0, 0, "across")

# Alternate directions for placing words
direction_pattern = ["down", "across"] * 10

# Try placing remaining words
for idx, word in enumerate(answers[:19]):
    placed = False
    for letter in word:
        r, c = pos(letter)
        print(f"row -{r} column -{c} letter -{letter}")
        if r is not None:
            clear_grid()
            direction = direction_pattern[idx]
            before_place_grid = [row.copy() for row in grid]  # backup grid

            success = place_word(word, r, c, direction)

            if success:
                placed = True
                break
            else:
                grid = [row.copy() for row in before_place_grid]  # restore if failed

    if not placed:
        unfitted_words.append(word)

# Print final grid
print("\nFinal Grid:")
for row in grid:
    print(" ".join(row))

# Print unique unfitted and fitted words
unfitted_unique_values = list(set(unfitted_words))
print(f"\nUnfitted words: {unfitted_unique_values}")

fitted_unique_values = list(set(fitted_words))
print(f"Fitted words: {fitted_unique_values}")
