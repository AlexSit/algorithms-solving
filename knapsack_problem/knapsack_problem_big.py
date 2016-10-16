# Ответ на первую проблему: 2493893
# Ответ на вторую проблему: 4243395
import sys
from fractions import gcd
import math

def get_gcd(l):
    divisor = None
    for i in l:
        if(divisor is None):
            divisor = i
        else:
            divisor = gcd(divisor, i)    
    return divisor    

print(sys.version)
input_text = open('./inputs/input2.txt').read().splitlines()

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

v_gcd = get_gcd(V)
w_gcd = get_gcd(W)
print(v_gcd)
print(w_gcd)

V = [int(i/v_gcd) for i in V]
W = [int(i/w_gcd) for i in W]
knapsack_size = math.floor(knapsack_size / w_gcd)

A = [[0 for i in range(knapsack_size+1)] for i in range(2)] #ASSUME ALL NUMBERS ARE POSITIVE!

for i in range(1, number_of_items+1):
    vi = V[i]
    for x in range(knapsack_size+1):        
        wi = W[i]
            
        A[1][x] = max(
            A[0][x], 
            ((A[0][x-wi] + vi) if (wi<=x) else 0) )
    A[0] = A[1][:]

answer_by_gcd = A[1][knapsack_size]
answer = answer_by_gcd * v_gcd
print(answer)
print('finish')