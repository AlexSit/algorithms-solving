__author__ = 'davide' # https://gist.github.com/DavideCanton/9173142 + @AlexSit (@asit) modifications 

import collections

class Element:
    def __init__(self, number, size=1):        #rank = 0
        self.number = number
        self.parent = number
        #self.rank = rank
        self.size = size
    def __str__(self):
        return 'number = %s, parent = %d, size = %d\n' % ("{0:b}".format(self.number), self.parent, self.size) # rank = %d,

class UnionFind:
    def __init__(self, init_list):
        self.elements = {}
        for i in init_list:
            self.elements[i] = Element(i)
        self.size = len(init_list)

    def printOneItemClusters(self):
        result = ''      
        for i in self.elements:            
            if i == self.elements[i].parent:
                print("number: " + str(i) + "; " +  str(self.elements[i]) + '; ')

    def find(self, x):
        #print('FIND: %d' % x)  
        cur = x
        while cur != self.elements[cur].parent:
            cur = self.elements[cur].parent
        self.elements[x].parent = cur #заодно проставляем родителя
        return self.elements[x]

    def union(self, parent1, parent2):
        #print('UNION')
        #print(parent1, parent2, sep=" ")
        if self.elements[parent1].size > self.elements[parent2].size:
            self.elements[parent2].parent = parent1            
            self.elements[parent1].size += self.elements[parent2].size
        else:
            self.elements[parent1].parent = parent2
            self.elements[parent2].size += self.elements[parent1].size
            #if self.elements[parent1].rank == self.elements[parent2].rank:
            #    self.elements[parent2].rank += 1
        self.size -= 1
        #print('ITOG')
        #print(self)
    def __len__(self):
        return self.size

    def size(self, x):
        return self.elements[x].size

    def __iter__(self):
        for i, key in enumerate(self.elements):            
            yield self.elements[key]

    def __str__(self):  
        result = ''      
        for i in self.elements:
            result += "number: " + str(i) + "; " +  str(self.elements[i]) + '; '
        return result

if __name__ == "__main__":    
    u = UnionFind([10,11,12,13,14]) 
    print(u)
    u.union(10, 13)
    print(u)
    print(u.find(10))
    print(u.find(13))