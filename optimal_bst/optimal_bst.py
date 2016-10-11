import sys
print(sys.version)

p = [0.05, 0.4, 0.08, 0.04, 0.1, 0.1, 0.23]
n = len(p)
A = [[0 for j in p] for i in p]
print(A)

s = 0
while s <= n-1:
    print('s = %d' % s)
    i = 0
    while i < n:
        print('i = %d' % i)
        minimum = 9999999 # meanwhile... =)
        
        p_sum = 0
        k = i
        j = i+s
        if j >= n:
            j = n - 1
        while k <= j:
            print('k = %d' % k)
            p_sum += p[k]       
            k += 1

        r = i
        while r <= j:
            print('r = %d' % r)
            if i <= r-1:                
                A1 = A[i][r-1]
            else:
                A1 = 0

            if r+1 <= j:                
                A2 = A[r+1][j]
            else:
                A2 = 0

            val = p_sum + A1 + A2
            if val < minimum:
                minimum = val

            r += 1
        A[i][j] = minimum      

        i += 1

    s += 1

print(A)
print(A[0][n-1])