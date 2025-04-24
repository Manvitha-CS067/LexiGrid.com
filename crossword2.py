grid = []

for i in range(8):
    row = []  
    for j in range(8):  
        row.append(" ") 
    grid.append(row)    


grid2 = []

for i in range(8):
    row = []  
    for j in range(8):  
        row.append(" ") 
    grid2.append(row)    


def pos(letter):
    for i in range(len(grid2)):
        for j in range(len(grid2[i])):  # safer: loop over length of row
            if letter == grid2[i][j]:
                return i, j
                

def clear_grid():
    for i in range(len(grid2)):
        for j in range(len(grid2[i])):  # safer: loop over length of row
            grid2[i][j]=" "
                





import csv
file_name='physics.csv'
answers=[]
clues=[]
with open(file_name,'r') as file:
    reader=csv.reader(file)
    for row in reader:
        answers.append(row[0])
        clues.append(row[1])

        print(row)
    print(reader)
print(answers)
print(clues)

first_word = answers[0]
print(first_word)
direction=['across','down','across','down','across']

# Place the word starting at (0, 0)
for i in range(len(first_word)):
    
    grid[0][i] = first_word[i]
    grid2[0][i]=first_word[i]
   
print(grid)


#prism
answers = [word for word in answers if word != first_word]
first_word
print(answers)
for i in first_word:
    print(i)
    for index,letter in enumerate(answers[0]):
   
       if letter==i:
           r,c=pos(letter)
           print(r," ------",c,"------",letter)
           clear_grid()
           for i in range(1,len(answers[0])+(r-1)):
             grid[i][c]=(answers[0])[i]
             
             grid2[i][c]=(answers[0])[i]
             
    break
first_word=answers[0]    
     




#indigo

answers = [word for word in answers if word != first_word]
first_word=answers[0]
for i in first_word:
    for index,letter in enumerate(answers[0]):
    
    
       if letter==i:
          r,c=pos(letter)
          print(r," ------",c,"------",letter)
          clear_grid()
          for i in range(2,len(answers[0])+1):
             grid[r][i]=(answers[0])[i-1]
             
             grid2[r][i]=(answers[0])[i-1]
             
    break
first_word=answers[0]



answers = [word for word in answers if word != first_word]
first_word=answers[0]

    
for i in first_word:
    for index,letter in enumerate(answers[0]):
       if letter==i:
           
           r,c=pos(letter)
           print(r," ------",c,"------",letter)
           clear_grid()
          
           for i in range(3,len(answers[0])+(c-1)):
             grid[i][c]=(answers[0])[i-(c-1)]
             grid2[i][c]=(answers[0])[i-2]
    break
first_word=answers[0]


answers = [word for word in answers if word != first_word]
first_word=answers[0]
for i in first_word:
    for index,letter in enumerate(answers[0]):
    
       if letter==i:
           r,c=pos(letter)
           print(r," ------",c,"------",letter)
           clear_grid()
        
           for i in range(4,len(answers[0])+3):
             grid[r][i]=(answers[0])[i-3]
             grid2[r][i]=(answers[0])[i-3]
    break
first_word=answers[0]



answers = [word for word in answers if word != first_word]
first_word=answers[0]
for i in first_word:
    for index,letter in enumerate(answers[0]):
    
    
       if letter==i:
           r,c=pos(letter)
           print(r," ------",c,"------",letter)
           clear_grid()
           
           for i in range(5,len(answers[0])+4):
             grid[i][c]=(answers[0])[i-4]
             grid2[i][c]=(answers[0])[i-4]
    break
first_word=answers[0]

for row in grid:  
    print(row)




           
# for row in grid:  
#     print(row)



