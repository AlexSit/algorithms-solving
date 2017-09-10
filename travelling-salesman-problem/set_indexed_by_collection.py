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

class SetIndexedByTuple:    
    def __init__(self):        
        self._set = {} # HINT TRY USE LIST NOT SEt

    def __str__(self):
        return str(self._set)

    def Set(self, tuple, value):          
        index = self.createIndex(tuple)
        self._set[index] = value

    def Get(self, tuple):
        index = self.createIndex(tuple)        
        if index not in self._set:
            self._set[index] = [inf for i in range(25)] # HINT TRY USE LIST NOT SEt
        return self._set[index]

    def Clear(self):
        self._set.clear()

    def Length(self):
        return len(self._set)

    @classmethod
    def Clone(cls, toClone):
        clone = cls()        
        clone._set = copy.deepcopy(toClone._set)
        return clone

    def createIndex(self, tuple):
        return hash(tuple)