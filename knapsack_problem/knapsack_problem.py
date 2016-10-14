# Ответ на первую проблему: 2493893

import sys

print(sys.version)
input_text = open('./inputs/input1.txt').read().splitlines()

first_line = input_text[0].split()
knapsack_size = int(first_line[0])
number_of_items = int(first_line[1])

print('knapsack_size = %d' % knapsack_size)
print('number_of_items = %d' % number_of_items)

V = [] 
W = []
for line in input_text[1:]:
    line_def = line.split()
    V.append(int(line_def[0]))
    W.append(int(line_def[1]))
V.insert(0,0)
W.insert(0,0)

print('solving...')

A = [[0 for i in range(knapsack_size+1)] for i in range(number_of_items+1)] #ASSUME ALL NUMBERS ARE POSITIVE!
# A[0] = [0 for i in range(knapsack_size+1)] no sense because of previous line

for i in range(1, number_of_items+1):
    vi = V[i]
    for x in range(knapsack_size+1):        
        wi = W[i]
            
        A[i][x] = max(
            A[i-1][x] if i-1>=0 else 0, 
            ((A[i-1][x-wi] + vi) if (wi<=x and i>0)else 0) )

print(A[number_of_items][knapsack_size])
print('finish')