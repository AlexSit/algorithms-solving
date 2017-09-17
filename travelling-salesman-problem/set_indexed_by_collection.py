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
        self._prevCurr = [{}, {}] # SETS      

    def __str__(self):
        return str(self._prevCurr)

    def  _printPrevCurr(self):
        prev = self._prevCurr[0]
        curr = self._prevCurr[1]
        formattedString = f'---\nprev: {prev}\ncurr: {curr}\n---\n'
        print(formattedString)

    def CurrToPrev(self):
        self._prevCurr[0] = self._prevCurr[1]
        self._prevCurr[1] = {}
        # for key in self._prevCurr[1].keys(): # OPTIMIZATION
        #     del self._prevCurr[1][key]

    def Set(self, tuple, value):          
        index = self.createIndex(tuple)
        self._prevCurr[1][index] = value

    def _getOrInitAndReturn(self, prevOrCurrIndex, tuple):
        index = self.createIndex(tuple)        
        if index not in self._prevCurr[prevOrCurrIndex]:
            self._prevCurr[prevOrCurrIndex][index] = [inf for i in range(25)] # OPTIMIZATION LIST OR SET?             
        return self._prevCurr[prevOrCurrIndex][index]    

    def InitCurr(self, tuple):
        return self._getOrInitAndReturn(1, tuple)

    def Get(self, tuple):
        index = self.createIndex(tuple)        
        if index not in self._prevCurr[0]:
            self._prevCurr[1][index] = [inf for i in range(25)] # OPTIMIZATION LIST OR SET? 
            return self._prevCurr[1][index]
        return self._prevCurr[0][index]

    def GetPrev(self, tuple):
        return self._getOrInitAndReturn(0, tuple)

    def SetPrev(self, tuple, i, value):        
        self._getOrInitAndReturn(0, tuple)[i] = value

    def Length(self):
        return len(self._set)

    @classmethod
    def Clone(cls, toClone):
        clone = cls()        
        clone._set = copy.deepcopy(toClone._set)
        return clone

    def createIndex(self, tuple):
        return hash(tuple)