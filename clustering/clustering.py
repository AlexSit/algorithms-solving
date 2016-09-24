import sys

class Edge:
    point1 = ''
    point2 = ''
    cost = 0
    def __init__(self, p1, p2, cost_):
        self.point1 = p1
        self.point2 = p2
        self.cost = cost_
    def __str__(self):
        return "{%s, %s, %s}" % (self.point1, self.point2, self.cost)
    def __repr__(self):
        return str(self)
    pass

def Print(str):    
    #print(str)
    pass

def merge_clusters(edges, cluster_points_tuple):
    point1 = cluster_points_tuple.point1
    point2 = cluster_points_tuple.point2
    cost = cluster_points_tuple.cost
    edges.remove(cluster_points_tuple)
    deleted_edges_count = 1
    Print('points to merge:')
    Print(point1)
    Print(point2)
    Print('EXPLORING EDGES')
    for edge in edges[:]:
        '''
        if((edge.point1 == 'M14' and edge.point2 == 'M23') or (edge.point1 == 'M23' and edge.point2 == 'M14')):
            is_test_case = True
            Print('points: ')
            Print(edge)

        else:
            is_test_case = False
        if(is_test_case):
            Print('edges before substitution')
            Print(edges)'''
        if(edge.point1 in [point1, point2]):
            edge.point1 = "M" + str(point1) + str(point2)                       
        if(edge.point2 in [point1, point2]):
            edge.point2 = "M" + str(point1) + str(point2)            
        '''if(is_test_case):
            Print('edges after substitution')
            Print(edges)'''
        if(edge.point1 == edge.point2):
            edges.remove(edge)
            '''if(is_test_case):
                Print('edges after deletion')
                Print(edges)'''
            deleted_edges_count += 1
    return deleted_edges_count

print(sys.version)
print('Clustering problem')

fileInput = open("./inputs/clustering.txt")
#fileInput = open("./inputs/tc1.txt")
#fileInput = open("./inputs/tc2.txt")
#fileInput = open("./inputs/tc3.txt")
#fileInput = open("./inputs/tc4.txt")

text = fileInput.read()
lines = text.splitlines()

(nodes_count, need_cluster_count) = lines[0].split()

edges = []
for l in lines[1:]:
    edge_definition = l.split()    
    e = Edge(
        edge_definition[0], 
        edge_definition[1], 
        int(edge_definition[2]))
    edges.append(e)
edges = sorted(edges, key = lambda e: e.cost)
print(edges)

nodes_count = int(nodes_count)
need_cluster_count = int(need_cluster_count)
#answer = int(answer)

current_cluster_count = nodes_count

print('number of nodes: %d'  % nodes_count)
print('need_cluster_count: %d'  % need_cluster_count)

while(current_cluster_count > need_cluster_count):    
    closest_pair = edges[0]
    merge_clusters(edges, closest_pair)
    Print('after merge')
    Print(edges)
    current_cluster_count -= 1
    Print("%d after merge" % current_cluster_count)

actual_answer = edges[0].cost
print(actual_answer)
'''
if(actual_answer == answer):
    print('SUCCESS')
else:
    print('FAIL')
'''
print('finish')
