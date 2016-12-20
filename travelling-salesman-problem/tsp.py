import sys
import math
import test_helper

inf = float('inf')

def tsp(points):
    init BaseCase

    n = len(points)
    for m in range(2, n+1):
        for each S:
            for each j in S:
                if j != 1:
                    min_result = inf
                    for k in S:
                        if k != j:
                            if min_result > A[S - j][k] + C[k][j]:
                                min_result = A[S - j][k] + C[k][j]
                    A[S][j] = min_result
    
    result = inf
    for j in range(2, n+1):
        if result > A[fullSet, j] + C[j][1]:
            result = A[fullSet, j] + C[j][1]
    return result

paths_to_cases = [
    './inputs/1.txt',
    './inputs/2.txt'    
]

'''
paths_to_cases = [
    './inputs/tsp.txt',    
]
'''

cases = []
for path_to_case in paths_to_cases:    
    # ------------- Считывание тестового файла --------
    lines = open(path_to_case).read().splitlines()
    points_count = int(lines[0])
    case = test_helper.TestCase(path_to_case, points_count)
    for line in lines[1:]:
        if (line.strip() == ''):
            continue
        if(line.find('Answer') != -1):
            case.parse_answer(line)
            break
        case.set_point(line)        
    cases.append(case)

# ------------- Проверка результатов ------------
for case in cases:
    #print(case)
    print('path_to_case: {},\nexpected_answer: {}'.format(case.path_to_case, case.answer))    
    actual_answer = tsp(case.points)
    print('actual_answer: {}'.format(actual_answer) )  
    if(case.answer is not None):
        if case.is_passed(actual_answer):
            print('Test case SUCCEEDED!')
        else:
            print('Test case FAILED!')
    print('--------')