import csv

# Initialize 8x8 grids
def create_grid():
    grid = []
    for i in range(20):
        row = []
        for j in range(20):
            row.append(" ")
        grid.append(row)
    return grid

grid = create_grid()
temp_grid = create_grid()

def pos(letter):
    for i in range(len(temp_grid)):
        for j in range(len(temp_grid[i])):
            if letter == temp_grid[i][j] :
                return i, j
            
    return None, None

def clear_grid():
    for i in range(len(temp_grid)):
        for j in range(len(temp_grid[i])):
            temp_grid[i][j] = " "

unfitted_words=[]
fitted_words=[]

def place_word(word, start_row, start_col, direction):
    for i in range(len(word)):
        
            if direction == "across":
                if start_col+len(word)<=16:
                    if grid[start_row][start_col + i] == ' ':
                        grid[start_row][start_col + i] = word[i]
                        temp_grid[start_row][start_col + i] = word[i]
                    fitted_words.append(word)
                else:
                    unfitted_words.append(word)
                
            elif direction == "down":
                 if start_row + len(word) <=16:
                    if  grid[start_row + i][start_col] ==' ':
                        grid[start_row + i][start_col] = word[i]
                        temp_grid[start_row + i][start_col] = word[i]
                    fitted_words.append(word)
                 else:
                    unfitted_words.append(word)
                 
            


# Load answers and clues
answers = []
clues = []
with open('physics3.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        if len(row) >= 2:  # Safely check row length
            answers.append(row[0].strip().upper())
            clues.append(row[1].strip())

# Place the first word
first_word = answers.pop(0)
place_word(first_word, 0, 0, "across")

# Define a direction pattern
direction_pattern = ["down", "across"]*10
for idx, word in enumerate(answers[:19]):
    for letter in word:
        r, c = pos(letter)
        print(f"row -{r} column -{c} letter -{letter}")
        if r is not None or c is not None:
            clear_grid()
            if direction_pattern[idx] == "down":
                place_word(word, r, c, "down")
            else:
                place_word(word, r, c, "across")
            break
    continue
            
 

# Print final grid
for row in grid:
    print(row)



fitted_unique_values = []
for item in fitted_words:
    if item not in fitted_unique_values:
        fitted_unique_values.append(item)
print(f"fitted words {fitted_unique_values}")

for word in answers:
    if word not in fitted_words:
        unfitted_words.append(word)

unfitted_unique_values = []
for item in unfitted_words:
    if item not in unfitted_unique_values:
        unfitted_unique_values.append(item)
print(f"Unfitted words{unfitted_unique_values}")


           