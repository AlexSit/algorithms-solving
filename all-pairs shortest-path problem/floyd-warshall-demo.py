import math

def k_to_array_index(k):
    return k - 1

def k_as_point(k):
    return k - 1

inf = float('inf')

edge_length = -1
points_count = 5
A =[[[0 for k in range(points_count+1)] for j in range(points_count)]  for i in range(points_count)]

if(points_count == 3):
    A[0][0][0] = 0 
    A[0][1][0] = edge_length
    A[0][2][0] = inf

    A[1][0][0] = inf
    A[1][1][0] = 0
    A[1][2][0] = edge_length

    A[2][0][0] = edge_length
    A[2][1][0] = inf
    A[2][2][0] = 0
elif(points_count == 4):
    A[0][0][0] = 0 
    A[0][1][0] = edge_length
    A[0][2][0] = inf
    A[0][3][0] = inf

    A[1][0][0] = inf
    A[1][1][0] = 0
    A[1][2][0] = edge_length
    A[1][3][0] = inf
    
    A[2][0][0] = inf
    A[2][1][0] = inf
    A[2][2][0] = 0
    A[2][3][0] = edge_length
    
    A[3][0][0] = edge_length
    A[3][1][0] = inf
    A[3][2][0] = inf
    A[3][3][0] = 0
elif(points_count == 5):
    A[0][0][0] = 0 
    A[0][1][0] = edge_length
    A[0][2][0] = 1
    A[0][3][0] = inf
    A[0][4][0] = inf

    A[1][0][0] = inf
    A[1][1][0] = 0
    A[1][2][0] = edge_length
    A[1][3][0] = edge_length
    A[1][4][0] = inf
    
    A[2][0][0] = inf
    A[2][1][0] = inf
    A[2][2][0] = 0
    A[2][3][0] = edge_length
    A[2][4][0] = edge_length
    
    A[3][0][0] = edge_length
    A[3][1][0] = inf
    A[3][2][0] = inf
    A[3][3][0] = 0
    A[3][4][0] = edge_length

    A[4][0][0] = edge_length
    A[4][1][0] = edge_length
    A[4][2][0] = inf
    A[4][3][0] = inf
    A[4][4][0] = 0

print(A)

for k in range(1,points_count+1):
    for i in range(points_count):
        for j in range(points_count):                      
            A[i][j][k] = min(A[i][j][k-1], A[i][k_as_point(k)][k-1] + A[k_as_point(k)][j][k-1])
            #print((i,j,k))
            #print('----------')
            
if(points_count != 5):
    print(A[0][1][points_count])
    print(A[0][2][points_count])
    print(A[0][3][points_count])
    print(A[1][0][points_count])
    print(A[1][2][points_count])
    print(A[1][3][points_count])
    print(A[2][0][points_count])
    print(A[2][1][points_count])
    print(A[2][3][points_count])
    print(A[3][0][points_count])
    print(A[3][1][points_count])
    print(A[3][2][points_count])
else:
    print(A[0][1][points_count])
    print(A[0][2][points_count])
    print(A[0][3][points_count])
    print(A[0][4][points_count])    
    print(A[1][0][points_count])
    print(A[1][2][points_count])
    print(A[1][3][points_count])
    print(A[1][4][points_count])
    print(A[2][0][points_count])
    print(A[2][1][points_count])
    print(A[2][3][points_count])
    print(A[2][4][points_count])
    print(A[3][0][points_count])
    print(A[3][1][points_count])
    print(A[3][2][points_count])
    print(A[3][4][points_count])
    print(A[4][0][points_count])
    print(A[4][1][points_count])
    print(A[4][2][points_count])
    print(A[4][3][points_count])