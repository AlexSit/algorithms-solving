import sys
import math
import test_helper

# from set_indexed_by_list import SetIndexedByList
from set_indexed_by_collection import SetIndexedByTuple
from collection_generator import generateTuplesWithoutReturnInAscending

from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

global IntermediatePointsToDestination
global C

def calcDistance(x1, y1, x2, y2): return math.sqrt(math.pow(x1-x2, 2) + math.pow(y1-y2, 2))

def calcDistances(points):    
    length = len(points)
    C = [[0 for j in range(length)] for i in range(length)]

    for i in range(length):
        for j in range(i+1, length):
            dist = calcDistance(points[i][0], points[i][1], points[j][0], points[j][1])
            C[i][j] = dist
            C[j][i] = dist
    return C 

inf = float('inf')


paths = [
    './inputs/1.txt',
    './inputs/2.txt'    
]
'''
paths = [
    './inputs/tsp.txt',    
]
'''

def setsAsymDiff(set1, set2): # NOTE возвращается сет, а не список
    return set1 ^ set2

def tsp(points):    
    IntermediatePointsToDestination = SetIndexedByTuple()
    n = len(points)
    initBaseCase(IntermediatePointsToDestination, n)
    
    #graphviz = GraphvizOutput()
    #graphviz.output_file = './output.png'
    #with PyCallGraph(output=GraphvizOutput()):  
    for m in range(1, n+1):
        print("m: {}".format(m))     
        collections = generateTuplesWithoutReturnInAscending(0, n - 1, m)
        for S in collections:   
            for j in S:
                if j != 0:
                    min_result = inf
                    for k in S:
                        if k != j:
                            S_without_j = setsAsymDiff(set(S), set([j]))
                            toDestinationDistances = IntermediatePointsToDestination.Get(tuple(S_without_j))                              
                            if k in toDestinationDistances:                                
                                if min_result > toDestinationDistances[k] + C[k][j]:
                                    min_result = toDestinationDistances[k] + C[k][j]                        
                    IntermediatePointsToDestination.Get(S)[j] = min_result #A TIP: keep only the last row/column of subproblems, etc.
    result = inf
    fullSet = tuple()
    for i in range(n):
        fullSet = fullSet + (i,)
    
    for j in range(1, n):              
        allPointsToDestination = IntermediatePointsToDestination.Get(fullSet)
        
        allPointsToJ = allPointsToDestination[j] 
        if allPointsToJ + C[j][0] < result: # NOTE при индексации в сете порядок не важен
            result = IntermediatePointsToDestination.Get(fullSet)[j] + C[j][0]
    return result

def initBaseCase(IntermediatePointsToDestination, n):
    for i in range(n):
        if i == 0:
            IntermediatePointsToDestination.Get(tuple([0]))[i] = 0            
        else:
            IntermediatePointsToDestination.Get(tuple([0]))[i] = inf

cases = test_helper.readCases(paths)

for case in cases:    
    print('path: {},\nexpected_answer: {}'.format(case.path, case.answer))
    C = calcDistances(case.points)    
    print(C)
    print('----------')    

    actualAnswer = tsp(case.points)
    print('actualAnswer: {}'.format(actualAnswer) )  
    if(case.answer is not None):
        if case.isPassed(actualAnswer):
            print('Test case SUCCEEDED!')
        else:
            print('Test case FAILED!')
    print('--------')