import copy
import random
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

inf = float('inf')

class SetIndexedByList:    
    def __init__(self):        
        self._set = {}

    def __str__(self):
        return str(self._set)

    def Set(self, list, value):          
        index = self.createIndex(list)
        self._set[index] = value

    def Get(self, list):
        index = self.createIndex(list)
        if index not in self._set:
            self._set[index] = {}        
        return self._set[index]

    def createIndex(self, list):
        return ','.join(str(num) for num in list)