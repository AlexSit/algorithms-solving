import math
inf = float('inf')

class TestCase:
    def __init__(self, path_to_case, points_count):
        self.path_to_case = path_to_case
        self.points = []
        self.answer = None
    def __str__(self):
        return str(self.points)  
    def is_passed(self, actual_answer):
        return self.answer == actual_answer
    def parse_answer(self, line):
        self.answer = float(line.split(':')[1].strip())
    def set_point(self, line):        
        (x, y) = tuple(map(float, line.split()))
        self.points.append((x, y))

def read_cases(paths_to_cases):
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
            case.set_point(line)    
        cases.append(case)
    return cases