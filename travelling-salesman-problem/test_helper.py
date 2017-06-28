import math
inf = float('inf')

class TestCase:
    def __init__(self, path, pointsCount):
        self.path = path
        self.points = []
        self.answer = None
    def __str__(self):
        return str(self.points)  
    def isPassed(self, actual_answer):
        return self.answer == actual_answer
    def _parseAnswer(self, line):
        self.answer = float(line.split(':')[1].strip())
    def setPoint(self, line):        
        (x, y) = tuple(map(float, line.split()))
        self.points.append((x, y))

def readCases(paths):
    cases = []
    for path in paths:    
        # ------------- Считывание тестового файла --------
        lines = open(path).read().splitlines()
        pointsCount = int(lines[0]) # !!!!!!!! NOTE может ли быть несколько параллельных рёбер     
        case = TestCase(path, pointsCount)
        for line in lines[1:]:
            if line.strip() == '':
                continue
            if line.find('Answer') != -1:
                case._parseAnswer(line)
                break
            case.setPoint(line)    
        cases.append(case)
    return cases