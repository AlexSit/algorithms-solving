import sys
import math
from test_helper import *
import time

# from set_indexed_by_list import SetIndexedByList
from set_indexed_by_collection import SetIndexedByTuple
from collection_generator import generateTuplesWithoutReturnInAscending

from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

def calcDistance(x1, y1, x2, y2): return math.sqrt(math.pow(x1-x2, 2) + math.pow(y1-y2, 2))

def calcDistances(points):    
    length = len(points)
    result = [[0 for j in range(length)] for i in range(length)]

    for i in range(length):
        for j in range(i+1, length):
            dist = calcDistance(points[i][0], points[i][1], points[j][0], points[j][1])
            if(dist != 0):
                result[i][j] = dist
                result[j][i] = dist
            else:
                del points[j]
    return result

inf = float('inf')

inputCases = [
    InputCase('./inputs/1.txt', True),
    InputCase('./inputs/2.txt', True),
    InputCase('./inputs/tsp.txt', False)
]

def setsAsymDiff(set1, set2): # NOTE возвращается сет, а не список
    return set1 ^ set2

def tsp(path, points, distances):    
    pointsToDst = SetIndexedByTuple()
    n = len(points)
    initBaseCase(pointsToDst, n)

    # graphviz = GraphvizOutput()
    # graphviz.output_file = f'./{path}.png'
    # with PyCallGraph(output=graphviz):  
    for m in range(2, n+1):
        print(f"m: {m}")
        tsBefore = time.time()     
        collections = generateTuplesWithoutReturnInAscending(0, n - 1, m)
        tsAfter = time.time()
        print(tsAfter - tsBefore)
        tsBefore = time.time()
        loggingInterval = 30
        tsStartPoint = time.time()       
        for S in collections:   # LATEST IDEA : THIS BLOCK PROCESSED FOR A LONG TIME 
            intermediatePoints = pointsToDst.InitCurr(S)
            for j in S:
                if j != 0:
                    min_result = inf                    
                    for k in S:
                        if k != j:        
                            # idea to check if memory is enough (for that sake we omit long calculations)                                            
                            S_without_j = setsAsymDiff(set(S), set([j]))
                            toDestinationDistances = pointsToDst.Get(tuple(S_without_j))                               
                            if min_result > toDestinationDistances[k] + distances[k][j]:
                                min_result = toDestinationDistances[k] + distances[k][j]                                                    
                             
                    intermediatePoints[j] = min_result # we keep only the last row/column of subproblems, etc.
            tsAfterIteration = time.time()
            if tsAfterIteration - tsStartPoint > loggingInterval:                
                print(tsAfterIteration - tsBefore)
                tsStartPoint = tsAfterIteration
        pointsToDst.CurrToPrev()
        tsAfter = time.time()
        print(tsAfter - tsBefore)
    result = inf
    fullSet = tuple()
    for i in range(n):
        fullSet = fullSet + (i,)
    
    allPointsToDestination = pointsToDst.GetPrev(fullSet)
    print(allPointsToDestination)
    for j in range(1, n):                              
        allPointsToJ = allPointsToDestination[j] 
        if allPointsToJ + distances[j][0] < result: # NOTE при индексации в сете порядок не важен
            result = allPointsToJ + distances[j][0]
    return result

def initBaseCase(pointsToDst, n):
    for i in range(n):
        if i == 0:
            pointsToDst.SetPrev(tuple([0]), i, 0)
        else:
            pointsToDst.SetPrev(tuple([0]), i, inf)

print('!')
cases = readCases(inputCases)

for case in cases:    
    print(f'path: {case.path},\nexpected_answer: {case.answer}')
    distances = calcDistances(case.points)        
    print('----------')    

    actualAnswer = tsp(case.path, case.points, distances)
    print(f'actualAnswer: {actualAnswer}')  
    if(case.answer is not None):
        if case.roundAnswer:
            actualAnswer = round(actualAnswer, 2)
        if case.isPassed(actualAnswer):
            print('Test case SUCCEEDED!')
        else:
            print('Test case FAILED!')
            raise Exception(f'{case.path} FAILED!')
    print('--------')