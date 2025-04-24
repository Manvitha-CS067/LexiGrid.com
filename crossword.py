grid = []

for i in range(8):
    row = []  
    for j in range(8):  
        row.append(" ") 
    grid.append(row)    
print(grid)



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
    print(i)
    grid[0][i] = first_word[i]
   
print(grid)



#prism
answers = [word for word in answers if word != first_word]
print(answers)
for index,letter in enumerate(answers[0]):
   
    for i in first_word:
       
       if letter==i:
           
           for i in range(1,len(answers[0])):
             grid[i][1]=(answers[0])[i]
       
    break
first_word=answers[0]    
     




#indigo

answers = [word for word in answers if word != first_word]
first_word=answers[0]
print(answers)

for index,letter in enumerate(answers[0]):
    
    for i in first_word:
       if letter==i:
          
          for i in range(2,len(answers[0])+1):
             grid[2][i]=(answers[0])[i-1]
             
    break
first_word=answers[0]
for row in grid:  
    print(row)


answers = [word for word in answers if word != first_word]
first_word=answers[0]
for index,letter in enumerate(answers[0]):
    
    for i in first_word:
       if letter==i:
           print(index,"  ",letter)

          
           for i in range(3,len(answers[0])+2):
             grid[i][3]=(answers[0])[i-2]
    break
first_word=answers[0]
for row in grid:  
    print(row)

answers = [word for word in answers if word != first_word]
first_word=answers[0]
for index,letter in enumerate(answers[0]):
     for i in first_word:
       if letter==i:
       
        
           print(index,"  ",letter)
           for i in range(4,len(answers[0])+3):
             grid[4][i]=(answers[0])[i-3]
     break
first_word=answers[0]
for row in grid:  
    print(row)

answers = [word for word in answers if word != first_word]
first_word=answers[0]
for index,letter in enumerate(answers[0]):
    
    for i in first_word:
       if letter==i:
         
           print(index,"  ",letter)
           for i in range(5,len(answers[0])+4):
             grid[i][7]=(answers[0])[i-4]
    break
first_word=answers[0]
for row in grid:  
    print(row)


print(answers)

           
# for row in grid:  
#     print(row)



