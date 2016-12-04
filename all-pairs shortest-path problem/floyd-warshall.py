import sys
import math

inf = float('inf')

class TestCase:
    def __init__(self, path_to_case, graph_size):
        self.path_to_case = path_to_case
        self.graph = [[inf if i != j else 0 for j in range(graph_size)] for i in range(graph_size)]
        self.answer = None
    def __str__(self):
        return str(self.graph)  
    def is_passed(self, actual_answer):
        return self.answer == actual_answer
    def parse_answer(self, line):
        self.answer = int(line.split(':')[1].strip())
    def set_graph_edge(self, line):        
        (i, j, c) = tuple(map(int, line.split())) 
        self.graph[i-1][j-1] = c      

def k_as_point(k):
    return k - 1

def floyd_warshall(A):    
    print('floyd_warshall started...')
    points_count = len(A[0])
    print('points_count: {}'.format(points_count))
    result = None    
    for k in range(1,points_count+1):
        #if(k %  100 == 0):
        #    print('K % 100! == 0')    
        #print('k = {}'.format(k))
        for i in range(points_count):
            #if(i % 500 == 0):
            #    print(i)
            for j in range(points_count):                  
                optimal_solution = min(
                    A[i][j], 
                    A[i][k_as_point(k)] + A[k_as_point(k)][j])  
                A[i][j] = optimal_solution
                #print((i,j,optimal_solution))
                #print(j)
                #if optimal_solution == -7:                            
                #    print('AHA!')
                #    print('result = {}'.format(result))
                if k+1 >= points_count:
                    if (result is None) or (optimal_solution < result):   
                        #if result == -7:                            
                        #    print('AHA!')
                        #    print(optimal_solution)                            
                        result = optimal_solution

                if(i == j and A[i][j] < 0):
                    print('NEGATIVE COST CYCLE!!!!!!!!!!!!!!!!!!!!!!!')
                    return None
    return result                    

'''
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

cases = []
for path_to_case in paths_to_cases:    
    # ------------- Считывание тестового файла --------
    lines = open(path_to_case).read().splitlines()
    (points_count, edge_count) = tuple(map(int, lines[0].split())) # !!!!!!!! NOTE может ли быть несколько параллельных рёбер     
    case = TestCase(path_to_case, points_count)
    for line in lines[1:]:
        if (line.strip() == ''):
            continue
        if(line.find('Answer') != -1):
            case.parse_answer(line)
            break
        case.set_graph_edge(line)    
    cases.append(case)

# ------------- Проверка результатов ------------
for case in cases:
    #print(case)
    print('path_to_case: {},\nexpected_answer: {}'.format(case.path_to_case, case.answer))    
    actual_answer = floyd_warshall(case.graph)
    print('actual_answer: {}'.format(actual_answer) )  
    if(case.answer is not None):
        if case.is_passed(actual_answer):
            print('Test case SUCCEEDED!')
        else:
            print('Test case FAILED!')
    print('--------')