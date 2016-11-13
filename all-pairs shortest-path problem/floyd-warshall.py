import sys
import math

class TestCase:
    def __init__(self, graph_size):
        self.graph = [[0 for y in range(graph_size)] for x in range(graph_size)]
        self.answer = 0
    def is_passed(self, actual_answer):
        return self.answer == actual_answer
    def parse_answer(self, line):
        self.answer = int(line.split(':')[1].strip())
    def add_graph_edge(self, line):
        (i, j, c) = tuple(map(int, line.split())) 
        self.graph[i-1][j-1] = c

def k_to_array_index(k):
    return k - 1

def k_as_point(k):
    return k - 1

inf = float('inf')

paths = [
    './tests/1.txt',
    './tests/2.txt'
]

for path in paths:    
    # ------------- Считывание тестового файла --------
    lines = open(path).read().splitlines()
    (points_count, edge_count) = tuple(map(int, lines[0].split())) # NOTE может ли быть несколько параллельных рёбер 
    case = TestCase(points_count)
    for line in lines[1:]:
        if (line.strip() == ''):
            continue
        if(line.find('Answer') != -1):
            case.answer = case.parse_answer(line)
            break
        case.add_graph_edge(line)       

sys.exit()

# ------------- Инициализация -----------
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

edge_length = -1
points_count = 5
A =[[[0 for k in range(points_count+1)] for j in range(points_count)]  for i in range(points_count)]
# ------------- Подсчёт --------------
for k in range(1,points_count+1):
    for i in range(points_count):
        for j in range(points_count):                      
            A[i][j][k] = min(A[i][j][k-1], A[i][k_as_point(k)][k-1] + A[k_as_point(k)][j][k-1])
            
            
# ------------- Проверка результатов ------------
