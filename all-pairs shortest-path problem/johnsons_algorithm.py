import sys
import math
import test_helper
import bellman_ford

# НЕ ЗАКОНЧЕН

inf = float('inf')

def k_as_point(k):
    return k - 1

def reweight(A):
    weights = []

    A_rew = A[:]
    for row in range(len(A_rew)):
        A_rew[row].append(inf)
    s_point_index = len(A) + 1
    A_rew.append([0 for i in range(s_point_index)])
    for j in range(len(A))
        weights[j] = bellman_ford(A_rew, s_point_index, j)

    return weights

def johnsons_algorithm(A):    
    print('floyd_warshall started...')    
    
    points_count = len(A[0])
    print('points_count: {}'.format(points_count))
    
    print('reweighting')
    weights = reweight(A)
    

    result = None    
    
    pass

paths_to_cases = [
    './tests/1.txt',
    './tests/2.txt',
    './tests/3.txt',
    './tests/4.txt',
    './tests/5.txt',
    './tests/g1b.txt',
    './tests/g2b.txt',
    './tests/g3b.txt',
    './tests/wiki.txt' #? может быть ошибка,
]

'''
paths_to_cases = [
    './g1.txt', # Negative cost cycle
    './g2.txt', # Negative cost cycle
    './g3.txt'  # -19
]
'''

cases = test_helper.read_cases(paths_to_cases)

# ------------- Проверка результатов ------------
for case in cases:    
    print('path_to_case: {},\nexpected_answer: {}'.format(case.path_to_case, case.answer))    
    actual_answer = johnsons_algorithm(case.graph)
    print('actual_answer: {}'.format(actual_answer) )  
    if(case.answer is not None):
        if case.is_passed(actual_answer):
            print('Test case SUCCEEDED!')
        else:
            print('Test case FAILED!')
    print('--------')