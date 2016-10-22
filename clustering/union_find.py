__author__ = 'davide' # https://gist.github.com/DavideCanton/9173142 + @AlexSit (@asit) modifications 

import collections

class Cluster:
    def __init__(self, elements = []):
        self.size = len(elements)
        self.elements = elements
    def __str__(self):
        return 'size = %d, elements_count = %d' % (self.size, len(self.elements))

class Element:
    def __init__(self, number, size=1):
        self.number = number
        self.parent = number        
        self.size = size
    def __str__(self):
        return 'number = %s, parent = %d, size = %d\n' % ("{0:b}".format(self.number), self.parent, self.size)

class UnionFind:
    def __init__(self, init_list):
        self.elements = {}
        self.parents = {}
        for i in init_list:
            self.elements[i] = Element(i)
            self.parents[i] = Cluster([i])
        self.size = len(init_list)

    def find_parent(self, x):        
        if x not in self.elements:
            return None
        return self.elements[x].parent

    def union(self, parent1, parent2):        
        if self.parents[parent1].size > self.parents[parent2].size:            
            main_cluster = self.parents[parent1]
            nested_cluster = self.parents[parent2] 
            new_parent = parent1
            obsolete_parent = parent2
        else:
            main_cluster = self.parents[parent2]
            nested_cluster = self.parents[parent1]
            new_parent = parent2            
            obsolete_parent = parent1            

        #пройтись по каждому элементу внедряемого кластера        
        for element in nested_cluster.elements:            
            # изменить ему родителя
            self.elements[element].parent = new_parent
            # изменить размер главного кластера на каждый внедряемый элемент
            main_cluster.size += 1
            # к главному кластеру добавить внедряемые элементы 
            main_cluster.elements.append(element)
        #удалить из parents внедрённый кластер
        self.parents.pop(obsolete_parent, None)

        self.size -= 1

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
    print(u.find_parent(10))
    print(u.find_parent(13))
    print(u.parents)