N = 2000

def fact(N):
    if(N == 2):
        return 2

    return N * fact(N - 1)

fact1 = 1
for i in range(2, N + 1):
    fact1 *= i

fact2 = fact(N)

if fact1 == fact2:
    print('CORRECT')
else:
    print('WRONG')